"""wa_chat: reads real-looking Android and iPhone exports correctly."""
from __future__ import annotations

import datetime as dt
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout

from helpers import ROOT, load_module

wa_chat = load_module("wa_chat", ROOT / "skills" / "whatsapp-catchup" / "scripts" / "wa_chat.py")

IOS = (
    "\u200e[01/11/26, 9:02:11 PM] Flat 4B Society: \u200eMessages and calls are end-to-end encrypted.\n"
    "[01/11/26, 9:05:40 PM] Rakesh Secretary: AGM is on Sun, 15 Nov at 11 am.\n"
    "Agenda: maintenance hike, parking.\n"
    "[01/11/26, 9:07:02 PM] Meera B-1204: Can we also discuss the lift?\n"
    "[02/11/26, 8:15:00 AM] Rakesh Secretary: Yes added. @Priya please share accounts https://docs.google.com/x\n"
    "[02/11/26, 8:16:10 AM] Priya: \u200eimage omitted\n"
    "[02/11/26, 8:17:10 AM] Priya: This message was deleted\n"
)
ANDROID = (
    "15/11/2026, 21:05 - Asha: hi all\n"
    "15/11/2026, 21:06 - Asha added Ravi\n"
    "16/11/2026, 07:00 - Ravi: <Media omitted>\n"
    "16/11/2026, 07:01 - Ravi: line one\nline two\n"
)
US_12H = "11/15/26, 9:05 PM - Jo: dinner at 8?\n11/15/26, 9:06 PM - Sam: yes\n"


class Parse(unittest.TestCase):
    def test_ios(self):
        msgs = wa_chat.parse(IOS)
        self.assertEqual(len(msgs), 6)
        self.assertTrue(msgs[0].system, "encryption notice under the group name is a system line")
        self.assertEqual(msgs[1].sender, "Rakesh Secretary")
        self.assertEqual(msgs[1].text, "AGM is on Sun, 15 Nov at 11 am.\nAgenda: maintenance hike, parking.")
        self.assertEqual(msgs[1].when, "2026-11-01T21:05:40")
        self.assertTrue(msgs[4].media and not msgs[4].system)
        self.assertTrue(msgs[5].deleted)

    def test_android_24h_system_and_multiline(self):
        msgs = wa_chat.parse(ANDROID)
        self.assertEqual([m.sender for m in msgs], ["Asha", None, "Ravi", "Ravi"])
        self.assertTrue(msgs[1].system)
        self.assertTrue(msgs[2].media)
        self.assertEqual(msgs[3].text, "line one\nline two")
        self.assertEqual(msgs[0].when, "2026-11-15T21:05:00")

    def test_month_first_dates_are_detected(self):
        self.assertEqual(wa_chat.guess_date_order(["11/15/26"]), "mdy")
        msgs = wa_chat.parse(US_12H)
        self.assertEqual(msgs[0].when, "2026-11-15T21:05:00")

    def test_12am_and_12pm(self):
        msgs = wa_chat.parse("01/11/26, 12:05 AM - A: x\n01/11/26, 12:05 PM - A: y\n")
        self.assertEqual([m.when[11:16] for m in msgs], ["00:05", "12:05"])

    def test_not_an_export(self):
        self.assertEqual(wa_chat.parse("hello\nthis is not a chat"), [])


class Filters(unittest.TestCase):
    def setUp(self):
        self.msgs = wa_chat.parse(IOS)

    def test_since(self):
        got = wa_chat.filter_messages(self.msgs, since=dt.date(2026, 11, 2))
        self.assertEqual(len(got), 3)

    def test_mentions(self):
        got = wa_chat.filter_messages(self.msgs, mentions="Priya")
        self.assertEqual(len(got), 1)
        self.assertIn("@Priya", got[0].text)

    def test_from_and_last(self):
        self.assertEqual(len(wa_chat.filter_messages(self.msgs, sender="rakesh")), 2)
        self.assertEqual(len(wa_chat.filter_messages(self.msgs, last=2)), 2)

    def test_overview(self):
        ov = wa_chat.overview(self.msgs)
        self.assertEqual(ov.messages, 5)
        self.assertEqual(ov.system, 1)
        self.assertEqual(ov.links, ["https://docs.google.com/x"])
        self.assertEqual(ov.media, 1)
        self.assertEqual(ov.deleted, 1)
        self.assertEqual(ov.senders[0], ["Rakesh Secretary", 2])
        self.assertEqual(ov.days, 2)


class CLI(unittest.TestCase):
    def run_cli(self, text, *args):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chat.txt"
            path.write_text(text, encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = wa_chat.main([str(path), *args])
            return code, out.getvalue(), err.getvalue()

    def test_overview_output(self):
        code, out, _ = self.run_cli(IOS)
        self.assertEqual(code, 0)
        self.assertIn("5 messages over 2 day(s)", out)
        self.assertIn("https://docs.google.com/x", out)

    def test_json(self):
        code, out, _ = self.run_cli(ANDROID, "--json", "--since", "2026-11-16")
        data = json.loads(out)
        self.assertEqual(data["overview"]["messages"], 2)

    def test_unrecognised(self):
        self.assertEqual(self.run_cli("not a chat")[0], 1)


if __name__ == "__main__":
    unittest.main()
