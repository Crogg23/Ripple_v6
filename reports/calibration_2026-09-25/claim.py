"""Claim the next unclaimed search batch, so every chat can paste the same prompt.

Creating batches/batch_NN.claimed is atomic: two chats can't claim the same batch.
Prints the batch number and its story IDs, or "none left".
"""
import os
from pathlib import Path

HERE = Path(__file__).parent / "batches"
for f in sorted(HERE.glob("batch_*.txt")):
    try:
        os.close(os.open(f.with_suffix(".claimed"), os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        continue
    print(f.stem)
    print(f.read_text(encoding="utf-8").strip())
    break
else:
    print("none left")
