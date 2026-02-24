# STATE.md — Bug-Fix Round

## Phase: SYNC | Round: 1 — COMPLETE

## Completed

- [x] **City_Context.md** — Binder error: removed `"Data Source \nImage"` column reference from `urban_sprawl` SQL and DataTable (column name with literal `\n` not queryable in DuckDB SQL identifiers)
- [x] **City_Context.md** — Added `xFmt='####'` to all 4 charts using numeric `census_year` / `Year` x-axes (was rendering "1,951", "2,021" etc. with thousand-separator)
- [x] **BRT_Corridors.md** — Fixed PointMap: `lon=mid_lng` → `long=mid_lng` (Evidence PointMap prop is `long=`, not `lon=`)
- [x] **Road_Accident_Statistics.md** — Added `xFmt='####'` to all 4 charts with integer `Year` x-axis
- [x] **app.css** — Added sidebar active-page CSS: `aside a.text-primary` gets `font-weight:600` + left accent bar via `::before` pseudo-element
- [x] **lint --strict** — 0 errors, 0 warnings ✓

## In Progress

None.

## Gaps / TODO(loop)

- **Visualization affordances**: User flagged that Evidence.dev's full component set is underused. Candidates for future rounds:
  - `ReferenceLine` on fleet utilization charts (target: 80%, norm staff ratio: 9.0)
  - `calendarHeatmap` for PMPML monthly ridership patterns
  - `BubbleChart` for depot comparison (fleet size × utilization × revenue/km)
  - `Annotation` on population chart to mark 2008 CMP planning baseline year
  - `BigValue comparison=` on overview BigValues for period-over-period deltas
  - `contentType=sparkline` in Depotwise DataTable

## Key Technical Notes

- `SPLIT_PART(Year, '-', 1)` produces a STRING year — no comma formatting issue
- Integer year columns (CSV: `Year` header, no split) are inferred as INT by DuckDB — use `xFmt='####'` on all charts
- Evidence PointMap: prop is `long=` (not `lon=`)
- DuckDB SQL: column names with literal `\n` in header are unreachable via double-quoted identifiers — rename or exclude

## Exit Criteria

- [x] lint --strict: 0 errors, 0 warnings
- [x] Binder error resolved (urban_sprawl)
- [x] PointMap renders (BRT_Corridors)
- [x] Year x-axes display without commas (City_Context, Road_Accident_Statistics)
- [x] Sidebar active state visually distinct
