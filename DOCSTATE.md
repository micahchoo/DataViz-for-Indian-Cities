# DOCSTATE.md — Documentation Status

## Round: 1 (2026-02-24) — COMPLETE

### Changes made this round

- **README.md** — Rewrote from scratch. Was the default Evidence template README (100% wrong for this project). Now covers: what the project is, run locally, build, lint, data sources table, site structure, adding a page, DepotWise pipeline, deployment.
- **CLAUDE.md** — Added `npm run lint` and `npm run lint:strict` to the Commands section (were missing entirely).
- **MEMORY.md** — Fixed `npm run lint --strict` → `npm run lint:strict` (invalid npm syntax, two places).
- **Drafts/DepotWise/yaml_config_guide.md** — Added "design proposal, not implemented" warning at top.
- **Drafts/DepotWise/PIPELINE.md** — Created extraction runbook: tabula → pmpml_csv_cleaner.py → ODS → extracted.csv → npm run sources. Includes current state table (Oct–Dec 2025 need ODS step).

### Current status

| Doc | Status | Notes |
|-----|--------|-------|
| `README.md` | ✅ Accurate | Covers all key workflows |
| `CLAUDE.md` | ✅ Accurate | Commands section complete; linter rules section is comprehensive |
| `STATE.md` | ⚠️ Stale | All items completed (bug-fix round, prior session). No active work tracked. Keep as historical record or delete. |
| `Drafts/DepotWise/yaml_config_guide.md` | ⚠️ Aspirational | Describes a YAML-based refactoring of `pmpml_csv_cleaner.py` that is not implemented. Following its instructions will not produce the described result. Marked as aspirational; add a header note before it misleads anyone. |
| `Drafts/DepotWise/data_structure_guide.md` | ✅ Accurate | Correct reference for tabula CSV column layout and depot list |
| `Drafts/DepotWise/Raw vs Derivable.md` | ✅ Accurate | Correct taxonomy of 32 raw vs 98+ derived PMPML metrics |
| `.github/workflows/deploy.yml` | ✅ Accurate | CI builds correctly (node 22, sources + build) |

### Gaps for next round

1. **CI does not run lint** — `deploy.yml` only runs `sources + build`. Consider adding `npm run lint:strict` before the build step to catch regressions before they ship. (Low priority — lint passes reliably at 0 errors/warnings.)
2. **PIPELINE.md tabula command** — The exact tabula CLI invocation is not verified against the installed version. Walk the tabula step with a real PDF to confirm the command flags.

### Zero-gap exit criteria

- [x] `yaml_config_guide.md` has a "this is aspirational" header ✅
- [x] DepotWise extraction has a runnable checklist doc ✅ (`PIPELINE.md`)
- [x] README describes the actual project, not the Evidence template ✅
- [x] CLAUDE.md commands section includes lint ✅
- [ ] PIPELINE.md tabula command verified against real PDF
