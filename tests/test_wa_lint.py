"""wa_lint: every check fires on the mistake it targets and stays quiet on the
look-alikes people type every day (5 * 3, ~5 km, file_name.pdf, @handles)."""
from __future__ import annotations

import datetime as dt
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import tempfile

from helpers import wa_lint

TODAY = dt.date(2026, 11, 2)


def codes(text, level=None, **kw):
    kw.setdefault("today", TODAY)
    return wa_lint.lint(text, **kw).codes(level)


class MarkdownLeaks(unittest.TestCase):
    def test_double_asterisk_bold(self):
        self.assertIn("MD_BOLD", codes("**Venue:** Hall 2", "error"))

    def test_double_underscore_bold(self):
        self.assertIn("MD_BOLD", codes("__Note__ bring ID", "error"))

    def test_heading(self):
        self.assertIn("MD_HEADING", codes("## Agenda\nItem one", "error"))

    def test_hashtag_is_not_a_heading(self):
        self.assertNotIn("MD_HEADING", codes("#Diwali sale"))

    def test_markdown_link(self):
        self.assertIn("MD_LINK", codes("Register [here](https://forms.gle/x)", "error"))

    def test_table_reported_once(self):
        text = "| Day | Time |\n|---|---|\n| Sat | 10 am |"
        self.assertEqual(codes(text, "error").count("MD_TABLE"), 1)

    def test_horizontal_rule(self):
        self.assertIn("MD_RULE", codes("Part one\n---\nPart two", "warn"))

    def test_html(self):
        self.assertIn("HTML_TAG", codes("Hello<br>world", "error"))

    def test_unclosed_code_fence(self):
        self.assertIn("UNCLOSED_CODE", codes("Code: ```1234", "error"))

    def test_nested_list(self):
        self.assertIn("NESTED_LIST", codes("- Food\n  - Veg\n  - Non-veg", "warn"))


class Markers(unittest.TestCase):
    def test_clean_whatsapp_formatting_passes(self):
        text = "*Date:* Sat, 14 Nov\n_bring your ID_\n~₹999~ *₹699*\n- item one\n* item two\n> note\n`CODE10`"
        self.assertEqual(codes(text, "error"), [])
        self.assertEqual(codes(text, "warn"), [])

    def test_loose_closing_marker(self):
        self.assertIn("LOOSE_MARKER", codes("*Venue * is fixed", "warn"))

    def test_loose_opening_marker(self):
        self.assertIn("UNPAIRED_MARKER", codes("* Venue* is fixed", "warn"))

    def test_marker_spanning_lines(self):
        self.assertEqual(codes("*Line one\nline two*", "warn").count("UNPAIRED_MARKER"), 2)

    def test_glued_marker(self):
        self.assertIn("GLUED_MARKER", codes("abc*def* ghi", "warn"))

    def test_bullet_is_not_a_marker(self):
        self.assertEqual(codes("* Bring laptop\n* Bring charger"), [])

    def test_math_asterisk_is_literal(self):
        self.assertEqual(codes("Total: 5 * 3 = 15"), [])

    def test_tilde_approximation(self):
        self.assertEqual(codes("~5 km from the station"), [])

    def test_underscores_inside_words(self):
        self.assertEqual(codes("Notes: Physics_Ch3_v2.pdf", "warn"), [])

    def test_italic_underscore_pair(self):
        self.assertEqual(codes("_please be on time_", "warn"), [])

    def test_markers_inside_code_ignored(self):
        self.assertEqual(codes("Use `**this**` literally", "error"), [])


class Links(unittest.TestCase):
    def test_marker_on_link(self):
        self.assertIn("MARKER_ON_LINK", codes("*https://example.com/x*", "error"))

    def test_bold_label_then_link_is_fine(self):
        self.assertEqual(codes("*Register:* https://forms.gle/AbC_12", "error"), [])

    def test_www_without_scheme(self):
        self.assertIn("NO_SCHEME", codes("Visit www.example.com", "warn"))

    def test_url_underscores_not_italic(self):
        self.assertEqual(codes("https://example.com/a_b_c_d", "warn"), [])

    def test_link_count_stat(self):
        r = wa_lint.lint("a https://x.com b https://y.com.", today=TODAY)
        self.assertEqual(r.stats["links"], 2)


class Dates(unittest.TestCase):
    def test_correct_weekday(self):
        self.assertEqual(codes("Sat, 14 Nov 2026"), [])

    def test_wrong_weekday(self):
        r = wa_lint.lint("Friday, 14 Nov 2026", today=TODAY)
        self.assertIn("WEEKDAY_MISMATCH", r.codes("error"))
        self.assertIn("Saturday", r.errors[0].message)

    def test_wrong_weekday_month_first(self):
        self.assertIn("WEEKDAY_MISMATCH", codes("Thursday, November 14th", "error"))

    def test_date_then_weekday_in_brackets(self):
        self.assertIn("WEEKDAY_MISMATCH", codes("14 Nov (Fri)", "error"))
        self.assertEqual(codes("14 Nov (Sat)", "error"), [])

    def test_year_inferred_from_today(self):
        self.assertIn("WEEKDAY_MISMATCH", codes("Friday 7 Nov", "error"))

    def test_next_year_inferred_for_january(self):
        # From December 2026, "Sat, 23 Jan" means 2027, which is a Saturday.
        self.assertEqual(codes("Sat, 23 Jan", "error", today=dt.date(2026, 12, 20)), [])

    def test_explicit_year_flag(self):
        self.assertIn("WEEKDAY_MISMATCH", codes("Sat 14 Nov", "error", year=2027))

    def test_no_reference_date_is_a_note(self):
        r = wa_lint.lint("Sat, 14 Nov", today=None)
        self.assertEqual(r.codes("error"), [])
        self.assertIn("DATE_UNCHECKED", r.codes("note"))

    def test_impossible_date(self):
        self.assertIn("BAD_DATE", codes("Mon, 31 Nov", "error"))

    def test_24h_time_is_not_a_year(self):
        self.assertEqual(codes("Sat 14 Nov 1930 hrs", "error"), [])

    def test_time_is_not_a_date(self):
        self.assertEqual(codes("Sat 7.30 pm and Sat 7-9 pm", "error"), [])

    def test_numeric_date_unambiguous(self):
        self.assertIn("WEEKDAY_MISMATCH", codes("Fri 14/11/2026", "error"))

    def test_numeric_date_ambiguous_skipped(self):
        self.assertEqual(codes("Fri 10/11/2026", "error"), [])
        self.assertIn("WEEKDAY_MISMATCH", codes("Fri 10/11/2026", "error", date_order="dmy"))

    def test_sat_as_verb_is_ignored(self):
        self.assertEqual(codes("We sat 14 people at the table"), [])


class Content(unittest.TestCase):
    def test_placeholder(self):
        self.assertIn("PLACEHOLDER", codes("Venue: [venue]", "warn"))

    def test_tbd_note(self):
        self.assertIn("TBD", codes("Venue: TBA", "note"))

    def test_ai_phrase(self):
        self.assertIn("AI_PHRASE", codes("I hope this message finds you well.", "warn"))

    def test_unlocked_is_fine(self):
        self.assertNotIn("AI_PHRASE", codes("The gate will be unlocked at 6."))

    def test_chain_message(self):
        self.assertIn("CHAIN_MESSAGE", codes("Forward this to 10 groups now", "warn"))

    def test_shouting(self):
        self.assertIn("SHOUTING", codes("PLEASE READ THIS NOW EVERYONE", "warn"))

    def test_one_caps_word_is_fine(self):
        self.assertNotIn("SHOUTING", codes("URGENT: water cut at 10 am"))

    def test_exclamations(self):
        self.assertIn("EXCLAIM", codes("Sale today!!!", "warn"))

    def test_blank_lines(self):
        self.assertIn("BLANK_LINES", codes("a\n\n\nb", "warn"))

    def test_any_em_dash_is_an_error(self):
        self.assertIn("EM_DASH", codes("Big news — we are live", "error"))

    def test_any_en_dash_is_an_error(self):
        self.assertIn("EN_DASH", codes("Open 10 am – 6 pm", "error"))

    def test_hyphens_are_fine(self):
        self.assertEqual(codes("A well-known 2-4 day trip, INV-2041"), [])

    def test_double_hyphen(self):
        self.assertIn("DOUBLE_HYPHEN", codes("we are live -- come over", "warn"))

    def test_dash_signoff(self):
        self.assertIn("DASH_SIGNOFF", codes("See you there!\n- Priya", "warn"))
        self.assertNotIn("DASH_SIGNOFF", codes("See you there!\nPriya"))

    def test_more_ai_vocabulary(self):
        for word in ("leverage", "streamline", "foster", "robust", "utilize", "synergy"):
            self.assertIn("AI_PHRASE", codes(f"We {word} this", "warn"), word)

    def test_mentions_note(self):
        r = wa_lint.lint("@Rahul please confirm", today=TODAY)
        self.assertIn("MENTIONS", r.codes("note"))

    def test_email_is_not_a_mention(self):
        self.assertNotIn("MENTIONS", codes("Mail priya@example.com"))

    def test_hashtags(self):
        self.assertIn("HASHTAGS", codes("#a #b #c #d", "warn"))

    def test_emoji_heavy(self):
        self.assertIn("EMOJI_HEAVY", codes("🎉🎉🎉🎉🎉 party 🎉", "warn"))

    def test_emoji_labels_are_fine(self):
        text = "📅 *Sat, 14 Nov*\n⏰ 7 pm onwards\n📍 Green Park Banquet, Sector 5"
        self.assertEqual(codes(text, "warn"), [])

    def test_max_emoji(self):
        self.assertIn("EMOJI_LIMIT", codes("Hi 🎉🎉🎉", "error", max_emoji=2))

    def test_count_emoji(self):
        self.assertEqual(wa_lint.count_emoji("🎉🇮🇳👍🏽❤️"), 4)

    def test_zwj_sequences_count_once(self):
        self.assertEqual(wa_lint.count_emoji("👨‍👩‍👧 💆‍♀️"), 2)


class Limits(unittest.TestCase):
    def test_status_limit(self):
        self.assertIn("TOO_LONG", codes("a" * 701, "error", kind="status"))
        self.assertEqual(codes("a" * 700, "error", kind="status"), [])

    def test_caption_soft_limit(self):
        self.assertIn("LONG_CAPTION", codes("word " * 230, "warn", kind="caption"))

    def test_unknown_kind(self):
        with self.assertRaises(ValueError):
            wa_lint.lint("x", kind="tweet")


class Fix(unittest.TestCase):
    def test_markdown_to_whatsapp(self):
        src = (
            "# Team Lunch\n\n**When:** Fri, 13 Nov\n**Where:** [Toit](https://maps.app.goo.gl/T01t)\n"
            "---\n+ bring cash\n  - nested\n*Venue *   later\n*https://example.com*\nwww.site.com\n"
        )
        out = wa_lint.fix(src)
        self.assertIn("*Team Lunch*", out)
        self.assertIn("*When:* Fri, 13 Nov", out)
        self.assertIn("*Where:* Toit: https://maps.app.goo.gl/T01t", out)
        self.assertIn("- bring cash", out)
        self.assertIn("- nested", out)
        self.assertIn("*Venue*", out)
        self.assertIn("\nhttps://example.com\n", out)
        self.assertIn("https://www.site.com", out)
        self.assertNotIn("**", out)
        self.assertNotIn("---", out)
        self.assertEqual(wa_lint.lint(out, today=TODAY).codes("error"), [])

    def test_table(self):
        out = wa_lint.fix("| Prize | Amount |\n|---|---|\n| 1st | ₹25,000 |")
        self.assertEqual(out, "*Prize · Amount*\n1st · ₹25,000")

    def test_html(self):
        out = wa_lint.fix('<b>Hi</b> <i>all</i><br><a href="https://x.com">site</a>')
        self.assertEqual(out, "*Hi* _all_\nsite: https://x.com")

    def test_link_label_equal_to_url(self):
        self.assertEqual(wa_lint.fix("[https://x.com](https://x.com)"), "https://x.com")

    def test_code_block_kept_language_dropped(self):
        out = wa_lint.fix("```python\nprint(**x**)\n```")
        self.assertEqual(out, "```print(**x**)\n```")

    def test_bold_italic(self):
        self.assertEqual(wa_lint.fix("***wow***"), "*_wow_*")

    def test_collapses_blank_lines(self):
        self.assertEqual(wa_lint.fix("a\n\n\n\nb"), "a\n\nb")

    def test_dashes_removed(self):
        self.assertEqual(wa_lint.fix("Big news — we are live!"), "Big news, we are live!")
        self.assertEqual(wa_lint.fix("Open 10 am – 6 pm, ages 2–4"), "Open 10 am to 6 pm, ages 2-4")
        self.assertEqual(wa_lint.fix("Sat, 5 Dec – Sun, 6 Dec"), "Sat, 5 Dec to Sun, 6 Dec")
        self.assertEqual(wa_lint.fix("Thanks!\n– Priya"), "Thanks!\nPriya")
        self.assertEqual(wa_lint.fix("Code: `a—b`"), "Code: `a—b`")
        self.assertEqual(wa_lint.lint(wa_lint.fix("x — y – z"), today=TODAY).codes("error"), [])

    def test_idempotent_on_clean_text(self):
        clean = "*Date:* Sat, 14 Nov\n\n- one\n- two\n\nhttps://forms.gle/x"
        self.assertEqual(wa_lint.fix(clean), clean)


class SensitiveData(unittest.TestCase):
    def kinds(self, text):
        return [k for _, _, k, _ in wa_lint.find_pii(text)]

    def test_each_kind(self):
        cases = {
            "+91 98765 43210": "phone", "98765 43210": "phone", "022 2654 1100": "phone",
            "rohan.k@gmail.com": "email", "rohan@okicici": "upi",
            "4111 1111 1111 1111": "card", "ABCPK1234L": "pan", "4918 3726 5017": "aadhaar",
            "GB82 WEST 1234 5698 7654 32": "iban", "OTP is 482913": "otp",
            "A/c no: 50100123456789": "account", "A/C: `50100123456789`": "account",
            "https://wa.me/919822012345": "phone",
        }
        for text, kind in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.kinds(text), [kind])

    def test_checksums_prevent_false_positives(self):
        self.assertEqual(self.kinds("Order 4111 1111 1111 1112"), [])  # fails Luhn
        self.assertEqual(self.kinds("Ref 4918 3726 5018"), [])  # fails Verhoeff, no Aadhaar word
        self.assertEqual(self.kinds("Aadhaar 4918 3726 5018"), ["aadhaar"])  # the word is enough

    def test_public_and_harmless_values_are_kept(self):
        for text in ("IFSC HDFC0001234", "₹1,49,999", "14/11/2026 at 10:30", "order #4567891230",
                     "@Rahul please confirm", "Room 204, 2-4 pm", "https://example.com/a1234567890"):
            with self.subTest(text=text):
                self.assertEqual(self.kinds(text), [])

    def test_consistent_labels(self):
        out, counts = wa_lint.redact("Call 98765 43210, or +91 98765 43210, or 98111 22334")
        self.assertEqual(out, "Call [phone 1], or [phone 1], or [phone 2]")
        self.assertEqual(counts, {"phone": 2})

    def test_single_value_has_no_number(self):
        self.assertEqual(wa_lint.redact("mail me at a.b@x.com")[0], "mail me at [email]")

    def test_partial_style(self):
        out, _ = wa_lint.redact("Card 4111 1111 1111 1111, UPI rohan@okicici", style="partial")
        self.assertEqual(out, "Card XXXX XXXX XXXX 1111, UPI r***@okicici")

    def test_keep(self):
        out, _ = wa_lint.redact("98765 43210 and a@b.com", keep=("email",))
        self.assertEqual(out, "[phone] and a@b.com")

    def test_otp_cvv_pin_labelled_code(self):
        self.assertEqual(wa_lint.redact("CVV 123, PIN 4455")[0], "CVV [code 1], PIN [code 2]")

    def test_wa_me_link_keeps_working_shape(self):
        self.assertEqual(wa_lint.redact("https://wa.me/919822012345")[0], "https://wa.me/[phone]")

    def test_lint_warns_on_high_risk_only(self):
        self.assertIn("SENSITIVE", codes("Your card 4111 1111 1111 1111", "warn"))
        self.assertNotIn("SENSITIVE", codes("Call Sameer +91 98200 11223"))

    def test_redaction_labels_are_not_placeholders(self):
        self.assertEqual(codes("[02/11/26, 10:15:32 AM] Person A: call [phone 1] or [link]", "warn"), [])
        self.assertIn("PLACEHOLDER", codes("Venue: [venue]", "warn"))


class CLI(unittest.TestCase):
    def run_cli(self, text, *args):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "m.txt"
            path.write_text(text, encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = wa_lint.main([str(path), "--today", "2026-11-02", *args])
            return code, out.getvalue(), err.getvalue()

    def test_clean_exit_zero(self):
        code, out, _ = self.run_cli("*Sat, 14 Nov* · 7 pm")
        self.assertEqual(code, 0)
        self.assertIn("ready to paste", out)

    def test_errors_exit_one(self):
        code, out, _ = self.run_cli("**Friday, 14 Nov**")
        self.assertEqual(code, 1)
        self.assertIn("WEEKDAY_MISMATCH", out)

    def test_strict_fails_on_warnings(self):
        self.assertEqual(self.run_cli("Venue: [venue]")[0], 0)
        self.assertEqual(self.run_cli("Venue: [venue]", "--strict")[0], 1)

    def test_json(self):
        code, out, _ = self.run_cli("**x**", "--json")
        data = json.loads(out)
        self.assertFalse(data["ok"])
        self.assertEqual(data["findings"][0]["code"], "MD_BOLD")

    def test_fix_prints_fixed_text_and_reports_on_stderr(self):
        code, out, err = self.run_cli("# Hello\n**bold**", "--fix")
        self.assertEqual(out, "*Hello*\n*bold*\n")
        self.assertIn("ready to paste", err)
        self.assertEqual(code, 0)

    def test_missing_file(self):
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(wa_lint.main(["/nonexistent/x.txt"]), 2)

    def test_redact_cli(self):
        code, out, err = self.run_cli("OTP is 482913, call 98765 43210", "--redact")
        self.assertEqual(code, 0)
        self.assertEqual(out, "OTP is [code], call [phone]\n")
        self.assertIn("masked", err)

    def test_pii_cli_json(self):
        code, out, _ = self.run_cli("rohan@okicici", "--pii", "--json")
        self.assertEqual(json.loads(out), [{"line": 1, "kind": "upi", "value": "rohan@okicici"}])

    def test_bad_keep(self):
        with redirect_stderr(io.StringIO()):
            self.assertEqual(self.run_cli("x", "--redact", "--keep", "nope")[0], 2)

    def test_about_kind(self):
        self.assertEqual(self.run_cli("a" * 140, "--kind", "about")[0], 1)
        self.assertEqual(self.run_cli("a" * 139, "--kind", "about")[0], 0)

    def test_status_kind(self):
        self.assertEqual(self.run_cli("a" * 800, "--kind", "status")[0], 1)


if __name__ == "__main__":
    unittest.main()
