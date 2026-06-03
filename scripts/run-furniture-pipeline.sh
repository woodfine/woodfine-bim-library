#!/usr/bin/env bash
# Nightly BIM furniture pipeline — regenerate DXF plan-view SVGs from tokens.
#
# Invoked by foundry-bim-furniture.timer (03:00 daily).
# WorkingDirectory=/srv/foundry/clones/project-bim
#
# Steps:
#   1. Regenerate key plan IFC compositions from DTCG tokens (generate-key-plans.py)
#   2. Convert any new DXF blocks to plan-view SVG (generate-furniture-plan-svg.py)
#
# Both scripts are idempotent: existing outputs are overwritten.
# Pipeline exits with the last non-zero exit code encountered, or 0 on success.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

log() { echo "[bim-pipeline] $(date -u +%H:%M:%SZ) $*"; }
fail() { echo "[bim-pipeline] ERROR: $*" >&2; exit 1; }

log "Starting BIM furniture pipeline — ${REPO_ROOT}"

# ── Step 1: Regenerate key plan IFC files ────────────────────────────────────
log "Step 1: Generating key plan IFC compositions"
python3 "${SCRIPT_DIR}/generate-key-plans.py" \
    || fail "generate-key-plans.py failed (exit $?)"

# ── Step 2: Convert DXF → plan-view SVG ──────────────────────────────────────
log "Step 2: Converting DXF blocks to plan-view SVG"
DXF_DIR="${REPO_ROOT}/blocks/furniture"

if ! command -v python3 &>/dev/null; then
    fail "python3 not found"
fi

if python3 -c "import ezdxf" 2>/dev/null; then
    python3 "${SCRIPT_DIR}/generate-furniture-plan-svg.py" \
        --dxf-dir "${DXF_DIR}" \
        --out-dir "${DXF_DIR}" \
        || fail "generate-furniture-plan-svg.py failed (exit $?)"
else
    log "SKIP: ezdxf not installed — no DXF→SVG conversion (pip install ezdxf to enable)"
fi

log "Pipeline complete."
