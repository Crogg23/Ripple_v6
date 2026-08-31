#!/usr/bin/env python3
"""Countable-rule gate for Chris's message shape.

Not a judge. A counter. Reads the Stop-hook payload on stdin and reports every
line that breaks a rule that can be counted. Rules that need judgment — bar
speak, walking the chain — are left to the prompt reader that runs after this.

Exit 0  = clean, or out of retries. Say nothing.
Exit 2  = broken. stderr goes back to Claude and stopping is blocked.

The retry budget is what keeps this from looping forever. Every rewrite IS
counted; after MAX_TRIES failed attempts the gate gives up loudly and lets the
message stand, so a rule the counter cannot express can never trap the session.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

MAX_WORDS = 12
MAX_TRIES = 3
MAX_LINK_TEXT = 40

# Forward-slash paths and this repo's native backslash ones, plus bare filenames
# carrying an extension the repo actually produces.
PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\[\w.\-\\]+)"
    r"|(?:[\w.\-]+/[\w.\-/]+)"
    r"|(?:[\w.\-]+\\[\w.\-\\]+)"
    r"|(?:\b[\w\-]+\.(?:py|md|sql|html|json|csv|yml|yaml|sh|jsonl|txt)\b)"
)
URL_RE = re.compile(r"https?://\S+")
LINK_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")
# A whole line that is nothing but a short label and one short markdown link.
LINK_ONLY_RE = re.compile(
    r"(?:\*\*)?[\w ’'\-.,]{0,30}(?:\*\*)?:?\s*\[[^\]]{1,%d}\]\([^)]+\)" % MAX_LINK_TEXT
)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿️⬀-⯿]")
OPEN_PARENS = "(（"
CLOSE_PARENS = ")）"


def strip_markup(line: str) -> str:
    """Line with markdown scaffolding removed, ready for word counting."""
    # Backticked words are words Chris still has to read, so only the ticks
    # come off. A long sentence in backticks must not hide from the count.
    out = line.replace("`", " ")
    out = URL_RE.sub(" x ", out)
    out = LINK_RE.sub(" x ", out)
    out = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", out)  # bullet marker
    out = re.sub(r"^\s*#{1,6}\s+", "", out)  # heading marker
    out = re.sub(r"^\s*>\s*", "", out)  # quote marker
    out = out.replace("**", "").replace("__", "")
    out = EMOJI_RE.sub(" ", out)
    return out.strip()


def content_lines(message: str):
    """Yield (line_no, raw) for prose lines only: no tables, no fenced code."""
    in_fence = False
    for i, raw in enumerate(message.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        if stripped.startswith("|") or " | " in stripped:  # table row
            continue
        if set(stripped) <= set("-—= "):  # horizontal rule
            continue
        yield i, raw


def check(message: str) -> list[str]:
    problems: list[str] = []
    pointers = 0
    seen_paths: set[str] = set()

    for lineno, raw in content_lines(message):
        stripped = raw.strip()

        # One clickable pointer to the report file is allowed, because Chris
        # still has to open the receipts. A second means receipts are leaking
        # back into chat.
        if LINK_ONLY_RE.fullmatch(stripped):
            pointers += 1
            if pointers > 1:
                problems.append(f"L{lineno}: second report link, one per message")
            continue

        text = strip_markup(raw)
        if text:
            words = [w for w in text.split() if any(c.isalnum() for c in w)]
            if len(words) > MAX_WORDS:
                problems.append(f"L{lineno}: {len(words)} words, max is {MAX_WORDS}")

            if any(c in text for c in OPEN_PARENS + CLOSE_PARENS):
                problems.append(f"L{lineno}: parenthesis")

            # Em and en dashes always count, tight or spaced — a tight em-dash
            # is the exact habit the rule targets. A plain hyphen only counts
            # when it is punctuation, so hyphenated words stay legal.
            dashes = text.count("—") + text.count("–")
            dashes += len(re.findall(r"(?<!\w)-(?!\w)", text))
            if dashes > 1:
                problems.append(f"L{lineno}: {dashes} dashes, max is 1")

        for hit in PATH_RE.findall(URL_RE.sub(" ", raw)):
            if hit not in seen_paths:
                seen_paths.add(hit)
                problems.append(f"L{lineno}: path in chat, {hit}")

    return problems


def _tries_file(session: str) -> Path:
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).parents[2])
    state = root / ".claude" / "state"
    state.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^\w.\-]", "_", session or "nosession")
    return state / f"{safe}.shape_tries"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    message = payload.get("last_assistant_message") or ""
    if not message.strip():
        return 0

    tries_path = _tries_file(payload.get("session_id", ""))
    problems = check(message)

    if not problems:
        tries_path.unlink(missing_ok=True)
        return 0

    try:
        tries = int(tries_path.read_text().strip())
    except Exception:
        tries = 0

    if tries >= MAX_TRIES:
        tries_path.unlink(missing_ok=True)
        print(
            f"shape counter gave up after {MAX_TRIES} rewrites. Still broken:\n"
            + "\n".join(f"  {p}" for p in problems[:6])
            + "\nLetting it stand so the session is not trapped.",
            file=sys.stderr,
        )
        return 0

    tries_path.write_text(str(tries + 1))

    shown = problems[:12]
    more = len(problems) - len(shown)
    lines = [
        f"shape counter blocked the last message. Countable rules, not opinions. "
        f"Attempt {tries + 1} of {MAX_TRIES}.",
        *(f"  {p}" for p in shown),
    ]
    if more:
        lines.append(f"  ...and {more} more")
    lines.append(
        "Rewrite the whole message so every one of these is gone, then stop. "
        "Do not apologize and do not explain the fix."
    )
    print("\n".join(lines), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
