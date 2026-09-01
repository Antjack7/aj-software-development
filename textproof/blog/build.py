"""
Builds the TextProof writing pages from _head.part, _foot.part and the bodies below.

Kept as a script rather than three hand-maintained files so the nav, the footer and the
stylesheet link cannot drift apart between posts. Run it from this folder:

    python build.py
"""

import io

HEAD = io.open("_head.part", encoding="utf-8").read()
FOOT = io.open("_foot.part", encoding="utf-8").read()


def page(fname: str, title: str, desc: str, body: str) -> None:
    head = HEAD.replace(
        '<link rel="stylesheet" href="post.css">',
        f'<title>{title}</title>\n'
        f'<meta name="description" content="{desc}" />\n'
        '<link rel="stylesheet" href="post.css">',
    )
    io.open(fname, "w", encoding="utf-8", newline="").write(head + body + FOOT)
    print("wrote", fname)


END = (
    '<div class="end"><p>TextProof turns a screen recording of a conversation into a '
    "timestamped, print-ready document — entirely on your iPhone. "
    '<a href="../index.html">See how it works →</a></p></div>'
)

# ---------------------------------------------------------------- post one
page(
    "nothing-leaves-your-phone.html",
    "Why there is no cloud, and never will be — TextProof",
    "Every competitor that syncs has a server holding your messages. We looked at what that "
    "would buy us and decided against it permanently.",
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
    "The document that admits what it missed — TextProof",
    'The hardest decision in the app was making it say "I might have missed something here" '
    "instead of quietly closing the gap.",
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
    "One payment, not a subscription — TextProof",
    "You need this app during a bad month, not forever. Charging monthly for that would be "
    "charging people for a problem they are trying to end.",
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

  <h2>And one free export, in full</h2>

  <p>One conversation exports free. Full quality, no watermark, up to the first 25 messages — a
  real document you can open and read, not a sample with the useful part removed.</p>

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
