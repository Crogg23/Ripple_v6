export const meta = {
  name: 'deep3-glance-only-tables',
  description: 'Proper look at the 415 warehouse tables that only got a glance, skeptic every live lead, rank the survivors',
  phases: [
    { title: 'Dig', detail: '83 agents, 5 tables each, up to 35 read-only queries' },
    { title: 'Skeptic', detail: 'one fresh skeptic per live lead, up to 12 queries' },
    { title: 'Rank', detail: 'judge ranks survivors against the existing menu' },
  ],
}

const GROUPS = args.groups

const TABLE_RESULT = {
  type: 'object',
  properties: {
    table: { type: 'string' },
    verdict: { type: 'string', enum: ['live', 'probed', 'dead', 'skip'] },
    headline: { type: 'string', description: 'plain words, one or two sentences, every number checked' },
    number: { type: 'string', description: 'the one number that carries it' },
    comparison: { type: 'string', description: 'the peer group or time comparison done' },
    checks: { type: 'array', items: { type: 'string' }, description: 'what was run, one line each, with result' },
    hit_means: { type: 'string' },
    miss_means: { type: 'string' },
    boring: { type: 'string', description: 'the dull explanation and whether it was tested' },
    next_join: { type: 'string' },
    traps_found: { type: 'array', items: { type: 'string' }, description: 'columns or loads that look real but are not' },
    statements_used: { type: 'number' },
  },
  required: ['table', 'verdict', 'headline', 'checks', 'boring', 'traps_found'],
}
const DIG_SCHEMA = {
  type: 'object',
  properties: {
    group: { type: 'string' },
    statements_used: { type: 'number' },
    results: { type: 'array', items: TABLE_RESULT },
  },
  required: ['group', 'results'],
}
const SKEPTIC_SCHEMA = {
  type: 'object',
  properties: {
    table: { type: 'string' },
    verdict: { type: 'string', enum: ['CONFIRMED', 'NARROWED', 'BROKEN'] },
    checks: { type: 'array', items: { type: 'string' }, description: 'each query run and the number it returned' },
    corrected_headline: { type: 'string', description: 'plain words; empty if BROKEN' },
    grade: { type: 'string', enum: ['A', 'B', 'C', 'D'], description: 'A publishable as is, B one join or outside check away, C footnote, D drop' },
    why_grade: { type: 'string' },
    next_join: { type: 'string' },
    new_traps: { type: 'array', items: { type: 'string' } },
  },
  required: ['table', 'verdict', 'checks', 'corrected_headline', 'grade', 'why_grade'],
}

const digPrompt = (g) => `Working directory C:\\Code\\Ripple_v6. Read reports/coverage_2026-09-24/deep3/BRIEF.md first and follow it exactly.
Your group id is ${g.id}. Your 5 tables: ${g.tables.join(', ')}.
Their facts are in reports/coverage_2026-09-24/deep3/chunks/${g.id}.json.
Write reports/coverage_2026-09-24/deep3/${g.id}.md and ${g.id}.sql, scratch only under reports/coverage_2026-09-24/deep3/${g.id}/.
Then return the structured result with one entry per table.`

const skepticPrompt = (g, t) => `Working directory C:\\Code\\Ripple_v6. You are a fresh-context skeptic. Break this lead; don't polish it.

Chris's words, verbatim: "3 strong leads is pitiful - do better" / "I need things that I can put in a portfolio." / "Yes. Go."
His pitch is "I can join public datasets." A lead only counts if a hostile data editor can't break it.

The claim, from deep pass 3 group ${g.id}, table ${t.table}:
HEADLINE: ${t.headline}
NUMBER: ${t.number || ''}
COMPARISON: ${t.comparison || ''}
CHECKS THE BUILDER RAN: ${(t.checks || []).join(' | ')}
BORING EXPLANATION PER BUILDER: ${t.boring || ''}
The builder's full notes are in reports/coverage_2026-09-24/deep3/${g.id}.md and every statement in ${g.id}.sql.

Attack in order: the denominator and peer group; duplicates, amendments, repeated totals; sentinels and caps; whether 3-4 units carry the whole effect (report the median unit); circular selection; self-coded fields; name matches without a second field; whether the table is complete enough; the dull explanation. Re-derive the headline number yourself.

Rules: Python door only from the repo root: from connect import db; c = db.connect(). First statements: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300, then ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'. SELECT and WITH only; the login is the all-powers admin role. At most 12 statements. Read C:\\Users\\wroge\\.claude\\projects\\c--Code-Ripple-v6\\memory\\MEMORY.md and trap files touching this table. Scratch only under reports/coverage_2026-09-24/deep3/${g.id}/skeptic_${t.table}/ if you can write at all. Every person or company named is a data match, not verified against primary records.

Return the structured verdict.`

phase('Dig')
const results = await pipeline(
  GROUPS,
  (g) => agent(digPrompt(g), { label: `dig:${g.id}`, phase: 'Dig', schema: DIG_SCHEMA, agentType: 'general-purpose' }),
  async (dig, g) => {
    if (!dig) return { group: g.id, failed: true, tables: g.tables }
    const live = (dig.results || []).filter((t) => t.verdict === 'live')
    const verdicts = await parallel(live.map((t) => () =>
      agent(skepticPrompt(g, t), { label: `skeptic:${g.id}:${t.table}`.slice(0, 80), phase: 'Skeptic', schema: SKEPTIC_SCHEMA, agentType: 'skeptic' })
        .then((v) => ({ ...t, skeptic: v }))
    ))
    const liveChecked = verdicts.filter(Boolean)
    const others = (dig.results || []).filter((t) => t.verdict !== 'live')
    log(`${g.id}: ${live.length} live, ${liveChecked.filter((t) => t.skeptic && ['A', 'B'].includes(t.skeptic.grade)).length} graded A/B`)
    return { group: g.id, statements: dig.statements_used, results: [...liveChecked, ...others] }
  }
)

const done = results.filter(Boolean)
const failed = done.filter((r) => r.failed)
if (failed.length) log(`WARNING: ${failed.length} groups failed to dig: ${failed.map((f) => f.group).join(', ')}`)
const all = done.filter((r) => !r.failed).flatMap((r) => r.results.map((t) => ({ ...t, group: r.group })))
const survivors = all.filter((t) => t.verdict === 'live' && t.skeptic && ['A', 'B'].includes(t.skeptic.grade))
log(`${all.length} tables looked at; ${all.filter((t) => t.verdict === 'live').length} live; ${survivors.length} survive at A/B`)

phase('Rank')
const survivorText = survivors.map((t, i) => `${i + 1}. [${t.group}] ${t.table} | grade ${t.skeptic.grade} | ${t.skeptic.verdict} | ${t.skeptic.corrected_headline} | why: ${t.skeptic.why_grade} | next join: ${t.skeptic.next_join || t.next_join || ''}`).join('\n')
const ranking = await agent(`Working directory C:\\Code\\Ripple_v6. You are the judge for deep pass 3.
Chris wants portfolio pieces; his pitch is "I can join public datasets."

Here are the new leads that survived a skeptic at grade A or B:
${survivorText || '(none)'}

Existing shelf to rank against: reports/coverage_2026-09-24/joins/PORTFOLIO.md (8 skeptic-checked dossiers) and reports/coverage_2026-09-24/skeptic2/SCOREBOARD.md (26 round-2 leads) and the menu in reports/coverage_2026-09-24/menu.md.

Write reports/coverage_2026-09-24/deep3/MENU.md: every new A/B lead scored 1-5 on size (money, harm, people), novelty (1 = famous story), defensible (survives a hostile editor), plus days for a solo analyst to publish, and which existing dossier or lead it beats or joins with. Plain words, short lines, a table. Then say which 5 new leads most deserve a join-pass dossier next, and why.
Return a short plain-text summary: the top 10 new leads in rank order with one line each, and the 5 dossier picks.`, { label: 'judge', phase: 'Rank', agentType: 'general-purpose' })

return {
  tables_looked_at: all.length,
  failed_groups: failed.map((f) => f.group),
  verdict_counts: all.reduce((m, t) => { m[t.verdict] = (m[t.verdict] || 0) + 1; return m }, {}),
  skeptic_counts: all.filter((t) => t.skeptic).reduce((m, t) => { const k = `${t.skeptic.verdict}/${t.skeptic.grade}`; m[k] = (m[k] || 0) + 1; return m }, {}),
  survivors: survivors.map((t) => ({ group: t.group, table: t.table, grade: t.skeptic.grade, verdict: t.skeptic.verdict, headline: t.skeptic.corrected_headline, next_join: t.skeptic.next_join || t.next_join })),
  broken_or_low: all.filter((t) => t.skeptic && !['A', 'B'].includes(t.skeptic.grade)).map((t) => ({ table: t.table, grade: t.skeptic.grade, verdict: t.skeptic.verdict, why: t.skeptic.why_grade })),
  traps: all.flatMap((t) => [...(t.traps_found || []), ...((t.skeptic && t.skeptic.new_traps) || [])].map((x) => `${t.table}: ${x}`)),
  ranking,
}
