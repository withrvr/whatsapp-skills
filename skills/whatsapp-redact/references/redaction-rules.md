# Redaction rules

## What counts as sensitive

| Kind | Looks like | `light` | `standard` | `full` | Script finds it |
|---|---|---|---|---|---|
| OTP, PIN, CVV, password | "OTP is 482913" | mask | mask | mask | yes (needs the word OTP/PIN/code/password nearby) |
| Card number | 4111 1111 1111 1111 | mask | mask | mask | yes (Luhn-checked) |
| Bank account | "A/c no 50100123456789" | mask | mask | mask | yes (needs "A/c", "account", "acct") |
| Aadhaar | 4918 3726 5017 | mask | mask | mask | yes (Verhoeff-checked, or the word Aadhaar nearby) |
| PAN | ABCPK1234L | mask | mask | mask | yes |
| IBAN | GB82 WEST 1234 5698 7654 32 | mask | mask | mask | yes (mod-97 checked) |
| UPI ID | rohan@okicici | mask | mask | mask | yes |
| Email | priya.k@gmail.com | mask | mask | mask | yes |
| Phone | +91 98765 43210, 022 2654 1100, wa.me/91… | mask | mask | mask | yes |
| Passport, voter ID, driving licence, employee ID | varies | mask | mask | mask | no: read for them |
| Private person's name | "Rahul", "Bittu", "Sharma aunty" | keep | Person A | Person A | no |
| Exact address | "Flat C-703, Sunrise Towers, Baner" | keep | "Baner, Pune" | "a housing society" | no |
| Flat, house, vehicle number | C-703, MH12 AB 1234 | keep | mask | mask | no |
| Child's school and class | "Class 5B at DPS" | keep | "a school" | "a school" | no |
| Health, religion, caste, finances of a named person | "Rahul's chemo" | keep | remove the link to the person | remove | no |
| Company, place names | "Infosys", "Apollo Hospital" | keep | keep | [company], "a hospital" | no |
| Dates | "Sat, 14 Nov" | keep | keep | Day 1, Day 2 | no |
| Public figures, businesses being reviewed | "Zomato", "the builder Lodha" | keep | keep | keep unless asked | no |

IFSC codes, store phone numbers printed on a public website and government
helplines (1930, 112) are public; keep them unless the user says otherwise.

## Stand-in styles

- **Labels** (default): `[phone 1]`, `[email]`, `[UPI ID]`, `[card]`, `Person A`, `Person B`.
  The same value always gets the same label; a second distinct value gets the next number.
- **Partial** (user says "keep last 4", "partially"): `XXXXX X3210`, `r***@okicici`,
  `XXXX XXXX XXXX 1111`. Good for proof of payment where the other side needs to recognise their account.
- **Removal**: drop the whole line when it adds nothing for the audience (your
  own reply with your details in a scam warning).
- People: `Person A, Person B, …` in order of first appearance. The user is `Me`.
  Keep roles when they matter and don't identify ("the secretary", "the delivery agent").

## Chat exports

Export lines look like:

```
[02/11/26, 10:15:32 AM] Rahul Sharma: see you at 5
02/11/2026, 10:15 - +91 98765 43210: ok
```

- Replace the **sender** too, consistently with the body: `Rahul Sharma` → `Person A` everywhere.
- A sender saved only as a number is a phone number: mask it.
- `<Media omitted>`, `image omitted`, `This message was deleted` stay as they are.
- Keep timestamps unless the level is `full`.
- Group names can identify a building or a family; mask them at `standard` if they contain one.

## Edge cases

- **The user's own scam warning**: keep the scammer's number, UPI ID and link (label them as the scammer's), mask the victim.
- **Evidence** for police, a bank, a lawyer or HR: don't redact. Suggest keeping the original export file unedited and sharing it as is.
- **Someone else's redacted text**: never try to fill in or guess the hidden parts.
- **Numbers that look like phones but aren't** (order IDs, tracking numbers): if unsure, mask and mention it in Notes; the user can unmask.
- **A name that's also a word** ("Rose", "Joy"): mask only where it's the person.
- **Forwarded text with a link**: keep the link only if the purpose needs it (a scam warning does); otherwise replace it with `[link]` so nobody taps it by habit.
