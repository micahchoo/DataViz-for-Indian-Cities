# STATE.md — Narrative Enhancement

## Phase: SYNC | Round: 3 — COMPLETE

## Completed

- [x] **1f** Ridership_and_Fares.md — fare revision note converted to `> blockquote` with framing sentence
- [x] **1a** index.md — added 3-sentence thesis (9x vehicle growth, ridership decline, the divergence)
- [x] **1b** index.md — added reading-guide note (narrative vs dashboard pages) before link list
- [x] **1c** PCMT_before_PMPML.md — removed artifact opener, added story-forward sentence
- [x] **1d** PCMT_before_PMPML.md — converted merger bullet list to prose with depot link
- [x] **1e** PCMT_before_PMPML.md — renamed "Gaps in Understanding" → "Data Limitations", declarative prose
- [x] **2a** City_Context.md — added "## Twenty Years Later" section with verified numbers; expanded See Also
- [x] **1g** Registered_Vehicles_2000_2018.md — added prose to Overall, Two Wheelers, Personal Vehicles, Commercial Vehicles sections
- [x] **1h** Registered_Vehicles_2000_2018.md — title rewritten to "A City on Two Wheels..."
- [x] **1i** Fleet_Composition_Trends.md — title rewritten; new intro links to Registered_Vehicles; removed "About This Data" section
- [x] **1j** Depot_Performance.md — dropped numbered prefixes from all 6 section headings
- [x] **1l** Depot_Performance.md — "## Reading the System" written with specific depot names, data-backed numbers, and three-cluster framing (owned-fleet / hired-fleet / dense-urban)
- [x] **1k** Depot_Performance.md — geographic parentheticals included inline in the synthesis (Bhosari: industrial northeast MIDC; Balewadi: northwest highway corridor; Maan: far-east outskirts; Swargate: old Pune city terminus)
- [x] **2b** PT/index.md — added "missing decade" bridge paragraph after the link list
- [x] **2c** Depotwise.md — added differentiation note at top linking to Depot_Performance
- [x] **2c** Depot_Performance.md — added differentiation note at top linking to Depotwise
- [x] **2d** Depot_Performance.md — added BRT and EBus See Also links
- [x] **2d** Financial_Performance.md — added BRT and EBus See Also links
- [x] **3a** PCMC/index.md — added data timeline paragraph below Data Coverage table
- [x] **R**  lint.py — added ARTIFACT_OPENER rule (warns on artifact-forward openers)
- [x] **R**  lint.py — added CONTENT_IFELSE rule (warns on conditional views without prose)
- [x] **R3a** Fleet_Composition_Trends.md — fixed YAML parse error (unquoted colon in description)
- [x] **R3b** PCMT_before_PMPML.md — fixed YAML parse error (unquoted colon in description)
- [x] **R3c** COVID_Era.md — moved prose before charts in "Daily Ridership by Depot" and "Own vs. Hired Buses On Road" sections
- [x] **R**  lint.py — added META_YAML_QUOTE rule (warns on unquoted title/description values containing colons)

## In Progress

None.

## Gaps / TODO(loop)

None. All items resolved.

## Delta This Round

- **Round 1+2 (11 files edited)**: index.md, City_Context.md, Registered_Vehicles_2000_2018.md,
  Fleet_Composition_Trends.md, PCMC/index.md, Public Transport/PCMT_before_PMPML.md,
  Public Transport/Ridership_and_Fares.md, Public Transport/Depot_Performance.md,
  Public Transport/Depotwise.md, Public Transport/Financial_Performance.md,
  Public Transport/index.md
- **Round 1+2 (1 file edited)**: lint.py (+2 new rules: ARTIFACT_OPENER, CONTENT_IFELSE)
- **Round 3 (3 files edited)**: Fleet_Composition_Trends.md (YAML fix), PCMT_before_PMPML.md (YAML fix),
  Public Transport/COVID_Era.md (prose ordering in 2 sections)
- **Round 3 (1 file edited)**: lint.py (+1 new rule: META_YAML_QUOTE)

## Exit Criteria

- [x] lint --strict: 0 errors, 0 warnings
- [x] All 10 implementation steps completed (+ Round 3 fixes)
- [x] No doc in pages/ claims a number not in Verified Data table
- [x] 1l Round 2: specific depot names in "Reading the System" — written from direct CSV queries
- [x] Round 3: prose-before-chart ordering in COVID_Era.md
- [x] Round 3: META_YAML_QUOTE linter rule prevents recurrence of YAML colon parse errors
