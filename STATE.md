# STATE.md — Balance Sheet Extension

## Phase: SYNC | Round: 1 — COMPLETE

## Completed

- [x] Renamed all 28 unorganized PDFs to human-readable names (TRANSCRIPTION.md created as guide)
- [x] User manually transcribed 6 years of balance sheet data (FY17-18 to FY22-23)
- [x] `PMPML_Balance_Sheet.csv` extended from 2 years to 8 years (FY17-18 → FY24-25), 9 items each
- [x] `Financial_Performance.md` — added `## Balance Sheet: Eight-Year Trends` section with LineChart
- [x] `Financial_Performance.md` — updated intro note on data quality (structural break documented)
- [x] `Financial_Performance.md` — updated footnote to reflect 8-year balance sheet extraction methods
- [x] `lint.py` — added DATA_BS rule (checks 9 items × 8 year columns)
- [x] `npm run sources` — PMPML_Balance_Sheet re-registered, 9 rows ✓
- [x] lint --strict: 0 errors, 0 warnings ✓

## In Progress

None.

## Gaps / TODO(loop)

None.

## Key Data Notes

- FY21-22 introduced Ind-AS reclassification: ~₹40 Cr moved from current to non-current assets
- FY17-21 figures are as-reported (original) from each year's own balance sheet
- FY22-23 doc shows minor restatement of FY21-22 Other Non-Current Assets (4,588 vs 4,285 — ~304 lakh diff)
- Short-term borrowings: zero through FY19-20, first appear FY20-21 (₹3 Cr), grow to ₹34 Cr by FY24-25
- PPE peak: FY19-20 at ₹214 Cr (fleet/depot investment), declined every year since to ₹33 Cr by FY24-25
- Cash peak: FY19-20 at ₹93 Cr, nadir FY22-23 at ₹9.9 Cr, partial recovery since

## Exit Criteria

- [x] lint --strict: 0 errors, 0 warnings
- [x] PMPML_Balance_Sheet.csv has 8 year columns + 9 items
- [x] Financial_Performance.md has 8-year trend chart
- [x] DATA_BS linter rule enforces schema going forward
