#!/usr/bin/env python3
"""wa_lint: check a WhatsApp message before you paste it, or fix one.

WhatsApp renders its own small formatting language, not Markdown. Text that an
AI assistant writes by habit (``**bold**``, ``# Heading``, ``[label](url)``,
tables) shows up in the chat as literal symbols. This script catches those, plus
the mistakes that cost the sender credibility in a group: a weekday that does
not match the date, a placeholder left in, a status over the length limit.

Usage
    python3 wa_lint.py message.txt
    python3 wa_lint.py - < message.txt            # read stdin
    python3 wa_lint.py --kind status message.txt  # apply the 700-char status limit
    python3 wa_lint.py --today 2026-11-02 message.txt
    python3 wa_lint.py --fix draft.md > message.txt   # convert Markdown to WhatsApp
    python3 wa_lint.py --json message.txt

Exit codes
    0  no errors (warnings and notes may be printed)
    1  errors found (or warnings too, with --strict)
    2  usage problem (missing file, bad flag)

Standard library only. Python 3.8+.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

__all__ = ["Finding", "Report", "lint", "fix", "main", "LIMITS", "KINDS"]
__version__ = "1.0.0"

# --------------------------------------------------------------------------
# Limits
# --------------------------------------------------------------------------

#: Hard and soft limits per message kind. ``hard`` is an error, ``soft`` a warning.
LIMITS: Dict[str, Dict[str, int]] = {
    "message": {"hard": 65536},
    "announcement": {"hard": 65536},
    "invitation": {"hard": 65536},
    "promotion": {"hard": 65536},
    "channel": {"hard": 65536},
    "reply": {"hard": 65536},
    # Text status updates are capped at 700 characters.
    "status": {"hard": 700},
    # The WhatsApp Business API caps media captions at 1,024 characters, and a
    # long caption collapses behind "Read more" anyway. Warn, do not fail.
    "caption": {"hard": 65536, "soft": 1024},
    # Profile and description text (whatsapp-setup). The personal and business
    # "About" line is capped at 139 characters. Descriptions get soft limits:
    # long ones are truncated behind "Read more" in the app.
    "about": {"hard": 139},
    "business-description": {"hard": 65536, "soft": 512},
    "group-description": {"hard": 65536, "soft": 2048},
    "quick-reply": {"hard": 65536, "soft": 1024},
    "redact": {"hard": 10_000_000},
}
KINDS = tuple(LIMITS)

# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------

LEVELS = ("error", "warn", "note")


@dataclass
class Finding:
    level: str  # error | warn | note
    code: str
    line: int  # 1-based, 0 when the finding is about the whole message
    message: str


@dataclass
class Report:
    findings: List[Finding] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)

    @property
    def errors(self) -> List[Finding]:
        return [f for f in self.findings if f.level == "error"]

    @property
    def warnings(self) -> List[Finding]:
        return [f for f in self.findings if f.level == "warn"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def codes(self, level: Optional[str] = None) -> List[str]:
        return [f.code for f in self.findings if level is None or f.level == level]

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "stats": dict(self.stats),
            "findings": [asdict(f) for f in self.findings],
        }


# --------------------------------------------------------------------------
# Shared patterns
# --------------------------------------------------------------------------

URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>]+", re.I)
_URL_TRAIL = ".,;:!?'\"*_~]}>"
FENCE_BLOCK_RE = re.compile(r"```[\s\S]*?```")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
MD_LINK_RE = re.compile(r"\[([^\]\n]+)\]\(\s*((?:https?://|www\.|mailto:|tel:)[^)\s]+)\s*\)", re.I)
MD_BOLD_RE = re.compile(r"\*\*(?=\S)[^*\n]+?\*\*|(?<![\w])__(?=\S)[^_\n]+?__(?![\w])")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,}|={3,})\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
HTML_RE = re.compile(r"</?(?:b|strong|i|em|u|s|del|strike|br|p|div|span|a|h[1-6]|ul|ol|li)\b[^>]*>", re.I)
NESTED_LIST_RE = re.compile(r"^(?: {2,}|\t+)(?:[-*•+]|\d{1,2}[.)])\s+\S")
PLACEHOLDER_RE = re.compile(r"\[(?!\s*\])[^\[\]\n]{1,48}\](?!\()")
REDACTION_LABEL_RE = re.compile(
    r"\[(?:phone|email|UPI ID|card|Aadhaar|PAN|IBAN|OTP|code|account no\.|address|name|company|school|"
    r"vehicle no\.|flat no\.|link|Person [A-Z]|redacted)(?: \d+)?\]")
CHAT_STAMP_RE = re.compile(r"\[\d{1,4}[./-]\d{1,2}[./-]\d{1,4},? \d{1,2}[:.]\d{2}(?:[:.]\d{2})?(?:\s?[APap]\.?[Mm]\.?)?\]")
TBD_RE = re.compile(r"\b(?:TBD|TBA|TBC|XXX+|xx:xx)\b")
MENTION_RE = re.compile(r"(?<![\w.@])@[^\W\d_][\w.]*", re.U)
HASHTAG_RE = re.compile(r"(?<![\w&#/])#[A-Za-z][\w]*")
EXCLAIM_RE = re.compile(r"[!?]{3,}")
CHAIN_RE = re.compile(
    r"forward (?:this|it|the message)? ?to (?:\d+|ten|all|every)|"
    r"share (?:this )?with as many|send (?:this )?to everyone you know|"
    r"before (?:it(?:'s| is| gets)) deleted|forwarded as received|"
    r"if you don'?t (?:forward|share)",
    re.I,
)

#: Phrases that read as AI-written or as a pasted email in a chat bubble.
AI_PHRASES: Tuple[str, ...] = (
    "i hope this message finds you well",
    "hope this message finds you",
    "i am writing to inform",
    "i'm writing to inform",
    "this is to inform",
    "please be informed",
    "kindly do the needful",
    "do the needful",
    "please find attached",
    "please find the attached",
    "at your earliest convenience",
    "in today's fast-paced",
    "delve",
    "seamless",
    "seamlessly",
    "elevate your",
    "unlock your potential",
    "unlock the power",
    "embark on",
    "a testament to",
    "game-changer",
    "game changer",
    "tapestry",
    "thrilled to announce",
    "look no further",
    "without further ado",
    "rest assured",
    "leverage",
    "leveraging",
    "utilize",
    "utilise",
    "streamline",
    "harness the",
    "foster",
    "robust",
    "fundamentally",
    "synergy",
    "cutting-edge",
    "plethora",
    "a myriad of",
    "navigate the complexities",
    "it's not just",
    "in conclusion",
    "i'd be happy to help",
    "feel free to reach out",
)
_AI_RE = re.compile(r"\b(?:" + "|".join(re.escape(p) for p in AI_PHRASES) + r")\b", re.I)

# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _trim_url(url: str) -> str:
    """Drop trailing punctuation that a reader (and WhatsApp) treats as prose."""
    while url and url[-1] in _URL_TRAIL:
        url = url[:-1]
    if url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1]
    return url


def _urls(text: str) -> List[Tuple[int, int, str]]:
    out = []
    for m in URL_RE.finditer(text):
        url = _trim_url(m.group(0))
        if url:
            out.append((m.start(), m.start() + len(url), url))
    return out


def _mask(text: str) -> str:
    """Replace code and URLs with filler of the same length so formatting checks
    ignore them. Newlines are kept so line numbers stay correct."""
    chars = list(text)

    def blank(start: int, end: int, filler: str) -> None:
        for i in range(start, end):
            if chars[i] != "\n":
                chars[i] = filler

    for m in FENCE_BLOCK_RE.finditer(text):
        blank(m.start(), m.end(), "x")
    partial = "".join(chars)
    for m in INLINE_CODE_RE.finditer(partial):
        blank(m.start(), m.end(), "x")
    for start, end, _ in _urls(text):
        blank(start, end, "x")
    return "".join(chars)


def _is_emoji(ch: str) -> bool:
    cp = ord(ch)
    return (
        0x1F300 <= cp <= 0x1FAFF
        or 0x1F000 <= cp <= 0x1F2FF
        or 0x2600 <= cp <= 0x27BF
        or 0x2300 <= cp <= 0x23FF
        or 0x2B00 <= cp <= 0x2BFF
        or cp in (0x203C, 0x2049, 0x3030, 0x303D, 0x3297, 0x3299)
    )


def count_emoji(text: str) -> int:
    """Count emoji as people see them: a flag (two regional letters), a skin
    tone and a zero-width-joiner sequence like 👨‍👩‍👧 each count once."""
    count, regional, prev = 0, 0, ""
    for ch in text:
        cp = ord(ch)
        if 0x1F1E6 <= cp <= 0x1F1FF:
            regional += 1
        elif 0x1F3FB <= cp <= 0x1F3FF:
            pass  # skin-tone modifier attaches to the previous emoji
        elif _is_emoji(ch) and prev != "‍":
            count += 1
        prev = ch
    return count + regional // 2


def _words(text: str) -> int:
    return len(re.findall(r"[^\s]+", text))


# --------------------------------------------------------------------------
# Marker pairing (shared by lint and fix)
# --------------------------------------------------------------------------


def _strip_bullet(line: str) -> str:
    """Blank out a leading ``* `` list bullet so it is not read as a marker."""
    m = re.match(r"^(\s*)\*(\s+)", line)
    if m:
        return m.group(1) + " " + line[m.end(1) + 1 :]
    return line


def _candidates(line: str, marker: str) -> List[int]:
    """Positions where ``marker`` could open or close formatting.

    A marker with whitespace on both sides can't open formatting, so it is a
    literal character (``5 * 3``) unless it closes a pair that is already open
    (``*Venue *``, a loose closer). An underscore inside a word (``file_name``)
    never formats, so it does not count either.
    """
    out = []
    for i, ch in enumerate(line):
        if ch != marker:
            continue
        prev = line[i - 1] if i > 0 else " "
        nxt = line[i + 1] if i + 1 < len(line) else " "
        if nxt == marker or prev == marker:
            # part of ** or __ : reported as Markdown bold instead
            continue
        if marker == "_" and prev.isalnum() and nxt.isalnum():
            continue
        if prev.isspace() and nxt.isspace() and len(out) % 2 == 0:
            continue
        out.append(i)
    return out


def _pairs(line: str, marker: str) -> Tuple[List[Tuple[int, int]], bool]:
    pos = _candidates(line, marker)
    pairs = [(pos[i], pos[i + 1]) for i in range(0, len(pos) - 1, 2)]
    return pairs, len(pos) % 2 == 1


# --------------------------------------------------------------------------
# Dates
# --------------------------------------------------------------------------

_WEEKDAYS = {
    "monday": 0, "mon": 0,
    "tuesday": 1, "tues": 1, "tue": 1,
    "wednesday": 2, "weds": 2, "wed": 2,
    "thursday": 3, "thurs": 3, "thur": 3, "thu": 3,
    "friday": 4, "fri": 4,
    "saturday": 5, "sat": 5,
    "sunday": 6, "sun": 6,
}
_WEEKDAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
_MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sept": 9, "sep": 9,
    "october": 10, "oct": 10, "november": 11, "nov": 11, "december": 12, "dec": 12,
}
_WD = r"(?P<wd>" + "|".join(sorted(_WEEKDAYS, key=len, reverse=True)) + r")\b\.?"
_MON = r"(?P<mon>" + "|".join(sorted(_MONTHS, key=len, reverse=True)) + r")\b\.?"
_YEAR = r"(?:,?\s+(?P<year>20\d{2})(?!\s*(?:hrs?\b|hours\b|h\b|:)))?"
_DAY = r"(?P<day>\d{1,2})(?:st|nd|rd|th)?"
_DATE_A = _DAY + r"\s+(?:of\s+)?" + _MON + _YEAR  # 14 Nov 2026, 14th of November
_DATE_B = _MON + r"\s+" + _DAY + r"\b" + _YEAR  # Nov 14, 2026
_DATE_C = r"(?P<n1>\d{1,2})/(?P<n2>\d{1,2})(?:/(?P<n3>\d{2}|\d{4}))?(?!\s*(?:am|pm)\b)(?![\d/])"
_GAP = r"[\s,()\-–—|·:]{0,4}(?:the\s+)?"

_DATE_RES = [re.compile(p, re.I) for p in (_DATE_A, _DATE_B, _DATE_C)]
_WD_RE = re.compile(r"\b" + _WD, re.I)
_GAP_RE = re.compile(_GAP, re.I)


def _date_at(text: str, pos: int, date_order: Optional[str]):
    """Try every date form at ``pos``; return (match, day, month, year_or_None)."""
    for rx in _DATE_RES:
        m = rx.match(text, pos)
        if not m:
            continue
        gd = m.groupdict()
        if gd.get("mon"):
            day, month = int(gd["day"]), _MONTHS[gd["mon"].lower().rstrip(".")]
            year = int(gd["year"]) if gd.get("year") else None
        else:
            a, b = int(gd["n1"]), int(gd["n2"])
            if date_order == "dmy":
                day, month = a, b
            elif date_order == "mdy":
                day, month = b, a
            elif a > 12 >= b:
                day, month = a, b
            elif b > 12 >= a:
                day, month = b, a
            else:
                continue  # 10/11 is ambiguous without --date-order
            year = None
            if gd.get("n3"):
                year = int(gd["n3"])
                year = year + 2000 if year < 100 else year
        return m, day, month, year
    return None


def _resolve_year(day: int, month: int, today: Optional[_dt.date]) -> Optional[int]:
    """The year a reader would assume: this year, or next year if the date is
    more than two months behind ``today`` (an invite in December for January)."""
    if today is None:
        return None
    try:
        candidate = _dt.date(today.year, month, day)
    except ValueError:
        return today.year
    if candidate < today - _dt.timedelta(days=60):
        return today.year + 1
    return today.year


def _check_dates(
    text: str,
    year: Optional[int],
    today: Optional[_dt.date],
    date_order: Optional[str],
    report: Report,
) -> None:
    seen = set()
    unchecked = False

    def evaluate(wd_match, date_info):
        nonlocal unchecked
        m, day, month, explicit_year = date_info
        key = (m.start(), m.end())
        if key in seen:
            return
        seen.add(key)
        line = _line_of(text, min(wd_match.start(), m.start()))
        y = explicit_year or year or _resolve_year(day, month, today)
        try:
            real = _dt.date(y or 2000, month, day)  # 2000 is a leap year
        except ValueError:
            report.findings.append(Finding(
                "error", "BAD_DATE", line,
                f"'{m.group(0).strip()}' is not a real date.",
            ))
            return
        if y is None:
            unchecked = True
            return
        said = _WEEKDAYS[wd_match.group("wd").lower()]
        if real.weekday() != said:
            report.findings.append(Finding(
                "error", "WEEKDAY_MISMATCH", line,
                f"{real.strftime('%d %b %Y').lstrip('0')} is a {_WEEKDAY_NAMES[real.weekday()]}, "
                f"not {_WEEKDAY_NAMES[said]}. Fix the day or the date before sending.",
            ))

    for wd in _WD_RE.finditer(text):
        # weekday first: "Sat, 14 Nov"
        gap = _GAP_RE.match(text, wd.end())
        info = _date_at(text, gap.end(), date_order) if gap else None
        if info:
            evaluate(wd, info)
            continue
        # date first: "14 Nov (Sat)" -> look back for a date that ends in the gap
        window_start = max(0, wd.start() - 40)
        for rx in _DATE_RES:
            for m in rx.finditer(text, window_start, wd.start()):
                between = text[m.end():wd.start()]
                if re.fullmatch(r"[\s,()\-–—|·:]{0,4}", between):
                    info = _date_at(text, m.start(), date_order)
                    if info and info[0].end() == m.end():
                        evaluate(wd, info)
    if unchecked:
        report.findings.append(Finding(
            "note", "DATE_UNCHECKED", 0,
            "A weekday sits next to a date with no year; pass --today or --year to verify it.",
        ))


# --------------------------------------------------------------------------
# Lint
# --------------------------------------------------------------------------


def lint(
    text: str,
    kind: str = "message",
    year: Optional[int] = None,
    today: Optional[_dt.date] = None,
    date_order: Optional[str] = None,
    max_emoji: Optional[int] = None,
) -> Report:
    """Check ``text`` as a WhatsApp message of ``kind``. Returns a Report."""
    if kind not in LIMITS:
        raise ValueError(f"unknown kind {kind!r}; choose from {', '.join(KINDS)}")
    report = Report()
    add = report.findings.append
    masked = _mask(text)
    lines = text.split("\n")
    mlines = masked.split("\n")

    # ---- Markdown and HTML that WhatsApp shows literally -----------------
    for m in MD_LINK_RE.finditer(text):
        add(Finding("error", "MD_LINK", _line_of(text, m.start()),
                    f"Markdown link '{m.group(0)[:60]}' shows as raw brackets. "
                    f"Write '{m.group(1)}: {m.group(2)}' instead."))
    for m in MD_BOLD_RE.finditer(masked):
        add(Finding("error", "MD_BOLD", _line_of(masked, m.start()),
                    f"'{text[m.start():m.end()][:40]}' is Markdown bold; WhatsApp bold is one "
                    f"asterisk each side: *{text[m.start() + 2:m.end() - 2][:30]}*."))
    for m in HTML_RE.finditer(masked):
        add(Finding("error", "HTML_TAG", _line_of(masked, m.start()),
                    f"HTML tag '{m.group(0)}' shows as text on WhatsApp."))
    if text.count("```") % 2:
        add(Finding("error", "UNCLOSED_CODE", 0,
                    "Odd number of ``` fences: everything after the last one turns monospace."))

    i = 0
    while i < len(mlines):
        start = i
        while i < len(mlines) and (TABLE_ROW_RE.match(mlines[i]) or TABLE_SEP_RE.match(mlines[i])):
            i += 1
        block = mlines[start:i]
        if len(block) >= 2 or (block and block[0].count("|") >= 3):
            add(Finding("error", "MD_TABLE", start + 1,
                        "Markdown tables don't render. Put one row per line, e.g. '*Mon* · 10 am · Room 4'."))
        i = max(i, start + 1)
    for i, ml in enumerate(mlines):
        n = i + 1
        if HEADING_RE.match(ml):
            add(Finding("error", "MD_HEADING", n,
                        "'#' headings show as a literal '#'. Use a bold line: *Title*."))
        if HR_RE.match(ml):
            add(Finding("warn", "MD_RULE", n,
                        "'---' rules don't render. Use a blank line to separate blocks."))
        if NESTED_LIST_RE.match(ml):
            add(Finding("warn", "NESTED_LIST", n,
                        "Indented sub-bullets don't render as nesting. Flatten the list."))

    # ---- Formatting markers ---------------------------------------------
    for i, ml in enumerate(mlines):
        n = i + 1
        work = _strip_bullet(ml)
        for marker, name in (("*", "bold"), ("_", "italic")):
            pairs, odd = _pairs(work, marker)
            if odd:
                add(Finding("warn", "UNPAIRED_MARKER", n,
                            f"Unpaired {marker} on this line: the {name} won't apply and the {marker} "
                            f"shows literally. Markers can't span a line break; close it on the same line."))
            for a, b in pairs:
                inner = work[a + 1:b]
                if not inner.strip():
                    continue
                if inner[0].isspace() or inner[-1].isspace():
                    add(Finding("warn", "LOOSE_MARKER", n,
                                f"'{work[a:b + 1][:40]}': the {marker} must touch the text "
                                f"({marker}{inner.strip()[:30]}{marker}) or it won't format."))
                elif (a > 0 and work[a - 1].isalnum()) or (b + 1 < len(work) and work[b + 1].isalnum()):
                    add(Finding("warn", "GLUED_MARKER", n,
                                f"'{work[max(0, a - 3):b + 4]}': a marker touching a letter outside "
                                f"often doesn't format. Put a space or punctuation outside it."))

    # ---- Links ------------------------------------------------------------
    urls = _urls(text)
    for start, end, url in urls:
        before = text[start - 1] if start > 0 else ""
        after = text[end] if end < len(text) else ""
        if (before and before in "*_~") or (after and after in "*_~"):
            add(Finding("error", "MARKER_ON_LINK", _line_of(text, start),
                        f"Formatting marker touching {url[:50]}: it can break the tap-to-open link. "
                        f"Bold the label, not the URL."))
        if url.lower().startswith("www."):
            add(Finding("warn", "NO_SCHEME", _line_of(text, start),
                        f"'{url[:50]}' has no https://; some phones won't make it tappable."))

    # ---- Content quality ----------------------------------------------------
    for m in PLACEHOLDER_RE.finditer(masked):
        if REDACTION_LABEL_RE.fullmatch(m.group(0)) or CHAT_STAMP_RE.fullmatch(m.group(0)):
            continue  # [phone 1], [Person A] and [02/11/26, 10:15 AM] are deliberate
        add(Finding("warn", "PLACEHOLDER", _line_of(masked, m.start()),
                    f"Placeholder {text[m.start():m.end()]} still needs a real value."))
    for m in TBD_RE.finditer(masked):
        add(Finding("note", "TBD", _line_of(masked, m.start()),
                    f"'{m.group(0)}' left in the message. Fine if intended, but readers will ask."))
    for m in _AI_RE.finditer(masked):
        add(Finding("warn", "AI_PHRASE", _line_of(masked, m.start()),
                    f"'{m.group(0)}' reads as AI-written or a pasted email. Say it plainly."))
    for m in CHAIN_RE.finditer(masked):
        add(Finding("warn", "CHAIN_MESSAGE", _line_of(masked, m.start()),
                    f"'{m.group(0)}' is a chain-message pattern; WhatsApp flags and people mute these."))
    for m in EXCLAIM_RE.finditer(masked):
        add(Finding("warn", "EXCLAIM", _line_of(masked, m.start()),
                    f"'{m.group(0)}' reads as shouting. One ! is enough."))
    if re.search(r"\n[ \t]*\n[ \t]*\n", text):
        add(Finding("warn", "BLANK_LINES", _line_of(text, re.search(r"\n[ \t]*\n[ \t]*\n", text).start()) + 1,
                    "Two or more blank lines in a row. One blank line between blocks is enough."))
    for i, ml in enumerate(mlines):
        letters = [c for c in ml if c.isalpha()]
        caps_words = re.findall(r"\b[A-Z]{2,}\b", ml)
        if len(letters) >= 12 and len(caps_words) >= 3 and all(not c.islower() for c in letters):
            add(Finding("warn", "SHOUTING", i + 1,
                        "Whole line in capitals reads as shouting. Bold the one word that matters."))

    words = _words(masked)
    # Dashes: the clearest "an AI wrote this" sign in a chat. None at all.
    for i, line in enumerate(lines):
        if "—" in line:
            add(Finding("error", "EM_DASH", i + 1,
                        "Em dash (—) in the message. Use a comma, full stop, colon or a new line instead."))
        if "–" in line:
            add(Finding("error", "EN_DASH", i + 1,
                        "En dash (–) in the message. Use 'to' or a plain hyphen for ranges (10-12), "
                        "a comma or colon elsewhere."))
        if re.search(r"\S\s--\s\S", line):
            add(Finding("warn", "DOUBLE_HYPHEN", i + 1, "'--' used as a dash. Use a comma or full stop."))
        if re.match(r"^\s*[-–—]\s*[A-Z][\w.]*(?:\s[\w.&()']+){0,4}\s*$", line) and i == len(lines) - 1:
            add(Finding("warn", "DASH_SIGNOFF", i + 1,
                        "Sign-off starts with a dash: '- ' at the start of a line renders as a bullet. "
                        "Put the name alone on the last line."))

    emoji = count_emoji(text)
    if max_emoji is not None and emoji > max_emoji:
        add(Finding("error", "EMOJI_LIMIT", 0, f"{emoji} emoji, limit is {max_emoji}."))
    elif emoji > 3 and emoji * 6 > max(words, 1):
        add(Finding("warn", "EMOJI_HEAVY", 0,
                    f"{emoji} emoji in {words} words. Use them as line labels, not decoration."))

    mentions = MENTION_RE.findall(masked)
    if mentions:
        add(Finding("note", "MENTIONS", 0,
                    f"{', '.join(sorted(set(mentions))[:5])}: pasted @names are plain text. "
                    f"Retype @ in WhatsApp and pick the contact to tag them."))
    tags = HASHTAG_RE.findall(masked)
    if len(tags) >= 4:
        add(Finding("warn", "HASHTAGS", 0,
                    f"{len(tags)} hashtags. Hashtags aren't clickable or searchable on WhatsApp."))

    # ---- Length -------------------------------------------------------------
    chars = len(text)
    limit = LIMITS[kind]
    if chars > limit["hard"]:
        add(Finding("error", "TOO_LONG", 0,
                    f"{chars} characters; a WhatsApp {kind} allows {limit['hard']}. Cut {chars - limit['hard']}."))
    elif "soft" in limit and chars > limit["soft"]:
        add(Finding("warn", "LONG_CAPTION", 0,
                    f"{chars} characters for a caption. Keep it under {limit['soft']}: send the media with a short "
                    f"caption and the details as a second message."))

    _check_dates(text, year, today, date_order, report)

    for a, _, kind, _ in find_pii(text):
        if kind in HIGH_RISK:
            add(Finding("warn", "SENSITIVE", _line_of(text, a),
                        f"Looks like a {PII_LABELS[kind]} number. Don't share it in a chat unless you must; "
                        f"mask it with --redact."))

    report.stats = {
        "chars": chars,
        "words": words,
        "lines": len(lines),
        "emoji": emoji,
        "links": len(urls),
        "mentions": len(mentions),
    }
    order = {lvl: i for i, lvl in enumerate(LEVELS)}
    report.findings.sort(key=lambda f: (order[f.level], f.line, f.code))
    return report



# --------------------------------------------------------------------------
# Sensitive data: find and mask (whatsapp-redact)
# --------------------------------------------------------------------------

#: Kinds in detection order. Earlier kinds win when spans overlap, so the ones
#: recognised by a context word ("OTP", "A/c no") go before pattern-only ones.
PII_KINDS = ("otp", "account", "card", "aadhaar", "pan", "iban", "email", "upi", "phone")
PII_LABELS = {
    "card": "card", "aadhaar": "Aadhaar", "pan": "PAN", "iban": "IBAN", "otp": "code",
    "account": "account no.", "email": "email", "upi": "UPI ID", "phone": "phone",
}
#: Never fine in a WhatsApp message to a group or a stranger.
HIGH_RISK = ("card", "aadhaar", "pan", "iban", "otp")

_VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]
_VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]


def verhoeff_ok(digits: str) -> bool:
    """Aadhaar numbers end in a Verhoeff check digit."""
    c = 0
    for i, ch in enumerate(reversed(digits)):
        c = _VERHOEFF_D[c][_VERHOEFF_P[i % 8][int(ch)]]
    return c == 0


def luhn_ok(digits: str) -> bool:
    """Payment card numbers end in a Luhn check digit."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
    return total % 10 == 0


def iban_ok(raw: str) -> bool:
    s = raw.replace(" ", "").upper()
    if not 15 <= len(s) <= 34:
        return False
    moved = s[4:] + s[:4]
    return int("".join(str(int(ch, 36)) for ch in moved)) % 97 == 1


_PII_RES = {
    "card": re.compile(r"(?<![\d.])(?:\d[ -]?){12,18}\d(?![\d.])"),
    "aadhaar": re.compile(r"(?<![\d.])[2-9]\d{3}[ -]?\d{4}[ -]?\d{4}(?![\d.])"),
    "pan": re.compile(r"\b[A-Z]{3}[ABCFGHLJPTK][A-Z]\d{4}[A-Z]\b"),
    "iban": re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,4})?\b"),
    "otp": re.compile(r"\b(?:otp|one[- ]time (?:password|code)|verification code|security code|passcode|"
                      r"pin|cvv|password)\b\D{0,20}?(\d{3,8})\b", re.I),
    "account": re.compile(r"\b(?:a/?c|acc(?:ount)?|acct)\.?(?:\s*(?:no|number|num)\.?)?\s*[:#-]?\s*[`'\"]?"
                          r"(\d[\d -]{6,20}\d)", re.I),
    "email": re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+"),
    "upi": re.compile(r"(?<![\w.@-])[\w.-]{2,}@[A-Za-z]{2,}\b(?![.\w@])"),
    "phone": re.compile(
        r"(?<![\w+])(?:"
        r"\+\d{1,3}[ -]?(?:\(?\d+\)?[ -]?){1,4}\d+"      # +91 98765 43210, +44 20 7946 0958
        r"|[6-9]\d{4}[ -]?\d{5}"                            # Indian mobile, 10 digits
        r"|0\d{2,4}[ -]?\d{3,4}[ -]?\d{4}"                  # landline with STD code
        r")(?![\w])"
    ),
}
_WA_ME_RE = re.compile(r"(?:https?://)?wa\.me/(\d{8,15})")


def find_pii(text: str) -> List[Tuple[int, int, str, str]]:
    """Every sensitive value as (start, end, kind, value), in text order."""
    taken: List[Tuple[int, int]] = []
    found: List[Tuple[int, int, str, str]] = []
    url_spans = [(a, b) for a, b, _ in _urls(text)]

    def free(a: int, b: int) -> bool:
        return all(b <= x or a >= y for x, y in taken)

    def in_url(a: int, b: int) -> bool:
        return any(x <= a and b <= y for x, y in url_spans)

    for m in _WA_ME_RE.finditer(text):
        taken.append((m.start(1), m.end(1)))
        found.append((m.start(1), m.end(1), "phone", m.group(1)))
    for kind in PII_KINDS:
        for m in _PII_RES[kind].finditer(text):
            grp = 1 if kind in ("otp", "account") else 0
            a, b, value = m.start(grp), m.end(grp), m.group(grp)
            digits = re.sub(r"\D", "", value)
            if in_url(a, b) or not free(a, b):
                continue
            if kind == "card" and not (13 <= len(digits) <= 19 and luhn_ok(digits)):
                continue
            if kind == "aadhaar":
                context = text[max(0, a - 25):a].lower()
                if not (verhoeff_ok(digits) or "aadhaar" in context or "aadhar" in context or "uid" in context):
                    continue
            if kind == "iban" and not iban_ok(value):
                continue
            if kind == "phone" and value.startswith("+") and not 8 <= len(digits) <= 15:
                continue
            taken.append((a, b))
            found.append((a, b, kind, value))
    found.sort()
    return found


def _normalise(kind: str, value: str) -> str:
    return value.lower() if kind in ("email", "upi") else re.sub(r"[^0-9A-Za-z]", "", value)[-10:]


def _partial(kind: str, value: str) -> str:
    if kind in ("email", "upi"):
        local, _, domain = value.partition("@")
        return f"{local[:1]}***@{domain}"
    keep = 4
    alnum = [i for i, ch in enumerate(value) if ch.isalnum()]
    hide = set(alnum[:-keep]) if len(alnum) > keep else set(alnum)
    return "".join("X" if i in hide else ch for i, ch in enumerate(value))


def redact(text: str, style: str = "label", keep: Sequence[str] = ()) -> Tuple[str, Dict[str, int]]:
    """Mask sensitive values. ``style="label"`` gives consistent stand-ins
    ([phone 1], [phone 2]: the same number gets the same label every time);
    ``style="partial"`` keeps the last 4 characters (XXXXX X3210).
    Returns the new text and a count per kind."""
    hits = [h for h in find_pii(text) if h[2] not in keep]
    distinct: Dict[str, List[str]] = {}
    for _, _, kind, value in hits:
        key = _normalise(kind, value)
        distinct.setdefault(kind, [])
        if key not in distinct[kind]:
            distinct[kind].append(key)
    out, last = [], 0
    for a, b, kind, value in hits:
        out.append(text[last:a])
        if style == "partial":
            out.append(_partial(kind, value))
        else:
            names = distinct[kind]
            n = names.index(_normalise(kind, value)) + 1
            out.append(f"[{PII_LABELS[kind]}{f' {n}' if len(names) > 1 else ''}]")
        last = b
    out.append(text[last:])
    return "".join(out), {k: len(v) for k, v in distinct.items()}

# --------------------------------------------------------------------------
# Fix: convert Markdown / HTML / email-ish text into WhatsApp formatting
# --------------------------------------------------------------------------


def _fix_markers(line: str) -> str:
    """Tighten loose markers: '*Venue *' -> '*Venue*'."""
    for marker in ("*", "_"):
        work = _strip_bullet(line) if marker == "*" else line
        pairs, _ = _pairs(work, marker)
        for a, b in reversed(pairs):
            inner = line[a + 1:b]
            if inner.strip() and (inner[0].isspace() or inner[-1].isspace()):
                lead = " " if a > 0 and not line[a - 1].isspace() and inner[0].isspace() else ""
                trail = " " if b + 1 < len(line) and not line[b + 1].isspace() and inner[-1].isspace() else ""
                line = line[:a] + lead + marker + inner.strip() + marker + trail + line[b + 1:]
    return line


def _fix_table(rows: List[str]) -> List[str]:
    out = []
    header_done = False
    for row in rows:
        if TABLE_SEP_RE.match(row):
            continue
        cells = [c.strip().replace("**", "") for c in row.strip().strip("|").split("|")]
        cells = [c for c in cells if c]
        if not cells:
            continue
        if not header_done:
            out.append("*" + " · ".join(cells) + "*")
            header_done = True
        else:
            out.append(" · ".join(cells))
    return out


def _fix_prose(segment: str) -> str:
    tokens: List[str] = []

    def protect(value: str) -> str:
        tokens.append(value)
        return f"\x01{len(tokens) - 1}\x01"

    s = segment
    # HTML first, it can contain links
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<a\s[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>",
               lambda m: m.group(1) if m.group(2).strip() in ("", m.group(1)) else f"{m.group(2)}: {m.group(1)}",
               s, flags=re.I | re.S)
    s = re.sub(r"<(b|strong)>(.*?)</\1>", r"*\2*", s, flags=re.I | re.S)
    s = re.sub(r"<(i|em)>(.*?)</\1>", r"_\2_", s, flags=re.I | re.S)
    s = re.sub(r"<(s|del|strike)>(.*?)</\1>", r"~\2~", s, flags=re.I | re.S)
    s = re.sub(r"<li[^>]*>", "- ", s, flags=re.I)
    s = re.sub(r"</(p|div|li|h[1-6])>", "\n", s, flags=re.I)
    s = HTML_RE.sub("", s)

    # Markdown links -> "label: url"
    def link(m: "re.Match[str]") -> str:
        label, url = m.group(1).strip().strip("*_"), m.group(2)
        if url.lower().startswith("www."):
            url = "https://" + url
        bare = re.sub(r"^(?:https?://|mailto:|tel:)", "", url, flags=re.I).rstrip("/")
        if label.rstrip("/") in (url.rstrip("/"), bare):
            return protect(url)
        return f"{label}: " + protect(url)

    s = MD_LINK_RE.sub(link, s)
    s = INLINE_CODE_RE.sub(lambda m: protect(m.group(0)), s)

    def url(m: "re.Match[str]") -> str:
        raw = m.group(0)
        clean = _trim_url(raw)
        fixed = ("https://" + clean) if clean.lower().startswith("www.") else clean
        return protect(fixed) + raw[len(clean):]

    s = URL_RE.sub(url, s)

    lines = s.split("\n")
    out: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if TABLE_ROW_RE.match(line) or TABLE_SEP_RE.match(line):
            block = []
            while i < len(lines) and (TABLE_ROW_RE.match(lines[i]) or TABLE_SEP_RE.match(lines[i])):
                block.append(lines[i])
                i += 1
            if len(block) >= 2:
                out.extend(_fix_table(block))
                continue
            line = block[0]
            i -= 1
        heading = re.match(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$", line)
        if heading:
            title = heading.group(1).replace("**", "").strip().strip("*_").strip()
            line = f"*{title}*" if title else ""
        elif HR_RE.match(line):
            line = ""
        else:
            line = re.sub(r"^(\s*)\+\s+", r"\1- ", line)
            nested = re.match(r"^(?: {2,}|\t+)((?:[-*•+]|\d{1,2}[.)])\s+.*)$", line)
            if nested:
                line = nested.group(1).replace("+ ", "- ", 1) if nested.group(1).startswith("+") else nested.group(1)
            line = re.sub(r"\*\*\*(?=\S)(.+?)(?<=\S)\*\*\*", r"*_\1_*", line)
            line = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"*\1*", line)
            line = re.sub(r"(?<![\w])__(?=\S)(.+?)(?<=\S)__(?![\w])", r"*\1*", line)
            line = _fix_markers(line)
        out.append(line.rstrip())
        i += 1
    s = "\n".join(out)

    # markers wrapped around a protected URL: *https://...* -> https://...
    s = re.sub(r"([*_~])(\x01\d+\x01)\1", r"\2", s)
    s = re.sub(r"\x01(\d+)\x01", lambda m: tokens[int(m.group(1))], s)
    return s


def _fix_dashes(s: str) -> str:
    """Remove em and en dashes outside code. Number ranges get a hyphen (2-4),
    spaced ranges of times and dates get "to", a dash starting a line (a
    sign-off) is dropped, and every other dash becomes a comma."""
    out = []
    for part in re.split(r"(```[\s\S]*?```|`[^`\n]+`)", s):
        if part.startswith("`"):
            out.append(part)
            continue
        part = re.sub(r"(\d)[–—](\d)", r"\1-\2", part)  # 2–4 -> 2-4
        # spaced ranges of times, dates and days: "10 am – 6 pm", "5 Dec – Sun, 6 Dec"
        part = re.sub(r"(?<=\S)\s+[–—]\s+(?=\d|(?:mon|tue|wed|thu|fri|sat|sun|jan|feb|mar|apr|may|jun|"
                      r"jul|aug|sep|oct|nov|dec)[a-z]*\b)", " to ", part, flags=re.I)
        part = re.sub(r"(?m)^([ \t]*)[–—][ \t]*", r"\1", part)
        part = re.sub(r"\s*[–—]\s*", ", ", part)
        part = re.sub(r"(?<=\S) -- (?=\S)", ", ", part)
        part = re.sub(r",\s*([,.!?;:])", r"\1", part)
        out.append(part)
    return "".join(out)


def fix(text: str) -> str:
    """Return ``text`` converted to WhatsApp formatting. Code blocks are kept,
    only a language tag on the opening fence is dropped (```python -> ```)."""
    parts: List[str] = []
    last = 0
    for m in re.finditer(r"```[^\n`]*\n[\s\S]*?```|```[\s\S]*?```", text):
        parts.append(_fix_prose(text[last:m.start()]))
        block = re.sub(r"^```[^\n`]*\n", "```", m.group(0))
        parts.append(block)
        last = m.end()
    parts.append(_fix_prose(text[last:]))
    s = "".join(parts)
    s = _fix_dashes(s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip("\n") + ("\n" if text.endswith("\n") else "")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _format_report(report: Report, kind: str) -> str:
    st = report.stats
    head = (f"wa_lint ({kind}): {st['chars']} chars · {st['words']} words · {st['lines']} lines · "
            f"{st['emoji']} emoji · {st['links']} links")
    rows = [head]
    for f in report.findings:
        where = f"L{f.line}" if f.line else "  -"
        rows.append(f"{f.level:<5} {where:<4} {f.code:<16} {f.message}")
    n_err, n_warn = len(report.errors), len(report.warnings)
    if n_err:
        rows.append(f"✗ {n_err} error(s), {n_warn} warning(s). Fix the errors before sending.")
    elif n_warn:
        rows.append(f"✓ no errors, {n_warn} warning(s) to review.")
    else:
        rows.append("✓ ready to paste.")
    return "\n".join(rows)


def _parse_date(value: str) -> _dt.date:
    try:
        return _dt.date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected YYYY-MM-DD, got {value!r}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="wa_lint",
        description="Check a WhatsApp message for formatting that won't render, date mistakes and length limits.",
    )
    p.add_argument("path", help="file with the message, or - for stdin")
    p.add_argument("--kind", choices=KINDS, default="message", help="message type, sets length limits")
    p.add_argument("--today", type=_parse_date, default=None,
                   help="reference date YYYY-MM-DD for dates without a year (default: system date)")
    p.add_argument("--year", type=int, default=None, help="assume this year for dates without one")
    p.add_argument("--no-today", action="store_true", help="don't assume a year for dates without one")
    p.add_argument("--date-order", choices=("dmy", "mdy"), default=None,
                   help="how to read numeric dates like 10/11 (default: only unambiguous ones)")
    p.add_argument("--max-emoji", type=int, default=None, help="fail when the message has more emoji")
    p.add_argument("--fix", action="store_true",
                   help="print the message converted to WhatsApp formatting; the report goes to stderr")
    p.add_argument("--redact", action="store_true",
                   help="print the text with sensitive values masked; a summary goes to stderr")
    p.add_argument("--style", choices=("label", "partial"), default="label",
                   help="--redact style: [phone 1] labels (default) or partial XXXXX X3210")
    p.add_argument("--keep", default="", help="--redact: comma-separated kinds to leave visible, e.g. phone,email")
    p.add_argument("--pii", action="store_true", help="list every sensitive value found, without changing the text")
    p.add_argument("--json", action="store_true", help="print the report as JSON")
    p.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    p.add_argument("--version", action="version", version=f"wa_lint {__version__}")
    args = p.parse_args(argv)

    try:
        if args.path == "-":
            text = sys.stdin.read()
        else:
            with open(args.path, encoding="utf-8") as fh:
                text = fh.read()
    except OSError as exc:
        print(f"wa_lint: cannot read {args.path}: {exc.strerror}", file=sys.stderr)
        return 2

    today = None if args.no_today else (args.today or _dt.date.today())
    if args.redact or args.pii:
        keep = tuple(k.strip() for k in args.keep.split(",") if k.strip())
        unknown = set(keep) - set(PII_KINDS)
        if unknown:
            print(f"wa_lint: unknown --keep kind(s): {', '.join(sorted(unknown))}; "
                  f"choose from {', '.join(PII_KINDS)}", file=sys.stderr)
            return 2
        hits = find_pii(text)
        if args.pii:
            rows = [{"line": _line_of(text, a), "kind": k, "value": v} for a, _, k, v in hits]
            if args.json:
                print(json.dumps(rows, ensure_ascii=False, indent=2))
            else:
                for r in rows:
                    print(f"L{r['line']:<4} {PII_LABELS[r['kind']]:<12} {r['value']}")
                print(f"{len(rows)} sensitive value(s) found.")
            return 0
        masked, counts = redact(text, style=args.style, keep=keep)
        sys.stdout.write(masked if masked.endswith("\n") else masked + "\n")
        summary = ", ".join(f"{n} {PII_LABELS[k]}" for k, n in counts.items()) or "nothing"
        print(f"wa_lint --redact: masked {summary}. Names, addresses and other context still need a human read.",
              file=sys.stderr)
        return 0
    if args.fix:
        text = fix(text)
        sys.stdout.write(text if text.endswith("\n") else text + "\n")
    report = lint(text.rstrip("\n"), kind=args.kind, year=args.year, today=today,
                  date_order=args.date_order, max_emoji=args.max_emoji)
    out = sys.stderr if args.fix else sys.stdout
    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), file=out)
    else:
        print(_format_report(report, args.kind), file=out)
    failed = bool(report.errors) or (args.strict and bool(report.warnings))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
