"""Add config(schema='<DOMAIN>') to mart models that are missing it.

Without a custom schema, macros/generate_schema_name.sql falls back to
target.schema, so a model in models/marts/health/ lands in
LIBRARY_MARTS.DBT_CROGERS instead of LIBRARY_MARTS.HEALTH. That is why 44 stray
tables were sitting in DBT_CROGERS while the domain schemas held the rest.

The schema is derived from the model's folder, which is the convention every
already-correct mart model follows (models/marts/health/ -> schema='HEALTH').

Files are edited as bytes: several mart models contain mojibake from an earlier
bad ingest, and a utf-8 decode/encode round trip would corrupt them further.

Usage: python scripts/add_mart_schema_config.py [--apply]
"""
import argparse
import os
import re
import sys

MARTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "library-onboarding", "ripple_dbt", "models", "marts")

HAS_SCHEMA = re.compile(rb"schema\s*=\s*['\"]")
CONFIG = re.compile(rb"\{\{\s*config\((?P<args>[^)]*)\)\s*\}\}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    changed, skipped, failed = [], [], []
    for dirpath, _dirnames, filenames in os.walk(MARTS):
        domain = os.path.basename(dirpath).upper()
        if dirpath == MARTS:
            continue
        for fn in sorted(filenames):
            if not fn.endswith(".sql"):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, "rb") as fh:
                raw = fh.read()
            if HAS_SCHEMA.search(raw):
                skipped.append(f"{domain}/{fn}")
                continue
            m = CONFIG.search(raw)
            if not m:
                failed.append(f"{domain}/{fn} (no config() block found)")
                continue
            inner = m.group("args").strip()
            addition = f"schema='{domain}'".encode()
            new_args = (inner + b", " + addition) if inner else addition
            new_raw = (raw[:m.start()] + b"{{ config(" + new_args + b") }}"
                       + raw[m.end():])
            changed.append(f"{domain}/{fn}")
            if args.apply:
                with open(path, "wb") as fh:
                    fh.write(new_raw)

    for c in changed:
        print("SET  ", c)
    for f in failed:
        print("FAIL ", f)
    print(f"\n{len(changed)} models given a schema, {len(skipped)} already had one, "
          f"{len(failed)} could not be parsed")
    if not args.apply:
        print("DRY RUN -- rerun with --apply to write changes")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
