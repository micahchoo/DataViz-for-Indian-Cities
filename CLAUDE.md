# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Evidence.dev static site for urban mobility data visualization focused on Pimpri-Chinchwad (PCMC), India. CSV data flows through embedded DuckDB SQL queries in markdown pages into chart/map/table components.

## Commands

- `npm run dev` — Start dev server (opens browser)
- `npm run build` — Static build to `./build/DataViz-for-Indian-Cities/`
- `npm run sources` — Validate data source connections (run after adding any new CSV)
- `npm run lint` — Report errors and warnings
- `npm run lint:strict` — Exit 1 on warnings (equivalent to `python3 lint.py --strict`)
- `npm run typecheck` — mypy type-check on lint.py (`--check-untyped-defs`)
- `npm run check` — Full quality gate: lint:strict + typecheck (run before committing)

## Architecture

**Data pipeline:** CSV files in `sources/CMP/` → auto-discovered as DuckDB tables → SQL queries in markdown → Evidence components render results.

**Key data files:**
- `extracted.csv` — PMPML monthly depot reports (178+ columns, Jan 2023–Jun 2025 with gaps)
- `Vehicle_Registrations_by_Type_and_Year.csv` — Annual RTO data 2000–2018
- `Road_Accident_Statistics.csv` — Accident data 2000–2007
- `Pimpri_Chinchwad_Traffic_at_Locations*.csv` — Traffic surveys (2008, 2021)
- `pcmc.csv` — Ward/zone boundaries
- `depot_locations.csv` — Bus depot coordinates (for PointMap)

**Static assets:** `static/` contains `pcmcg.geojson` (ward map boundaries).

**Deployment base path:** `/DataViz-for-Indian-Cities` (set in `evidence.config.yaml`).

## Page Conventions

Pages are markdown files in `pages/`. Routing follows the filesystem. Frontmatter uses `title` and `description`:

```yaml
---
title: Page Title
description: One-line summary
---
```

Other valid frontmatter: `sidebar` (show/hide/never), `sidebar_position`, `full_width`.

## SQL Conventions (DuckDB dialect)

**Numeric columns from CSVs must be cast safely:**
```sql
TRY_CAST("Column Name With Spaces (₹)" AS DOUBLE)
```

**Date parsing for month-year strings** (e.g., "Jan 2023"):
```sql
STRPTIME(Date, '%b %Y') as date_parsed
```

**Year extraction from fiscal year format** (e.g., "2000-2001"):
```sql
SPLIT_PART(Year, '-', 1) as display_year
```

**Standard filter for PMPML depot data:**
```sql
WHERE Date IS NOT NULL AND Depot IS NOT NULL
```

**Weighted averages** (don't use simple AVG for system-wide rates — weight by fleet size or KMs):
```sql
ROUND(
    SUM(TRY_CAST("metric" AS DOUBLE) * TRY_CAST("weight" AS DOUBLE)) /
    NULLIF(SUM(TRY_CAST("weight" AS DOUBLE)), 0)
, 1) as weighted_metric
```

## Component Patterns

SQL queries are named in fenced code blocks and referenced by components:

````markdown
```sql query_name
SELECT ... FROM table_name
```

<LineChart data={query_name} x=date_parsed y=metric_column />
````

Common components: `LineChart`, `BarChart`, `AreaChart`, `DataTable`, `BigValue`, `PointMap`, `AreaMap`, `Dropdown`, `ButtonGroup`.

**Format strings** use Excel-style syntax: `fmt='#,##0'`, `fmt='"₹"#,##0.00" Cr"'`, `fmt='#0.0"%"'`.

**PointMap basemap pattern** (matches existing traffic pages):
```svelte
basemap={`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`}
```

## Critical: Link Encoding

Spaces in markdown link paths **must** be URL-encoded as `%20`. CommonMark (used by Evidence's mdsvex parser) does not support unescaped spaces in link destinations:

```markdown
<!-- Correct -->
[Link Text](/PCMC/Public%20Transport/Depotwise)

<!-- Broken — space truncates the URL -->
[Link Text](/PCMC/Public Transport/Depotwise)
```

## Column Name Reference (extracted.csv)

Column names contain spaces, periods, parentheses, and ₹ symbols. Always quote them in SQL. Key groups:

- **Fleet:** `"Total Vehicles Per Day"`, `"% of Fleet Utilization(PMPML+PPP)"`, `"Avg. Vehicles On Road- PMPML Per Day (OWN)"`, `"On Road PPP Vehicles per day"`, `"On Road Hire Vehicles Per Day"`
- **KMs:** `"Total Eff.Km (Own+Hire)"`, `"Effective Km Per Bus Per day"`, `"Total Dead KMs (Diesel+CNG+E)"`
- **Revenue:** `"All Traffic Earning (₹)"`, `"Passenger Earning (Sale of Ticket)(₹)"`, `"Earning per KMs in Rs.(EPK) (₹)"`, `"Earning Per Vehicle Per day in Rs."`
- **Passes:** `"One Day Passes ₹ 10 (Punyadasham)"` through `"One Day Passes ₹ 120 (All Route)"`, `"Monthly Passes ₹ 500 (Sr.Citizens)"` through `"Monthly Passes ₹ 2700 (All Route)"`
- **Safety:** `"No.of Accidents (PMPML) 1. Fatal"` through `"No.of Accidents (PMPML) Total"`, `"Rate of Accidents per 1 Lakh KMs (PMPML)"`
- **Schedules:** `"No.of Schedules Sanctioned Per Day (PMPML + PPP)"`, `"Average No.of Schedule operated Per Day (PMPML+PPP)"`

## Unreliable Columns — Never Use in SQL

**`"Total Gross KMs (Diesel+CNG+E)"`** — structurally broken across all months. It only covers PMPML own buses (not hire fleet), so it is always less than `"Total Eff.Km (Own+Hire)"` for hire-heavy depots, violating the basic constraint Gross ≥ Effective. January 2023 values are in the hundreds (should be ~1M). Use `"Total Dead KMs (Diesel+CNG+E)"` instead (independently recorded from sub-components and reliable).

**Schedule columns require defensive SQL** — Jan 2023 and Mar 2023 have the Sanctioned/Operated columns swapped for 8 depots (Balewadi, Baner, Bhekrai Nagar, Wagholi, Bhosari, Nigadi, Pimpri, Pune Station). Always use `GREATEST(Sanctioned, Operated)` as the true sanctioned figure:

```sql
GREATEST(
    COALESCE(TRY_CAST("No.of Schedules Sanctioned Per Day (PMPML + PPP)" AS DOUBLE), 0),
    COALESCE(TRY_CAST("Average No.of Schedule operated Per Day (PMPML+PPP)" AS DOUBLE), 0)
) as true_sanctioned,
LEAST(
    COALESCE(TRY_CAST("No.of Schedules Sanctioned Per Day (PMPML + PPP)" AS DOUBLE), 0),
    COALESCE(TRY_CAST("Average No.of Schedule operated Per Day (PMPML+PPP)" AS DOUBLE), 0)
) as true_operated
```
