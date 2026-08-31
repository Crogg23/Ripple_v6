#!/usr/bin/env bash
# Ripple — The Reading Room. Local only: no deploy, no auth layer, no exposure.
# Port 8890 (the control panel owns 8899).
set -euo pipefail
cd "$(dirname "$0")/.."
exec streamlit run reading_room/app.py \
  --server.port "${READING_ROOM_PORT:-8890}" \
  --server.address 127.0.0.1 \
  --browser.gatherUsageStats false
