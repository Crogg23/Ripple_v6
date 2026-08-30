---
description: Save a correction from Chris so it fires on every future prompt. Usage /correction <what I got wrong, in his words>
---
Append one line to `.claude/corrections.md` in the form `YYYY-MM-DD — <the correction, plain words, one line>` using today's date and this text: $ARGUMENTS

If $ARGUMENTS is empty, use the last thing Chris corrected in this conversation.
Then fix the thing in your next message. No explanation, no apology. Reply with just the line you saved.
