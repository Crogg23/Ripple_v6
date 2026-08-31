"""Ripple — The Data: What's Actually In Here?

A breakdown of what data we have, organized by domain, with plain-English
descriptions of what each piece is and why it's here.
"""
import os
import sys
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "library-onboarding"))

from dotenv import load_dotenv
load_dotenv(REPO / "library-onboarding/.env", override=True)

import snow  # noqa: E402

st.set_page_config(page_title="Ripple — The Data", page_icon="📡", layout="wide")


@st.cache_resource
def _conn():
    serve_pat = (os.environ.get("SNOWFLAKE_SERVE_PAT") or "").strip() or None
    if serve_pat:
        try:
            return snow.connect(
                pat=serve_pat,
                role=os.environ.get("RIPPLE_SERVE_ROLE", "RIPPLE_READER"),
                warehouse=os.environ.get("RIPPLE_SERVE_WH", "SERVE_WH"),
            )
        except Exception:
            return snow.connect()
    else:
        return snow.connect()


st.markdown("""
# The Data

## What's actually in here?

Think of this as a library card catalog — except instead of books, it's
every government database we could get our hands on. Here's what's on the
shelves, organized by what it covers.

---

## Healthcare & Public Health

The biggest domain. Government tracks every dollar it pays to healthcare
providers, every adverse drug event, every hospital inspection.

| Dataset | What it is | Why we have it |
|---------|-----------|---------------|
| **CMS Open Payments** | Every payment from a drug/device company to a doctor — meals, speaking fees, research grants. ~43M records. | Connect corporate money to individual providers. |
| **HHS OIG LEIE** | The "banned list" — providers excluded from federal healthcare programs. ~83K entries. | The watchlist. Cross-ref against payment databases = our biggest detector. |
| **CMS NPPES** | The national registry of every healthcare provider (NPI numbers). ~7.7M providers. | The phone book. Every provider in the country, with their identifier. |
| **FDA FAERS** | Every adverse drug event reported to the FDA. Millions of reports. | Drug safety signals. Which drugs, which doctors, which outcomes. |
| **CMS Nursing Home data** | Inspections, penalties, deficiencies, staffing for every nursing home. | Facility quality + enforcement history. |

**What connects:** NPI (provider IDs) links doctors across all these databases.
A single NPI number proves "this banned doctor is the same person receiving these payments."

---

## Money & Spending

Where the federal budget actually goes. Who gets contracts, who gets grants,
who gets paid.

| Dataset | What it is | Why we have it |
|---------|-----------|---------------|
| **USASpending Contracts** | Every federal contract award. Who got paid, how much, for what. ~$7T tracked. | Follow the money to companies. |
| **USASpending Assistance** | Grants, loans, direct payments. The non-contract half of federal spending. | Same, for non-contract recipients. |
| **SEC 13F Holdings** | What big institutional investors own. Quarterly disclosures. | Who owns what. Corporate network mapping. |
| **FAC Single Audit** | Annual audits of entities that receive federal money. 411K records. | Who's been audited, what they found. |

**What connects:** UEI (company IDs) and EIN (tax IDs) link companies across
contract, spending, and tax-exempt databases.

---

## Corporate & Financial

Who companies are, who owns them, and how they connect.

| Dataset | What it is | Why we have it |
|---------|-----------|---------------|
| **GLEIF** | The global registry of legal entities (LEI numbers). ~2.4M worldwide. | Corporate identity backbone. Ties companies to parents/subsidiaries. |
| **GLEIF Level 2** | Ownership relationships between companies. Who owns whom. ~482K links. | The corporate family tree. |
| **IRS Exempt Orgs (BMF)** | Every tax-exempt organization in the US. ~1.9M nonprofits. | Connects nonprofits to EINs. |
| **SEC EDGAR** | Corporate filings — 10-Ks, proxies, ownership disclosures. | Company disclosures, officer names, relationships. |

**What connects:** LEI links across international corporate data. EIN links
across domestic. CIK links SEC filings to real companies.

---

## Sanctions & Security

Who the government says you can't do business with — and whether anyone's
listening.

| Dataset | What it is | Why we have it |
|---------|-----------|---------------|
| **OFAC SDN** | The Treasury sanctions list — every sanctioned person, company, and vessel. | The "do not touch" list. |
| **NOAA AIS** | Ship position broadcasts in U.S. waters. ~58M records (8-day snapshot). | Where ships actually are. Cross-ref against sanctions = are sanctioned ships in US waters? |
| **SAM Exclusions** | Debarred government contractors — companies banned from federal work. | The procurement watchlist. |

**What connects:** IMO numbers link ships across maritime/sanctions databases.
Entity names + identifying info link sanctioned persons to other appearances.

---

## Justice & Courts

The legal system's paper trail.

| Dataset | What it is | Why we have it |
|---------|-----------|---------------|
| **CourtListener Dockets** | Federal court dockets. ~71.7M records across all courts. | Who's suing whom, and the government's legal actions. |
| **SCOTUS/Oyez** | Supreme Court decisions and oral arguments. | Historical legal record. |
| **Voteview** | Congressional voting records. Every roll call vote, every member. | How legislators vote on relevant issues. |

---

## Environment & Safety

What's in the air, the water, the workplace.

| Dataset | What it is | Why we have it |
|---------|-----------|---------------|
| **EPA FRS/ECHO** | Every regulated facility in the US. Permits, violations, enforcement. ~4M facilities. | Environmental enforcement history. |
| **OSHA Inspections** | Workplace safety inspections and violations. | Worker safety record by employer. |
| **CPSC NEISS** | ER visits from product injuries. Statistical national sample. | Consumer safety patterns. |

**What connects:** EIN/facility IDs link companies to their environmental and
safety records.

---

## How this all fits together

Imagine you're looking at one company. With these connections, you can see:

1. **What contracts they got** (USASpending)
2. **Who owns them** (GLEIF Level 2)
3. **Whether they've been sanctioned** (OFAC)
4. **Their environmental violations** (EPA)
5. **Their workplace safety record** (OSHA)
6. **Whether they're debarred** (SAM)
7. **Court cases they're involved in** (CourtListener)
8. **All from public data, all linked by hard identifiers.**

That's the power of putting it all in one room. No single database tells
the full story. All of them together do.

---

*This is a living document. As new data gets loaded, this page gets updated.*
""")
