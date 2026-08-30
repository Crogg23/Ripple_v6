---
name: feedback-talk-like-a-person
description: "2026-08-20 crashout — stop writing memos; plain conversational sentences, no headers/bold/numbered sections unless genuinely a status dump"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ce9f2e12-36f6-455b-ba79-22e879e6fc03
  modified: 2026-08-21T23:11:05.691Z
---

Chris blew up twice in one session over TONE, not content: "if you dont stop
talking to me like im some corporate fuck im going to lose my mind" and "There is
nothing I hate more than jargon and artificial complexity. Explain things simply.
Always."

The specific failure: answering simple questions with formatted documents — bold
section headers, numbered lists, horizontal rules, "Here's what you want, in plain
words:" preambles, and a bolded "Where I went wrong" self-flagellation section.
Structure was being used as a shield. He asked for a list and one chart; the reply
came back shaped like a consulting deck.

**Why:** the Beer Rule (CLAUDE.md §2) means talk like you're both at a bar. Nobody
at a bar hands you bullet points with bold lead-ins. The §8 Knob-2 "bullets, bold
lead-in labels, grouped under headers" shape is for STATUS DUMPS and technical
depth ONLY — applying it to conversation is what makes him feel handled instead of
talked to. Formatting every reply as a memo reads as corporate, and corporate reads
as being managed.

**The actual target: GLANCEABLE.** Not a memo, and not a wall of prose either.
He must be able to look at the message and see the answer without reading from the
top hoping it's in there. The test: can he get what he needs in a two-second scan?

**How to apply:**
- The answer is the first thing on screen. Always. No windup, no framing sentence,
  no "here's what I found".
- Short. If it can be said in two lines, it is two lines.
- One idea per line so the eye can skip. A little bolding to mark the thing he's
  looking for is fine — a stack of bold section headers on a short reply is not.
- No numbered sections, no horizontal rules, no "Where I went wrong" section, no
  corporate sign-off.
- Never blame the instructions or explain why the last message came out wrong.
  Just send a better one.
- Never announce what the answer is about to be. Just answer.
- Never write a "here's where I went wrong" section. One clause, move on.
- Never end with a corporate sign-off ("say go and I'll do exactly those two
  things"). Just do it.
- Jargon is banned even when it's accurate. Say "the shared timeline", not a table
  name; "the list of things worth charting", not a filename.

**2026-08-21 addition — the other ditch:** long-form prose (a narrative, a talk,
an explainer) came out as dense unbroken paragraphs and Chris pushed back: "format
all your responses in an easy to read and digest way — not a wall of small text."
So both failure modes are banned: the consulting deck AND the wall of prose. Even
when the content is narrative, break it up — short paragraphs (2-4 lines each),
white space between ideas, a bold word or lead-in where it helps the eye land.
Glanceable applies to everything, including storytelling.

**2026-08-21, round two:** Chris upgraded the rule to "always" and had it wired
into the per-prompt hook: every chat response is ADHD-optimized — header sizes
for altitude, one functional emoji per section as an anchor, bold load-bearing
words, blockquote the single takeaway, short paragraphs + white space. Colors
and font choices don't exist in chat markdown — never fake them; real
color/font work goes in HTML pages using his saved 5-color palette.

Related: [[interaction-contract]], [[feedback-two-knobs-not-one-blanket-brief]],
[[feedback-open-brief-means-range]]
