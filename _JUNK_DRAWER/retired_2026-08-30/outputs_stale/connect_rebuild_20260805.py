"""2026-08-05 ingestion-sweep connect rebuild driver.

Runs the standard sequence (fingerprint -> discover -> spine -> explore) with
resume-mode fingerprinting: only tables absent from the fmt-2 cache are scanned
(tonight's ~160 new landings), plus INT_UK_COMPANIES_HOUSE evicted by hand so the
new COMPANY_NO key is picked up on the one pre-existing table that carries it.
Progress + errors stream to outputs/connect_rebuild_20260805.log (utf-8).
"""
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

LOG = REPO / "outputs" / "connect_rebuild_20260805.log"


class Tee:
    def __init__(self, stream, path):
        self.stream = stream
        self.fh = open(path, "a", encoding="utf-8", buffering=1)

    def write(self, s):
        self.stream.write(s)
        self.fh.write(s)

    def flush(self):
        self.stream.flush()
        self.fh.flush()


sys.stdout = Tee(sys.stdout, LOG)
sys.stderr = Tee(sys.stderr, LOG)


def stamp(msg):
    print(f"[{time.strftime('%H:%M:%S')}] ===== {msg} =====")


try:
    from connect import fingerprint as fp

    # Evict the one pre-existing table whose cached fingerprint predates COMPANY_NO.
    if fp.OUT.exists():
        data = json.loads(fp.OUT.read_text())
        if data.pop("INT_UK_COMPANIES_HOUSE", None) is not None:
            fp.OUT.write_text(json.dumps(data))
            stamp("evicted INT_UK_COMPANIES_HOUSE from fingerprint cache")

    stamp("fingerprint (resume)")
    fp.run(resume=True)

    stamp("discover")
    from connect import discover
    discover.run()

    stamp("spine")
    from connect import spine
    spine.run()

    stamp("explore")
    from connect import explore
    explore.render()

    stamp("DONE OK")
except Exception:
    import traceback
    traceback.print_exc()
    stamp("FAILED")
    raise
