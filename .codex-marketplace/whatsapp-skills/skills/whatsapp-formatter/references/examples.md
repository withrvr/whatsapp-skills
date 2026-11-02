# Worked examples: whatsapp-formatter

## 1. Convert: AI-written Markdown notice

**Input:**

```markdown
# 📢 Hackathon Registration Open

**Dates:** Saturday, 5 December – Sunday, 6 December
**Venue:** Main Auditorium, Block C

## How to register
1. Form a team of 2–4
2. Register at [this link](https://forms.gle/Hack26)
3. Pay ₹200 per team

| Prize | Amount |
|---|---|
| 1st | ₹25,000 |
| 2nd | ₹15,000 |

---
*Questions?* Contact @Aditi
```

**Output:**

```text
*📢 Hackathon Registration Open*

*Dates:* Saturday, 5 December to Sunday, 6 December
*Venue:* Main Auditorium, Block C

*How to register*
1. Form a team of 2-4
2. Register at this link: https://forms.gle/Hack26
3. Pay ₹200 per team

*Prize · Amount*
1st · ₹25,000
2nd · ₹15,000

_Questions?_ Contact @Aditi
```

Notes:
- Converted headings, bold, the link and the prize table. The single-asterisk *Questions?* was Markdown italic, now `_Questions?_`.
- Retype @Aditi in WhatsApp to tag her.

## 2. Polish: typos, keep the voice

**Input:** *hey all, reminder that tommorow's practise is shifted to 7am insted of 6, ground no 2. pls dont be late, coach is comming 😅*

**Output:**

```text
Hey all, reminder that tomorrow's practice is shifted to 7 am instead of 6, Ground No. 2. Pls don't be late, coach is coming 😅
```

Notes:
- Fixed 5 typos (tomorrow, practice, instead, don't, coming). Kept "pls" and the emoji.

## 3. Check: report only

**Input:** *Status: Big sale this Friday, 20 Nov! **Flat 30% off** on all shoes. Visit www.shoebox.in*

**Output:**

Problems:
1. `**Flat 30% off**` shows the asterisks on WhatsApp → use `*Flat 30% off*`.
2. `www.shoebox.in` has no https:// → `https://www.shoebox.in`.

Fri, 20 Nov is correct, and the length is fine for a status.

## 4. Convert: an AI answer with nested bullets, for a group

**Input:**

```markdown
**Trek checklist for Sunday:**

* **Clothes**
    * 2 pairs of socks
    * Rain jacket
* **Food**
    * 1 litre water
    * Dry fruits
* Meet at *Swargate bus stand*, 5:30 AM sharp
```

**Output:**

```text
*Trek checklist for Sunday:*

*Clothes*
- 2 pairs of socks
- Rain jacket

*Food*
- 1 litre water
- Dry fruits

Meet at _Swargate bus stand_, 5:30 AM sharp
```

Notes:
- WhatsApp can't show nested lists, so each group got a bold label with a flat list under it. The single-asterisk italic became `_italic_`.

## 5. Convert: email to WhatsApp, words kept

**Input:**

```markdown
Subject: Payment reminder – Invoice #INV-2041

Dear Mr. Khanna,

This is a reminder that invoice #INV-2041 for ₹48,000 was due on 30 October.
Please find the payment details below:
Bank: HDFC Bank
A/C: 50100123456789
IFSC: HDFC0001234

Thanks & Regards,
Sanjay Verma
Accounts, BrightPrint Pvt Ltd
```

**Output:**

```text
*Payment reminder: Invoice #INV-2041*

Dear Mr. Khanna,

This is a reminder that invoice #INV-2041 for ₹48,000 was due on 30 October.

Please find the payment details below:
Bank: HDFC Bank
A/C: `50100123456789`
IFSC: `HDFC0001234`

Thanks & Regards,
Sanjay Verma
Accounts, BrightPrint Pvt Ltd
```

Notes:
- Kept your wording (convert mode). Account number and IFSC are in monospace so they're easy to copy. Say "polish" for a shorter WhatsApp-style version.
