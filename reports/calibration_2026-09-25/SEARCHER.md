# Searcher brief, calibration test, 2026-09-25

You're a press researcher. For each story you're given, find out whether anyone has already published it.
You collect evidence. **You never decide the verdict.** A separate judge does that from your quotes alone.

## Read first
- `reports/calibration_2026-09-25/RUBRIC.md`: the rules. Read "The six bins" so you know what evidence matters.
- `reports/calibration_2026-09-25/stories.tsv`: tab-separated. Your stories' rows hold the frozen headline, number and caveats.
- Every person or company in a lead is a data match, not verified. Nothing gets published.

## For each story

1. **Name the entity.** The company, facility, person, agency, or for a national number, place + measure + period. Write it down before searching.
2. **Search at least 5 queries, target 8, never more than 10.** Web searches are capped per session and shared by every agent. Mix them:
   - entity + the finding in plain words
   - entity + the agency that regulates it: DOJ, OIG, CMS, EPA, SEC, state agency
   - the distinctive number from the lead
   - the local outlet: city paper, state public radio, trade press
   - the agency's own enforcement or press-release pages
   - one query aimed at **disagreement**: coverage that says the opposite
   - one query aimed at **recent coverage**, July to September 2026
3. **Open every promising page with WebFetch** and ask it for the exact sentences about the entity. Search snippets aren't evidence.
4. **Record up to 6 sources**, best first:
   - sources that name the entity and report the same finding
   - the earliest coverage you can find
   - any coverage dated after 2026-06-30
   - sources that disagree with the lead
   - if nothing names the entity: the best 1-2 sources on the same pattern or scheme
5. **Quotes must be copied exactly from the page**, at most 40 words, no ellipses inside. A script will fetch the URL and check that the quote is really there. A paraphrase fails the check.

## Rules
- **Memory never counts.** If you remember a story but can't find a live URL for it, it doesn't exist for this test. Say so in notes.
- Search a private person's name only when the lead itself names them.
- Don't open or edit any other file. No warehouse queries. No git.
- If a page is paywalled, record it with the headline or dek as the quote, and set `"paywalled": true`.

## Output: one JSON file per story
Write `reports/calibration_2026-09-25/search/<story_id>.json` with the Write tool:

```json
{
  "story_id": "S001",
  "entity": "Las Vegas Sands, Texas lobby media spending 2021-2026",
  "queries": [
    {"q": "Las Vegas Sands Texas lobby spending ads", "found_useful": true},
    {"q": "...", "found_useful": false}
  ],
  "sources": [
    {
      "url": "https://...",
      "outlet": "Texas Tribune",
      "date": "2021-04-14",
      "source_type": "news",
      "entity_named": "yes",
      "quote": "exact words from the page",
      "paywalled": false,
      "searcher_note": "what this source covers, one line"
    }
  ],
  "notes": "anything the judge's work depends on: e.g. only pattern coverage found; memory suggested X but no URL"
}
```

- `source_type`: news · trade press · government · court · testimony · research · company
- `date`: YYYY-MM-DD from the page, or "unknown"
- `sources` may be empty. Log the queries anyway.

## Your final reply
One line per story: story_id, queries run, sources recorded, and whether any source names the entity. Nothing else.
