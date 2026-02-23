#!/usr/bin/env python3
"""
lint.py — Architecture-as-code linter for DataViz-for-Indian-Cities.

Encodes the project's conventions so they can be verified automatically.
Run: python3 lint.py         — report errors and warnings
     python3 lint.py --strict — exit 1 on warnings too

Rules are grouped by what they protect:
  SQL        — DuckDB query correctness and safety
  COMPONENT  — Evidence.dev component conventions
  DATA       — CSV source file integrity
  LINK       — Markdown link encoding
  META       — Page frontmatter completeness
"""

import csv
import datetime
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
PAGES_DIR = BASE / "pages"
SOURCES_DIR = BASE / "sources" / "CMP"

# ── Known acceptable exceptions ────────────────────────────────────────────────
# These suppress specific linter warnings for documented reasons.

# BRT depots that exist only in brt_extracted.csv, not in extracted.csv.
# M.Yard: main PMPML maintenance yard used as a BRT operational base in 2023.
# From April 2024 it appears as "Upper Depot" — same coordinates, renamed.
BRT_ONLY_DEPOTS = {"M.Yard"}

# Date ranges where source reports are known to be missing.
# Format: (file_label, start_inclusive, end_inclusive, note)
KNOWN_GAPS = [
    ("extracted",      "Jan 2024", "Mar 2024", "Source reports not published for Q4 FY2023-24"),
    ("extracted",      "Nov 2024", "Mar 2025", "Source reports not published for partial FY2024-25"),
    ("brt_extracted",  "Jan 2023", "Jan 2023", "BRT Jan 2023 report was not available for download"),
    ("brt_extracted",  "Jan 2024", "Mar 2024", "Source reports not published for Q4 FY2023-24"),
    ("brt_extracted",  "Nov 2024", "Mar 2025", "Source reports not published for partial FY2024-25"),
    ("ebus_extracted", "Jan 2024", "Mar 2024", "Source reports not published for Q4 FY2023-24"),
    ("ebus_extracted", "Nov 2024", "Mar 2025", "Source reports not published for partial FY2024-25"),
]

# Known data quality issues in source CSVs that have been handled in SQL/notes.
# Adding an entry here suppresses the linter check and documents the known issue.
KNOWN_DATA_ISSUES = {
    # (file, date, depot, column): explanation
    ("extracted.csv", "Dec 2023", "Pune Station", "% of Fleet Utilization(PMPML+PPP)"):
        "Source report shows 200% — formula quirk when hired fleet > PMPML own schedule count. "
        "Handled via LEAST(..., 100.0) in all SQL queries.",
    ("extracted.csv", "Dec 2023", "Nigadi", "% of Fleet Utilization(PMPML+PPP)"):
        "Source report shows 116.67% — same quirk as Pune Station. Capped in SQL.",
    ("extracted.csv", "Feb 2023", "*", "All Traffic Earning (₹)"):
        "Original tabula extraction had a column shift. Values imputed as "
        "ticket + pass + student earnings (see extract_pdfs.py).",
    ("extracted.csv", "Apr 2023", "*", "Earning per KMs in Rs.(EPK) (₹)"):
        "Source report had the all-traffic EPK value in the ticket-only EPK column position. "
        "Reported values (~₹60-75) were ~3x the correct ~₹25-38. "
        "Imputed as Passenger Earning (Sale of Ticket) / Total Eff.Km (Own+Hire).",
    ("extracted.csv", "*", "*", "Total Gross KMs (Diesel+CNG+E)"):
        "Jan 2023 shows values of 100-2,158 (should be ~1-1.5M). From Feb 2023 onward, "
        "this column appears to record only PMPML diesel gross KMs for many depots, "
        "omitting CNG and hire. Not used in any current visualisation.",
    ("ebus_extracted.csv", "Dec 2023", "Hadapsar", "passengers_per_day"):
        "Source report shows 21,071 passengers/day (double normal ~11,000). "
        "Earning, KMs, and EPK columns are internally consistent, suggesting the "
        "passenger count was entered as a monthly total instead of a daily average. "
        "Imputed as all_traffic_earning / (days_in_month × earn_per_pax_from_Oct-Nov_2023). "
        "System Total for Dec 2023 adjusted accordingly.",
    ("extracted.csv", "Jan 2023", "*", "No.of Schedules Sanctioned Per Day (PMPML + PPP)"):
        "Sanctioned and Operated columns are content-swapped for 8 depots (Balewadi, Baner, "
        "Bhekrai Nagar, Wagholi, Bhosari, Nigadi, Pimpri, Pune Station) — Sanctioned holds "
        "PMPML-only count while Operated holds full PPP+hire total. "
        "All schedule queries use GREATEST/LEAST to reconstruct correct values.",
    ("extracted.csv", "Mar 2023", "*", "No.of Schedules Sanctioned Per Day (PMPML + PPP)"):
        "Same Sanctioned/Operated column swap as Jan 2023 for the same 8 depots. "
        "All schedule queries use GREATEST/LEAST to reconstruct correct values.",
    ("extracted.csv", "Oct 2023", "Nigadi", "Gross KMs- Diesel (Own)"):
        "Reports 104,315 gross diesel km for 9 own buses (373 km/bus/day vs. typical 150-200). "
        "Appears to be a data entry error — likely hire fleet gross km entered in own-bus column. "
        "Column not used in any visualisation.",
    ("extracted.csv", "Nov 2023", "Nigadi", "Gross KMs- Diesel (Own)"):
        "Reports 81,248 gross diesel km for 5 own buses (541 km/bus/day vs. typical 150-200). "
        "Same data entry error pattern as Oct 2023. Column not used in any visualisation.",
}

# Deprecated depot name spellings that must not appear in source data or SQL.
DEPRECATED_DEPOT_NAMES = {
    "Bhekrainagar":    "Bhekrai Nagar",
    "P.Station":       "Pune Station",
    "Shewal-wadi":     "Shewalwadi",
    "Shewal- wadi":    "Shewalwadi",
    "Bhekrai\nNagar":  "Bhekrai Nagar",
    "Pune\nStation":   "Pune Station",
    "Uppar Depot":     "Upper Depot",
}

# ── Findings collector ─────────────────────────────────────────────────────────

findings = []  # [(severity, rule, file, message)]


def error(rule, file, msg):
    findings.append(("ERROR", rule, str(file), msg))


def warn(rule, file, msg):
    findings.append(("WARN", rule, str(file), msg))


# ── Rule helpers ───────────────────────────────────────────────────────────────

def extract_sql_blocks(content):
    """Return [(name, sql_text)] for each named SQL fenced block."""
    return re.findall(r"```sql\s+(\w+)\n(.*?)```", content, re.DOTALL)


def uses_pmpml_table(sql_text):
    return any(
        f"FROM {t}" in sql_text or f"JOIN {t}" in sql_text
        for t in ("extracted", "brt_extracted", "ebus_extracted")
    )


# ── Page rules ─────────────────────────────────────────────────────────────────

def check_meta(path, content):
    """META: every page needs title and description frontmatter."""
    fm = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not fm:
        error("META_FRONTMATTER", path, "Missing YAML frontmatter block")
        return
    body = fm.group(1)
    if "title:" not in body:
        error("META_FRONTMATTER", path, "Frontmatter missing 'title:'")
    if "description:" not in body:
        warn("META_FRONTMATTER", path, "Frontmatter missing 'description:'")


def check_links(path, content):
    """LINK: spaces in markdown link destinations must be %20-encoded."""
    for m in re.finditer(r"\[([^\]]+)\]\((/[^)\s]*[ ][^)]*)\)", content):
        error("LINK_ENCODING", path,
              f"Unencoded space in link path — use %%20: ({m.group(2)})")


def check_sql(path, content):
    """SQL: enforce DuckDB safety patterns used throughout this project."""
    blocks = extract_sql_blocks(content)
    if not blocks:
        return

    all_sql = "\n".join(sql for _, sql in blocks)

    # Rule: Bare CAST() without TRY_ on quoted long-name columns
    # Pattern: CAST("something with space" — not preceded by TRY_
    if re.search(r'(?<!TRY_)CAST\s*\("[^"]+\s[^"]*"\s+AS', all_sql):
        warn("SQL_TRY_CAST", path,
             "Bare CAST(\"...\") on a quoted column — use TRY_CAST to handle "
             "null/unparseable cells from tabula-extracted CSVs")

    # Rule: Fleet utilization column must be wrapped in LEAST(..., 100.0)
    # Reason: Dec 2023 has 200%/116% outliers from source report formula quirk.
    util_pattern = r'TRY_CAST\("% of Fleet Utilization\(PMPML\+PPP\)" AS DOUBLE\)'
    for m in re.finditer(util_pattern, all_sql):
        preceding = all_sql[max(0, m.start() - 7): m.start()]
        if "LEAST(" not in preceding:
            error("SQL_UTIL_CAP", path,
                  "Fleet utilization not wrapped in LEAST(..., 100.0) — "
                  "Dec 2023 Pune Station/Nigadi report >100% due to source formula quirk")

    # Rule: Date parsing must use '%b %Y' (abbreviated month) not '%B %Y' (full)
    if re.search(r"STRPTIME\(Date,\s*'%B %Y'\)", all_sql):
        error("SQL_DATE_FORMAT", path,
              "Use STRPTIME(Date, '%b %Y') with abbreviated month, not '%B %Y'")

    # Rule: PMPML table queries need NULL guard
    if uses_pmpml_table(all_sql) and "Date IS NOT NULL" not in all_sql:
        error("SQL_NULL_GUARD", path,
              "Query against PMPML table missing 'WHERE Date IS NOT NULL' — "
              "null Date rows exist and will corrupt aggregates")

    # Rule: Division without NULLIF risks division-by-zero
    if re.search(r"/\s*(?:SUM|AVG|COUNT)\s*\(", all_sql) and "NULLIF(" not in all_sql:
        warn("SQL_NULLIF", path,
             "SQL divides by an aggregate without NULLIF — add "
             "NULLIF(denominator, 0) to guard against division-by-zero")

    # Rule: Total Gross KMs column is structurally broken — never use it
    if '"Total Gross KMs (Diesel+CNG+E)"' in all_sql:
        error("SQL_GROSS_KM", path,
              '"Total Gross KMs (Diesel+CNG+E)" is structurally unreliable — '
              "it omits hire fleet and has wrong values in Jan 2023. "
              "Use \"Total Dead KMs (Diesel+CNG+E)\" (independently recorded) instead.")

    # Rule: Raw schedule columns without GREATEST/LEAST correction
    sanctioned_col = '"No.of Schedules Sanctioned Per Day (PMPML + PPP)"'
    operated_col   = '"Average No.of Schedule operated Per Day (PMPML+PPP)"'
    if (sanctioned_col in all_sql or operated_col in all_sql) and "GREATEST(" not in all_sql:
        error("SQL_SCHEDULE_SWAP", path,
              "Schedule columns used without GREATEST/LEAST correction — "
              "Jan 2023 and Mar 2023 have Sanctioned/Operated swapped for 8 depots. "
              "Wrap both columns in GREATEST(...) and LEAST(...) to reconstruct correct values. "
              "See CLAUDE.md 'Unreliable Columns' section.")

    # Rule: Deprecated depot names must not appear in SQL string literals
    for bad, good in DEPRECATED_DEPOT_NAMES.items():
        if bad in all_sql:
            error("SQL_DEPOT_NAME", path,
                  f"Deprecated depot name '{bad}' in SQL — use '{good}'")


def check_components(path, content):
    """COMPONENT: Evidence.dev component patterns."""

    # Rule: Invalid format string decimals (#,##0.1 is not a valid Excel format)
    for pat, fix in [
        (r"fmt='[^']*#,##0\.1[^']*'", "#,##0.0"),
        (r"fmt='[^']*#0\.1[^']*'",    "#0.0"),
    ]:
        if re.search(pat, content):
            error("COMPONENT_FMT", path,
                  f"Invalid format string — decimal digit count uses '0' not '1' "
                  f"(e.g. #,##0.0 for one decimal, not #,##0.1). Fix: use {fix}")

    # Rule: scaleColor= is deprecated; use colorScale=
    # (warning only — it still works but generates console noise)
    if "scaleColor=" in content:
        warn("COMPONENT_DEPRECATED", path,
             "scaleColor= is deprecated — use colorScale= (Evidence v40+)")

    # Rule: Multiple time-series charts on one page should use connectGroup
    time_charts_with_date = re.findall(
        r"<(?:LineChart|BarChart|AreaChart)\b[^>]*x=date_parsed", content, re.DOTALL
    )
    charts_with_connect = re.findall(
        r"<(?:LineChart|BarChart|AreaChart)\b[^>]*connectGroup=", content, re.DOTALL
    )
    if len(time_charts_with_date) >= 2 and len(charts_with_connect) < len(time_charts_with_date):
        warn("COMPONENT_CONNECT", path,
             f"{len(time_charts_with_date)} time-series charts but only "
             f"{len(charts_with_connect)} use connectGroup= — "
             "add connectGroup to synchronize tooltip hover across charts")

    # Rule: Pages using PMPML monthly data should annotate the two known gaps
    blocks = extract_sql_blocks(content)
    all_sql = "\n".join(sql for _, sql in blocks)
    if uses_pmpml_table(all_sql):
        has_charts = bool(re.search(r"<(?:LineChart|BarChart|AreaChart)\b", content))
        if has_charts:
            if "ReferenceArea" not in content:
                warn("COMPONENT_GAPS", path,
                     "PMPML time-series page has no ReferenceArea gap annotations — "
                     "add for Jan–Mar 2024 and Nov 2024–Mar 2025 data gaps")
            else:
                if "2024-01-01" not in content or "2024-03-31" not in content:
                    warn("COMPONENT_GAPS", path,
                         "Missing Jan–Mar 2024 gap annotation "
                         "(xMin='2024-01-01' xMax='2024-03-31')")
                if "2024-11-01" not in content or "2025-03-31" not in content:
                    warn("COMPONENT_GAPS", path,
                         "Missing Nov 2024–Mar 2025 gap annotation "
                         "(xMin='2024-11-01' xMax='2025-03-31')")


def check_sql_position(path, content):
    """SQL_POSITION: SQL blocks should live in '## Data Queries' at page bottom.

    Exception: SQL blocks whose query name is ONLY referenced by BigValue components
    (summary cards) are allowed before charts — they serve as page-header KPIs,
    not as chart data sources. Only flag if the SQL also feeds LineChart/BarChart/etc.
    """
    blocks = extract_sql_blocks(content)
    if len(blocks) <= 1:
        return  # small pages with 1 inline SQL block are fine

    dq_pos = content.find("## Data Queries")
    first_viz = re.search(
        r"<(?:LineChart|BarChart|AreaChart|DataTable|PointMap|AreaMap)\b", content
    )

    if dq_pos == -1 and first_viz:
        # Check if any SQL block precedes the first viz component
        for name, sql in blocks:
            block_pos = content.find(f"```sql {name}")
            if block_pos >= first_viz.start():
                continue
            # Check if this query is referenced by chart components (not just BigValue)
            chart_types = r"(?:LineChart|BarChart|AreaChart|DataTable|PointMap|AreaMap)"
            if re.search(rf"<{chart_types}\b[^>]*data={{['\"]?{re.escape(name)}['\"]?}}", content):
                warn("SQL_POSITION", path,
                     f"SQL block '{name}' appears before visualizations — "
                     "move all SQL to a '## Data Queries' section at page bottom "
                     "(SQL-as-citation pattern: narrative + charts first, queries last)")
                break
            # BigValue-only SQL before charts is acceptable (summary cards)


def check_component_query_refs(path, content):
    """COMPONENT_QUERY_REF: every data={query} reference must have a matching sql block.

    Missing queries produce empty/broken charts in Evidence.dev with no build error —
    the chart renders as blank and silently shows nothing.
    Orphaned queries (defined but never referenced) are a warning — likely dead code
    from a refactor, or a query that was renamed but the component wasn't updated.
    """
    defined = {name for name, _ in extract_sql_blocks(content)}
    if not defined:
        return

    # Find all data={name} references from components
    component_refs = set(re.findall(r'data=\{(\w+)\}', content))
    # Find all ${name} references in SQL composition (Evidence.dev query chaining)
    sql_composition_refs = set(re.findall(r'\$\{(\w+)\}', content))
    referenced = component_refs | sql_composition_refs

    missing = component_refs - defined
    for name in sorted(missing):
        error("COMPONENT_QUERY_REF", path,
              f"Component references data={{{name}}} but no 'sql {name}' block defined — "
              "chart will render blank. Define the query or fix the name.")

    orphaned = defined - referenced
    # Only warn about orphaned if there are actually chart components on the page
    has_components = bool(re.search(
        r"<(?:LineChart|BarChart|AreaChart|DataTable|BigValue|PointMap|AreaMap)\b", content
    ))
    if has_components:
        for name in sorted(orphaned):
            warn("COMPONENT_QUERY_REF", path,
                 f"SQL block '{name}' is defined but never referenced by any component or "
                 "query composition — dead query, or data= attribute was renamed without "
                 "updating the SQL block")


def check_component_self_close(path, content):
    """COMPONENT_SELF_CLOSE: Charts with children must use open/close tags.

    Evidence.dev uses mdsvex (Svelte). A self-closing chart tag (<Chart ... />)
    silently drops any children that follow — ReferenceArea annotations, Column
    definitions, etc. are all swallowed with no warning. Charts that need children
    must end with > and close with </ChartType>.

    Detection: look for a self-closing chart tag immediately followed (within 5 lines)
    by a ReferenceArea or Column child element.
    """
    # Match a self-closing chart tag followed IMMEDIATELY (same or next line, no blank
    # lines, no new element starts) by a ReferenceArea or Column child element.
    # The key constraint: no '<' allowed between the '/>' and the child — that would
    # mean a new sibling element started, so the Column/ReferenceArea isn't an intended
    # child of the self-closing tag.
    chart_pat = re.compile(
        r"<(?:LineChart|BarChart|AreaChart|PointMap)\b[^>]*/>"
        r"(?![ \t]*\n[ \t]*\n)"          # no blank line separator
        r"[ \t\n]*"                        # only whitespace/newlines between
        r"(?=[^<]*<(?:ReferenceArea|Column)\b)",  # lookahead: next tag is a child
        re.DOTALL,
    )
    for m in chart_pat.finditer(content):
        # Find which child tag triggered this
        after = content[m.end():m.end() + 200]
        child_m = re.search(r"<(ReferenceArea|Column)\b", after)
        child_tag = child_m.group(1) if child_m else "child"
        error("COMPONENT_SELF_CLOSE", path,
              f"Self-closing chart tag followed by <{child_tag}> child — "
              f"children are silently ignored. Change '/>' to '>' and add a closing tag.")


def check_series_color_order(path, content):
    """COMPONENT_COLOR_ORDER: When the same concept appears in multiple charts on a page,
    series order (and therefore auto-assigned colors) should be consistent.

    Evidence.dev assigns colors by series position: first series = color1, second = color2.
    In wide-format charts (y=[col1, col2]) order is explicit. In series= charts,
    order follows the first occurrence in query results (usually alphabetical after ORDER BY).

    Flag if a page uses the same data in both wide and series= formats with different orderings.
    This rule specifically checks the known fuel-type pattern (CNG/Diesel/E-Bus).
    """
    # Find wide-format fuel charts and series-format fuel charts on the same page
    wide_fuel = re.findall(
        r"y=\{\[(['\"]?(?:cng|diesel|ebus|e.bus)[^'\"]*['\"]?,\s*)+['\"]?(?:cng|diesel|ebus|e.bus)[^'\"]*['\"]?\]\}",
        content, re.IGNORECASE
    )
    series_fuel = re.search(r"series=fuel_type", content, re.IGNORECASE)

    if wide_fuel and series_fuel:
        for yval in wide_fuel:
            # The series= chart sorts alphabetically: CNG first, Diesel second
            # The wide chart should match: cng first, diesel second
            if re.search(r"diesel[^,]*,\s*['\"]?cng", yval, re.IGNORECASE):
                warn("COMPONENT_COLOR_ORDER", path,
                     "Wide-format chart has diesel before CNG, but series= chart sorts "
                     "alphabetically (CNG first). Colors will be swapped between charts. "
                     "Reorder y=[cng_..., diesel_..., ebus_...] to match.")


# ── Data file rules ────────────────────────────────────────────────────────────

def check_data_files():
    """DATA: CSV source integrity, depot name consistency, value ranges."""

    def load_csv(name):
        p = SOURCES_DIR / name
        if not p.exists():
            return None, p
        with open(p, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f)), p

    rows_ext,  p_ext  = load_csv("extracted.csv")
    rows_brt,  p_brt  = load_csv("brt_extracted.csv")
    rows_ebus, p_ebus = load_csv("ebus_extracted.csv")
    rows_dl,   p_dl   = load_csv("depot_locations.csv")

    # ── Depot name consistency ──────────────────────────────────────────────

    def depots_in(rows, col="Depot", exclude=("System Total",)):
        if rows is None:
            return set()
        return {r[col] for r in rows if r.get(col, "").strip() and r[col] not in exclude}

    ext_depots = depots_in(rows_ext)
    brt_depots = depots_in(rows_brt)
    ebus_depots = depots_in(rows_ebus)
    dl_depots   = depots_in(rows_dl, col="depot", exclude=())

    for label, depots, path in [
        ("extracted.csv",      ext_depots,  p_ext),
        ("brt_extracted.csv",  brt_depots,  p_brt),
        ("ebus_extracted.csv", ebus_depots, p_ebus),
        ("depot_locations.csv", dl_depots,  p_dl),
    ]:
        if depots is None:
            continue
        for bad in DEPRECATED_DEPOT_NAMES:
            if bad in depots:
                error("DATA_DEPOT_NAME", path,
                      f"Deprecated depot name '{bad}' — "
                      f"use '{DEPRECATED_DEPOT_NAMES[bad]}'")

    # ── depot_locations completeness ────────────────────────────────────────

    if rows_dl is not None:
        for r in rows_dl:
            if not r.get("latitude", "").strip() or not r.get("longitude", "").strip():
                error("DATA_COORDS", p_dl,
                      f"Depot '{r['depot']}' missing latitude/longitude")

    # All depots in extracted.csv must have coordinates
    if ext_depots and dl_depots:
        missing = ext_depots - dl_depots
        if missing:
            for d in sorted(missing):
                error("DATA_COORDS", p_dl,
                      f"Depot '{d}' in extracted.csv has no entry in depot_locations.csv")

    # BRT-only depots (not in extracted.csv) should either be in depot_locations
    # or be listed in BRT_ONLY_DEPOTS as a known exception
    if brt_depots and ext_depots:
        brt_exclusive = brt_depots - ext_depots - BRT_ONLY_DEPOTS
        for d in sorted(brt_exclusive):
            warn("DATA_DEPOT_BRT_ONLY", p_brt,
                 f"BRT depot '{d}' not in extracted.csv or BRT_ONLY_DEPOTS allowlist — "
                 "add coordinates to depot_locations.csv or document the exception")

    # BRT_ONLY_DEPOTS should also be in depot_locations (for completeness)
    if dl_depots:
        for d in sorted(BRT_ONLY_DEPOTS):
            if d not in dl_depots:
                warn("DATA_COORDS", p_dl,
                     f"BRT-only depot '{d}' ({BRT_ONLY_DEPOTS}) has no entry in depot_locations.csv — "
                     "add coordinates even if this depot only appears in BRT data")

    # ── Value range checks ──────────────────────────────────────────────────

    if rows_ext is not None:
        for r in rows_ext:
            date, depot = r.get("Date", ""), r.get("Depot", "")
            key = ("extracted.csv", date, depot, "% of Fleet Utilization(PMPML+PPP)")
            key_wild = ("extracted.csv", date, "*", "% of Fleet Utilization(PMPML+PPP)")
            v = r.get("% of Fleet Utilization(PMPML+PPP)", "").strip()
            if v:
                try:
                    fv = float(v)
                    if fv > 110 and key not in KNOWN_DATA_ISSUES and key_wild not in KNOWN_DATA_ISSUES:
                        warn("DATA_UTIL_OUTLIER", p_ext,
                             f"{date} / {depot}: fleet utilization = {fv}% — "
                             "add to KNOWN_DATA_ISSUES if this is expected, "
                             "or fix in source CSV")
                except ValueError:
                    pass

        # Feb 2023 All Traffic Earning sanity check
        feb = [r for r in rows_ext if r.get("Date") == "Feb 2023"]
        if feb:
            total = sum(
                float(r.get("All Traffic Earning (₹)", 0) or 0)
                for r in feb
                if r.get("All Traffic Earning (₹)", "").strip()
            )
            if total < 100_000_000:
                key = ("extracted.csv", "Feb 2023", "*", "All Traffic Earning (₹)")
                if key not in KNOWN_DATA_ISSUES:
                    error("DATA_EARNINGS", p_ext,
                          f"Feb 2023 All Traffic Earning total = ₹{total:,.0f} — "
                          "suspiciously low (expected ~₹450M). "
                          "Add to KNOWN_DATA_ISSUES if this has been addressed.")

    # ── Date format consistency ─────────────────────────────────────────────

    for label, rows, path in [
        ("extracted",      rows_ext,  p_ext),
        ("brt_extracted",  rows_brt,  p_brt),
        ("ebus_extracted", rows_ebus, p_ebus),
    ]:
        if rows is None:
            continue
        for r in rows:
            d = r.get("Date", "").strip()
            if d:
                try:
                    datetime.datetime.strptime(d, "%b %Y")
                except ValueError:
                    error("DATA_DATE_FMT", path,
                          f"Non-standard date value '{d}' — expected 'Mon YYYY' format "
                          "(e.g. 'Jan 2023'). Fix in extract_pdfs.py parse_date().")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    strict = "--strict" in sys.argv

    md_files = sorted(PAGES_DIR.rglob("*.md"))
    for md_path in md_files:
        content = md_path.read_text(encoding="utf-8")
        rel = md_path.relative_to(BASE)
        check_meta(rel, content)
        check_links(rel, content)
        check_sql(rel, content)
        check_components(rel, content)
        check_sql_position(rel, content)
        check_component_query_refs(rel, content)
        check_component_self_close(rel, content)
        check_series_color_order(rel, content)

    check_data_files()

    # ── Report ──────────────────────────────────────────────────────────────
    errors   = [f for f in findings if f[0] == "ERROR"]
    warnings = [f for f in findings if f[0] == "WARN"]

    csv_count = len(list(SOURCES_DIR.glob("*.csv")))
    print(f"\n{'═' * 68}")
    print(f"  DataViz Linter  ·  {len(md_files)} pages  ·  {csv_count} data files")
    print(f"{'═' * 68}\n")

    if not findings:
        print("  ✓  All checks passed\n")
    else:
        by_file = {}
        for sev, rule, file, msg in findings:
            by_file.setdefault(file, []).append((sev, rule, msg))

        for file in sorted(by_file):
            rel_file = file.replace(str(BASE) + "/", "")
            print(f"  {rel_file}")
            for sev, rule, msg in by_file[file]:
                icon = "✗" if sev == "ERROR" else "⚠"
                # Wrap long messages
                prefix = f"    {icon} [{rule}] "
                wrap = 68 - len(prefix)
                words = msg.split()
                lines, cur = [], []
                for w in words:
                    if sum(len(x) + 1 for x in cur) + len(w) > wrap and cur:
                        lines.append(" ".join(cur))
                        cur = [w]
                    else:
                        cur.append(w)
                if cur:
                    lines.append(" ".join(cur))
                print(prefix + lines[0])
                for l in lines[1:]:
                    print(" " * len(prefix) + l)
            print()

    print(f"{'─' * 68}")
    status = "FAIL" if errors or (strict and warnings) else "PASS"
    print(f"  {status}  ·  {len(errors)} error(s)  ·  {len(warnings)} warning(s)")
    if strict and warnings and not errors:
        print("  (--strict: warnings treated as errors)")
    print(f"{'─' * 68}\n")

    sys.exit(1 if (errors or (strict and warnings)) else 0)


if __name__ == "__main__":
    main()
