#!/usr/bin/env python3
"""wa_chat: read a WhatsApp chat export so a long group chat can be summarised.

Parses the .txt file from WhatsApp's "Export chat" (Android and iPhone formats,
12- or 24-hour clocks, multi-line messages, system lines) and prints the part
you need, with the numbers a summary should be built on.

Usage
    python3 wa_chat.py chat.txt                      # overview: dates, people, links, media
    python3 wa_chat.py chat.txt --since 2026-11-01   # only messages from that date
    python3 wa_chat.py chat.txt --last 200           # only the last 200 messages
    python3 wa_chat.py chat.txt --mentions Priya     # messages that name or tag Priya
    python3 wa_chat.py chat.txt --from Rahul         # messages Rahul sent
    python3 wa_chat.py chat.txt --messages           # print the filtered messages
    python3 wa_chat.py chat.txt --json               # everything as JSON

Exit codes: 0 ok, 1 no messages recognised, 2 usage problem.
Standard library only. Python 3.9+. Nothing leaves your machine.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import List, Optional, Sequence

__version__ = "1.0.0"

# Invisible marks iPhone exports put around names and at line starts.
_INVISIBLE = "‎‏‪‬⁨⁩﻿"

# [02/11/26, 10:15:32 AM] Rahul: text          (iPhone)
# 02/11/2026, 10:15 - Rahul: text              (Android, 24 h)
# 2/11/26, 10:15 pm - Rahul: text              (Android, 12 h)
LINE_RE = re.compile(
    r"^\[?(?P<date>\d{1,4}[./-]\d{1,2}[./-]\d{1,4}),?\s+"
    r"(?P<time>\d{1,2}[:.]\d{2}(?:[:.]\d{2})?(?:\s?[APap]\.?\s?[Mm]\.?)?)\]?"
    r"\s*(?:-|–|:)?\s*(?P<rest>.*)$"
)
SENDER_RE = re.compile(r"^(?P<sender>[^:]{1,80}?):\s(?P<text>.*)$", re.S)
URL_RE = re.compile(r"https?://[^\s<>]+")
MEDIA_RE = re.compile(
    r"<Media omitted>|\b(?:image|video|audio|sticker|GIF|document|Contact card) omitted\b|"
    r"\(file attached\)|\.(?:jpg|jpeg|png|webp|mp4|opus|pdf|docx?|xlsx?|pptx?) \(file attached\)",
    re.I,
)
DELETED_RE = re.compile(r"^(?:This message was deleted|You deleted this message)\.?$", re.I)
SYSTEM_HINTS = re.compile(
    r"end-to-end encrypted|created group|created this group|added|removed|left$|joined using|"
    r"changed the (?:subject|group|description|icon)|changed this group|security code|"
    r"is now an admin|disappearing messages|pinned a message|now a community",
    re.I,
)


SYSTEM_TEXT = re.compile(r"^(?:Messages and calls are end-to-end encrypted|Messages to this group are now secured|"
                         r"This group was created|You joined|You were added)", re.I)


@dataclass
class Message:
    when: str  # ISO timestamp
    sender: Optional[str]  # None for system lines
    text: str
    media: bool = False
    deleted: bool = False
    system: bool = False

    @property
    def date(self) -> dt.date:
        return dt.datetime.fromisoformat(self.when).date()


@dataclass
class Overview:
    messages: int = 0
    first: Optional[str] = None
    last: Optional[str] = None
    days: int = 0
    senders: List[List] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    media: int = 0
    deleted: int = 0
    system: int = 0
    date_order: str = "dmy"


def _clean(s: str) -> str:
    return s.translate({ord(c): None for c in _INVISIBLE}).replace(" ", " ").replace("\xa0", " ")


def guess_date_order(dates: Sequence[str]) -> str:
    """dmy or mdy, from the first two numbers of every date. ymd stays ymd."""
    firsts, seconds = [], []
    for d in dates:
        parts = re.split(r"[./-]", d)
        if len(parts[0]) == 4:
            return "ymd"
        firsts.append(int(parts[0]))
        seconds.append(int(parts[1]))
    if any(n > 12 for n in seconds):
        return "mdy"
    return "dmy"  # also the default when nothing disambiguates


def _parse_when(date: str, time: str, order: str) -> dt.datetime:
    a, b, c = (int(x) for x in re.split(r"[./-]", date))
    if order == "ymd":
        y, m, d = a, b, c
    elif order == "mdy":
        m, d, y = a, b, c
    else:
        d, m, y = a, b, c
    if y < 100:
        y += 2000
    t = time.strip().lower().replace(".", ":").replace(" ", "")
    pm = t.endswith(("pm", "p:m:", "pm:"))
    am = t.endswith(("am", "a:m:", "am:"))
    t = re.sub(r"[ap]:?m:?$", "", t)
    parts = [int(x) for x in t.split(":") if x]
    hour, minute = parts[0], parts[1]
    second = parts[2] if len(parts) > 2 else 0
    if pm and hour < 12:
        hour += 12
    if am and hour == 12:
        hour = 0
    return dt.datetime(y, m, d, hour, minute, second)


def parse(text: str, date_order: Optional[str] = None) -> List[Message]:
    raw_lines = text.splitlines()
    lines = [_clean(l) for l in raw_lines]
    heads = [(i, m) for i, l in enumerate(lines) if (m := LINE_RE.match(l.strip()))]
    if not heads:
        return []
    order = date_order or guess_date_order([m.group("date") for _, m in heads])
    out: List[Message] = []
    for n, (i, m) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        body = "\n".join([m.group("rest")] + lines[i + 1:end]).strip()
        try:
            when = _parse_when(m.group("date"), m.group("time"), order)
        except ValueError:
            continue
        sm = SENDER_RE.match(body)
        # iPhone puts system lines under the group's name and marks the text with
        # an invisible left-to-right mark; media lines carry the same mark.
        marked = bool(re.search(r":\s\u200e", raw_lines[i]))
        is_media = bool(sm and MEDIA_RE.search(sm.group("text")))
        system_text = bool(sm and SYSTEM_TEXT.search(sm.group("text")))
        if sm and not SYSTEM_HINTS.search(sm.group("sender")) and not system_text and not (marked and not is_media):
            sender, msg = sm.group("sender").strip(), sm.group("text").strip()
            out.append(Message(when.isoformat(), sender, msg,
                               media=bool(MEDIA_RE.search(msg)), deleted=bool(DELETED_RE.match(msg))))
        else:
            out.append(Message(when.isoformat(), None, body, system=True))
    return out


def filter_messages(msgs: List[Message], since: Optional[dt.date] = None, last: Optional[int] = None,
                    sender: Optional[str] = None, mentions: Optional[str] = None) -> List[Message]:
    out = [m for m in msgs if not since or m.date >= since]
    if sender:
        out = [m for m in out if m.sender and sender.lower() in m.sender.lower()]
    if mentions:
        rx = re.compile(r"(?<!\w)@?" + re.escape(mentions) + r"(?!\w)", re.I)
        out = [m for m in out if rx.search(m.text)]
    if last:
        out = out[-last:]
    return out


def overview(msgs: List[Message], date_order: str = "dmy") -> Overview:
    talk = [m for m in msgs if not m.system]
    ov = Overview(date_order=date_order)
    ov.messages = len(talk)
    if msgs:
        ov.first, ov.last = msgs[0].when, msgs[-1].when
        ov.days = len({m.date for m in msgs})
    ov.senders = [[s, n] for s, n in Counter(m.sender for m in talk).most_common()]
    seen = []
    for m in talk:
        for url in URL_RE.findall(m.text):
            url = url.rstrip(".,;:!?)")
            if url not in seen:
                seen.append(url)
    ov.links = seen
    ov.media = sum(m.media for m in talk)
    ov.deleted = sum(m.deleted for m in talk)
    ov.system = len(msgs) - len(talk)
    return ov


def _fmt(m: Message) -> str:
    when = dt.datetime.fromisoformat(m.when).strftime("%a %d %b %H:%M")
    who = m.sender or "·system·"
    text = "[media]" if m.media and len(m.text) < 40 else m.text
    return f"{when}  {who}: {text}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="wa_chat", description="Read a WhatsApp chat export.")
    p.add_argument("path", help="the exported .txt file, or - for stdin")
    p.add_argument("--since", type=dt.date.fromisoformat, help="only messages on or after YYYY-MM-DD")
    p.add_argument("--last", type=int, help="only the last N messages")
    p.add_argument("--from", dest="sender", help="only messages from this sender (name contains)")
    p.add_argument("--mentions", help="only messages that name or @tag this person")
    p.add_argument("--date-order", choices=("dmy", "mdy", "ymd"), help="override the guessed date order")
    p.add_argument("--messages", action="store_true", help="print the filtered messages too")
    p.add_argument("--json", action="store_true", help="print overview and messages as JSON")
    p.add_argument("--version", action="version", version=f"wa_chat {__version__}")
    args = p.parse_args(argv)
    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
    except OSError as exc:
        print(f"wa_chat: cannot read {args.path}: {exc.strerror}", file=sys.stderr)
        return 2

    msgs = parse(text, args.date_order)
    if not msgs:
        print("wa_chat: no WhatsApp messages recognised. Is this an exported chat (.txt)?", file=sys.stderr)
        return 1
    order = args.date_order or guess_date_order(
        [m.group("date") for l in text.splitlines() if (m := LINE_RE.match(_clean(l).strip()))])
    picked = filter_messages(msgs, args.since, args.last, args.sender, args.mentions)
    ov = overview(picked, order)
    if args.json:
        print(json.dumps({"overview": asdict(ov), "messages": [asdict(m) for m in picked]},
                         ensure_ascii=False, indent=2))
        return 0
    span = f"{ov.first[:16].replace('T', ' ')} to {ov.last[:16].replace('T', ' ')}" if ov.first else "-"
    print(f"{ov.messages} messages over {ov.days} day(s), {span} (dates read as {order})")
    print("People: " + ", ".join(f"{s} ({n})" for s, n in ov.senders[:12]))
    print(f"Media: {ov.media} · deleted: {ov.deleted} · system lines: {ov.system}")
    if ov.links:
        print("Links:")
        for url in ov.links:
            print(f"  {url}")
    if args.messages:
        print()
        for m in picked:
            print(_fmt(m))
    return 0


if __name__ == "__main__":
    sys.exit(main())
