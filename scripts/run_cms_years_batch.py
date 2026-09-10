"""Run the 48 CMS year-series specs one at a time, small families first.

Each spec is its own subprocess so one failure never stops the batch. The loader
skips specs already landed, so a rerun resumes where it stopped.
Log: .scratch/cms_years/batch.log   Summary: .scratch/cms_years/batch_summary.csv

    python scripts/run_cms_years_batch.py                        # all four families
    python scripts/run_cms_years_batch.py PARTB_PROVIDER,PARTD_PRESCRIBER   # small ones only
Big families go through scripts/cms_years_fast_load.py (PUT + COPY), not here.
"""
from __future__ import annotations
import csv, datetime as dt, subprocess, sys, time
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
import sprint_cms_years_specs as S  # noqa: E402

ORDER = ["PARTB_PROVIDER", "PARTD_PRESCRIBER", "PARTB_PROVIDER_SERVICE", "PARTD_PRESCRIBER_DRUG"]
OUT = _REPO / ".scratch" / "cms_years"
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "batch.log"
SUM = OUT / "batch_summary.csv"

def log(msg: str) -> None:
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def main() -> int:
    fams = sys.argv[1].split(",") if len(sys.argv) > 1 else ORDER
    sids = [f"FED_CMS_{fam}_DY{y}" for fam in fams for y in S._YEARS]
    new = not SUM.exists()
    with open(SUM, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["source_id", "status", "rows", "minutes", "finished_at"])
    log(f"batch start: {len(sids)} specs")
    for sid in sids:
        t0 = time.time()
        log(f"--> {sid}")
        p = subprocess.run([sys.executable, str(_REPO / "scripts" / "bridge_fuel_load.py"),
                            "--spec", sid, "--run"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", cwd=str(_REPO))
        tail = (p.stdout or "")[-4000:]
        (OUT / f"{sid}.log").write_text((p.stdout or "") + "\n--- stderr ---\n" + (p.stderr or ""), encoding="utf-8")
        mins = round((time.time() - t0) / 60, 1)
        if "already landed" in tail:
            status, rows = "skip", ""
        elif "LOADED" in tail and p.returncode == 0:
            status = "success"
            rows = next((ln.split("LOADED")[1].split("rows")[0].strip() for ln in tail.splitlines() if "LOADED" in ln), "")
        else:
            status, rows = f"FAILED rc={p.returncode}", ""
        log(f"<-- {sid}  {status}  rows={rows}  {mins} min")
        with open(SUM, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([sid, status, rows, mins, dt.datetime.now().isoformat(timespec="seconds")])
    log("batch done")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
