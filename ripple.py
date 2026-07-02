#!/usr/bin/env python3
"""Convenience shim so `python ripple.py <verb>` works from the repo root
(identical to `python -m ripple <verb>`)."""
import sys
from ripple.__main__ import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
