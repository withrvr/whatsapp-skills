# Worked examples: whatsapp-redact

## 1. Chat excerpt for the building group (standard)

**Brief:** *hide names and numbers, I want to post this in our tower group so others know the plumber rate*

```chat
[01/11/26, 9:05:40 PM] Rakesh Sharma: Plumber Sunil's number is 98201 33445, he charged me ₹1,800 for the same leak
[01/11/26, 9:07:02 PM] Meera Iyer: Thanks! Also the builder's office email is complaints@sunrisebuilders.in
[01/11/26, 9:08:15 PM] Meera Iyer: My flat C-703 has the same seepage, call me on 98330 12345
```

**Output:**

```text
[01/11/26, 9:05:40 PM] Person A: Plumber Sunil's number is [phone 1], he charged me ₹1,800 for the same leak
[01/11/26, 9:07:02 PM] Person B: Thanks! Also the builder's office email is complaints@sunrisebuilders.in
[01/11/26, 9:08:15 PM] Person B: My flat [flat no.] has the same seepage, call me on [phone 2]
```

Notes:
- Key (keep private): Person A = Rakesh Sharma, Person B = Meera Iyer, [phone 1] = the plumber, [phone 2] = Meera.
- Left the builder's complaints email visible: it's a public business address and useful to the group. If the point is the plumber's rate, you may want to keep his number visible too.

## 2. Scam warning: keep the scammer, hide the victim

**Brief:** *got this, want to warn the parents group. keep scammer details, remove mine*

> *From +44 7700 900123: "Hi Mom, this is my new number, phone fell in water. Send ₹18,000 to rentpay.fast@ybl urgently, I'll return tomorrow"*
> *Me: who is this? I'm Kavita, Aarav's mother, my number is 98111 22334*

```text
⚠️ Scam alert, please don't fall for this

I got this on WhatsApp today from +44 7700 900123:

"Hi Mom, this is my new number, phone fell in water. Send ₹18,000 to rentpay.fast@ybl urgently, I'll return tomorrow"

It's the "new number" scam. If you get it, call your child on their old number before doing anything. Block and report the number in WhatsApp.
```

Notes:
- Kept the scammer's number and UPI ID on purpose so others can recognise them. Removed your reply (your name, child's name, number).

## 3. Before pasting into an AI (light, numbers only)

**Brief:** *remove sensitive stuff, I'll ask chatgpt to write my brother a reply*

```chat
Hi bhai, card is 4111 1111 1111 1111, expiry 09/29, CVV 123. OTP aaya hai 482913. Aadhaar 4918 3726 5017 bhi chahiye toh bata
```

**Output:**

```text
Hi bhai, card is [card], expiry 09/29, CVV [code 1]. OTP aaya hai [code 2]. Aadhaar [Aadhaar] bhi chahiye toh bata
```

Notes:
- Never send a CVV or OTP to anyone, family included; banks never need them over chat. If this was a request from someone, it may be a scam.

## 4. Proof of payment, partial masking

**Brief:** *share this with my flatmates as proof I paid, hide account but keep last 4*

```chat
Paid ₹4,500 rent from A/c no 50100123456789 to UPI landlord.k@okhdfcbank, ref 432198765012
```

**Output:**

```text
Paid ₹4,500 rent from A/c no XXXXXXXXXX6789 to UPI l***@okhdfcbank, ref 432198765012
```

Notes:
- Kept the payment reference so the transaction can be matched if anyone checks.

## 5. Full anonymisation for a public post

**Brief:** *full anonymise, posting on a consumer forum about the hospital bill*

```chat
Dr. Mehta at Apollo Hospital Baner told my father Ramesh on 3 Nov that the stent costs ₹1,20,000, but the bill on 6 Nov said ₹1,85,000. Call me on 98765 43210.
```

**Output:**

```text
The doctor at [company] told my father on Day 1 that the stent costs ₹1,20,000, but the bill on Day 4 said ₹1,85,000.
```

Notes:
- Key (keep private): [company] = Apollo Hospital Baner, Day 1 = 3 Nov, Day 4 = 6 Nov.
- On a consumer forum you may want to name the hospital (it's a business, not a person). Removed your number.
