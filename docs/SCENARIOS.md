# Scenario catalog

The everyday situations these skills are built for, grouped by who's sending.
Each row names the skill that handles it and the dials it starts from. You never
have to name the skill: describe the situation and the right one activates.

Dials: **L** length (1-liner / short / medium / long) · **T** tone · **F** formatting (plain / light / full) · **E** emoji (none / few / rich).

Missing a scenario you use? [Open a scenario request](../.github/ISSUE_TEMPLATE/scenario_request.md).

## Office and work

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 1 | Running late to work or a meeting | `whatsapp-message` | short · friendly-professional · plain · none |
| 2 | Sick leave / personal leave request | `whatsapp-message` | short · friendly-professional · plain · none |
| 3 | Work-from-home request | `whatsapp-message` | short · friendly-professional · plain · none |
| 4 | Task done / status update to the manager | `whatsapp-message` | short · friendly-professional · light · none |
| 5 | Escalating a blocker | `whatsapp-message` | short · friendly-professional · plain · none |
| 6 | Asking for a meeting about a raise or review | `whatsapp-message` | short · friendly-professional · plain · none |
| 7 | Handover to a colleague before leave | `whatsapp-message` | medium · friendly-professional · light · none |
| 8 | Saying no to extra work, offering an alternative | `whatsapp-reply` | short · friendly-professional · plain · none |
| 9 | Pushing back on a deadline with options | `whatsapp-reply` | short · friendly-professional · light · none |
| 10 | Replying to a late-night work message (boundary) | `whatsapp-reply` | one-liner · friendly-professional · plain · none |
| 11 | Team meeting notice | `whatsapp-announcement` | medium · friendly-professional · light · few |
| 12 | Meeting moved / cancelled | `whatsapp-announcement` | short · friendly-professional · light · few |
| 13 | Office closed for a holiday | `whatsapp-announcement` | short · warm · light · few |
| 14 | Holiday list for the year | `whatsapp-announcement` | long · friendly-professional · full · few |
| 15 | New policy or process change | `whatsapp-announcement` | medium · friendly-professional · light · few |
| 16 | Welcoming a new joiner | `whatsapp-announcement` | short · warm · light · few |
| 17 | Farewell for a colleague | `whatsapp-invitation` | medium · warm · full · few |
| 18 | Office party / team outing invite | `whatsapp-invitation` | medium · celebratory · full · few |
| 19 | Server or tool outage alert | `whatsapp-announcement` | short · urgent · light · none |
| 20 | Weekly team update / digest | `whatsapp-announcement` | long · friendly-professional · full · few |
| 21 | Collecting money for a colleague's gift | `whatsapp-announcement` | short · warm · light · few |
| 22 | Converting an email update into a group message | `whatsapp-formatter` | keeps source |

## HR, recruiting and job search

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 23 | First message to a recruiter or hiring manager | `whatsapp-message` | short · friendly-professional · plain · none |
| 24 | Following up after an interview | `whatsapp-message` | short · friendly-professional · plain · none |
| 25 | Replying to a recruiter's outreach (interested / not) | `whatsapp-reply` | short · friendly-professional · plain · none |
| 26 | Sharing availability and expected CTC | `whatsapp-reply` | short · friendly-professional · plain · none |
| 27 | Accepting an offer | `whatsapp-message` | short · warm · plain · none |
| 28 | Declining an offer, door open | `whatsapp-message` | short · friendly-professional · plain · none |
| 29 | Negotiating salary or joining date | `whatsapp-message` | short · friendly-professional · plain · none |
| 30 | HR: interview schedule to a candidate | `whatsapp-message` | medium · friendly-professional · light · none |
| 31 | HR: offer-letter-sent / document checklist | `whatsapp-message` | medium · friendly-professional · light · none |
| 32 | HR: onboarding day-1 details | `whatsapp-announcement` | medium · warm · full · few |
| 33 | Heads-up to the manager before resigning | `whatsapp-message` | one-liner · friendly-professional · plain · none |

## Clients, vendors and freelancers

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 34 | Following up on a proposal | `whatsapp-message` | short · friendly-professional · plain · none |
| 35 | Payment reminder for an invoice | `whatsapp-message` | short · friendly-professional · light · none |
| 36 | Sharing a deliverable with a link | `whatsapp-message` | short · friendly-professional · plain · none |
| 37 | Client asks for a discount | `whatsapp-reply` | short · friendly-professional · plain · none |
| 38 | Client wants it earlier | `whatsapp-reply` | short · friendly-professional · plain · none |
| 39 | Angry customer complaint | `whatsapp-reply` | short · apologetic · plain · none |
| 40 | Quoting a price to an enquiry | `whatsapp-reply` | short · warm · light · few |
| 41 | Rescheduling an appointment | `whatsapp-message` | short · friendly-professional · plain · none |

## Small business and promotions

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 42 | Sale / discount broadcast | `whatsapp-promotion` | short · upbeat · light · few |
| 43 | Festive offer (Diwali, Eid, Christmas, New Year) | `whatsapp-promotion` | short · warm · light · few |
| 44 | New arrivals / new collection | `whatsapp-promotion` | short · warm · light · few |
| 45 | Back in stock | `whatsapp-promotion` | one-liner · warm · plain · few |
| 46 | Product or service launch | `whatsapp-promotion` | medium · upbeat · light · few |
| 47 | Course, webinar or workshop promo | `whatsapp-promotion` | medium · persuasive · light · few |
| 48 | Coaching / tuition batch admissions | `whatsapp-promotion` | medium · friendly-professional · light · few |
| 49 | Appointment / service-due reminder | `whatsapp-promotion` | short · warm · plain · few |
| 50 | Enquiry follow-up | `whatsapp-promotion` | short · warm · plain · none |
| 51 | Asking for a Google review | `whatsapp-promotion` | short · warm · plain · none |
| 52 | Referral request | `whatsapp-promotion` | short · warm · plain · few |
| 53 | Price list / catalog share | `whatsapp-promotion` | medium · warm · light · few |
| 54 | Property or rental listing | `whatsapp-promotion` | short · friendly-professional · light · few |
| 55 | Paid event tickets | `whatsapp-promotion` | medium · upbeat · light · few |
| 56 | Creator affiliate / sponsored post | `whatsapp-promotion` | short · creator voice · light · few |
| 57 | "Open on Sunday" / shop timings | `whatsapp-status` | one-liner · warm · plain · few |
| 58 | Offer as a status | `whatsapp-status` | one-liner · upbeat · plain · few |
| 59 | Order confirmed / out for delivery note | `whatsapp-message` | short · warm · plain · few |

## School, college and coaching

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 60 | PTM notice to the parents group | `whatsapp-announcement` | medium · friendly-professional · full · few |
| 61 | Test / exam schedule | `whatsapp-announcement` | medium · friendly-professional · full · few |
| 62 | Exam or class moved | `whatsapp-announcement` | short · friendly-professional · light · few |
| 63 | Homework / assignment deadline | `whatsapp-announcement` | short · friendly-professional · light · few |
| 64 | Sharing notes, PDFs, recordings, links | `whatsapp-announcement` | medium · friendly-professional · full · few |
| 65 | Fee due reminder | `whatsapp-announcement` | short · friendly-professional · light · none |
| 66 | School closed (rain, elections, holiday) | `whatsapp-announcement` | short · urgent · light · none |
| 67 | Results / selections list | `whatsapp-announcement` | medium · warm · full · few |
| 68 | Sports day / annual day invite to parents | `whatsapp-invitation` | medium · warm · full · few |
| 69 | Class rep notice to the batch | `whatsapp-announcement` | short · casual · light · few |
| 70 | Parent to teacher: absence note | `whatsapp-message` | short · respectful · plain · none |
| 71 | Student to professor: extension request | `whatsapp-message` | short · respectful · plain · none |
| 72 | Coaching channel: daily practice question | `whatsapp-channel` | short · friendly-professional · light · few |
| 73 | College fest announcement / registration | `whatsapp-announcement` | medium · celebratory · full · rich |

## Society, community and groups

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 74 | Water / power cut alert | `whatsapp-announcement` | short · urgent · light · none |
| 75 | Lift or maintenance work notice | `whatsapp-announcement` | short · friendly-professional · light · few |
| 76 | Society meeting / AGM notice | `whatsapp-announcement` | medium · friendly-professional · full · few |
| 77 | Maintenance dues reminder | `whatsapp-announcement` | short · friendly-professional · light · none |
| 78 | Fundraiser / contribution drive | `whatsapp-announcement` | medium · respectful · full · few |
| 79 | Volunteer call / sign-up | `whatsapp-announcement` | short · warm · light · few |
| 80 | Festival celebration in the society | `whatsapp-invitation` | medium · celebratory · full · rich |
| 81 | Lost and found | `whatsapp-announcement` | short · friendly-professional · light · few |
| 82 | Security alert (verified) | `whatsapp-announcement` | short · urgent · light · none |
| 83 | New group welcome + rules | `whatsapp-announcement` | medium · warm · full · few |
| 84 | Reminding members of group rules | `whatsapp-announcement` | short · friendly-professional · light · few |
| 85 | Complaint to the society office | `whatsapp-message` | short · firm · plain · none |
| 86 | Community meetup / club event | `whatsapp-invitation` | medium · warm · full · few |
| 87 | Community channel weekly roundup | `whatsapp-channel` | long · community voice · full · few |

## Family, friends and celebrations

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 88 | Wedding invite with every function | `whatsapp-invitation` | long · warm · full · few |
| 89 | Save the date | `whatsapp-invitation` | short · warm · full · few |
| 90 | E-card / video invite caption | `whatsapp-invitation` | short · warm · full · few |
| 91 | Personal invite to elders | `whatsapp-invitation` | short · respectful · plain · few |
| 92 | Function reminder (sangeet tonight) | `whatsapp-invitation` | short · warm · light · few |
| 93 | Thank-you after the wedding | `whatsapp-invitation` | short · warm · plain · few |
| 94 | Kid's birthday party invite | `whatsapp-invitation` | medium · celebratory · full · rich |
| 95 | Housewarming / griha pravesh | `whatsapp-invitation` | medium · warm · full · few |
| 96 | Pooja / religious ceremony invite | `whatsapp-invitation` | medium · respectful · full · few |
| 97 | Baby shower, naming ceremony | `whatsapp-invitation` | medium · warm · full · few |
| 98 | Anniversary party | `whatsapp-invitation` | medium · celebratory · full · few |
| 99 | School / college reunion | `whatsapp-invitation` | medium · celebratory · full · few |
| 100 | Birthday wish | `whatsapp-message` | short · warm · plain · few |
| 101 | Congratulations (job, wedding, baby, results) | `whatsapp-message` | short · warm · plain · few |
| 102 | Condolence | `whatsapp-message` | short · respectful · plain · none |
| 103 | Apology | `whatsapp-message` | short · apologetic · plain · none |
| 104 | Asking a friend to pay back | `whatsapp-message` | short · casual · plain · few |
| 105 | Splitting a bill in the trip group | `whatsapp-announcement` | short · casual · light · few |
| 106 | Planning a trip / outing in a group | `whatsapp-announcement` | medium · casual · light · few |
| 107 | Declining an invitation | `whatsapp-reply` | short · warm · plain · few |
| 108 | Thanking everyone for birthday wishes | `whatsapp-reply` | short · warm · plain · few |
| 109 | Replying in the family group respectfully | `whatsapp-reply` | short · respectful · plain · few |

## Status and channels

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 110 | Milestone status (new job, graduation) | `whatsapp-status` | one-liner · personal · plain · few |
| 111 | Festival wish status | `whatsapp-status` | one-liner · warm · plain · few |
| 112 | Memorial / tribute status | `whatsapp-status` | one-liner · respectful · plain · none |
| 113 | Out of office / travelling status | `whatsapp-status` | one-liner · casual · plain · none |
| 114 | Photo or video status caption | `whatsapp-status` | one-liner · personal · plain · few |
| 115 | Status slides for an event or offer | `whatsapp-status` | short ×3 · upbeat · plain · few |
| 116 | Channel welcome post | `whatsapp-channel` | short · creator voice · light · few |
| 117 | Daily / weekly series post | `whatsapp-channel` | short · creator voice · light · few |
| 118 | Planning a channel series | `whatsapp-channel` | plan + post 1 |
| 119 | News or update post | `whatsapp-channel` | short · neutral · light · few |
| 120 | Channel poll post | `whatsapp-channel` | short · creator voice · light · few |

## New people and strangers

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 121 | First message after getting a referral | `whatsapp-message` | short · friendly-professional · plain · none |
| 122 | Following up with someone met at an event | `whatsapp-message` | short · warm · plain · few |
| 123 | Messaging a seller, broker or PG owner | `whatsapp-message` | short · friendly-professional · plain · none |
| 124 | Messaging a service provider found online | `whatsapp-message` | short · friendly-professional · plain · none |
| 125 | Wrong-number reply | `whatsapp-reply` | one-liner · neutral · plain · none |
| 126 | Suspicious "bank/KYC/OTP" or "Hi Mom, new number" message | `whatsapp-reply` | explains the scam, no engaging reply |

## Fixing text you already have

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 127 | ChatGPT/Claude answer full of `**` and `#` | `whatsapp-formatter` | convert |
| 128 | Email or letter to send on WhatsApp | `whatsapp-formatter` | convert (or polish) |
| 129 | Typos and grammar, keep my voice | `whatsapp-formatter` | polish |
| 130 | "Is this okay to send?" | `whatsapp-formatter` | check |
| 131 | Status too long | `whatsapp-formatter` | check, then polish |

## Business messages to customers

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 132 | Order confirmed | `whatsapp-promotion` | short · warm · light · few |
| 133 | Order shipped / out for delivery | `whatsapp-promotion` | short · warm · light · few |
| 134 | Delivered, anything wrong? | `whatsapp-promotion` | one-liner · warm · plain · few |
| 135 | Payment received / receipt | `whatsapp-promotion` | one-liner · warm · plain · few |
| 136 | Payment due reminder to a customer | `whatsapp-promotion` | short · friendly-professional · plain · none |
| 137 | Cart or pending-order reminder (opted-in, once) | `whatsapp-promotion` | short · warm · plain · few |
| 138 | Welcome to my broadcast list | `whatsapp-promotion` | short · warm · light · few |

## More group posts

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 139 | Job opening in an alumni or community group | `whatsapp-announcement` | medium · friendly-professional · light · few |
| 140 | Urgent blood donation request (dated) | `whatsapp-announcement` | short · urgent · light · none |
| 141 | Missing person or pet alert | `whatsapp-announcement` | short · urgent · light · none |
| 142 | Meeting minutes from my notes | `whatsapp-announcement` | medium · friendly-professional · full · few |
| 143 | Daily stand-up update in the team group | `whatsapp-announcement` | short · friendly-professional · light · few |
| 144 | Selling something in the society group | `whatsapp-announcement` | short · casual · light · few |
| 145 | Looking for a flatmate / flat to rent | `whatsapp-announcement` | short · casual · light · few |
| 146 | Carpool or ride share | `whatsapp-announcement` | short · casual · light · few |
| 147 | Thank-you and photos after an event | `whatsapp-announcement` | short · warm · light · few |
| 148 | Voice-note script for an elder or a long explanation | `whatsapp-message` | short · warm · plain · none |

## Profile, business and group setup

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 149 | WhatsApp Business description | `whatsapp-setup` | medium · warm · plain · few |
| 150 | Greeting message for new customers | `whatsapp-setup` | short · warm · plain · few |
| 151 | Away message outside business hours | `whatsapp-setup` | short · warm · plain · none |
| 152 | Quick replies (/price, /loc, /pay, /hours) | `whatsapp-setup` | short · warm · plain · few |
| 153 | Catalog item names and descriptions | `whatsapp-setup` | short · warm · plain · none |
| 154 | Labels for sorting chats | `whatsapp-setup` | one-liner each |
| 155 | Personal About line | `whatsapp-setup` | one-liner · personal · plain · few |
| 156 | Group name, description and rules | `whatsapp-setup` | medium · friendly-professional · plain · none |
| 157 | Community name and description | `whatsapp-setup` | short · friendly-professional · plain · none |
| 158 | Channel name and description | `whatsapp-setup` | one-liner · creator voice · plain · few |

## Privacy and redaction

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 159 | Hide names and numbers before posting a chat in a group | `whatsapp-redact` | standard |
| 160 | Scam warning that keeps the scammer's number, hides mine | `whatsapp-redact` | standard |
| 161 | Remove personal info before pasting into an AI | `whatsapp-redact` | light |
| 162 | Proof of payment with the account partly masked | `whatsapp-redact` | light · partial |
| 163 | Anonymise a story for a public review or forum | `whatsapp-redact` | full |
| 164 | What to cover in a screenshot before sharing it | `whatsapp-redact` | checklist |

## Catching up on chats

| # | Scenario | Skill | Starts as |
|---|---|---|---|
| 165 | "What did I miss?" in a busy group | `whatsapp-catchup` | summary |
| 166 | "Is anything asked of me?" | `whatsapp-catchup` | summary, mentions only |
| 167 | Only messages since a date | `whatsapp-catchup` | summary |
| 168 | Minutes of a discussion to post back | `whatsapp-catchup` | full · friendly-professional |
| 169 | Recap of trip or event planning | `whatsapp-catchup` | short · casual · light |
| 170 | Decisions from a long family or society thread | `whatsapp-catchup` | summary |

