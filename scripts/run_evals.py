#!/usr/bin/env python3
"""Run the skills against real prompts and grade what comes back.

    python3 scripts/run_evals.py --list
    python3 scripts/run_evals.py                          # every eval, with skills
    python3 scripts/run_evals.py --skill whatsapp-status  # one skill
    python3 scripts/run_evals.py --eval refuses-fake-scarcity
    python3 scripts/run_evals.py --baseline               # also run without skills, report the delta
    python3 scripts/run_evals.py --via plugin             # load the repo as a plugin (--plugin-dir)
    python3 scripts/run_evals.py --judge                  # also LLM-grade the natural-language assertions
    python3 scripts/run_evals.py --grade-only evals-workspace/iteration-3

Each skill keeps its cases in `skills/<name>/evals/evals.json`, in the Agent
Skills eval format: `prompt`, `expected_output`, natural-language `assertions`,
plus `checks`, a list of mechanical checks this script grades without a model
(text present, links intact, lint-clean, length, emoji count, script).

Runs use the Claude Code CLI in print mode (`claude -p`). Each run happens in a
fresh temp directory so nothing the agent writes lands in the repo:

  with_skill     temp dir with .claude/skills/<every skill> copied in
  without_skill  empty temp dir (only with --baseline)

User settings, plugins and MCP servers are not loaded (`--setting-sources
project --strict-mcp-config`), so the result reflects this repo only.

Results follow the spec's workspace layout:
  evals-workspace/iteration-N/eval-<skill>-<name>/<config>/outputs/response.md
                                                     .../timing.json, grading.json
  evals-workspace/iteration-N/benchmark.json

Costs one model call per eval per config (two with --judge).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import importlib.util
import json
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "evals-workspace"
ALLOWED_TOOLS = ["Skill", "Read", "Write", "Glob", "Grep", "Bash(python3:*)", "Bash(cat:*)"]
FENCE = re.compile(r"^(?P<fence>`{3,})(?P<lang>[\w-]*)[ \t]*\n(?P<body>.*?)\n(?P=fence)[ \t]*$", re.S | re.M)
MESSAGE_LANGS = {"", "text", "txt", "plaintext", "whatsapp"}


def _load_lint():
    spec = importlib.util.spec_from_file_location("wa_lint", ROOT / "shared" / "scripts" / "wa_lint.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["wa_lint"] = module
    spec.loader.exec_module(module)
    return module


wa_lint = _load_lint()

# ---------------------------------------------------------------- loading ---


def load_cases(skill: Optional[str], name: Optional[str]) -> List[dict]:
    cases = []
    for path in sorted((ROOT / "skills").glob("*/evals/evals.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for case in data["evals"]:
            case = dict(case, skill=data["skill_name"])
            if skill and case["skill"] != skill:
                continue
            if name and case["name"] != name:
                continue
            cases.append(case)
    return cases


def case_dir(iteration: Path, case: dict) -> Path:
    return iteration / f"eval-{case['skill']}-{case['name']}"


def next_iteration() -> Path:
    WORKSPACE.mkdir(exist_ok=True)
    nums = [int(p.name.split("-")[1]) for p in WORKSPACE.glob("iteration-*") if p.name.split("-")[1].isdigit()]
    path = WORKSPACE / f"iteration-{max(nums, default=0) + 1}"
    path.mkdir()
    return path


# ---------------------------------------------------------------- running ---


def _prepare_cwd(config: str, via: str) -> Tuple[tempfile.TemporaryDirectory, List[str]]:
    tmp = tempfile.TemporaryDirectory(prefix="wa-eval-")
    extra: List[str] = []
    if config == "with_skill":
        if via == "plugin":
            extra = ["--plugin-dir", str(ROOT)]
        else:
            dest = Path(tmp.name) / ".claude" / "skills"
            dest.mkdir(parents=True)
            for skill in sorted((ROOT / "skills").iterdir()):
                if (skill / "SKILL.md").is_file():
                    shutil.copytree(skill, dest / skill.name, ignore=shutil.ignore_patterns("evals"))
    return tmp, extra


def run_claude(prompt: str, cwd: str, extra: List[str], model: Optional[str], timeout: int) -> dict:
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "stream-json", "--verbose",
        "--setting-sources", "project",
        "--strict-mcp-config",
        "--no-session-persistence",
        "--allowedTools", *ALLOWED_TOOLS,
    ] + extra
    if model:
        cmd += ["--model", model]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"error": f"timed out after {timeout}s", "duration_ms": timeout * 1000}
    except FileNotFoundError:
        raise SystemExit("The `claude` CLI is not on PATH. Install Claude Code to run evals.")
    elapsed = int((time.time() - started) * 1000)

    result, skills_used, tokens = None, [], 0
    transcript = proc.stdout
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use" and block.get("name") == "Skill":
                    skills_used.append(str(block.get("input", {}).get("skill") or block.get("input", {}).get("command")))
        if event.get("type") == "result":
            result = event
    if result is None:
        return {"error": (proc.stderr or proc.stdout)[-2000:], "duration_ms": elapsed, "transcript": transcript}
    usage = result.get("usage") or {}
    tokens = sum(int(usage.get(k) or 0) for k in ("input_tokens", "output_tokens",
                                                     "cache_creation_input_tokens", "cache_read_input_tokens"))
    return {
        "response": result.get("result") or "",
        "duration_ms": int(result.get("duration_ms") or elapsed),
        "total_tokens": tokens,
        "cost_usd": result.get("total_cost_usd"),
        "num_turns": result.get("num_turns"),
        "skills_used": skills_used,
        "is_error": bool(result.get("is_error")),
        "transcript": transcript,
    }


# ---------------------------------------------------------------- grading ---


def messages(response: str) -> List[str]:
    """The copy-ready blocks: fenced code with no language or a text-like one."""
    return [m.group("body") for m in FENCE.finditer(response) if m.group("lang").lower() in MESSAGE_LANGS]


def _flags(check: dict) -> int:
    f = 0
    for ch in check.get("flags", ""):
        f |= {"i": re.I, "m": re.M, "s": re.S}[ch]
    return f


def grade_check(check: dict, response: str, msgs: List[str], today: dt.date) -> Tuple[bool, str]:
    kind = check["type"]
    joined = "\n\n".join(msgs)
    if kind == "starts_with_message":
        lines = [l for l in response.strip().splitlines() if l.strip()]
        if not lines:
            return False, "empty response"
        if lines[0].startswith("```"):
            return True, "response opens with the message block"
        if len(lines) > 1 and len(lines[0]) <= 40 and lines[1].startswith("```"):
            return True, f"opens with label '{lines[0].strip()}' then the block"
        return False, f"opens with: {lines[0][:80]!r}"
    if kind == "message_count":
        n = len(msgs)
        ok = check.get("min", 0) <= n <= check.get("max", 10**6)
        return ok, f"{n} message block(s)"
    if not msgs and kind not in ("response_regex", "response_not_regex", "not_regex", "not_contains"):
        return False, "no message block in the response"
    if kind == "contains":
        return check["value"] in joined, f"{'found' if check['value'] in joined else 'missing'}: {check['value']!r}"
    if kind == "icontains":
        ok = check["value"].lower() in joined.lower()
        return ok, f"{'found' if ok else 'missing'} (case-insensitive): {check['value']!r}"
    if kind == "contains_any":
        hit = [v for v in check["values"] if v.lower() in joined.lower()]
        return bool(hit), f"found {hit}" if hit else f"none of {check['values']}"
    if kind == "not_contains":
        ok = check["value"].lower() not in joined.lower()
        return ok, "absent" if ok else f"present: {check['value']!r}"
    if kind in ("regex", "not_regex", "response_regex", "response_not_regex"):
        target = response if kind.startswith("response") else joined
        m = re.search(check["pattern"], target, _flags(check))
        want = not kind.endswith("not_regex")
        evidence = f"matched {m.group(0)[:60]!r}" if m else f"no match for /{check['pattern']}/"
        return (bool(m) == want), evidence
    if kind == "max_chars":
        longest = max(len(m) for m in msgs)
        return longest <= check["value"], f"longest message {longest} chars (max {check['value']})"
    if kind == "min_chars":
        shortest = min(len(m) for m in msgs)
        return shortest >= check["value"], f"shortest message {shortest} chars (min {check['value']})"
    if kind == "max_emoji":
        most = max(wa_lint.count_emoji(m) for m in msgs)
        return most <= check["value"], f"{most} emoji (max {check['value']})"
    if kind == "script":
        ranges = {"devanagari": (0x0900, 0x097F), "tamil": (0x0B80, 0x0BFF), "bengali": (0x0980, 0x09FF),
                  "arabic": (0x0600, 0x06FF), "gujarati": (0x0A80, 0x0AFF)}
        lo, hi = ranges[check["value"]]
        n = sum(1 for ch in joined if lo <= ord(ch) <= hi)
        return n >= check.get("min", 20), f"{n} {check['value']} characters"
    if kind == "lint_clean":
        problems = []
        for i, m in enumerate(msgs, 1):
            report = wa_lint.lint(m, kind=check.get("kind", "message"), today=today)
            problems += [f"msg {i}: {f.code}" for f in report.errors]
        return not problems, "no lint errors" if not problems else ", ".join(problems)
    raise ValueError(f"unknown check type {kind!r}")


def judge(case: dict, response: str, model: Optional[str], timeout: int) -> List[dict]:
    """LLM-grade the natural-language assertions. Strict: evidence required for PASS."""
    prompt = (
        "You are grading an AI assistant's output against assertions. Be strict: PASS only with "
        "concrete evidence quoted from the output.\n\n"
        f"TASK GIVEN TO THE ASSISTANT:\n{case['prompt']}\n\nOUTPUT:\n{response}\n\n"
        "ASSERTIONS:\n" + "\n".join(f"{i}. {a}" for i, a in enumerate(case["assertions"], 1)) +
        "\n\nReply with only a JSON array, one object per assertion: "
        '[{"text": "...", "passed": true, "evidence": "..."}]'
    )
    with tempfile.TemporaryDirectory() as tmp:
        out = run_claude(prompt, tmp, [], model, timeout)
    raw = out.get("response", "")
    m = re.search(r"\[.*\]", raw, re.S)
    try:
        return json.loads(m.group(0)) if m else []
    except json.JSONDecodeError:
        return [{"text": a, "passed": False, "evidence": "judge output unparseable"} for a in case["assertions"]]


def grade(case: dict, response: str, today: dt.date) -> dict:
    blocks = messages(response)
    # No copy-ready block (typical without the skill): judge the content of the
    # whole response, so the baseline is graded on substance, not on fencing.
    content = blocks or ([response.strip()] if response.strip() else [])
    results = []
    for check in case.get("checks", []):
        scoped = check["type"] in ("starts_with_message", "message_count") or check.get("scope") == "blocks"
        msgs = blocks if scoped else content
        try:
            passed, evidence = grade_check(check, response, msgs, today)
        except Exception as exc:  # a broken check must not kill the run
            passed, evidence = False, f"check error: {exc}"
        label = check.get("why") or f"{check['type']} {check.get('value', check.get('pattern', ''))}".strip()
        results.append({"text": label, "passed": passed, "evidence": evidence})
    passed = sum(r["passed"] for r in results)
    return {
        "assertion_results": results,
        "summary": {"passed": passed, "failed": len(results) - passed, "total": len(results),
                    "pass_rate": round(passed / len(results), 3) if results else 0.0},
    }


# ------------------------------------------------------------------- main ---


def run_one(case: dict, config: str, iteration: Path, args, today: dt.date) -> dict:
    out_dir = case_dir(iteration, case) / config
    (out_dir / "outputs").mkdir(parents=True, exist_ok=True)
    tmp, extra = _prepare_cwd(config, args.via)
    try:
        run = run_claude(case["prompt"], tmp.name, extra, args.model, args.timeout)
    finally:
        tmp.cleanup()
    response = run.get("response", "") if "error" not in run else f"[run failed] {run['error']}"
    (out_dir / "outputs" / "response.md").write_text(response, encoding="utf-8")
    (out_dir / "transcript.jsonl").write_text(run.get("transcript") or "", encoding="utf-8")
    timing = {k: run.get(k) for k in ("total_tokens", "duration_ms", "cost_usd", "num_turns", "skills_used")}
    (out_dir / "timing.json").write_text(json.dumps(timing, indent=2) + "\n", encoding="utf-8")
    grading = grade(case, response, today)
    if args.judge and "error" not in run:
        grading["judge_results"] = judge(case, response, args.model, args.timeout)
    grading["skill_triggered"] = case["skill"] in " ".join(run.get("skills_used") or [])
    (out_dir / "grading.json").write_text(json.dumps(grading, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"case": case, "config": config, "grading": grading, "timing": timing}


def _stats(values: List[float]) -> dict:
    if not values:
        return {"mean": 0.0, "stddev": 0.0}
    return {"mean": round(statistics.mean(values), 3),
            "stddev": round(statistics.pstdev(values), 3) if len(values) > 1 else 0.0}


def benchmark(results: List[dict]) -> dict:
    summary = {}
    for config in sorted({r["config"] for r in results}):
        rows = [r for r in results if r["config"] == config]
        summary[config] = {
            "pass_rate": _stats([r["grading"]["summary"]["pass_rate"] for r in rows]),
            "time_seconds": _stats([(r["timing"].get("duration_ms") or 0) / 1000 for r in rows]),
            "tokens": _stats([r["timing"].get("total_tokens") or 0 for r in rows]),
            "evals": len(rows),
        }
        if config == "with_skill":
            summary[config]["skill_trigger_rate"] = round(
                sum(r["grading"].get("skill_triggered", False) for r in rows) / len(rows), 3)
    if "with_skill" in summary and "without_skill" in summary:
        w, wo = summary["with_skill"], summary["without_skill"]
        summary["delta"] = {k: round(w[k]["mean"] - wo[k]["mean"], 3) for k in ("pass_rate", "time_seconds", "tokens")}
    return {"run_summary": summary, "generated": dt.datetime.now().isoformat(timespec="seconds")}


def print_report(results: List[dict], bench: dict) -> None:
    print()
    for r in sorted(results, key=lambda r: (r["case"]["skill"], r["case"]["id"], r["config"])):
        s = r["grading"]["summary"]
        mark = "✓" if s["failed"] == 0 else "✗"
        trig = "" if r["config"] != "with_skill" else (" [skill used]" if r["grading"].get("skill_triggered") else " [skill NOT used]")
        print(f"{mark} {r['case']['skill']:<22} {r['case']['name']:<34} {r['config']:<13} {s['passed']}/{s['total']}{trig}")
        for a in r["grading"]["assertion_results"]:
            if not a["passed"]:
                print(f"      ✗ {a['text']}: {a['evidence']}")
    print()
    for config, row in bench["run_summary"].items():
        if config == "delta":
            print(f"delta (with - without): pass rate {row['pass_rate']:+.0%}, "
                  f"time {row['time_seconds']:+.1f}s, tokens {row['tokens']:+.0f}")
        else:
            trig = f", skill triggered {row['skill_trigger_rate']:.0%}" if "skill_trigger_rate" in row else ""
            print(f"{config}: pass rate {row['pass_rate']['mean']:.0%} over {row['evals']} evals, "
                  f"{row['time_seconds']['mean']:.1f}s avg{trig}")


def regrade(iteration: Path, today: dt.date) -> int:
    results = []
    cases = {f"eval-{c['skill']}-{c['name']}": c for c in load_cases(None, None)}
    for ev in sorted(iteration.glob("eval-*")):
        case = cases.get(ev.name)
        if not case:
            continue
        for cfg_dir in sorted(p for p in ev.iterdir() if p.is_dir()):
            response = (cfg_dir / "outputs" / "response.md").read_text(encoding="utf-8")
            timing = json.loads((cfg_dir / "timing.json").read_text(encoding="utf-8"))
            grading = grade(case, response, today)
            grading["skill_triggered"] = case["skill"] in " ".join(timing.get("skills_used") or [])
            (cfg_dir / "grading.json").write_text(json.dumps(grading, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            results.append({"case": case, "config": cfg_dir.name, "grading": grading, "timing": timing})
    bench = benchmark(results)
    (iteration / "benchmark.json").write_text(json.dumps(bench, indent=2) + "\n", encoding="utf-8")
    print_report(results, bench)
    return 0 if all(r["grading"]["summary"]["failed"] == 0 for r in results if r["config"] == "with_skill") else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Run and grade the skill evals with the Claude Code CLI.")
    p.add_argument("--skill", help="only this skill")
    p.add_argument("--eval", dest="eval_name", help="only the eval with this name")
    p.add_argument("--baseline", action="store_true", help="also run each eval without the skills")
    p.add_argument("--via", choices=("project", "plugin"), default="project",
                   help="load skills as project skills (default) or the repo as a plugin")
    p.add_argument("--judge", action="store_true", help="LLM-grade the natural-language assertions too")
    p.add_argument("--model", help="model for the runs (default: the CLI's default)")
    p.add_argument("--jobs", type=int, default=4, help="parallel runs (default 4)")
    p.add_argument("--timeout", type=int, default=300, help="seconds per run (default 300)")
    p.add_argument("--today", type=wa_lint._parse_date, default=None, help="date for the lint check (default: today)")
    p.add_argument("--list", action="store_true", help="list evals and exit")
    p.add_argument("--grade-only", type=Path, metavar="ITERATION_DIR", help="re-grade saved responses, no model calls")
    args = p.parse_args(argv)
    today = args.today or dt.date.today()

    if args.grade_only:
        return regrade(args.grade_only, today)
    cases = load_cases(args.skill, args.eval_name)
    if args.list or not cases:
        for c in cases:
            print(f"{c['skill']:<22} {c['name']:<34} {len(c.get('checks', []))} checks")
        if not cases:
            print("No evals matched.")
        return 0 if cases else 1

    iteration = next_iteration()
    configs = ["with_skill"] + (["without_skill"] if args.baseline else [])
    jobs = [(c, cfg) for c in cases for cfg in configs]
    print(f"Running {len(jobs)} run(s) into {iteration.relative_to(ROOT)} …")
    results = []
    with cf.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = {pool.submit(run_one, c, cfg, iteration, args, today): (c, cfg) for c, cfg in jobs}
        for fut in cf.as_completed(futures):
            c, cfg = futures[fut]
            r = fut.result()
            s = r["grading"]["summary"]
            print(f"  done {c['skill']}/{c['name']} [{cfg}] {s['passed']}/{s['total']}", flush=True)
            results.append(r)
    bench = benchmark(results)
    (iteration / "benchmark.json").write_text(json.dumps(bench, indent=2) + "\n", encoding="utf-8")
    print_report(results, bench)
    print(f"\nDetails: {iteration.relative_to(ROOT)}/")
    return 0 if all(r["grading"]["summary"]["failed"] == 0 for r in results if r["config"] == "with_skill") else 1


if __name__ == "__main__":
    sys.exit(main())
