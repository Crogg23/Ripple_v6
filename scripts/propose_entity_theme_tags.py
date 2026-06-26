#!/usr/bin/env python3
"""Propose ENTITY_TYPES + THEMES facet tags for the 54 landed/modeled sources.

These two facets were left for agent-assignment at the REGISTRY checkpoint:
ENTITY_TYPES was 100% empty; only the 'epstein' THEME was populated. This fills
both from each source's identity (name / domain / real populated columns), using
ONLY the controlled FACET_VOCAB tokens.

SAFE BY DEFAULT — previews + validates against the live vocab. Pass --apply to write.
  ENTITY_TYPES is SET (it was empty). THEMES is SET to the reviewed list (authoritative) —
  this is deliberate: the only theme currently in the system is 'epstein', and the audit
  found it OVER-APPLIED (it sits on NPPES, NOAA-AIS, SEC-EDGAR, bioRxiv, earthquakes — sources
  with no Epstein connection). Setting the reviewed themes here DE-CONTAMINATES the 54 landed
  sources (keeps 'epstein' only on the 4 real DOJ/Epstein corpora). The ~140 non-landed
  epstein-tagged sources are out of scope — flag separately. Idempotent: re-running is a no-op.

  python3 scripts/propose_entity_theme_tags.py            # preview + vocab check
  python3 scripts/propose_entity_theme_tags.py --apply    # write (REGISTRY checkpoint)

Array binding uses PARSE_JSON(json.dumps(list)) — the load-bearing register.py fix
(a naked Python list silently splats into adjacent columns).
"""
import sys, json, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, "/Users/chrisr./Documents/GitHub/Ripple_v6/library-onboarding")
from snow import connect

# entity_types vocab: aircraft asset case company event facility filing organization payment person place vessel
# themes vocab: civil_rights_history corporate_ownership enforcement_actions epstein follow_the_money
#               harm_to_people power_who_holds_it public_health_safety revolving_door sanctions_illicit
TAGS = {
    # --- health / providers / facilities ---
    "fed_cms_nppes":              (["person", "organization"],            ["public_health_safety"]),
    "fed_cms_facility_affiliation":(["person", "facility"],               ["public_health_safety"]),
    "fed_hhs_oig_leie":           (["person", "organization"],            ["enforcement_actions", "public_health_safety"]),
    "fed_cms_pos_other":          (["facility"],                          ["public_health_safety"]),
    "fed_cms_nursing_home":       (["facility", "organization"],          ["public_health_safety"]),
    "fed_cms_home_health":        (["facility"],                          ["public_health_safety"]),
    "fed_cms_dialysis":           (["facility"],                          ["public_health_safety"]),
    "fed_cms_hospice":            (["facility"],                          ["public_health_safety"]),
    "fed_cms_hcris":              (["facility"],                          ["public_health_safety"]),
    "fed_cms_hospital_general":   (["facility"],                          ["public_health_safety"]),
    "fed_cms_irf":                (["facility"],                          ["public_health_safety"]),
    "fed_cms_ltch":               (["facility"],                          ["public_health_safety"]),
    "fed_fda_drug_enforcement":   (["company", "event"],                  ["public_health_safety", "enforcement_actions"]),
    "fed_clinicaltrials":         (["organization", "event"],             ["public_health_safety"]),
    # --- money / spending / corporate ---
    "fed_usaspending_contracts":  (["company", "payment"],                ["follow_the_money", "corporate_ownership"]),
    "fed_usaspending_toptier_agencies":(["organization"],                 ["follow_the_money"]),
    "fed_hhs_taggs":              (["organization", "payment"],           ["follow_the_money"]),          # BROKEN load (re-ingest)
    "intl_ec_sercop":             (["organization", "company", "payment"],["follow_the_money"]),
    "fed_sec_edgar_company_tickers":(["company"],                         ["corporate_ownership"]),
    "xc_wikipedia_largest_us_companies":(["company"],                     ["corporate_ownership"]),
    "intl_gr_gemi":               (["company"],                           ["corporate_ownership"]),       # PARTIAL load
    "intl_es_borme":              (["company", "filing"],                 ["corporate_ownership"]),
    "intl_ch_zefix":              (["company"],                           ["corporate_ownership"]),       # PARTIAL load
    "intl_ie_cro":                (["company"],                           ["corporate_ownership"]),
    "fed_cfpb_complaints":        (["company", "event"],                  ["harm_to_people"]),
    "fed_fdic_failed_banks":      (["company", "event"],                  ["follow_the_money"]),
    "fed_treasury_debt_to_penny": ([],                                    ["follow_the_money"]),
    "fed_treasury_avg_interest_rates":([],                                []),
    # --- sanctions / maritime ---
    "fed_ofac_sdn":               (["person", "organization", "vessel"],  ["sanctions_illicit", "enforcement_actions"]),
    "fed_noaa_ais":               (["vessel"],                            ["sanctions_illicit"]),
    # --- power / influence / courts ---
    "fed_fara_bulk":              (["person", "organization", "filing"],  ["power_who_holds_it", "follow_the_money"]),
    "fed_revolvingdoor_project":  (["person", "organization"],            ["revolving_door", "power_who_holds_it", "corporate_ownership"]),
    "fed_federal_register_documents":(["filing"],                         ["power_who_holds_it"]),
    "fed_scdb":                   (["case"],                              ["power_who_holds_it"]),
    "fed_oyez":                   (["case"],                              ["power_who_holds_it"]),
    "fed_fjc_idb":                (["case"],                              ["enforcement_actions"]),       # EMPTY load (re-ingest)
    "fed_doj_fca_settlements":    (["company", "case"],                   ["enforcement_actions", "follow_the_money"]),
    "fed_naag_multistate_settlements":(["company", "case"],               ["enforcement_actions"]),       # PARTIAL load
    "fed_fdic_enforcement":       (["organization", "case"],              ["enforcement_actions"]),       # PARTIAL load
    "fed_doj_crt_cases":          (["case"],                              ["civil_rights_history"]),      # thin
    "intl_hudoc":                 (["case", "person"],                    ["civil_rights_history"]),
    # --- epstein corpora (theme already set; merge entity types) ---
    "xc_wayback_doj_epstein":     (["filing"],                            ["epstein"]),
    "xc_wayback_replay_doj_listing":(["filing"],                          ["epstein"]),
    "xc_wayback_replay_doj_deep_pages":(["filing"],                       ["epstein"]),
    "fed_doj_epstein_library":    (["filing"],                            ["epstein"]),
    # --- civil-rights / history ---
    "fed_mapping_inequality":     (["place"],                             ["civil_rights_history"]),
    "fed_slavevoyages_intraamerican":(["event", "person"],               ["civil_rights_history"]),      # BROKEN load (HTML)
    "fed_wpa_slave_narratives":   (["person", "filing"],                  ["civil_rights_history"]),
    "fed_nara_wra_aad":           (["person"],                            ["civil_rights_history"]),      # PARTIAL load
    # --- science / geo / other (no investigative theme) ---
    "fed_usgs_earthquakes":       (["event", "place"],                    []),
    "intl_ember_elec":            (["place"],                             []),
    "intl_it_istat":              (["place"],                             []),
    "xc_biorxiv_medrxiv":         (["filing", "person"],                  []),
    "fed_nara_aad":               (["filing"],                            []),                            # PARTIAL load
}

apply = "--apply" in sys.argv
conn = connect(); cur = conn.cursor()

# load live vocab
def vocab(facet):
    cur.execute("SELECT value FROM LIBRARY_META.REGISTRY.FACET_VOCAB WHERE facet=%s", (facet,))
    return {r[0] for r in cur.fetchall()}
EVOC, TVOC = vocab("ENTITY_TYPE"), vocab("THEME")

# validate every token against the live vocab BEFORE touching anything
bad = []
for sid, (ents, thms) in TAGS.items():
    for e in ents:
        if e not in EVOC: bad.append(f"{sid}: entity '{e}' not in vocab")
    for t in thms:
        if t not in TVOC: bad.append(f"{sid}: theme '{t}' not in vocab")
if bad:
    print("VOCAB VIOLATIONS — aborting:"); [print("  " + b) for b in bad]; sys.exit(1)
print(f"[vocab] all {sum(len(e)+len(t) for e,t in TAGS.values())} tokens conform "
      f"({len(EVOC)} entity_types, {len(TVOC)} themes available)\n")

# preview / apply
n_ent = n_thm = n_clean = 0
for sid, (ents, thms) in TAGS.items():
    cur.execute("SELECT ARRAY_TO_STRING(entity_types,','), ARRAY_TO_STRING(themes,',') "
                "FROM LIBRARY_META.REGISTRY.SOURCE_REGISTRY WHERE source_id=%s", (sid,))
    row = cur.fetchone()
    if not row:
        print(f"  ?? {sid:<34} NOT IN REGISTRY — skipped"); continue
    cur_e = [x for x in (row[0] or "").split(",") if x]
    cur_t = [x for x in (row[1] or "").split(",") if x]
    proposed_t = sorted(set(thms))
    removed = sorted(set(cur_t) - set(thms))   # bogus epstein tags being cleaned
    new_e = bool(ents) and set(ents) != set(cur_e)
    new_t = set(proposed_t) != set(cur_t)
    if new_e: n_ent += 1
    if new_t: n_thm += 1
    if removed: n_clean += 1
    flag = "  APPLY" if apply else ""
    print(f"  {sid:<34} entity:[{','.join(ents)}]  theme:[{','.join(proposed_t)}]"
          f"{'  +ent' if new_e else ''}{'  ~thm' if new_t else ''}"
          f"{'  -[' + ','.join(removed) + ']' if removed else ''}{flag}")
    if apply:
        cur.execute(
            "UPDATE LIBRARY_META.REGISTRY.SOURCE_REGISTRY "
            "SET ENTITY_TYPES = PARSE_JSON(%s), THEMES = PARSE_JSON(%s) "
            "WHERE source_id = %s",
            (json.dumps(ents), json.dumps(thms), sid))

print(f"\n{'APPLIED' if apply else 'PREVIEW'}: {len(TAGS)} sources | {n_ent} get entity_types | "
      f"{n_thm} change themes | {n_clean} have a bogus 'epstein' tag cleaned")
if not apply:
    print("Re-run with --apply to write (entity_types + themes SET authoritatively for these 54).")
conn.close()
