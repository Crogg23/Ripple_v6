#!/usr/bin/env bash
cd "$(dirname "$0")/.."
streamlit run playground/app.py --server.port 8502 --server.address 127.0.0.1 --browser.gatherUsageStats false
