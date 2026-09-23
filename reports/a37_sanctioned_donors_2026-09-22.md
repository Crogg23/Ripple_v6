# A37 — sanctioned people as political donors

Run 2026-09-22. Query in `scripts/probe_a37_sanctioned_donors.py`.

## What was checked

Three sanctions lists, individuals only:

| list | people |
|---|---|
| OFAC SDN | 7,488 individuals of 19,114 rows |
| UK OFSI | persons with NAME_6 and NAME_1 |
| UN consolidated | 736 individuals of 1,011 rows |

Joined to FEC individual contributions, 283,771,819 rows,
`ENTITY_TYPE = 'IND'`, memo rows excluded.

Match key: surname and first name, letters only, uppercased.
Middle names dropped on both sides. Keys under 3 letters dropped.

## Raw result

| measure | value |
|---|---|
| sanctioned people with a name hit | 440 |
| donation rows touched | 67,146 |
| dollars on those rows | $10,737,832 |
| distinct sanctioned-name to donor-name pairs | 9,065 |

## Why the raw result is not a finding

KIM, Jong Un matched KIM, JONG OK in California.
KRSTIC, Radislav matched a window cleaner in Ridgewood.
GRIMM, Matthew Simon carries the largest dollar total, $186,400 in one pair.

The key is surname plus first name. That is not an identity.
The saved trap on this is direct: single-word name matches clear at 8 percent.
Two words is better, still not proof.

## The rarity cut

Keeping only keys seen in 3 or fewer zip codes leaves 266 candidates.
That cut removes the JOHN SMITH problem. It does not remove the
MOHAMMAD ALI problem — a rare key can still be two different people.

## What would make it real

FEC carries no date of birth, no passport, no national ID.
The sanctions lists carry all three.
There is no shared hard identifier between the two sides.

So corroboration has to come from soft fields:

- city and state against the sanctions address country
- employer and occupation against the sanctions designation text
- gift dates against the designation date

That is a human read of 266 rows, not a query.

## Files

- `outputs/a37_sanctioned_donor_name_matches.csv` — 9,065 pairs
- `outputs/a37_rare_key_candidates.csv` — 266 rare-key candidates

## Card correction

The docket grades A37 "A measured". The measured join behind that grade is
`IMO_NUMBER`, 29 shared values between OFAC and the UK list.
IMO numbers are ship hull numbers. They do not touch FEC.
For this question the real grade is D, name match.
