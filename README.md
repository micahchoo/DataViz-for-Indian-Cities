# DataViz for Indian Cities — PCMC Urban Mobility

A static data visualization site built with [Evidence.dev](https://evidence.dev) for Pimpri-Chinchwad (PCMC/PMRDA region), Maharashtra, India. Covers public transport performance, traffic surveys, vehicle registrations, and financial data for PMPML (Pimpri-Chinchwad Municipal Transport).

**Live site:** `https://<org>.github.io/DataViz-for-Indian-Cities/`

---

## Run locally

```bash
npm install
npm run sources   # discovers CSV data files as DuckDB tables
npm run dev       # starts dev server at localhost:3000
```

The dev server opens `/` automatically. Data queries run in-browser via DuckDB-WASM.

## Build for production

```bash
npm run sources
npm run build     # outputs to ./build/DataViz-for-Indian-Cities/
```

## Lint before committing

```bash
npm run lint          # report errors and warnings
npm run lint:strict   # exit 1 on warnings — run before committing
```

The linter (`lint.py`) enforces SQL safety patterns, component conventions, chart affordances, and data integrity rules for the PMPML datasets. See `CLAUDE.md` for a full rule list.

---

## Data sources

All CSV files live in `sources/CMP/`. Evidence auto-discovers them as DuckDB tables (by filename, without extension). Run `npm run sources` after adding any new CSV — Evidence doesn't hot-reload new files.

| File | What it contains |
|------|-----------------|
| `extracted.csv` | PMPML monthly depot reports, 178+ columns, Jan 2023–Jun 2025 (with gaps) |
| `brt_extracted.csv` | BRT service stats, Feb 2023–Dec 2025 |
| `ebus_extracted.csv` | E-Bus stats, Jan 2023–Dec 2025 |
| `PMPML_Financial_PnL.csv` | Annual P&L FY2017-18 to FY2024-25 (₹ lakhs) |
| `PMPML_Balance_Sheet.csv` | Balance sheet FY2017-18 to FY2024-25 (₹ lakhs) |
| `Annual_Statistics_2023_2025.csv` | Yearly summary stats FY2023-24 and FY2024-25 |
| `depot_locations.csv` | Bus depot lat/long coordinates |
| `Vehicle_Registrations_by_Type_and_Year.csv` | PCMC RTO data 2000–2018 |
| `pune_vehicle_registrations.csv` | Pune + PCMC registrations 2000–2018 |
| `Road_Accident_Statistics.csv` | Accident data 2000–2007 |
| `Pimpri_Chinchwad_Traffic_at_Locations*.csv` | Traffic surveys 2008 and 2021 |
| `pcmc.csv` | Ward/zone boundaries |

Static assets: `static/pcmcg.geojson` (ward map boundaries for AreaMap).

---

## Site structure (21 pages)

```
pages/
├── index.md                          # Entry point
└── PCMC/
    ├── index.md                      # City overview
    ├── City_Context.md               # Population, land use, transport projections
    ├── Fleet_Composition_Trends.md   # Vehicle type trends
    ├── Registered_Vehicles_2000_2018.md
    ├── Road_Accident_Statistics.md
    ├── Pune_PCMC_Comparison.md
    ├── Public Transport/
    │   ├── index.md
    │   ├── Depotwise.md              # Full monthly depot dashboard
    │   ├── Depot_Performance.md      # Interactive depot selector
    │   ├── Ridership_and_Fares.md
    │   ├── Financial_Performance.md  # P&L + balance sheet
    │   ├── BRT.md
    │   ├── BRT_Corridors.md
    │   ├── EBus.md
    │   ├── Annual_Statistics.md
    │   ├── COVID_Era.md
    │   └── PCMT_before_PMPML.md
    └── Traffic/
        ├── index.md
        ├── Pimpri_Chinchwad_Traffic_at_Locations.md   # 2008 survey
        └── Pimpri_Chinchwad_Traffic_at_Locations_2021.md
```

---

## Adding a page

1. Create a `.md` file under `pages/` at the path you want as the URL.
2. Add frontmatter:
   ```yaml
   ---
   title: Page Title
   description: One-line summary (20–160 chars)
   ---
   ```
3. Write SQL in named fenced code blocks — queries become DuckDB table references:
   ````markdown
   ```sql my_query
   SELECT * FROM extracted WHERE Date IS NOT NULL
   ```
   <LineChart data={my_query} x=date_parsed y=metric title="Chart Title" yAxisTitle="Unit" />
   ````
4. Spaces in link paths must be URL-encoded: `/Public%20Transport/Depotwise` not `/Public Transport/Depotwise`.
5. Run `npm run lint:strict` — it will catch missing titles, broken refs, unannotated data gaps, and SQL safety issues.

See `CLAUDE.md` for full SQL conventions, component patterns, and column name reference.

---

## Data pipeline (DepotWise extraction)

The monthly PMPML depot PDFs follow a multi-step process:

```
PDFs → tabula (Java) → tabula-DepotWise Month Year.csv
     → pmpml_csv_cleaner.py → cleaned output
     → manual consolidation in Manually Consolidated.ods
     → extracted.csv
```

Working files are in `Drafts/PMPML Report Downloads/DepotWise/`. BRT and E-Bus PDFs use a simpler pipeline (`extract_pdfs.py` via pdfplumber).

PDFs for Oct–Dec 2025 are staged in `DepotWise/PDFs/` awaiting tabula extraction.

---

## Deployment

GitHub Actions (`.github/workflows/deploy.yml`) deploys to GitHub Pages on push to `master`:
- Node 22, `npm run sources && npm run build`
- Output path: `build/DataViz-for-Indian-Cities/` → deployed at `/DataViz-for-Indian-Cities`
