#!/usr/bin/env bash
# Recrea data/tickets.db con los 40 tickets en estado pendiente.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/seed.py
