"""
Builds the TextProof writing pages from _head.part, _foot.part and the bodies below.

Kept as a script rather than hand-maintained files so the nav, the footer, the stylesheet
links and the SEO head (canonical, Open Graph, Twitter, JSON-LD) cannot drift apart
between posts. Run it from this folder:

    python build.py

It also writes index.html, the list of posts.
"""

import io
import json

HEAD = io.open("_head.part", encoding="utf-8").read()
FOOT = io.open("_foot.part", encoding="utf-8").read()

SITE = "https://textproof.net"
DATE = "2026-09-01"
DATE_TEXT = "1 September 2026"
AUTHOR = "Anthony Jackson"
PUBLISHER = {"@type": "Organization", "name": "AJ Software Development", "url": "https://ajsoftwaredev.org/"}

POSTS = []  # (fname, desc, h1, date, date_text); the index lists them newest first


def meta(title: str, desc: str, url: str, og_type: str, ld: dict) -> str:
    return (
        f"<title>{title}</title>\n"
        f'<meta name="description" content="{desc}">\n'
        '<link rel="stylesheet" href="post.css">\n'
        '<link rel="stylesheet" href="../design.css">\n'
        f'<link rel="canonical" href="{url}">\n'
        '<meta name="robots" content="index,follow">\n'
        f'<meta property="og:type" content="{og_type}">\n'
        '<meta property="og:site_name" content="TextProof">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        '<meta name="twitter:card" content="summary">\n'
        f'<meta name="twitter:title" content="{title}">\n'
        f'<meta name="twitter:description" content="{desc}">\n'
        f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    )


def write(fname: str, head_meta: str, body: str) -> None:
    io.open(fname, "w", encoding="utf-8", newline="").write(
        HEAD.replace("{{META}}", head_meta) + body + FOOT
    )
    print("wrote", fname)


def page(fname: str, title: str, desc: str, body: str, date: str = DATE, date_text: str = DATE_TEXT) -> None:
    url = f"{SITE}/blog/{fname}"
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "name": title,
        "description": desc,
        "url": url,
        "inLanguage": "en-GB",
        "publisher": PUBLISHER,
        "headline": title,
        "author": {"@type": "Person", "name": AUTHOR},
        "datePublished": date,
    }
    write(fname, meta(title, desc, url, "article", ld), body)
    POSTS.append((fname, desc, body.split("<h1>", 1)[1].split("</h1>", 1)[0], date, date_text))


END = (
    '<div class="end"><p>TextProof turns a screen recording of a conversation into a '
    "timestamped, print-ready document — entirely on your iPhone. "
    '<a href="/">See how it works →</a></p></div>'
)

# ---------------------------------------------------------------- post one
page(
    "nothing-leaves-your-phone.html",
    "Private iPhone Message Extraction, On-Device | TextProof",
    "Why TextProof reads iPhone conversation recordings on-device instead of uploading your "
    "messages for cloud text recognition.",
    """
<article>
  <div class="tag">Privacy</div>
  <h1>Why there is no cloud, and never will be</h1>
  <div class="byline">1 September 2026 · Anthony Jackson</div>

  <p class="standfirst">People reach for this app during the worst month of their year. Whatever
  else we get wrong, we are not going to be one more organisation holding a copy of it.</p>

  <p>The conversations that end up in TextProof are not small talk. They are the row with the
  landlord about the deposit. The messages from the ex. The thing the builder promised and then
  denied promising. The chain that proves you did tell them, on the ninth, in writing.</p>

  <p>People do not export a conversation because they are curious. They do it because something
  has gone wrong and they need to show somebody what was actually said.</p>

  <h2>The obvious way to build this</h2>

  <p>The straightforward version of this app uploads your recording to a server, does the reading
  there, and sends back a document. It would be easier to build. The processing would be faster.
  We could fix problems without shipping an update, see exactly what went wrong when somebody
  complains, and add web access, sync between devices, and a dashboard.</p>

  <p>And it would mean a machine somewhere in a data centre holding the worst month of a
  stranger's year.</p>

  <div class="pull">
    <p><b>The question that settled it</b></p>
    <p>Not "would we look after it properly?" — we would try. The question is what happens on the
    day we are careless, or acquired, or subpoenaed, or simply wrong about a permission setting.
    A promise is only as good as the worst day it has to survive.</p>
  </div>

  <h2>So there is no server</h2>

  <p>Not a small one. Not an encrypted one. Not one that "only holds it briefly".
  <strong>There is no network code in the app at all.</strong></p>

  <p>Your recording is read on your own phone, by the text recognition Apple already builds into
  iOS. The transcript is written to your phone. The PDF is made on your phone. Nothing is
  transmitted, because there is nothing to transmit it to.</p>

  <p>That is a stronger promise than a privacy policy, and a different kind of promise. A policy
  says we choose not to look. This says we <em>cannot</em>. If somebody demanded every message
  TextProof has ever processed, the honest answer would be that we do not have one, and never
  did.</p>

  <h2>What it costs us</h2>

  <p>We would rather be straight about this than pretend the decision was free.</p>

  <ul>
    <li><strong>No sync.</strong> Your exports live on the phone that made them. Move phones and
    they do not follow.</li>
    <li><strong>No web version.</strong> There is nowhere for one to run.</li>
    <li><strong>Slower on older phones.</strong> A server rack would be quicker than an iPhone.</li>
    <li><strong>Debugging in the dark.</strong> When somebody reports a bad export we cannot look
    at it.</li>
  </ul>

  <p>That last one has genuinely slowed development down. Almost every fault worth fixing in this
  app was found by replaying what it read off somebody's screen — and every time, we had to ask
  permission first, explain exactly what was in the file, and wait.</p>

  <p>We think that is the right trade. The alternative is convenience for us, paid for with a copy
  of your conversation sitting on a machine you have never seen.</p>

  <h2>How to check we are telling the truth</h2>

  <p>Put your phone in aeroplane mode and use the app. All of it works: importing, reading,
  editing, exporting, sharing. Nothing degrades, nothing waits, nothing complains about a
  connection.</p>

  <p>An app that needs the internet cannot hide it. This one does not need it.</p>
"""
    + END
    + "</article>",
)

# ---------------------------------------------------------------- post two
page(
    "admitting-what-it-missed.html",
    "Review OCR Gaps in Your Message Export | TextProof",
    "Why a conversation transcript should flag possible gaps and uncertain readings. Learn how "
    "to check an iPhone message export against the original recording.",
    """
<article>
  <div class="tag">Design</div>
  <h1>The document that admits what it missed</h1>
  <div class="byline">1 September 2026 · Anthony Jackson</div>

  <p class="standfirst">A record with a quiet hole in it is worse than no record at all, because
  nobody reading it knows the hole is there.</p>

  <p>When you film a conversation and scroll too quickly, the app sometimes cannot be certain it
  saw everything between one screen and the next. The screens do not quite overlap. Something may
  have gone past in between.</p>

  <p>There are two things a piece of software can do at that moment, and the choice says
  everything about what it is for.</p>

  <h2>What most software does</h2>

  <p>It closes the gap. Joins what it has, produces a document that reads perfectly, and says
  nothing. The output is tidy. The customer is happy. Nobody ever finds out.</p>

  <p>And if a message did go past in that gap, the document is now <strong>a lie with a timestamp
  on it</strong>. Somebody might rely on it in a dispute, in front of a solicitor, in front of a
  tribunal. It looks complete. It reads complete. It is not complete, and there is nothing in it
  that would ever tell you.</p>

  <h2>What ours does</h2>

  <p>It stops and says so, at the exact spot, in the middle of the transcript:</p>

  <blockquote>Possible gap in the recording. Content may have scrolled past here without being
  captured. If this section matters, re-record it scrolling slowly.</blockquote>

  <p>The front page of the document also gives a count, or says <strong>"None detected"</strong>
  when there were none — so the absence of gaps is itself stated, rather than assumed from
  silence.</p>

  <div class="pull">
    <p><b>The principle, and we hold to it everywhere</b></p>
    <p>Where the app is uncertain, the uncertainty goes <em>in the document</em>. Never in a log
    file, never in a support article, never nowhere at all.</p>
  </div>

  <h2>It runs deeper than gap markers</h2>

  <p>Once you accept that rule, it decides a surprising number of other things.</p>

  <p><strong>Nothing is ever thrown away.</strong> The app makes judgements constantly — is this a
  message, or the time, or a button, or writing on a photograph somebody shared? It gets some of
  them wrong. So everything it decided was <em>not</em> a message is listed at the back of the
  document. If it judged wrongly, that thing is in the wrong section. It is never gone. A
  misjudgement costs you a footnote instead of a message.</p>

  <p><strong>It never invents a time.</strong> iOS hides the time on each message until you swipe
  for it. If you did not swipe, we do not know when a message was sent, and the document says so
  rather than estimating from the date heading. An invented timestamp on an evidence document is
  not a convenience, it is a fabrication.</p>

  <p><strong>The numbers add up.</strong> The cover sheet states how many readings were taken off
  your screen, how many were printed as messages, and how many were set aside. You can add them up
  and check. We run that check ourselves on every build, because a document that accounts for its
  own contents is worth more than one that asks to be trusted.</p>

  <h2>The uncomfortable part</h2>

  <p>Being honest about uncertainty means our documents occasionally look worse than a
  competitor's. Theirs is clean. Ours has a marked gap in it and a list at the back.</p>

  <p>We have thought about that a lot, and keep landing in the same place. If you are handing this
  to somebody who matters, you need to know what it does not cover. A document that hides its own
  weak point is not doing you a favour — it is doing itself one.</p>

  <p>The gap marker is not a defect we failed to remove. <strong>It is the feature.</strong></p>
"""
    + END
    + "</article>",
)

# -------------------------------------------------------------- post three
page(
    "one-payment.html",
    "Export Text Messages Without a Subscription | TextProof",
    "Why TextProof uses a one-time payment for iPhone conversation exports instead of a "
    "monthly subscription. Try an export before deciding.",
    """
<article>
  <div class="tag">Pricing</div>
  <h1>One payment, not a subscription</h1>
  <div class="byline">1 September 2026 · Anthony Jackson</div>

  <p class="standfirst">You need this app during a bad month, not for the rest of your life.
  Billing you every month for that would be charging rent on a problem you are trying to end.</p>

  <p>Almost every app in this category is a subscription now. Some are five pounds a month, some
  are nine, and a few will happily take it for years while you use the thing once.</p>

  <p>We understand exactly why. Subscriptions are worth far more per customer, they make revenue
  predictable, and the App Store rewards them. Every piece of advice a small developer reads says
  charge monthly.</p>

  <h2>Why we are not going to</h2>

  <p>Think about when somebody actually opens this app.</p>

  <p>Their tenancy has ended and the deposit has not come back. The insurer is disputing what was
  agreed on the phone. A relationship has ended badly and there are messages that matter. They
  need a document this week, and then — with any luck — they need never think about it again.</p>

  <p>A subscription turns that into a small monthly reminder of the worst thing that happened to
  them that year. Either they remember to cancel, or they pay for months out of inattention. Both
  are bad. One is worse for them and better for us, which is precisely why we should not build
  it.</p>

  <div class="pull">
    <p><b>£9.99, once.</b></p>
    <p>Every message, every conversation, any length, forever. No renewal, nothing to cancel,
    nothing to remember.</p>
  </div>

  <h2>And the first 20 messages are free</h2>

  <p>Every conversation exports its first 20 messages free. Full quality, no watermark, every
  chat and as often as you like — a real document you can open and read, not a sample with the
  useful part removed.</p>

  <p>That is deliberate too. This app does something difficult and does not do it perfectly every
  time. If somebody shared a poster into the chat, the app reads the writing on the poster and
  cannot always tell it from a message. You should find that out before paying, not after.</p>

  <p>So the free export is not a taster. It is the actual product, on your actual conversation, so
  you can judge it on your own evidence.</p>

  <h2>What one payment means for us</h2>

  <p>We make money once per customer, so the app has to be good enough that people recommend it.
  There is no recurring revenue to smooth over a bad version. If it does not work we do not get a
  second month to fix it — we get a refund and a one-star review.</p>

  <p>That is a healthier pressure than the alternative, which is designing for retention on an app
  nobody should need to retain.</p>

  <h2>Will the price go up?</h2>

  <p>Possibly, later. Introductory prices exist for a reason and this is one: a new app with no
  reviews has to earn its way past apps with thousands.</p>

  <p>If it does rise, <strong>it will not rise for anybody who has already bought it.</strong>
  That is the whole point of a one-time purchase — you bought the app, not a month of it.</p>
"""
    + END
    + "</article>",
)

# ---------------------------------------------------------------- guides
# Search-led how-to pages. Copy rules: never "admissible" / "legally valid" as a claim, own
# conversations only, no accuracy numbers, and link to the App Store listing (on sale since 22 Sep 2026).
GUIDE_DATE = "2026-10-07"
GUIDE_DATE_TEXT = "7 October 2026"

# ------------------------------------------------------ guide one
page(
    "export-text-messages-iphone-pdf.html",
    "How to Export Text Messages From iPhone to PDF | TextProof",
    "Every way to turn an iPhone text conversation into a PDF: free methods first, with and "
    "without a Mac, plus the one-step option. Plain steps.",
    """
<article>
  <div class="tag">Guide</div>
  <h1>How to Export Text Messages From iPhone to PDF</h1>
  <div class="byline">7 October 2026 · Anthony Jackson</div>

  <p class="standfirst">Your iPhone has no button that saves a text conversation as a PDF. The free ways are to take screenshots and turn them into a PDF on the phone, or to print the conversation to PDF from the Messages app on a Mac. If you want the whole thread as one dated document without a Mac, you need an app that reads your screen and builds the PDF for you.</p>

  <p>Below is every method, free ones first. Each one has a catch, and it helps to know the catch before you start.</p>

  <h2>Before you start: show the times</h2>

  <p>Messages hides the time of each message. It only shows a date and time now and then, above a group of messages.</p>

  <p>To see every time, drag the conversation to the left with your finger and hold it there. The times appear down the right-hand side. Whatever method you use, a record with times is more useful than one without.</p>

  <h2>Method 1: Screenshots turned into a PDF (free, no Mac)</h2>

  <p>This works on any iPhone and costs nothing.</p>

  <ol>
    <li>Open the conversation and scroll to the first message you need.</li>
    <li>Take a screenshot. On most iPhones, press the side button and volume up together. On iPhones with a Home button, press the side button and the Home button.</li>
    <li>Scroll down one screen and take another. Repeat until you reach the last message.</li>
    <li>Open Photos, tap Select, and pick all the screenshots in order.</li>
    <li>Tap Share, then Print. The print screen turns your pictures into pages. From there you can save or share them as a PDF instead of printing. The exact button has moved between iOS versions, so look for a Share icon on the print screen.</li>
  </ol>

  <p>The Files app can also combine images into a single PDF, if you save the screenshots there first.</p>

  <p><strong>The catch.</strong> A screenshot only shows one screen at a time. A long conversation can mean dozens or hundreds of pictures. It is easy to skip a screen by accident, and nothing will tell you. The iPhone's "Full Page" screenshot option does not help here. It works for web pages, not for Messages.</p>

  <h2>Method 2: Print to PDF from a Mac (free, needs a Mac)</h2>

  <p>If you have a Mac, this is the best free option. It gives you real text, not pictures.</p>

  <ol>
    <li>Make sure the conversation shows up in Messages on your Mac. That usually means turning on Messages in iCloud on both your iPhone and your Mac, signed in with the same Apple Account.</li>
    <li>Open the conversation in Messages on the Mac.</li>
    <li>Choose File, then Print.</li>
    <li>At the bottom of the print window, use the PDF option to save it as a PDF.</li>
  </ol>

  <p><strong>The catch.</strong> You need a Mac, and the conversation has to have synced to it. Long threads can take a while to load. Check the preview before you save, so you know the start of the conversation is really there.</p>

  <h2>Method 3: Copy and paste (free, slow)</h2>

  <p>You can press and hold a message, tap Copy, and paste it into Notes or an email. Then save or print that as a PDF.</p>

  <p><strong>The catch.</strong> It works one message at a time. You lose who sent what and when, unless you type it in yourself. It is fine for three or four messages. It is not practical for a whole conversation.</p>

  <h2>Method 4: Computer software that reads a backup</h2>

  <p>There are desktop programs that copy your messages out of an iPhone backup on a Windows PC or a Mac.</p>

  <p><strong>The catch.</strong> You need a computer, usually a cable, and often your backup password. Most of these programs are paid, and some are subscriptions. They also mean handing your whole phone backup to a third-party program.</p>

  <h2>Method 5: An app that builds the PDF on your phone</h2>

  <p>This is the gap TextProof is built for, and it is <a href="https://apps.apple.com/app/textproof-text-message-export/id6804264075">free to try on the App Store</a>.</p>

  <p>You record your screen while you scroll through your own conversation, or import screenshots you already took. The app reads every screen, puts the conversation back together in order, and works out who said what. You check it, fix anything it got wrong, and export.</p>

  <p>You get a PDF laid out like the conversation, with dates and times wherever they were on screen. You can also export a spreadsheet (CSV), plain text, or a photo record of the original screens. It works with iMessage, SMS and WhatsApp conversations. Everything happens on the phone. Nothing is uploaded. It is £9.99 or $9.99, paid once, with no subscription.</p>

  <p><strong>The honest trade-offs:</strong></p>

  <ul>
    <li>You still have to scroll through the whole conversation once while recording. A very long thread takes a few minutes.</li>
    <li>Pictures shared in the chat are marked in place, not reproduced in the transcript. The photo record keeps the screens as they looked.</li>
    <li>If the app cannot be sure it caught every screen, it marks a possible gap rather than hiding it. You then re-record that part more slowly. We explain why in <a href="admitting-what-it-missed.html">The document that admits what it missed</a>.</li>
    <li>It only shows a time where the time was visible on screen. It never guesses one.</li>
  </ul>

  <h2>Which method should you use?</h2>

  <ul>
    <li><strong>A few messages:</strong> screenshots or copy and paste.</li>
    <li><strong>A long conversation and you have a Mac:</strong> print to PDF from Messages on the Mac.</li>
    <li><strong>A long conversation and no Mac:</strong> screenshots if you have the patience, or an app that does it in one go.</li>
    <li><strong>For a solicitor, a lawyer, a landlord or an insurer:</strong> read <a href="save-text-messages-for-court.html">How to Save Text Messages for Court or a Dispute</a> first. It covers what a complete record should show.</li>
  </ul>

  <p>If you want paper rather than a file, see <a href="print-text-messages-iphone.html">How to Print Text Messages From Your iPhone</a>.</p>

  <h2>Questions</h2>

  <h3>Can I export text messages from iPhone to PDF for free?</h3>

  <p>Yes. Take screenshots and combine them into a PDF on the phone, or print the conversation to PDF from Messages on a Mac. Both are free. Both take longer than an app, and screenshots make it easy to miss a screen.</p>

  <h3>Can I do it without a Mac?</h3>

  <p>Yes. Screenshots turned into a PDF work on the iPhone alone. So does an app that reads a screen recording. Computer software that reads a backup also works on Windows, but you need the computer.</p>

  <h3>Does it work for WhatsApp too?</h3>

  <p>WhatsApp has its own export, but it gives you a text file, not a PDF. See <a href="export-whatsapp-chat-pdf-iphone.html">How to Export a WhatsApp Chat to PDF on iPhone</a>. For help with TextProof itself, see the <a href="../support.html">support page</a>.</p>
"""
    + END
    + "</article>",
    GUIDE_DATE,
    GUIDE_DATE_TEXT,
)

# ------------------------------------------------------ guide two
page(
    "print-text-messages-iphone.html",
    "How to Print Text Messages From Your iPhone | TextProof",
    "The Messages app has no Print button. Here are the free ways to print a text "
    "conversation from your iPhone, with or without a wireless printer.",
    """
<article>
  <div class="tag">Guide</div>
  <h1>How to Print Text Messages From Your iPhone</h1>
  <div class="byline">7 October 2026 · Anthony Jackson</div>

  <p class="standfirst">The Messages app on iPhone has no Print button. The free way is to take screenshots of the conversation and print them from the Photos app, straight to a wireless printer. If you have a Mac, you can print the whole conversation from Messages there instead, which gives you proper text rather than pictures.</p>

  <p>Here is how each way works, what it costs, and where it goes wrong.</p>

  <h2>What you need</h2>

  <ul>
    <li><strong>A printer your iPhone can see.</strong> iPhones print over Wi-Fi using Apple's AirPrint. Most home printers from the big brands support it. Your phone and printer need to be on the same Wi-Fi network.</li>
    <li><strong>No suitable printer?</strong> Make a PDF instead and print it from any computer, a library or a print shop. Our guide to <a href="export-text-messages-iphone-pdf.html">exporting text messages to PDF</a> covers that.</li>
  </ul>

  <h2>First: make the times show</h2>

  <p>Messages only shows a date and time every so often. Before you take any screenshots, drag the conversation to the left and hold it. The time of every message appears on the right. On paper, the time is often the part that matters most.</p>

  <h2>Method 1: Screenshots, printed from Photos (free)</h2>

  <ol>
    <li>Open the conversation and scroll to the first message you need.</li>
    <li>Take a screenshot. On most iPhones, press the side button and volume up together. On iPhones with a Home button, press the side button and the Home button.</li>
    <li>Scroll down one screen and take the next screenshot. Keep going until you reach the end.</li>
    <li>Open Photos, tap Select, and choose your screenshots.</li>
    <li>Tap the Share button, scroll down and tap Print.</li>
    <li>Choose your printer, set the number of copies, and tap Print.</li>
  </ol>

  <p>Apple's guide to AirPrint describes the same steps for any app with a Share button.</p>

  <p><strong>Tips for a cleaner printout:</strong></p>

  <ul>
    <li>Overlap each screenshot slightly with the last one. Then nobody can say a message fell between two pages.</li>
    <li>Take one screenshot of the contact details too. Tap the name at the top of the conversation to see their number.</li>
    <li>Check the screenshots are in the right order before you print.</li>
  </ul>

  <p><strong>The catch.</strong> One screenshot usually becomes one page. A long conversation can mean a thick stack of paper, mostly white space. It is also easy to skip a screen and not notice.</p>

  <h2>Method 2: Print from a Mac (free, needs a Mac)</h2>

  <p>If your messages sync to a Mac, this is the tidiest free option.</p>

  <ol>
    <li>Make sure the conversation appears in Messages on the Mac. That usually means Messages in iCloud is turned on for both devices.</li>
    <li>Open the conversation.</li>
    <li>Choose File, then Print, and pick your printer.</li>
  </ol>

  <p>You can also save it as a PDF from the same print window. Check the preview first, so you know the whole conversation has loaded.</p>

  <p><strong>The catch.</strong> You need a Mac, and the conversation must have synced to it.</p>

  <h2>Method 3: Print a few messages as text (free)</h2>

  <p>For two or three messages, press and hold each one, tap Copy, and paste it into Notes. Then print the note from its Share menu.</p>

  <p><strong>The catch.</strong> You lose who sent each message and when. Fine for a quick note. Not good enough for a record.</p>

  <h2>Method 4: Turn the conversation into a document first</h2>

  <p>The free methods print pictures of your screen, or need a Mac. The alternative is to turn the conversation into a proper document on your phone first, then print that.</p>

  <p>TextProof does this in one go, and it is <a href="https://apps.apple.com/app/textproof-text-message-export/id6804264075">free to try on the App Store</a>. You record your screen while you scroll through your own conversation, or import screenshots. It reads the text on the phone, puts the messages in order and works out who said what. You check it and fix anything wrong. Then you export a print-ready PDF with dates, times where they were on screen, and page numbers. Nothing is uploaded. It costs £9.99 or $9.99 once, with no subscription.</p>

  <p><strong>The trade-offs, honestly:</strong></p>

  <ul>
    <li>You still scroll through the conversation once while recording.</li>
    <li>It is a transcript. Pictures sent in the chat are marked where they were sent, not printed. If you want the screens themselves, it can also export a photo record of them.</li>
  </ul>

  <h2>Which method is right for you?</h2>

  <ul>
    <li><strong>A handful of messages:</strong> screenshots, or copy into Notes.</li>
    <li><strong>A long conversation and a Mac:</strong> print from Messages on the Mac.</li>
    <li><strong>A long conversation, iPhone only:</strong> screenshots if you have the time, or a document app if you want fewer pages and real text.</li>
  </ul>

  <p>If you are printing messages for a dispute, court or tribunal, read <a href="save-text-messages-for-court.html">How to Save Text Messages for Court or a Dispute</a>. It explains what a complete record should show, and why you should keep the original phone.</p>

  <h2>Questions</h2>

  <h3>Can I print text messages from my iPhone for free?</h3>

  <p>Yes. Screenshot the conversation and print the screenshots from Photos using the Share button and Print. You need a printer that supports AirPrint on the same Wi-Fi. A Mac can also print the conversation for free.</p>

  <h3>How do I print text messages without a wireless printer?</h3>

  <p>Save them as a PDF instead. Then email the PDF to yourself and print it from a computer, or take it to a library or print shop. See <a href="export-text-messages-iphone-pdf.html">How to Export Text Messages From iPhone to PDF</a>.</p>

  <h3>Why is there no Print option in Messages?</h3>

  <p>The iPhone version of Messages does not include one. The Mac version of Messages does have Print in its File menu. For help with TextProof exports, see our <a href="../support.html">support page</a>.</p>
"""
    + END
    + "</article>",
    GUIDE_DATE,
    GUIDE_DATE_TEXT,
)

# ---------------------------------------------------- guide three
page(
    "save-text-messages-for-court.html",
    "How to Save Text Messages for Court or a Dispute | TextProof",
    "How to keep iPhone text messages for a court case or dispute: what to save, a checklist "
    "for a complete record, and what to ask your solicitor or lawyer.",
    """
<article>
  <div class="tag">Guide</div>
  <h1>How to Save Text Messages for Court or a Dispute</h1>
  <div class="byline">7 October 2026 · Anthony Jackson</div>

  <p class="standfirst">Keep the original phone and the full conversation, and do not delete anything. Then make a complete copy that shows every message in order, with who sent it and the date and time. Ask your solicitor or lawyer what format they want before you go to a lot of trouble, because they may already have a preferred way.</p>

  <p>This is general information, not legal advice. Rules differ between countries, courts and types of case. Your solicitor or lawyer can tell you what applies to yours.</p>

  <h2>Step 1: Protect the originals</h2>

  <p>The messages on your phone are the original record. Everything else is a copy.</p>

  <ul>
    <li><strong>Do not delete the conversation</strong>, even the parts you think are unhelpful.</li>
    <li><strong>Keep the phone.</strong> If you plan to replace it, keep the old one too, or make sure the messages have moved across first.</li>
    <li><strong>Back up your phone</strong>, so a lost or broken phone does not mean lost messages.</li>
    <li><strong>Check auto-delete.</strong> iPhone can delete old messages automatically. Go to Settings, then Apps, then Messages, and check that Keep Messages is set to Forever.</li>
    <li><strong>Only use your own messages.</strong> Save the conversations on your own phone. Do not go into someone else's phone to get theirs.</li>
  </ul>

  <h2>Step 2: Make a complete copy</h2>

  <p>A copy is what you hand to a solicitor, a lawyer, a tribunal, a landlord or an insurer. It needs to be complete and easy to follow.</p>

  <p>Before you start, make the times visible. Messages hides them. Drag the conversation to the left and hold it, and the time of each message appears.</p>

  <p>Then pick a method:</p>

  <ul>
    <li><strong>Screenshots.</strong> Free, and work on any iPhone. Overlap each one with the last, so nothing falls between them. Long threads mean a lot of screenshots.</li>
    <li><strong>Print to PDF from a Mac.</strong> Free, if the conversation syncs to Messages on your Mac. It gives you real text.</li>
    <li><strong>An app that builds the document on your phone.</strong> TextProof is one, and you can <a href="https://apps.apple.com/app/textproof-text-message-export/id6804264075">try it free on the App Store</a>. You record your screen while you scroll through your conversation, and it produces a timestamped, print-ready PDF. It marks any place it might have missed something, rather than hiding it. It never invents a time that was not on screen.</li>
  </ul>

  <p>Our pillar guide, <a href="export-text-messages-iphone-pdf.html">How to Export Text Messages From iPhone to PDF</a>, walks through each method step by step.</p>

  <h2>Checklist: what a complete record should show</h2>

  <p>Whatever method you use, check your copy against this list.</p>

  <ul>
    <li><strong>Who the other person is.</strong> Their name and phone number, not just a nickname. Tap their name at the top of the conversation to see the number, and include that.</li>
    <li><strong>Who sent each message.</strong> It should be obvious which messages are yours and which are theirs.</li>
    <li><strong>The date and time of each message</strong>, wherever the phone shows it.</li>
    <li><strong>The whole thread,</strong> not only the parts that help you. Include the messages before and after the key moments, so nothing is out of context.</li>
    <li><strong>Pictures, voice notes and attachments</strong>, at least noted where they were sent.</li>
    <li><strong>No edits on the copy.</strong> No cropping, no covering up, no highlighting on the copy itself. If you want to point things out, do it in a separate note.</li>
    <li><strong>Pages in order</strong>, numbered if printed.</li>
  </ul>

  <h2>Are screenshots of text messages admissible in court?</h2>

  <p>Often they can be used, but nobody can promise it. Whether a court accepts them, and how much they count, depends on the court, the type of case and the judge.</p>

  <p>A few things are widely true:</p>

  <ul>
    <li><strong>Screenshots can be challenged.</strong> If a screenshot looks edited, cropped or incomplete, the other side can question it. The court may then give it little weight.</li>
    <li><strong>The original may be asked for.</strong> This is why you keep the phone and the full conversation.</li>
    <li><strong>Context matters.</strong> A single message on its own can look very different from the same message in the middle of a conversation.</li>
  </ul>

  <p><strong>In the UK,</strong> courts and tribunals regularly see text messages. The judge decides how much weight to give them. Scotland and Northern Ireland have their own court systems, so the details can differ.</p>

  <p><strong>In the US,</strong> rules vary by state and by court. In general, the person relying on a message may need to show it is genuine and who sent it. Lawyers call this authentication. Your lawyer or attorney will know what your court expects.</p>

  <p>No app, including ours, can make a document "court admissible". Anyone who claims that is promising something only a court can decide.</p>

  <h2>Step 3: Ask what format they want</h2>

  <p>Before you print a hundred pages, ask your solicitor or lawyer:</p>

  <ul>
    <li>Do they want screenshots, a PDF, or both?</li>
    <li>Do they want the whole conversation, or a date range?</li>
    <li>Should it be printed, or sent by email?</li>
    <li>Do they need to see the phone itself?</li>
  </ul>

  <p>This isn't legal advice. Ask your solicitor or lawyer what format they want. Their answer saves you time, and it is the format that matters for your case.</p>

  <p>If you need paper copies, see <a href="print-text-messages-iphone.html">How to Print Text Messages From Your iPhone</a>.</p>

  <h2>Questions</h2>

  <h3>How do I export text messages from iPhone for court?</h3>

  <p>Keep the original phone and conversation. Then make a complete copy: screenshots, a PDF printed from a Mac, or a PDF from an app. Show who sent each message, with dates and times. Ask your solicitor or lawyer which format they want.</p>

  <h3>Can I use text messages as evidence?</h3>

  <p>Text messages are often used in disputes and court cases in both the UK and the US. Whether they are accepted, and how much they count, is up to the court. A complete, unedited copy, with the original phone kept safe, gives you the best footing.</p>

  <h3>Is a PDF better than screenshots?</h3>

  <p>Not automatically. A PDF is easier to read and search, while screenshots show exactly what was on your screen. Many people keep both. Your solicitor or lawyer can say which they prefer. For help with TextProof exports, see the <a href="../support.html">support page</a>, and read <a href="nothing-leaves-your-phone.html">why nothing leaves your phone</a>.</p>
"""
    + END
    + "</article>",
    GUIDE_DATE,
    GUIDE_DATE_TEXT,
)

# ----------------------------------------------------- guide four
page(
    "export-whatsapp-chat-pdf-iphone.html",
    "How to Export a WhatsApp Chat to PDF on iPhone | TextProof",
    "WhatsApp's Export Chat gives you a text file, not a PDF. Here is how to export a chat on "
    "iPhone and turn it into a PDF, free or in one step.",
    """
<article>
  <div class="tag">Guide</div>
  <h1>How to Export a WhatsApp Chat to PDF on iPhone</h1>
  <div class="byline">7 October 2026 · Anthony Jackson</div>

  <p class="standfirst">WhatsApp can't save a chat as a PDF directly. Its built-in Export Chat option gives you a plain text file, with or without the photos and videos as separate files. To get a PDF, you either turn that text file into one yourself, take screenshots and combine them, or use an app that builds the PDF from your screen.</p>

  <p>Here is each way, step by step, with the catch for each one.</p>

  <h2>Method 1: WhatsApp's own Export Chat (free)</h2>

  <p>This is built into WhatsApp and costs nothing.</p>

  <ol>
    <li>Open the chat you want to export. It can be a one-to-one chat or a group.</li>
    <li>Tap the person's name, or the group name, at the top of the screen.</li>
    <li>Scroll down and tap Export Chat.</li>
    <li>Choose Attach Media or Without Media.</li>
    <li>Pick where to send it. You can email it to yourself, save it to Files, or share it another way.</li>
  </ol>

  <p>WhatsApp's help centre describes the same steps.</p>

  <p><strong>What you get.</strong> A plain text file of the messages. Each line shows the date, time, the sender's name and the message. If you chose Attach Media, the photos, videos and voice notes come as separate files alongside it. It may arrive as a zip file. In the Files app, tap a zip file to open it.</p>

  <p><strong>The catch.</strong> It is not a PDF, and it does not look like the chat. It is one long block of text. Pictures are not shown in place, only noted or attached separately. For a long chat, check the file goes back as far as you need.</p>

  <h2>Turning the text file into a PDF</h2>

  <p>Once you have the text file, you can make a PDF from it for free.</p>

  <ul>
    <li><strong>On your iPhone:</strong> paste the text into a document app such as Pages, then export that as a PDF. Pages has Export in its menu, with PDF as one of the formats. You can also try opening the text file and using Share, then Print, which can save it as a PDF. The steps vary a little between iOS versions.</li>
    <li><strong>On a computer:</strong> open the text file in any word processor and save or print it as a PDF.</li>
  </ul>

  <p>You can tidy the layout while you are there. Do not change any of the words, if the PDF might be used as a record. If you need to point something out, do it in a separate note.</p>

  <h2>Method 2: Screenshots combined into a PDF (free)</h2>

  <p>If you want the PDF to look like the chat itself, screenshots are the free way.</p>

  <ol>
    <li>Scroll to the first message you need.</li>
    <li>Take a screenshot. On most iPhones, press the side button and volume up together. On iPhones with a Home button, press the side button and the Home button.</li>
    <li>Scroll down one screen and repeat until the end.</li>
    <li>In Photos, select the screenshots, tap Share and choose Print. From the print screen you can save them as a PDF instead of printing.</li>
  </ol>

  <p><strong>The catch.</strong> A long chat means a lot of screenshots. It is easy to skip a screen. The iPhone's "Full Page" screenshot only works for web pages, so it will not capture a whole chat.</p>

  <h2>Method 3: An app that builds the PDF for you</h2>

  <p>TextProof does this in one go. <a href="https://apps.apple.com/app/textproof-text-message-export/id6804264075">Try it free on the App Store</a>.</p>

  <p>You record your screen while you scroll through your own WhatsApp chat, or import screenshots. The app reads every screen on the phone, puts the messages back in order and works out who said what. You check the result and fix anything it got wrong. Then you export a PDF laid out like the conversation, with dates and times wherever they were on screen. You can also export a spreadsheet (CSV), plain text, or a photo record of the original screens.</p>

  <p>Nothing is uploaded. It costs £9.99 or $9.99 once, with no subscription. We explain why in <a href="one-payment.html">One payment, not a subscription</a>.</p>

  <p><strong>The trade-offs:</strong></p>

  <ul>
    <li>You scroll through the chat once while recording, so a very long chat takes a few minutes.</li>
    <li>Pictures are marked where they were sent, not reproduced in the transcript. If a picture has words in it, those words are labelled as coming from a picture.</li>
    <li>In group chats, check the names on the review screen before you export.</li>
    <li>The full version costs £9.99, once. WhatsApp's own export is free, if a plain text file is all you need.</li>
  </ul>

  <h2>Which way should you choose?</h2>

  <ul>
    <li><strong>You just want a copy of the words:</strong> WhatsApp's Export Chat.</li>
    <li><strong>You want a PDF and do not mind some work:</strong> export the text file and turn it into a PDF, or take screenshots.</li>
    <li><strong>You want a PDF that looks like the chat, in one step:</strong> an app that builds it from your screen.</li>
  </ul>

  <p>If the chat matters for a dispute, read <a href="save-text-messages-for-court.html">How to Save Text Messages for Court or a Dispute</a>. The same rules apply to WhatsApp: keep the original phone and the whole chat. For iMessage and SMS, see <a href="export-text-messages-iphone-pdf.html">How to Export Text Messages From iPhone to PDF</a>.</p>

  <h2>Questions</h2>

  <h3>Can WhatsApp export a chat as a PDF?</h3>

  <p>No. WhatsApp's Export Chat gives you a text file, plus media files if you choose. You can turn that text into a PDF yourself, or use screenshots or an app instead.</p>

  <h3>How do I export a WhatsApp chat on iPhone?</h3>

  <p>Open the chat, tap the name at the top, scroll down and tap Export Chat. Choose whether to attach media, then send or save the file.</p>

  <h3>Is a WhatsApp backup the same as an export?</h3>

  <p>No. A WhatsApp backup to iCloud is for restoring your chats onto a phone. You cannot open it and read it as a document. An export gives you a file you can read. For help with TextProof, see our <a href="../support.html">support page</a>.</p>
"""
    + END
    + "</article>",
    GUIDE_DATE,
    GUIDE_DATE_TEXT,
)

# ---------------------------------------------------------------- index page
INDEX_TITLE = "TextProof Blog — Exporting and Keeping iPhone Messages"
INDEX_DESC = (
    "Plain guides to exporting, printing and saving iPhone text messages, and short pieces on "
    "why TextProof works the way it does."
)
INDEX_URL = f"{SITE}/blog/"

items = "\n".join(
    f"""    <li>
      <h2><a href="{fname}">{h1}</a></h2>
      <div class="byline">{date_text} · {AUTHOR}</div>
      <p>{desc}</p>
    </li>"""
    for fname, desc, h1, date, date_text in sorted(POSTS, key=lambda p: p[3], reverse=True)
)

write(
    "index.html",
    meta(
        INDEX_TITLE,
        INDEX_DESC,
        INDEX_URL,
        "website",
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": INDEX_TITLE,
            "description": INDEX_DESC,
            "url": INDEX_URL,
            "inLanguage": "en-GB",
            "publisher": PUBLISHER,
        },
    ),
    f"""
<article>
  <div class="tag">Writing</div>
  <h1>Writing from TextProof</h1>
  <p class="standfirst">Plain guides to exporting, printing and keeping your messages. And why the app works the way it does: no cloud, honest documents, one payment.</p>
  <ul class="posts">
{items}
  </ul>
"""
    + END
    + "</article>",
)
