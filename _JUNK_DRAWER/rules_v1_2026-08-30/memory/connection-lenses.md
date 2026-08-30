---
name: connection-lenses
description: "The investigative \"lenses\" / KPI families the connected Library can produce — the analytical payoff, in Chris's Power-BI-measures framing"
metadata: 
  node_type: memory
  type: project
  originSessionId: ed14949d-db3e-47b1-8731-0fce125ae10d
---

Worked out 2026-06-24. Chris thinks in Power BI "measures + lenses" (Epic ED dev). The connected corpus produces KPIs shaped "**count of X where Y has Z**" — count rows on one side, filtered by a fact on the other; only works because tables are joined.

**The lens families (the payoff of the connection engine):**
1. **Bad-Actor Cross-Check** — exclusion/enforcement list vs active operations. *Proven:* HHS-OIG banned providers ↔ NPPES active providers = **8,503 exact NPI matches**. Lowest-hanging real story ("banned but still operating"). Chris's pick to chase first.
2. **Follow-the-Money** — federal $ (USASpending/HHS grants, EIN) → recipients → who they also are (FARA foreign agents, SEC filers, court defendants).
3. **Place-Based** — anything with FIPS/ZIP/lat-lon rolled up by geography (redlining overlays, enforcement per capita, provider density).
4. **Entity Dossier** — pick one EIN/NPI/name → every dataset it appears in across domains; "reach" = # domains touched. This is what the bridge layer unlocks.
5. **Trend Over Time** — court cases (4.1M FJC), settlements, recalls, debt over time.

Example KPIs: banned-but-active providers; nursing homes whose owner also owns a banned provider; grant recipients who are also foreign agents; providers in historically-redlined ZIPs; recalled drugs whose maker was also in a settlement.

✅ = computable now (proven joins). Rest light up as the bridge layer ([[CLAUDE.md]] connect engine work) + more sources land. Could be materialized as a `connect__metrics` dbt mart. Serves [[platform-vision]].
