# What data is behind the docket

Checked against the live warehouse on 2026-09-06. Read only.

## What this page does and does not tell you

It tells you the tables are on the shelf. That is all it tells you.

A question needs four things to be answerable. This checks the first one.

| what it needs | checked here | what a failure looks like |
|---|---|---|
| the tables exist | yes | the query errors straight away |
| the two sides share years | 139 of 150 | the query runs and returns nothing |
| a column that really joins them | no | it runs and matches strangers |
| a match meaning what you think | no | it runs and the answer is a mirage |

Last week six questions were checked and all six failed.
Every one of them would still score `all tables here` on this page.

Gate two closed on 2026-09-06. 128 of the 190 tables now have a measured year
span, so 139 of 150 entries can be checked for overlap before anyone writes a
join.

## The numbers

| | count |
|---|---|
| entries | 150 |
| still open | 86 |
| tables they touch | 190 |
| rows reachable | 3,085,758,088 |
| tables that are missing | 0 |
| entries whose years are measured | 139 |

There is a lot of data, and now most of it is labelled by year.

62 tables still have no measured span. 43 of those carry no date column at all,
which is right for a lookup table. The rest fail to parse.

27 measured tables have a quarter or more of their rows unreadable as dates.
Their spans describe the rows that parsed, not the table. Read them with care.

## How big each open question is

| size | questions |
|---|---|
| under 100k | 7 |
| 100k to 1M | 18 |
| 1M to 10M | 22 |
| 10M to 100M | 35 |
| over 100M | 4 |

## Every entry

`tables` is how many we have out of how many it needs.
`on the shelf` says whether they are all there and whether any reads old.

| # | question | where it stands | tables | rows | years known | on the shelf |
|---|---|---|---|---|---|---|
| 1 | Are doctors banned from Medicare still showing up on hospice paperwork | part done | 4/4 | 2,364,431 | — | all tables here |
| 2 | Which nursing home owners get fined the most per home, and does it rep | found something | 3/3 | 449,372 | — | all tables here |
| 3 | Do banks that lend money also own the polluting sites? | nothing there | 2/2 | 5,305,548 | — | all tables here |
| 4 | Do addiction doctors get paid more by drugmakers when they prescribe m | missing a piece | 3/3 | 39,177,643 | — | all tables here |
| 5 | Do people get worse loan terms right after a hurricane or flood? | part done | 2/2 | 71,243,587 | — | all tables here |
| 6 | Do dialysis chains that dominate a rural area have worse patient outco | part done | 5/5 | 30,613,170 | — | all tables here |
| 7 | Are banned doctors working at clinics serving poor neighborhoods? | missing a piece | 3/3 | 159,994 | — | all tables here |
| 8 | When a county's jail population spikes, does drug overdose rise later? | part done | 3/3 | 347,425 | — | all tables here |
| 9 | Do the biggest polluters also pay their workers the least? | part done | 3/3 | 3,887,442 | — | all tables here |
| 10 | Are the suppliers who bill the most also getting kickback-like payment | part done | 1/1 | 381,228 | — | all tables here |
| 11 | Do money-losing hospitals still have doctors taking big drug company p | part done | 3/3 | 16,967,082 | — | all tables here |
| 12 | Do hospitals with financial trouble also have padded ventilator equipm | part done | 4/4 | 17,689,980 | — | all tables here |
| 13 | Do owners re-register the business right after getting fire-safety fin | same as another | 2/2 | 214,455 | — | all tables here |
| 14 | Are clinics claiming to be 'rural' actually sitting in cities? | nothing there | 1/1 | 5,530 | — | all tables here |
| 15 | Are banned companies still getting paid on disaster relief contracts? | found something | 2/2 | 93,321,752 | — | all tables here |
| 16 | Are any of them on the federal fraud exclusion list? | nothing there | 2/2 | 84,784 | — | all tables here |
| 17 | Same as #3 but through a different bank record | missing a piece | 2/2 | 5,327,985 | — | all tables here |
| 18 | Do they order more of that device at the hospital they work for? | part done | 2/2 | 15,501,229 | — | all tables here |
| 19 | Do the ones taking industry payments still get top bonuses? | nothing there | 2/2 | 1,920,800 | — | all tables here |
| 20 | Are the same people running both, and is that a conflict? | found a little | 1/1 | 2,260,193 | — | all tables here |
| 21 | Do hospital employees get paid less than the local average wage? | part done | 2/2 | 3,625,540 | — | all tables here |
| 22 | Do those same neighborhoods have more toxic factories today? | found something | 4/4 | 276,792 | — | all tables here |
| 23 | How much money did banned suppliers still collect? | found something | 2/2 | 524,417 | — | all tables here |
| 24 | Nothing to compare yet, program just started | not started | 1/1 | 6,637 | — | all tables here |
| 25 | Are centers whose local site shut down still collecting Medicare money | found a little | 3/3 | 221,023 | — | all tables here |
| 26 | Does housing sit empty after a big storm instead of getting rebuilt? | part done | 2/2 | 1,794,280 | — | all tables here |
| 27 | Are any of them already banned for past fraud? | found something | 4/4 | 2,358,060 | — | all tables here |
| 28 | Do homes exaggerate patient sickness to get paid more? | part done | 3/3 | 31,836,407 | — | all tables here |
| 29 | Do hospitals near the most toxic sites fail financially more often? | part done | 3/3 | 115,522 | — | all tables here |
| 30 | Do new owners appear right after a home gets penalized, like a shell g | found something | 2/2 | 30,605 | — | all tables here |
| 31 | Do hospital-owned home health agencies perform worse but cost more? | found a little | 3/3 | 33,075 | — | all tables here |
| 76 | Do they sell their company stock right before bad news like a fine hit | not started | 3/3 | 2,697,968 | — | all tables here |
| 77 | Do they own stock in companies whose cases they're deciding? | not started | 3/3 | 12,810,285 | — | all tables here |
| 78 | Do they trade stock in industries their own committee oversees? | not started | 3/3 | 957,752 | — | all tables here |
| 79 | Did they quietly switch auditors right before collapsing? | not started | 3/3 | 2,981,945 | — | all tables here |
| 80 | Do they still keep winning government contracts? | not started | 2/2 | 93,565,062 | — | all tables here |
| 81 | Did executives sell their own stock right before the collapse? | not started | 4/4 | 6,983,857 | — | all tables here |
| 82 | Do unions reporting missing money also have an active political fund? | not started | 2/2 | 677,741 | — | all tables here |
| 83 | Does lobbying spending spike right before a new safety rule is finaliz | not started | 2/2 | 914,380 | — | all tables here |
| 84 | Who's spending money for or against them in elections? | not started | 4/4 | 308,215 | — | all tables here |
| 85 | Does it flow from their corporate PAC into top leaders' campaign funds | not started | 3/3 | 15,453,697 | — | all tables here |
| 86 | Are big-spending political advertisers avoiding official campaign fina | not started | 3/3 | 374,229 | — | all tables here |
| 87 | Do they also personally donate to U.S. political campaigns? | not started | 2/2 | 84,394,012 | 1942-2026 | here but going stale |
| 88 | Are the same people also treasurers of federal campaign committees? | not started | 2/2 | 249,624 | — | all tables here |
| 89 | Do the same people wine and dine state lawmakers and donate federally? | not started | 3/3 | 84,980,743 | — | all tables here |
| 90 | Do agency contracts shift toward an official's old industry after they | not started | 2/2 | 93,153,830 | — | all tables here |
| 91 | Do they buy a stock, then introduce a bill that helps it? | not started | 3/3 | 412,557 | 2023-2026 | all tables here |
| 92 | Does office spending go to vendors who are also campaign donors? | not started | 2/2 | 89,086,588 | — | all tables here |
| 93 | Do places with more rejected mail ballots overlap with high-incarcerat | not started | 3/3 | 164,603 | — | all tables here |
| 94 | Does a judge's political leaning or donations predict how they rule? | not started | 3/3 | 95,037,994 | — | all tables here |
| 95 | Do gifts or debts they report ever involve parties in their own courtr | not started | 3/3 | 54,272 | — | all tables here |
| 96 | Do they still get disaster payouts for flood damage? | not started | 2/2 | 26,276,045 | — | all tables here |
| 97 | Are they being rebuilt each time instead of relocated? | not started | 3/3 | 26,300,071 | — | all tables here |
| 98 | Are any sitting downstream of a dam rated poor with no emergency plan? | not started | 2/2 | 107,466 | — | all tables here |
| 99 | Do the ones with unsafe dams also have a pile of unpaid safety fines? | not started | 3/3 | 3,271,937 | — | all tables here |
| 100 | Did they spring up right after the disaster was declared? | not started | 2/2 | 119,404,344 | — | all tables here |
| 101 | Are they still using outdated flood maps? | not started | 2/2 | 1,805,855 | — | all tables here |
| 102 | Do they also have the worst drinking water problems? | not started | 4/4 | 22,752,998 | — | all tables here |
| 103 | Do they still win federal contracts afterward? | not started | 3/3 | 94,350,772 | — | all tables here |
| 104 | Do the same addresses show up behind multiple fatal crashes? | not started | 3/3 | 377,918 | — | all tables here |
| 105 | Do the same crossings get hit by trains again and again? | not started | 2/2 | 1,401,937 | — | all tables here |
| 106 | Are those same counties still struggling with opioids today? | not started | 3/3 | 180,068,296 | — | all tables here |
| 107 | Did the biggest distributors in a state match who actually got sued? | not started | 2/2 | 178,598,908 | — | all tables here |
| 108 | Were they still being paid after their device got recalled? | not started | 3/3 | 15,600,368 | — | all tables here |
| 109 | Do they have more reported deaths than devices reviewed the normal way | not started | 2/2 | 2,919,247 | — | all tables here |
| 110 | Do the same doctors' prescribing costs jump right along with it? | not started | 3/3 | 27,525,898 | 2022-2024 | here but going stale |
| 111 | Did their nearest full-service hospital shut down? | not started | 3/3 | 54,168 | — | all tables here |
| 112 | Do the ones with more retracted (fake or flawed) studies keep getting  | not started | 3/3 | 2,413,705 | — | all tables here |
| 113 | Are companies still paying doctors to promote them? | not started | 2/2 | 15,385,209 | — | all tables here |
| 114 | Are they going uninspected for years at a time? | not started | 3/3 | 9,214,469 | — | all tables here |
| 115 | Do accidents happen at their mines afterward? | not started | 2/2 | 3,360,888 | — | all tables here |
| 116 | Do they pay the legal minimum wage and also rack up serious safety vio | not started | 3/3 | 6,029,356 | — | all tables here |
| 117 | Did the same ones get hit with health and safety fines? | not started | 3/3 | 999,129 | — | all tables here |
| 118 | Do the ones with the worst loan losses also have enforcement actions a | missing a piece | 2/2 | 2,174,516 | — | all tables here |
| 119 | How much do they get paid per day, per detained person? | not started | 3/3 | 95,726,889 | — | all tables here |
| 120 | Do they also have high jail populations generally? | not started | 2/2 | 738,276 | — | all tables here |
| 121 | Are any of them U.S. doctors or political donors? | not started | 3/3 | 100,328,474 | — | all tables here |
| 122 | Are any of them under U.S. or international sanctions? | not started | 3/3 | 17,105,571 | — | all tables here |
| 123 | Who's the real parent company hiding behind them? | not started | 4/4 | 15,001,221 | — | all tables here |
| 124 | How much do they pay their top executives? | missing a piece | 2/2 | 7,519,456 | — | all tables here |
| 125 | Are they still operating and filing paperwork as if nothing happened? | not started | 3/3 | 1,340,465 | — | all tables here |
| 126 | Do consumer complaints about them pile up before regulators catch on? | not started | 2/2 | 17,173,686 | — | all tables here |
| 127 | Are banks pulling branches out of those neighborhoods over time? | not started | 2/2 | 2,824,132 | — | all tables here |
| 128 | Were failed banks still active members right up until they collapsed? | part done | 2/2 | 9,911 | — | all tables here |
| 129 | Do complaints pile up for years before an official recall happens? | not started | 2/2 | 2,469,802 | — | all tables here |
| 130 | Are their affordability contracts expiring in fast-gentrifying areas? | not started | 2/2 | 209,116 | — | all tables here |
| 131 | Do they charge higher rates in historically redlined neighborhoods? | not started | 3/3 | 45,055,469 | — | all tables here |
| 132 | Do bankruptcy filings spike in the year after? | not started | 2/2 | 33,216,361 | — | all tables here |
| 133 | Do the most-sued chains also get the most fines? | not started | 3/3 | 10,888,289 | — | all tables here |
| 134 | Are they still allowed to work in health care because they were never  | not started | 2/2 | 6,383,655 | — | all tables here |
| 135 | Does patient care quality drop afterward? | not started | 3/3 | 50,806 | — | all tables here |
| 136 | Do the ones with the most known security flaws still win contracts? | not started | 2/2 | 93,155,098 | — | all tables here |
| 137 | Are any of them showing up at U.S. ports anyway? | not started | 2/2 | 58,125,631 | 2024-2024 | here but going stale |
| 138 | Do the ones involved in the most killings still get the most federal g | not started | 2/2 | 19,918,355 | — | all tables here |
| 139 | Are more dealers in an area linked to more gun deaths? | part done | 3/3 | 225,959 | — | all tables here |
| 140 | Which investment funds and political donors are behind them? | not started | 4/4 | 3,886,063 | — | all tables here |
| 141 | Do the ones with the worst storm outages also charge the highest rates | not started | 4/4 | 1,796,291 | — | all tables here |
| 142 | Do some have pollution spikes that never trigger a violation? | not started | 3/3 | 16,637,002 | — | all tables here |
| 143 | Are they paying the same doctors running the trial to also promote the | missing a piece | 2/2 | 15,385,547 | — | all tables here |
| 144 | Do outcomes vary a lot by judge and detention facility? | missing a piece | 1/1 | 12,631,225 | — | all tables here |
| A32 | Do banned companies' owners also donate to political campaigns? | not started | 3/3 | 84,424,187 | — | all tables here |
| A33 | Do the worst-fined chains also run a political action committee? | not started | 2/2 | 74,744 | — | all tables here |
| A34 | Do polluted districts get less help from their representative? | not started | 3/3 | 4,980,621 | — | all tables here |
| A35 | Do members trade stock in industries their committee oversees? | not started | 2/2 | 45,762 | 2008-2026 | all tables here |
| A36 | Do the industries caught defrauding Medicare fund the committees that  | not started | 2/2 | 870,609 | — | all tables here |
| A37 | Do sanctioned individuals still show up as political donors? | not started | 4/4 | 84,250,573 | — | all tables here |
| E32 | Do drinking water violations spike after a flood? | nothing there | 2/2 | 41,683,657 | — | all tables here |
| E33 | Do they violate pollution rules more right after a storm? | found a little | 2/2 | 9,732,386 | — | all tables here |
| E34 | Do they have more drug overdose deaths? | nothing there | 2/2 | 761,501 | — | all tables here |
| E35 | Did overdose deaths rise where jails emptied out? | found a little | 2/2 | 260,507 | — | all tables here |
| E36 | Does overdose death rise after a disaster? | nothing there | 2/2 | 26,382,920 | — | all tables here |
| E37 | Does a pay raise from a drug company lead to more prescriptions? | nothing there | 3/3 | 31,502,716 | — | all tables here |
| E38 | Are drug and device companies still paying them anyway? | found something | 2/2 | 15,442,256 | — | all tables here |
| E39 | Do the paid ones prescribe way more opioids than unpaid ones? | found something | 2/2 | 16,801,930 | — | all tables here |
| E40 | Are brand-new doctors billing Medicare for millions in expensive wound | found something | 2/2 | 19,388,356 | — | all tables here |
| E41 | Can hospitals still legally order tests and equipment through them? | found something | 2/2 | 2,102,101 | — | all tables here |
| E42 | Is drug industry money still being sent to them? | found something | 2/2 | 24,991,730 | — | all tables here |
| E43 | Were they already losing money before the sale? | found something | 2/2 | 50,532 | — | all tables here |
| E44 | Did its safety violations get worse right before the fines hit? | found something | 2/2 | 434,659 | — | all tables here |
| E45 | Do safety violations spike after a storm hits the area? | nothing there | 2/2 | 2,199,209 | — | all tables here |
| E46 | Are these 'triple owners' actually better or worse than others? | nothing there | 2/2 | 2,274,906 | — | all tables here |
| E47 | Were they already in financial trouble before converting? | found something | 2/2 | 50,532 | — | all tables here |
| E48 | Were their financial reports already bad beforehand? | found something | 2/2 | 50,532 | — | all tables here |
| E49 | Did they win government contracts specifically during their ban? | found something | 2/2 | 93,321,752 | — | all tables here |
| E50 | Do new health care businesses pop up right after, chasing relief money | nothing there | 2/2 | 26,262,428 | — | all tables here |
| E51 | Does that label actually bring in more clinics? | found a little | 2/2 | 98,196 | — | all tables here |
| E52 | Do wages, suicide, and overdose rates all get worse there? | found a little | 3/3 | 3,879,944 | — | all tables here |
| E53 | Do they get penalized less often than other neighborhoods? | nothing there | 2/2 | 3,220,945 | — | all tables here |
| E54 | Do they pay workers less than clean factories? | nothing there | 2/2 | 3,721,474 | — | all tables here |
| E55 | Is poor housing placed disproportionately near hazards? | nothing there | 3/3 | 18,603,892 | — | all tables here |
| E56 | Do bonus and non-bonus doctors get similar industry money? | nothing there | 2/2 | 15,888,964 | — | all tables here |
| E57 | Are they also the ones industry pays the most? | found something | 2/2 | 16,681,786 | — | all tables here |
| E58 | Do states with more malpractice payouts also get more industry money? | nothing there | 3/3 | 17,115,888 | — | all tables here |
| E59 | Do they have the worst quality ratings? | nothing there | 2/2 | 8,476 | — | all tables here |
| E60 | Do they die at a higher rate? | found a little | 2/2 | 27,889,193 | — | all tables here |
| E61 | Do they also have worse finances? | found a little | 2/2 | 714,217 | — | all tables here |
| E62 | Are they still getting cited for missing sprinkler systems? | found something | 2/2 | 433,192 | — | all tables here |
| E63 | Does patient harm go up when leadership keeps turning over? | found a little | 2/2 | 433,192 | — | all tables here |
| E64 | Does the money keep flowing to them anyway? | found a little | 2/2 | 20,314,517 | — | all tables here |
| E65 | Were they still getting paid after losing it? | nothing there | 2/2 | 21,090,245 | — | all tables here |
| E66 | Are they still getting health grants? | nothing there | 2/2 | 20,071,207 | — | all tables here |
| E67 | Do they also have fewer doctors available? | nothing there | 2/2 | 9,735,190 | — | all tables here |
| E68 | Do they give very little free care to the poor despite huge profits? | found something | 1/1 | 6,103 | — | all tables here |
| E69 | How much grant money reaches each patient? | part done | 3/3 | 19,905,591 | — | all tables here |
| E70 | Are the worst-rated homes still getting VA contracts? | nothing there | 2/2 | 93,168,137 | — | all tables here |
| E71 | Does more payment per person mean more opioid prescribing? | found a little | 2/2 | 16,801,930 | — | all tables here |
| E72 | Is it sitting empty more than in safer counties? | nothing there | 2/2 | 26,286,521 | — | all tables here |
| E73 | Do banned contractors turn out to also be doctors? | missing a piece | 2/2 | 9,775,011 | — | all tables here |
| E74 | Is there a record of who the new owner is? | missing a piece | 2/2 | 56,821 | — | all tables here |
| E75 | Did the worst chains get big pandemic bailout money? | missing a piece | 2/2 | 14,758 | — | all tables here |

---

Rebuild with `python scripts/docket_data_check.py`.
The numbers come from the warehouse, not from the sheet.
