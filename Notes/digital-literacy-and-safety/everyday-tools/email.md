---
title: "Email"
tags: ["digital-literacy", "email", "security", "track-a"]
updated: "2026-07-10"
---

# Email

*Email was designed in the 1970s to be trusting, and it still is. Anyone can put any name in the From field — the truth is in the headers, and almost nobody reads them.*

> Type any name you like into the From field. Type your CEO's. **The protocol will not stop
> you** — SMTP, designed in 1982 for a network where everyone knew everyone, has no concept of
> proving who you are. Every anti-spoofing mechanism that exists today (SPF, DKIM, DMARC) was
> bolted on afterwards, and they are *advisory*. The From line is a claim, not a fact. Your
> inbox displays it in bold, next to a photograph, as though it were a fact.

> **In real life**
>
> Email is **postcards, not sealed letters.** Anyone handling one along the way can read it,
> and the return address is written by the sender, in their own handwriting, unverified. We
> built a global business infrastructure on postcards and then acted surprised when people
> started writing "From: The Bank" on them. TLS put the postcards in envelopes *between post
> offices* — it did nothing about who wrote the return address.

## What an email actually is

Two parts, and only one of them is shown to you:

**The headers** — the metadata. `From`, `To`, `Subject`, `Date`, and dozens more you never
see: `Received` (a stamp from every server it passed through, added bottom-up), `Return-Path`
(where bounces go — often *not* the From address), `Authentication-Results` (whether SPF/DKIM
passed), `Message-ID`, `Reply-To`.

**The body** — usually sent twice, as `text/plain` and `text/html`, and your client picks
one. So an email can display one thing to you and something completely different to someone
reading it as plain text. Phishers exploit this constantly.

The three acronyms worth knowing, because they are the entire defence:

- **SPF** — the domain publishes which servers may send its mail. "Only these post offices may stamp my letters."
- **DKIM** — the sending server cryptographically signs the message. "This letter carries my seal."
- **DMARC** — tells receivers what to do when SPF/DKIM fail, and asks for reports. "If the seal is missing, bin it and tell me."

![An email client showing an inbox list and a message](email-inbox.png)
*Mailpile inbox — Wikimedia Commons, CC BY-SA 3.0. [Source](https://commons.wikimedia.org/wiki/File:Mailpile-inbox.png)*
- **The From line is a claim, not a fact** — SMTP has no authentication. Anyone can write any address here. Your client renders it in bold beside an avatar, which is a design decision that makes an unverified string look like an identity. This is the root of the entire phishing industry.
- **The display name hides the address** — `Sagar Thapa <attacker@evil.tld>` displays as just 'Sagar Thapa' in most clients, on most phones, by default. The part that could save you is the part that's hidden. Click or hover to expand the actual address — always, on anything asking you to act.
- **Reply-To can differ from From** — The email says it's from your finance director. You hit reply, and it goes to the attacker, because `Reply-To` is a separate header. Perfectly legitimate feature (mailing lists need it), perfectly abused. Check it before replying to anything about money.
- **The body is sent TWICE** — `text/plain` and `text/html`. Your client shows one. A link can display 'yourbank.com' as its text while its href points anywhere. Hover it and read the status bar — the visible text of a link is decoration, and always was.
- **Received headers: the real journey, bottom-up** — Each server that touches the message stamps a `Received` header ON TOP. So you read them bottom to top to trace the path. A message claiming to be from a bank whose earliest hop is a residential IP in another country has just told you the truth about itself.
- **Authentication-Results: the verdict** — `spf=pass dkim=pass dmarc=pass` — the receiving server checked and the mail is what it claims. `spf=fail` on a message from your CEO is not a formality. This one line is the closest email ever gets to saying 'this is genuinely who it says'.

**Reading the headers on a suspicious email — press Play**

1. **It looks perfect. Logo, tone, signature, urgency.** — 'Please pay this invoice today — I'm in a meeting and can't take calls.' From your CEO. The display name is right. The photo is right. Nothing on the visible surface is wrong, because everything on the visible surface is chosen by the sender.
2. **Expand the actual address** — The display name says 'Sagar Thapa'. The address, once expanded, is `sagar.thapa@company-payments.net`. Not `company.com`. A lookalike domain, registered nine days ago, which nobody would notice in a phone client that never shows it.
3. **Open the raw headers** — Gmail: 'Show original'. Outlook: 'View source'. The whole message, as it arrived, before any client dressed it up for you. This is the Network tab of email, and reading it is the same skill.
4. **Read Authentication-Results** — `spf=fail (sender IP is not permitted) dkim=none dmarc=fail`. The real company.com publishes an SPF record; this message did not come from a server it permits. The protocol caught the lie, wrote it down, and delivered the mail anyway — because DMARC policy was set to 'none'.
5. **Read Received, bottom to top** — The earliest hop is a consumer broadband IP in a country your company doesn't operate in. Every stamp above it is legitimate mail infrastructure faithfully carrying a forgery. Nothing broke. Email is behaving exactly as designed — and that is the finding.

*Try it — triage an email from its headers alone*

```python
email = {
    "From":                  "Sagar Thapa <sagar.thapa@company-payments.net>",
    "Reply-To":              "finance.urgent@mail.ru",
    "Return-Path":           "bounce@company-payments.net",
    "Subject":               "URGENT: invoice payment needed today",
    "Authentication-Results":"spf=fail dkim=none dmarc=fail",
    "Received": [  # newest first, as they appear in the raw source
        "from mx.company.com by inbox.company.com",
        "from smtp.cheap-vps.example by mx.company.com",
        "from [92.51.x.x] (dsl-static.isp.example) by smtp.cheap-vps.example",
    ],
    "link_text": "https://company.com/invoice",
    "link_href": "https://company-payments.net/pay?id=88213",
}

CORPORATE_DOMAIN = "company.com"
flags = []

addr = email["From"].split("<")[-1].rstrip(">")
domain = addr.split("@")[-1]
if domain != CORPORATE_DOMAIN:
    flags.append(f"From domain is '{domain}', not '{CORPORATE_DOMAIN}' -- lookalike")

if email["Reply-To"].split("@")[-1] != domain:
    flags.append(f"Reply-To goes to a DIFFERENT domain: {email['Reply-To']}")

for check in ("spf", "dkim", "dmarc"):
    if f"{check}=pass" not in email["Authentication-Results"]:
        flags.append(f"{check.upper()} did not pass")

if email["link_text"].split("/")[2] != email["link_href"].split("/")[2]:
    flags.append(f"Link TEXT says {email['link_text'].split('/')[2]}, href goes to {email['link_href'].split('/')[2]}")

origin = email["Received"][-1]   # bottom of the list = first hop = the real origin
if "dsl" in origin or "static.isp" in origin:
    flags.append("Earliest Received hop is a residential/consumer IP")

print(f"Subject: {email['Subject']}\\n")
print(f"{len(flags)} red flags, none of them visible in the inbox view:\\n")
for f in flags: print(f"  !! {f}")
print()
print("The message was DELIVERED. spf=fail and dmarc=fail were recorded")
print("faithfully and ignored, because company.com publishes DMARC p=none.")
print("The protocol did its job. Nobody was listening.")
```

## Why this is a tester's note, not a security note

Three reasons, and the third is the one that gets you hired:

1. **Your application sends email.** Password resets, receipts, verification links. That makes deliverability, spoofability and link-safety *your test surface*. Does your reset link expire? Is it single-use? Does it appear in the plain-text part too?
2. **Email is where phishing meets your users**, and claude-2's `phishing-and-scams` note covers the human side of that. This note covers the machine side: where the evidence lives.
3. **Reading raw headers is exactly the same skill as reading the Network tab.** A message you can see, and a truthful record underneath it that nobody looks at. Same instinct, different protocol.

> **Tip**
>
> Learn the one menu item: in Gmail it's **Show original**; in Outlook, **View source**; in
> Apple Mail, **View → Message → Raw Source**. That's it. That's the skill. Every phishing
> argument, every "did this actually send?" question, and every deliverability bug is settled
> by the raw headers, and the people who can't settle them are simply people who never found
> that menu item.

SPF, DKIM and DMARC

### Your first time: Your mission: read the truth under an email

- [ ] Open any email and show the original — Gmail: ⋮ → Show original. Outlook: View source. You'll see fifty lines of headers you have never looked at, on a message you've already read.
- [ ] Find Authentication-Results — Read the spf, dkim and dmarc verdicts. Do this on a real email from your bank, then on a marketing email. Note which ones pass.
- [ ] Read the Received chain bottom-up — The last one in the list is the FIRST hop — where the message really started. Each server stamps its line on top as the message travels.
- [ ] Compare From and Reply-To — On a mailing-list email they'll legitimately differ. On a message from a colleague asking about money, a difference is an emergency.
- [ ] Check a domain's DMARC policy — `dig TXT _dmarc.gmail.com +short`. Then try your own employer's domain. If it says `p=none`, anyone can spoof it and receivers are told to deliver it anyway.

You can now determine whether an email is genuinely from who it claims — a skill most people in your office do not have.

- **An email from my CEO asks me to buy gift cards, urgently, and not to call.**
  Textbook business email compromise. Expand the actual From address (the display name is attacker-controlled and phones hide the address by default). Check Reply-To. Open the raw headers and read Authentication-Results. Then — and this is the part that matters — verify through a channel the sender did not choose: phone the person on a number you already had. 'I can't take calls' is not an inconvenience in the story; it is the entire mechanism of the attack.
- **Our app's password reset emails go to spam.**
  A deliverability bug, and it's yours to test. Check that your sending domain publishes SPF, DKIM and DMARC and that your provider is authorised in the SPF record. Send a test to `mail-tester.com` for a scored report. Note this is a *real defect with a real user impact* — users who never receive a reset email do not file a bug, they leave, and your funnel records it as abandonment.
- **The link in the email says one thing and goes somewhere else.**
  Entirely normal HTML: link text is decoration, the `href` is the destination. Hover it and read the status bar; on mobile, long-press to preview. Your own application's emails should be tested for this too — a redirect endpoint that accepts an arbitrary `?next=` parameter turns your legitimate domain into a phisher's launchpad, and it will pass every SPF check because it genuinely is you.
- **The plain-text version of our email says something different from the HTML.**
  Every email is sent as both, and clients pick. Templating systems that build them separately drift apart — the plain-text part keeps an old URL, or an unsubscribe link, or a discount code that was meant to be removed. Nobody tests it because nobody reads it, and that is precisely why it's worth reading.

### Where to check

Everything worth knowing is in the raw source:

- **Show original / View source** — the one menu item. Learn where it is in your client.
- **`Authentication-Results`** — `spf=pass dkim=pass dmarc=pass`, or the message is not what it claims.
- **`Received`, read bottom-up** — the real path. The earliest hop is the origin.
- **`From` vs `Reply-To` vs `Return-Path`** — three different addresses, three different purposes, all forgeable except where DKIM signs them.
- **`dig TXT _dmarc.example.com +short`** — the domain's own policy. `p=none` means "deliver forgeries of me."
- **Hover any link** — the `href`, not the text.

Tester's habit: **the inbox view is a rendering, the headers are the record.** It's the same
relationship as a rendered page to its DOM, or a spreadsheet cell to its formula bar. Every
one of these notes is teaching the same reflex: *what is displayed was chosen for you; find
the thing underneath that wasn't.*

### Worked example: the invoice that nearly paid itself

1. **A finance assistant receives an email from the CFO.** Change of bank details for a supplier, invoice attached, pay today, "I'm boarding a flight — don't call, just confirm by email."
2. **Everything looks right.** Display name, signature, the company's exact email footer, the CFO's usual slightly clipped tone. The supplier is real and an invoice is genuinely due.
3. **She almost pays it.** What stops her is a rule she'd been taught by a tester, of all people: *for anything about money, expand the address.*
4. **The From address**, once expanded: `cfo@cornpany.com`. Not `company.com`. **`rn` instead of `m`.** In the default sans-serif font, at 13px, on a phone, `rn` and `m` are visually identical. The domain was registered eleven days earlier.
5. **She opens the raw headers.** `spf=fail`. `dkim=none`. `dmarc=fail`. The receiving server had detected the forgery, recorded the verdict, and delivered the message to her inbox anyway — because `company.com` publishes `p=none`, which instructs receivers to take no action.
6. **`Reply-To` points somewhere else again.** Had she "confirmed by email" as instructed, the confirmation would have gone to the attacker, who would have replied approvingly, in the CFO's voice.
7. **The `Received` chain**, read bottom-up, starts at a consumer broadband address. Every hop above it is a real, well-behaved mail server, faithfully relaying a lie. Nothing malfunctioned.
8. **What the company changed:** DMARC from `p=none` to `p=reject` (so receivers bin forgeries of their domain), and a rule that bank-detail changes are confirmed by phone, on a number from the supplier record — never a number, or an email address, supplied by the message requesting the change.
9. **The general lesson, and it is the lesson of this whole module.** The protocol *told the truth*, in a header, to nobody. The information needed to stop this was present, machine-generated, and free. It sat one menu item away, unread, because the interface above it was built to look convincing — and the person who happened to know where to look was a tester.

> **Common mistake**
>
> Believing the From line. It is a string the sender chose, rendered in bold beside an avatar
> your own client picked out of your contacts, which makes an unverified claim look like an
> established identity. Everything trustworthy about an email lives in `Authentication-Results`
> and the `Received` chain — machine-written, hard to forge, and hidden behind a menu item most
> people have never clicked. Phones make it worse: they show the display name and hide the
> address entirely, so the single field that would expose the attack is the field your device
> has decided you don't need. Expand the address. Every time money is involved, without
> exception.

**Quiz.** An email's headers show `spf=fail dkim=none dmarc=fail`, yet it arrived in the inbox rather than spam. What does that tell you?

- [ ] The headers are wrong — the mail server verified it or it wouldn't have been delivered
- [x] The receiving server detected the forgery and recorded it, but the sending domain publishes DMARC `p=none`, which instructs receivers to take no action on failures. The protocol caught the lie and was told to deliver it anyway.
- [ ] SPF and DKIM only apply to attachments
- [ ] It means the email is safe — delivery implies verification

*This is the gap that keeps business email compromise profitable. SPF and DKIM are checks; DMARC is the *policy* saying what to do when they fail — and the majority of domains publish `p=none`, meaning 'record the failure and deliver anyway.' So the message is stamped, accurately, as a forgery, and lands in the inbox looking exactly like real mail. Delivery has never implied verification. Check the policy yourself: `dig TXT _dmarc.yourcompany.com +short`. If it says `p=none`, anyone on earth can send mail as your CEO and receivers are instructed not to stop it.*

- **Why the From line can't be trusted** — SMTP (1982) has no authentication. Any sender can write any address. Your client renders the claim in bold beside an avatar, which makes it look like a fact.
- **The one menu item** — Gmail: Show original. Outlook: View source. Apple Mail: View → Message → Raw Source. Every email argument is settled here.
- **SPF / DKIM / DMARC** — SPF: which servers may send. DKIM: cryptographic signature. DMARC: what to do when those fail (`p=none` / `quarantine` / `reject`) plus reporting.
- **`p=none` means…** — 'Record forgeries of my domain and deliver them anyway.' The majority of domains publish this. Check with `dig TXT _dmarc.domain.com +short`.
- **Received headers** — Each server stamps one on TOP as the mail travels. Read bottom-up: the last line is the first hop — the real origin.
- **From vs Reply-To vs Return-Path** — Three separate headers, three purposes. A reply goes to Reply-To. A mismatch on anything about money is an emergency.
- **The body is sent twice** — `text/plain` and `text/html`. Clients pick one. They drift apart, and nobody tests the plain-text version because nobody reads it.
- **`cornpany.com`** — `rn` renders identically to `m` at small sizes. Lookalike domains beat human eyes, which is why you expand the address rather than glance at it.

### Challenge

Open a real email from your bank and one from a marketing list. Show original on both. Find
`Authentication-Results` and compare the spf/dkim/dmarc verdicts. Then run
`dig TXT _dmarc.yourbank.com +short` and `dig TXT _dmarc.youremployer.com +short`. If your
employer publishes `p=none`, you have just discovered that anyone in the world can send email
as your CEO and receiving servers are instructed to deliver it. Write that up. It is a real,
filable finding, and you found it with one DNS query.

### Ask the community

> Email question: message claims From `[address]`. Authentication-Results: `[paste the spf/dkim/dmarc line]`. Reply-To: `[address]`. Earliest Received hop: `[paste bottom Received line]`. Link text vs href: `[text]` -> `[href]`. Sending domain's DMARC policy (`dig TXT _dmarc.domain +short`): `[paste]`

Paste the raw `Authentication-Results` line rather than describing it. It is machine-written,
it cannot be argued with, and it usually ends the conversation in one reply. The DMARC policy
is the second half of the answer — it explains why a message stamped as a forgery was
delivered to you anyway.

- [MXToolbox — paste raw headers, get them parsed and explained](https://mxtoolbox.com/EmailHeaders.aspx)
- [mail-tester.com — send your app's email here, get a deliverability score](https://www.mail-tester.com/)
- [DMARC.org — what the policy actually does](https://dmarc.org/overview/)
- [FBI — business email compromise, and what it costs](https://www.ic3.gov/Media/Y2022/PSA220504)

🎬 [How email spoofing works, and how headers expose it](https://www.youtube.com/watch?v=NpaBc0kmS0I) (12 min)

- The From line is a claim the sender wrote. SMTP has no authentication; SPF, DKIM and DMARC were bolted on and remain advisory.
- Learn one menu item — Show original / View source. `Authentication-Results` gives the verdict, and `Received` read bottom-up gives the real origin.
- A domain publishing DMARC `p=none` has told the world's mail servers to deliver forgeries of it. Check with `dig TXT _dmarc.domain +short`.
- Your app sends email, so deliverability, link safety and the untested plain-text body are your test surface — and a reset email in spam is a bug users never report.
- The inbox is a rendering; the headers are the record. Same reflex as the DOM under a page and the formula bar under a cell.


---
_Source: `packages/curriculum/content/notes/digital-literacy-and-safety/everyday-tools/email.mdx`_
