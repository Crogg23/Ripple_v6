# Judge brief, calibration test, 2026-09-25

You're the judge. For each story, you decide one bin from the packet alone.
You didn't search, and you don't search now. No web, no memory: if it isn't in the packet, it doesn't exist.

## Read first
- `reports/calibration_2026-09-25/RUBRIC.md`, sections "The six bins" and "Tie-breaks". Those rules are the law here.
- Your packets: `reports/calibration_2026-09-25/judge/packets/<story_id>.json`

## Evidence rules
- `quote_check` = **exact** or **near**: the quote is really on the page. Full evidence.
- `quote_check` = **missing**: the quote isn't on the page. **Ignore that source completely.**
- `quote_check` = **blocked**: the page wouldn't load for the checker. Use it only if `paywalled` is true and the quote is a headline or dek. Mark the verdict `"blocked_evidence": true` if it decides the bin.
- `entity_named` is the searcher's claim. Check it yourself against the quote.
- `page_context` is about 300 characters around the quote on the saved page. Use it to read the window, the date and what the quote refers to.
- **Copies count once:** a rewrite of another outlet's story, a wire copy, or the same URL twice is one source. An op-ed or opinion column is never news.

## The decision, in order
0. **Name the entity**: the headline's subject, who or what did the thing. For a national number, place + measure; the period is the window.
1. **Contradicted first.** Split the lead into its claims. If a usable source on the same entity, measure and overlapping window contradicts **any** claim, opposite direction or a number more than 25% off, the bin is Contradicted, even if another claim matches. Say which claim matched.
2. **Matched.** A usable source names the entity and states the same finding in the same direction, in numbers or in words.
   - **Matched + more** if our headline or number line has something countable no usable source states: a number, a named entity, a comparison. A claim with no count or name isn't more.
3. **Not comparable.** Only when a source gives a number for the entity that differs from ours because its window or definition differs, and nothing else matches.
4. **Known pattern.** No source names the entity, but one reports the same kind of finding about other entities or in general. An explainer on a rule, program or deadline isn't a pattern.
5. **Unreported**, but only if `queries_logged` is 5 or more. Under 5: `"bin": "Insufficient search"`.

## Output: one JSON per story
Write `reports/calibration_2026-09-25/judge/<story_id>.json`:

```json
{
  "story_id": "S001",
  "bin": "Matched + more",
  "entity": "what you took the entity to be",
  "deciding_sources": [0, 2],
  "earliest_match_date": "2021-04-14",
  "post_cutoff_match": false,
  "what_we_add": "the lead's number or link the press lacks, or empty",
  "why": "two short lines, plain words",
  "confidence": "high | medium | low",
  "blocked_evidence": false
}
```

- `earliest_match_date`: the oldest usable source that reaches Matched. Empty if no match.
- `post_cutoff_match`: true if any usable matching source is dated after 2026-06-30.

## Your final reply
One line per story: story_id, bin, confidence. Nothing else.
