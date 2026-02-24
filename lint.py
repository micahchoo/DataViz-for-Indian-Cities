#!/usr/bin/env python3
"""
lint.py — Architecture-as-code linter for DataViz-for-Indian-Cities.

Encodes the project's conventions so they can be verified automatically.
Run: python3 lint.py         — report errors and warnings
     python3 lint.py --strict — exit 1 on warnings too

Rules are grouped by what they protect:
  SQL        — DuckDB query correctness and safety
  COMPONENT  — Evidence.dev component conventions
  CHART      — Per-diagram-type affordance enforcement (Evidence.dev)
  MAP        — Map component prop correctness
  DATA       — CSV source file integrity
  LINK       — Markdown link encoding
  META       — Page frontmatter completeness

─── Adapting this linter for another Indian city ───────────────────────────

About 57% of these rules are purely Evidence.dev + DuckDB conventions that
apply to any project built with this stack (LINK_ENCODING, COMPONENT_SELF_CLOSE,
COMPONENT_QUERY_REF, all CHART/MAP/UX/narrative rules, SQL safety patterns).
They can be kept verbatim.

About 30% are PMPML-specific data integrity rules (SQL_UTIL_CAP, SQL_GROSS_KM,
SQL_SCHEDULE_SWAP, DATA_PNL, DATA_PVR, DATA_BS, DATA_EARNINGS, META_CITATION,
REFERENCELINE_EBUS_FLEET, REFERENCELINE_DIESEL_EST).
Delete these and replace with your own city's data quality checks — the structure
(KNOWN_DATA_ISSUES dict, per-file schema validators) is the pattern to follow.

About 14% are hybrid rules (COMPONENT_GAPS, SQL_NULL_GUARD, SQL_DEPOT_NAME,
DATA_COORDS, COMPONENT_COLOR_ORDER, AREACHART_MISSING): the rule logic is general
but the constants are PMPML-specific. Update:
  - KNOWN_GAPS         → your city's data gap date ranges
  - DEPRECATED_DEPOT_NAMES → your agency's renamed stations/depots
  - BRT_ONLY_DEPOTS    → your city's transit-mode-specific locations
  - Table name strings ("extracted", "brt_extracted", ...) → your CSV names

The main() loop, findings collector, _tag_bodies() helper, and all rule
function signatures are fully reusable without modification.
"""

import calendar
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
    ("extracted",      "Jan 2024", "Mar 2024", "Reports not retrieved for Q4 FY2023-24"),
    ("extracted",      "Nov 2024", "Mar 2025", "Reports not retrieved for partial FY2024-25"),
    ("extracted",      "Jul 2025", "Sep 2025", "Reports not retrieved; PMPML publishes quarterly batches"),
    ("brt_extracted",  "Jan 2023", "Jan 2023", "BRT Jan 2023 report not retrieved"),
    ("brt_extracted",  "Jan 2024", "Mar 2024", "Reports not retrieved for Q4 FY2023-24"),
    ("brt_extracted",  "Nov 2024", "Mar 2025", "Reports not retrieved for partial FY2024-25"),
    ("brt_extracted",  "Jul 2025", "Sep 2025", "Reports not retrieved; PMPML publishes quarterly batches"),
    ("ebus_extracted", "Jan 2024", "Mar 2024", "Reports not retrieved for Q4 FY2023-24"),
    ("ebus_extracted", "Nov 2024", "Mar 2025", "Reports not retrieved for partial FY2024-25"),
    ("ebus_extracted", "Jul 2025", "Sep 2025", "Reports not retrieved; PMPML publishes quarterly batches"),
]

def _gap_iso_ranges() -> list[tuple[str, str, str]]:
    """Convert KNOWN_GAPS month strings to ISO date ranges for component checks.

    Derives *cross-cutting* gap periods from KNOWN_GAPS and returns them as
    (xMin, xMax, human_label) tuples for ReferenceArea annotation checks.

    "Cross-cutting" means the gap appears for at least 2 distinct file labels
    (e.g., extracted + brt_extracted + ebus_extracted). Table-specific gaps
    (e.g., BRT Jan 2023 only in brt_extracted) are excluded — they should be
    annotated only on the pages that use that table, not enforced site-wide.

    Update KNOWN_GAPS to add or remove gaps — this derives the ISO dates and
    filtering automatically so the rule stays in sync with no extra maintenance.
    """
    from collections import defaultdict
    pair_labels: dict[tuple[str, str], set[str]] = defaultdict(set)
    pair_info: dict[tuple[str, str], str] = {}
    for file_label, start_mon, end_mon, _ in KNOWN_GAPS:
        try:
            s_dt = datetime.datetime.strptime(start_mon, '%b %Y')
            e_dt = datetime.datetime.strptime(end_mon, '%b %Y')
        except ValueError:
            continue
        xmin = f"{s_dt.year:04d}-{s_dt.month:02d}-01"
        last = calendar.monthrange(e_dt.year, e_dt.month)[1]
        xmax = f"{e_dt.year:04d}-{e_dt.month:02d}-{last:02d}"
        pair_labels[(xmin, xmax)].add(file_label)
        if (xmin, xmax) not in pair_info:
            label = f"{start_mon}–{end_mon}" if start_mon != end_mon else start_mon
            pair_info[(xmin, xmax)] = label
    # Only include gaps shared across 2+ file labels (universal annotation obligation)
    result: list[tuple[str, str, str]] = [
        (xmin, xmax, pair_info[(xmin, xmax)])
        for (xmin, xmax), labels in pair_labels.items()
        if len(labels) >= 2
    ]
    return sorted(result)


# ISO date ranges derived from KNOWN_GAPS for use in COMPONENT_GAPS checks.
# Each entry is (xMin_iso, xMax_iso, human_label). Gaps that appear for multiple
# file labels are de-duplicated — one annotation is enough per chart.
_GAP_RANGES: list[tuple[str, str, str]] = _gap_iso_ranges()

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


# ── UX helpers ─────────────────────────────────────────────────────────────────

_CHART_TAGS = ("LineChart", "BarChart", "AreaChart")
_VIZ_TAGS   = ("LineChart", "BarChart", "AreaChart", "DataTable", "PointMap", "AreaMap")

# Column names that DuckDB infers as INTEGER from this project's CSVs.
# Charts using these as x= display "2,021" without xFmt='####'.
# Safe to skip: display_year (SPLIT_PART → string), date_parsed (STRPTIME → date).
_INT_YEAR_COLS = frozenset(["Year", "census_year", "year_num"])

def _tag_bodies(content, tags):
    """Yield (tag_name, attr_string) for each opening Evidence.dev component tag.

    Matches the opening tag and captures all attributes before the closing > or />.
    Works because Evidence.dev attribute values (single-quoted strings, {[...]}
    array expressions) never contain the > character.
    """
    tag_group = "|".join(re.escape(t) for t in tags)
    for m in re.finditer(rf'<({tag_group})\b([^>]*)(?:/>|>)', content, re.DOTALL):
        yield m.group(1), m.group(2)


# BigValue value= column name substrings that imply numeric formatting is needed.
# Plain count columns (total_months, total_depots, years_covered) are intentionally absent.
_FMT_KEYWORDS = frozenset([
    "revenue", "earning", "crore", "deficit", "profit", "loss",
    "reimburse", "income", "expense", "cost", "utiliz", "pct",
    "rate", "ratio", "passengers", "ridership", "km", "fare",
    "cumulative", "total_revenue", "avg_fleet",
])


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

    # Rule META_YAML_QUOTE: title/description values containing a colon must be
    # quoted, otherwise YAML parses them as nested mappings and the dev server
    # crashes with "Nested mappings are not allowed in compact mappings".
    # Pattern: bare (unquoted) value — i.e. not starting with " or '
    for line in body.splitlines():
        m = re.match(r'^(title|description):\s*([^"\'\s].*)', line)
        if m and ":" in m.group(2):
            warn("META_YAML_QUOTE", path,
                 f"{m.group(1)}: value contains a colon but is not quoted — "
                 "wrap in double quotes to prevent YAML parse error: "
                 f"{line.strip()!r}")


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
    # Optional table alias before column name: TRY_CAST(e."% ..." or TRY_CAST("% ...")
    util_pattern = r'TRY_CAST\((?:\w+\.)?"% of Fleet Utilization\(PMPML\+PPP\)" AS DOUBLE\)'
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

    # Rule: Pages using PMPML monthly data should annotate all known data gaps.
    # Gap date ranges are derived from KNOWN_GAPS (top of file) — update KNOWN_GAPS
    # to add or remove gaps and this check automatically stays in sync.
    blocks = extract_sql_blocks(content)
    all_sql = "\n".join(sql for _, sql in blocks)
    if uses_pmpml_table(all_sql):
        has_charts = bool(re.search(r"<(?:LineChart|BarChart|AreaChart)\b", content))
        if has_charts:
            if "ReferenceArea" not in content:
                gap_summary = ", ".join(label for _, _, label in _GAP_RANGES)
                warn("COMPONENT_GAPS", path,
                     "PMPML time-series page has no ReferenceArea gap annotations — "
                     f"add annotations for: {gap_summary}")
            else:
                for xmin, xmax, gap_label in _GAP_RANGES:
                    if xmin not in content or xmax not in content:
                        warn("COMPONENT_GAPS", path,
                             f"Missing {gap_label} gap annotation "
                             f"(xMin='{xmin}' xMax='{xmax}')")
            # Sub-rule: self-closing LineChart with x=date_parsed cannot contain
            # ReferenceArea children (mdsvex silently drops them). Flag any that
            # exist so authors convert them to open/close tags.
            for m in re.finditer(
                r'<LineChart\b([^>]*?)/>',
                content,
                re.DOTALL,
            ):
                attrs = m.group(1)
                if "date_parsed" in attrs:
                    title_m = re.search(r'title="([^"]+)"', attrs)
                    label = title_m.group(1) if title_m else "(no title)"
                    warn("COMPONENT_GAPS", path,
                         f"Self-closing LineChart '{label}' uses date_parsed but cannot "
                         "contain <ReferenceArea> children — convert to open/close tag "
                         "and add gap annotations")


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


def check_financial_citation(path, content):
    """META_CITATION: Financial_Performance.md must cite pmpml.org/financial_performance.

    The annual P&L data comes from a different source than the monthly statistical
    reports. Pages using PMPML_Financial_PnL must link to the financial_performance
    URL, not just the statistics URL.
    """
    if "PMPML_Financial_PnL" not in content:
        return
    if "pmpml.org/financial_performance" not in content:
        warn("META_CITATION", path,
             "Page queries PMPML_Financial_PnL but does not cite "
             "https://pmpml.org/financial_performance — add to the source footnote")


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
    # Find wide-format fuel charts and series-format fuel charts on the same page.
    # Extract y={[...]} blocks first (simple character-class quantifier, no nesting),
    # then filter to blocks containing fuel-type column names.
    y_blocks = re.findall(r'y=\{(\[[^\]]+\])\}', content, re.IGNORECASE)
    fuel_kw = re.compile(r'\b(?:cng|diesel|ebus|e[-_]bus)\b', re.IGNORECASE)
    wide_fuel = [b for b in y_blocks if fuel_kw.search(b)]
    series_fuel = re.search(r"series=fuel_type", content, re.IGNORECASE)

    if wide_fuel and series_fuel:
        for yval in wide_fuel:
            # The series= chart sorts alphabetically: CNG first, Diesel second.
            # The wide chart should match: cng first, diesel second.
            # [^,\]]* is safe (no nested quantifiers — simple class with *).
            if re.search(r"diesel[^,\]]*,\s*['\"]?cng", yval, re.IGNORECASE):
                warn("COMPONENT_COLOR_ORDER", path,
                     "Wide-format chart has diesel before CNG, but series= chart sorts "
                     "alphabetically (CNG first). Colors will be swapped between charts. "
                     "Reorder y=[cng_..., diesel_..., ebus_...] to match.")


# ── Per-diagram affordance rules ──────────────────────────────────────────────

def check_chart_affordances(path, content):
    """CHART_XFMT_YEAR / BARCHART_MULTITYPE / AREACHART_MISSING / REFERENCELINE_ZERO
    / REFERENCELINE_EBUS_FLEET / REFERENCELINE_DIESEL_EST: per-diagram-type affordances.

    CHART_XFMT_YEAR
        DuckDB infers Year, census_year, year_num as INTEGER. On chart axes these
        render as "2,021" (thousands-separated) without xFmt='####'. String years
        from SPLIT_PART (display_year) and STRPTIME dates (date_parsed) are exempt.

    BARCHART_MULTITYPE
        Multi-series BarCharts (series= or y=[...]) without explicit type= rely on
        the Evidence.dev default (grouped). Making type= explicit prevents accidental
        misreads when someone later changes the data shape or Evidence changes its
        default. Use type=grouped when comparing separate quantities side-by-side,
        type=stacked when the series are additive parts of a whole.

    AREACHART_MISSING
        Evidence.dev AreaChart defaults to handleMissing=zero for multi-series charts.
        On PMPML time-series pages (x=date_parsed) this silently fills the three known
        data gaps with zero values — showing a real ridership/km drop that did not happen.
        Multi-series AreaCharts on date_parsed axes must use handleMissing=gap so gaps
        render as breaks rather than false zeroes. Error-level: this is a data correctness
        issue, not just cosmetic.

    REFERENCELINE_ZERO
        Charts showing financial profit/loss, deficit, or net P&L values that can cross
        zero — without a <ReferenceLine y=0> anywhere on the page — are missing the
        baseline that separates surplus from deficit. A zero-baseline line is the clearest
        possible encoding of "profit vs. loss" in a line or bar chart. Covers column names
        containing: pl_cr, net_pl, operating_pl, profit_loss, deficit, net_position.

    REFERENCELINE_EBUS_FLEET  [PMPML-specific]
        EBus.md fleet charts (y=avg_on_road or fleet_utilization_pct) should annotate
        the three known fleet expansion events: Oct 2023 (458→473), Aug 2024 (473→490),
        and Apr 2025 (Hadapsar depot exit + Charholi/Maan additions). Without these
        markers, step-changes in fleet size and ridership are unexplained.

    REFERENCELINE_DIESEL_EST  [PMPML-specific]
        Pages that use the diesel km back-calculation (COALESCE/NULLIF with "Total
        Eff;km.Diesel") should mark x='2024-04-01' as the estimation boundary. From
        April 2024, extracted.csv diesel km is null — all values are computed from
        KMPL × consumption. Readers need a visible boundary to trust the data.
    """
    for tag, attrs in _tag_bodies(content, _CHART_TAGS):
        # CHART_XFMT_YEAR
        x_m = re.search(r'\bx=(\w+)', attrs)
        if x_m and x_m.group(1) in _INT_YEAR_COLS and 'xFmt=' not in attrs:
            warn("CHART_XFMT_YEAR", path,
                 f"<{tag} x={x_m.group(1)}> missing xFmt='####' — "
                 "integer year column renders with thousands separator ('2,021'). "
                 "Add xFmt='####'.")

    for tag, attrs in _tag_bodies(content, ["BarChart"]):
        # BARCHART_MULTITYPE
        if 'type=' not in attrs:
            has_multi_y = bool(re.search(r"y=\{?\[", attrs))
            has_series  = 'series=' in attrs
            if has_multi_y or has_series:
                title_m = re.search(r'title="([^"]+)"', attrs)
                label   = f'"{title_m.group(1)}"' if title_m else "(no title)"
                warn("BARCHART_MULTITYPE", path,
                     f"<BarChart {label}> has multiple series but no type= — "
                     "add type=grouped (side-by-side comparison) or "
                     "type=stacked (additive parts of a whole) to make intent explicit")

    for tag, attrs in _tag_bodies(content, ["AreaChart"]):
        # AREACHART_MISSING: multi-series AreaChart on date_parsed without handleMissing=gap
        x_m = re.search(r'\bx=(\w+)', attrs)
        if x_m and x_m.group(1) == "date_parsed":
            has_multi_y = bool(re.search(r"y=\{\[.+?,", attrs, re.DOTALL))
            has_series  = 'series=' in attrs
            if (has_multi_y or has_series) and 'handleMissing=' not in attrs:
                title_m = re.search(r'title="([^"]+)"', attrs)
                label   = f'"{title_m.group(1)}"' if title_m else "(no title)"
                error("AREACHART_MISSING", path,
                      f"<AreaChart {label}> is multi-series on date_parsed but missing "
                      "handleMissing=gap — Evidence.dev default is handleMissing=zero, "
                      "which fills PMPML data gaps with false zeroes. "
                      "Add handleMissing=gap so gaps render as breaks.")

    # REFERENCELINE_ZERO: charts with profit/loss columns should have <ReferenceLine y=0>
    # Column names that indicate values can go negative (profit vs. loss)
    _ZERO_CROSS_COLS = frozenset([
        "pl_cr", "net_pl", "operating_pl", "profit_loss",
        "deficit", "surplus", "net_position", "net_profit",
    ])
    has_zero_refline = bool(re.search(r'<ReferenceLine\b[^/]*/?\s*y=0\b', content))
    if not has_zero_refline:
        for tag, attrs in _tag_bodies(content, _CHART_TAGS):
            y_m = re.search(r'\by=(\w+)', attrs)
            if y_m:
                col = y_m.group(1).lower()
                if any(kw in col for kw in _ZERO_CROSS_COLS):
                    title_m = re.search(r'title="([^"]+)"', attrs)
                    label   = f'"{title_m.group(1)}"' if title_m else "(no title)"
                    warn("REFERENCELINE_ZERO", path,
                         f"<{tag} {label}> shows profit/loss values (y={y_m.group(1)}) "
                         "but has no <ReferenceLine y=0> — add a zero baseline to make "
                         "surplus vs. deficit visually explicit. "
                         "Use: <ReferenceLine y=0 label=\"Breakeven\" color=base-content-muted "
                         "hideValue=true/>")
                    break  # one warning per page is enough

    # REFERENCELINE_EBUS_FLEET: EBus fleet charts should annotate expansion events.
    # Fleet step-changes: Oct 2023 (458→473), Aug 2024 (473→490), Apr 2025 (depot change).
    _EBUS_FLEET_COLS: frozenset[str] = frozenset(["avg_on_road", "avg_off_road", "fleet_utilization_pct"])
    if "EBus" in path.name or "ebus" in path.name.lower():
        has_fleet_chart = any(
            any(kw in attrs for kw in _EBUS_FLEET_COLS)
            for _tag, attrs in _tag_bodies(content, _CHART_TAGS)
        )
        has_fleet_refline = bool(re.search(r"<ReferenceLine\b[^>]*x='2023-10-01'", content))
        if has_fleet_chart and not has_fleet_refline:
            warn("REFERENCELINE_EBUS_FLEET", path,
                 "EBus fleet chart is missing fleet expansion markers. "
                 "The e-bus fleet stepped up Oct 2023 (458→473), Aug 2024 (473→490), "
                 "and changed Apr 2025. Add: "
                 "<ReferenceLine x='2023-10-01' label=\"Fleet: 458→473\" hideValue=true color=base-content-muted/> "
                 "(and similarly for 2024-08-01 and 2025-04-01).")

    # REFERENCELINE_DIESEL_EST: diesel km back-calculation pages should mark the
    # estimation boundary at April 2024 (where extracted.csv diesel column goes null).
    _DIESEL_BACKCALC_PAT: re.Pattern[str] = re.compile(
        r'COALESCE\s*\(\s*NULLIF.*?Total Eff;km\.Diesel', re.DOTALL | re.IGNORECASE
    )
    if _DIESEL_BACKCALC_PAT.search(content):
        has_est_marker = bool(re.search(r"<ReferenceLine\b[^>]*x='2024-04-01'", content))
        if not has_est_marker:
            warn("REFERENCELINE_DIESEL_EST", path,
                 "Page uses diesel km back-calculation (COALESCE/NULLIF on 'Total Eff;km.Diesel') "
                 "but has no estimation-boundary marker. From April 2024, diesel km values are "
                 "estimated from KMPL × consumption — add: "
                 "<ReferenceLine x='2024-04-01' label=\"Diesel km estimated\" "
                 "hideValue=true color=base-content-muted lineType=dashed/>")


def check_map_props(path, content):
    """MAP_LON_PROP / MAP_VALUE_FMT: PointMap prop correctness and affordances.

    MAP_LON_PROP
        Evidence.dev PointMap requires long= (not lon=). Using lon= silently omits
        the required prop, producing a 'long is required' render error. Error-level
        because it breaks rendering entirely.

    MAP_VALUE_FMT
        PointMap with value= but no valueFmt= shows raw integers in bubble tooltips
        (e.g. "12345" instead of "12,345"). Add valueFmt='#,##0' or an appropriate
        format string so tooltip values are readable at a glance.
    """
    for tag, attrs in _tag_bodies(content, ["PointMap"]):
        # MAP_LON_PROP: lon= is wrong, long= is correct
        if re.search(r'\blon=', attrs):
            error("MAP_LON_PROP", path,
                  "<PointMap> uses lon= but the correct Evidence.dev prop is long= — "
                  "lon= is silently ignored, causing a 'long is required' render error. "
                  "Rename to long=.")

        # MAP_VALUE_FMT: value= without valueFmt=
        if 'value=' in attrs and 'valueFmt=' not in attrs:
            vm = re.search(r'\bvalue=(\w+)', attrs)
            col = vm.group(1) if vm else "?"
            warn("MAP_VALUE_FMT", path,
                 f"<PointMap value={col}> missing valueFmt= — "
                 "bubble tooltip shows raw integer; add valueFmt='#,##0' "
                 "(or currency/pct format) for readable tooltip values")


# ── UX / Design rules ─────────────────────────────────────────────────────────

def check_chart_ux(path, content):
    """UX rules for chart components: titles, axis labels, type, invalid props.

    Rules:
      CHART_TITLE          — every chart needs a title for reader orientation
      CHART_YAXIS          — every chart should declare yAxisTitle= for unit context
      CHART_AREA_TYPE      — multi-series AreaChart without type= will overlap
      COMPONENT_INVALID_PROP — seriesLabels= is not a valid Evidence.dev prop
      CHART_DATATABLE_ROWS — explicit rows= prevents unpredictable default pagination
      BIGVALUE_FMT         — monetary/rate BigValues need fmt= for readability
    """

    # CHART_TITLE — every LineChart/BarChart/AreaChart must have a title
    for tag, attrs in _tag_bodies(content, _CHART_TAGS):
        if "title=" not in attrs:
            warn("CHART_TITLE", path,
                 f"<{tag}> missing title= — every chart needs a title for reader orientation")

    # CHART_YAXIS — primary charts should declare yAxisTitle= for unit context
    for tag, attrs in _tag_bodies(content, _CHART_TAGS):
        if "yAxisTitle=" not in attrs:
            warn("CHART_YAXIS", path,
                 f"<{tag}> missing yAxisTitle= — axis label tells readers what units they're reading")

    # CHART_AREA_TYPE — AreaChart with multiple y-series needs type=stacked/stacked100
    for tag, attrs in _tag_bodies(content, ["AreaChart"]):
        if re.search(r"y=\{\[.+?,", attrs, re.DOTALL) and "type=" not in attrs:
            warn("CHART_AREA_TYPE", path,
                 "<AreaChart> has multiple y-series but no type= — "
                 "without type=stacked or type=stacked100, series will overlap instead of stack")

    # COMPONENT_INVALID_PROP — seriesLabels= is not a valid Evidence.dev BarChart prop;
    # it is silently ignored, causing series to display column-name labels instead of
    # the intended human-readable labels. Rename columns in SQL instead.
    if "seriesLabels=" in content:
        warn("COMPONENT_INVALID_PROP", path,
             "seriesLabels= is not a valid Evidence.dev prop (silently ignored) — "
             "rename series by aliasing columns in SQL (e.g. revenue AS \"Bus Revenue\")")

    # CHART_DATATABLE_ROWS — DataTable must declare rows= to control pagination
    for tag, attrs in _tag_bodies(content, ["DataTable"]):
        if "rows=" not in attrs:
            warn("CHART_DATATABLE_ROWS", path,
                 "<DataTable> missing rows= — "
                 "set rows=all to show all records, or rows=N for explicit page size")

    # BIGVALUE_FMT — monetary/rate BigValues need fmt= so numbers render readably
    for tag, attrs in _tag_bodies(content, ["BigValue"]):
        if "fmt=" not in attrs:
            vm = re.search(r'\bvalue=(\w+)', attrs)
            if vm and any(kw in vm.group(1).lower() for kw in _FMT_KEYWORDS):
                warn("BIGVALUE_FMT", path,
                     f"<BigValue value={vm.group(1)}> missing fmt= — "
                     "add a format string (e.g. '#,##0' or '\"₹\"#,##0\" Cr\"')")


def check_artifact_opener(path, content):
    """ARTIFACT_OPENER: pages must not open with an artifact-forward sentence.

    Artifact-forward openers ("Looking at the visualization below...", "As we can
    see in the chart...") lead with the tool, not the story. Every data page must
    open with a claim about the world, not a pointer to a chart.

    Warning only — some navigation-hub index pages may intentionally begin with
    a structural description rather than an argumentative claim.
    """
    body = re.sub(r"^---\n.*?\n---\n?", "", content, count=1, flags=re.DOTALL)
    # Find first non-empty, non-heading line
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Check if the first sentence matches artifact-opener patterns
        if re.match(
            r"^(?:Looking at|As we can see|As shown|We can see|"
            r"In this (?:page|visualization|chart|dashboard))",
            stripped,
            re.IGNORECASE,
        ):
            warn("ARTIFACT_OPENER", path,
                 f"Page opens with artifact-forward sentence: '{stripped[:80]}...' — "
                 "lead with a claim about the world, not a pointer to a chart")
        break  # only check the first non-empty, non-heading line


def check_content_ifelse(path, content):
    """CONTENT_IFELSE: ButtonGroup/conditional views must have prose before first chart.

    Any {#if inputs.} or {:else if inputs.} block that selects a VIEW (not just
    a chart format) but contains no prose paragraph (20+ characters of non-tag,
    non-SQL text) before the first chart component is flagged. This prevents
    ButtonGroup views from being added without explanatory text.

    Chart-type/format switcher blocks are intentionally exempt — they select
    display format (Line vs Area vs Bar, Percentage vs Absolute) within a
    section that is already narrated, so prose is expected before the switcher,
    not inside each branch. These are identified by condition variable names
    ending in _chart_type, _display, or _metric, or by condition values that
    are chart format names ("Line Chart", "Area Chart", "Percentage", etc.).

    Warning only.
    """
    # Chart-type/format condition patterns to skip (these are display-format switchers,
    # not view selectors — the prose lives outside the switcher block).
    FORMAT_VAR_SUFFIXES = ("_chart_type", "_display", "_metric")
    FORMAT_VALUES = frozenset([
        '"Line Chart"', '"Area Chart"', '"Bar Chart"',
        '"Percentage"', '"Split"', '"Both"', '"Absolute"',
    ])

    # Match {#if inputs.expr} or {:else if inputs.expr}
    block_pat = re.compile(
        r'\{(?:#if|:else if)\s+(inputs\.[^}]+)\}(.*?)(?=\{(?:#if|:else if|/if)\b|$)',
        re.DOTALL
    )
    for m in block_pat.finditer(content):
        condition = m.group(1).strip()  # e.g. inputs.selected_view === "Two Wheelers"
        block_body = m.group(2)

        # Skip chart-type / format switchers
        # Check if the input variable name ends with a format-switcher suffix
        var_m = re.match(r'inputs\.(\w+)', condition)
        if var_m:
            var_name = var_m.group(1)
            if any(var_name.endswith(sfx) for sfx in FORMAT_VAR_SUFFIXES):
                continue
        # Check if the condition value is a chart format name
        val_m = re.search(r'===\s*("[^"]*")', condition)
        if val_m and val_m.group(1) in FORMAT_VALUES:
            continue

        # Find first Evidence chart/viz component in this block
        first_component = re.search(
            r'<(?:LineChart|BarChart|AreaChart|DataTable|PointMap|AreaMap|BigValue)\b',
            block_body
        )
        if not first_component:
            continue

        # Check for prose (20+ non-tag, non-SQL chars) before the first component
        pre_component = block_body[:first_component.start()]
        pre_clean = re.sub(r"```.*?```", "", pre_component, flags=re.DOTALL)
        pre_clean = re.sub(r"^#{1,6}\s+.*$", "", pre_clean, flags=re.MULTILINE)
        # Strip Evidence component open-tags (multi-line) and self-closing tags
        pre_clean = re.sub(r"<\w[^>]*/?>", "", pre_clean, flags=re.DOTALL)
        pre_clean = pre_clean.strip()

        if len(pre_clean) < 20:
            preceding = content[:m.start()]
            heading_m = re.findall(r"^#{1,6}\s+(.+)$", preceding, re.MULTILINE)
            section = heading_m[-1] if heading_m else "(unknown section)"
            warn("CONTENT_IFELSE", path,
                 f"Conditional view '{section}' contains charts but no prose paragraph "
                 f"({len(pre_clean)} chars before first component) — "
                 "add at least one orienting sentence before the first chart")


def check_page_ux(path, content):
    """UX rules for page narrative structure: intro prose, See Also, source footnote.

    Rules:
      META_DESCRIPTION     — description should be 20–160 chars
      PAGE_INTRO           — at least 30 words of prose before first visualization
      PAGE_SEE_ALSO        — data pages should link to related pages
      PAGE_FOOTER          — data pages should cite their source
    """
    path_str = str(path)
    has_sql = bool(extract_sql_blocks(content))
    has_viz = bool(re.search(r'<(?:' + '|'.join(_VIZ_TAGS) + r')\b', content))

    # META_DESCRIPTION_LEN — applies to all pages with frontmatter
    fm = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if fm:
        desc_m = re.search(r"description:\s*(.+)", fm.group(1))
        if desc_m:
            desc = desc_m.group(1).strip()
            if len(desc) < 20:
                warn("META_DESCRIPTION", path,
                     f"description too short ({len(desc)} chars) — "
                     "a concise one-liner helps readers and sidebar navigation")
            elif len(desc) > 160:
                warn("META_DESCRIPTION", path,
                     f"description too long ({len(desc)} chars, max 160) — "
                     "trim for sidebar and link preview readability")

    if not (has_sql and has_viz):
        return  # remaining structural rules only apply to data visualization pages

    # PAGE_INTRO — at least 30 words of prose should appear before the first chart
    body = re.sub(r"^---\n.*?\n---\n?", "", content, count=1, flags=re.DOTALL)
    first_component_m = re.search(
        r'<(?:' + '|'.join(_VIZ_TAGS + ("Grid", "BigValue")) + r')\b', body
    )
    if first_component_m:
        pre = body[:first_component_m.start()]
        pre = re.sub(r"```.*?```", "", pre, flags=re.DOTALL)   # strip SQL blocks
        pre = re.sub(r"^#{1,6}\s+.*$", "", pre, flags=re.MULTILINE)  # strip headings
        words = pre.split()
        if len(words) < 30:
            warn("PAGE_INTRO", path,
                 f"Only {len(words)} words of prose before first visualization — "
                 "add a narrative paragraph so readers have context before the charts")

    # PAGE_SEE_ALSO — data pages should have a See Also navigation section
    # Index pages serve as navigation hubs themselves, so they are exempt
    if not path_str.endswith("index.md") and "## See Also" not in content:
        warn("PAGE_SEE_ALSO", path,
             "Data page missing '## See Also' section — "
             "add cross-links to help readers discover related pages")

    # PAGE_FOOTER — data pages should have an italicized source footnote or
    # a dedicated ## Sources section. Accepts:
    #   *Data covers..., *Data:..., *Data from...   (italic data-coverage note)
    #   *Source:... / *Sources:...                  (italic source citation)
    #   ## Sources / ## Source                      (dedicated section heading)
    if not re.search(
        r'^\*(?:Data|Source)|^## Source',
        content, re.MULTILINE | re.IGNORECASE
    ):
        warn("PAGE_FOOTER", path,
             "Data page missing source footnote — "
             "add *Data covers [period]. Source: [URL].* or a ## Sources section")


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

    # ── PMPML_Financial_PnL.csv integrity ───────────────────────────────────

    rows_pnl, p_pnl = load_csv("PMPML_Financial_PnL.csv")
    if rows_pnl is None:
        error("DATA_PNL", p_pnl,
              "PMPML_Financial_PnL.csv not found — run /tmp/build_pnl_csv.py to regenerate")
    else:
        required_cols = {
            "fiscal_year", "revenue_bus_ops", "employee_benefits",
            "total_expenses", "operating_profit_loss",
            "total_reimbursements", "net_profit_loss",
        }
        missing_cols = required_cols - set(rows_pnl[0].keys())
        if missing_cols:
            error("DATA_PNL", p_pnl,
                  f"PMPML_Financial_PnL.csv missing columns: {sorted(missing_cols)}")
        expected_years = {
            "2017-18", "2018-19", "2019-20", "2020-21",
            "2021-22", "2022-23", "2023-24", "2024-25",
        }
        actual_years = {r.get("fiscal_year", "") for r in rows_pnl}
        missing_years = expected_years - actual_years
        if missing_years:
            warn("DATA_PNL", p_pnl,
                 f"PMPML_Financial_PnL.csv missing fiscal years: {sorted(missing_years)}")
        if len(rows_pnl) > len(expected_years):
            warn("DATA_PNL", p_pnl,
                 f"PMPML_Financial_PnL.csv has {len(rows_pnl)} rows — expected 8 "
                 "(one per fiscal year 2017-18 to 2024-25)")

    # ── pune_vehicle_registrations.csv integrity ─────────────────────────────

    rows_pvr, p_pvr = load_csv("pune_vehicle_registrations.csv")
    if rows_pvr is None:
        error("DATA_PVR", p_pvr,
              "pune_vehicle_registrations.csv not found — source: "
              "/media/2TA/DevStuff/Mapping/Publish/maharashtravehicle registrations.csv")
    else:
        required_cols_pvr = {"year", "city", "motor_cycles", "cars", "auto_rickshaws"}
        missing_cols_pvr = required_cols_pvr - set(rows_pvr[0].keys())
        if missing_cols_pvr:
            error("DATA_PVR", p_pvr,
                  f"pune_vehicle_registrations.csv missing columns: {sorted(missing_cols_pvr)}")
        cities = {r.get("city", "") for r in rows_pvr}
        if "Pune" not in cities:
            error("DATA_PVR", p_pvr,
                  "pune_vehicle_registrations.csv missing Pune city rows")
        if "Pimpri-Chinchwad" not in cities:
            error("DATA_PVR", p_pvr,
                  "pune_vehicle_registrations.csv missing Pimpri-Chinchwad rows")
        years_pvr = {r.get("year", "") for r in rows_pvr}
        if "2000-2001" not in years_pvr or "2017-2018" not in years_pvr:
            warn("DATA_PVR", p_pvr,
                 "pune_vehicle_registrations.csv should cover 2000-2001 to 2017-2018")

    # ── PMPML_Balance_Sheet.csv integrity ────────────────────────────────────

    rows_bs, p_bs = load_csv("PMPML_Balance_Sheet.csv")
    if rows_bs is None:
        error("DATA_BS", p_bs,
              "PMPML_Balance_Sheet.csv not found")
    else:
        required_year_cols = {
            "fy2017_18_lakhs", "fy2018_19_lakhs", "fy2019_20_lakhs", "fy2020_21_lakhs",
            "fy2021_22_lakhs", "fy2022_23_lakhs", "fy2023_24_lakhs", "fy2024_25_lakhs",
        }
        missing_year_cols = required_year_cols - set(rows_bs[0].keys())
        if missing_year_cols:
            error("DATA_BS", p_bs,
                  f"PMPML_Balance_Sheet.csv missing year columns: {sorted(missing_year_cols)}")
        required_items = {
            "Property Plant & Equipment (Net)",
            "Other Non-Current Assets",
            "Inventories",
            "Trade Receivables",
            "Cash & Cash Equivalents",
            "Loans & Advances",
            "Other Current Assets",
            "Short-Term Borrowings",
            "Other Non-Current Liabilities",
        }
        actual_items = {r.get("item", "") for r in rows_bs}
        missing_items = required_items - actual_items
        if missing_items:
            error("DATA_BS", p_bs,
                  f"PMPML_Balance_Sheet.csv missing items: {sorted(missing_items)}")
        if len(rows_bs) != 9:
            warn("DATA_BS", p_bs,
                 f"PMPML_Balance_Sheet.csv has {len(rows_bs)} rows — expected 9")

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
        check_financial_citation(rel, content)
        check_chart_affordances(rel, content)
        check_map_props(rel, content)
        check_chart_ux(rel, content)
        check_page_ux(rel, content)
        check_artifact_opener(rel, content)
        check_content_ifelse(rel, content)

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
        by_file: dict[str, list[tuple[str, str, str]]] = {}
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
                lines: list[str]
                cur: list[str]
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
