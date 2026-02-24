---
title: PMPML Financial Performance
description: Annual profit & loss 2017-18 to 2024-25 — revenue, operating deficit, and how municipal reimbursements bridge the gap
---

PMPML's finances follow a structural pattern: bus revenue has held roughly flat while employee costs have more than tripled, pushing the pre-reimbursement operating deficit from ₹204 Cr in FY17-18 to ₹889 Cr in FY24-25. Pune Municipal Corporation (PMC) and Pimpri-Chinchwad Municipal Corporation (PCMC) cover this deficit through annual reimbursements — but these arrive a year or more after the loss is incurred, on a schedule set by each municipal body's budget calendar.

The eight-year record captures the COVID collapse (FY20-21: revenue down 70%, employees still 97% paid), the recovery (FY22-23: first net profit in years), and the FY24-25 return to loss as employee costs outran both revenue and the reimbursement ceiling.

**Note on data quality:** P&L figures for FY17-18 to FY20-21 are from text-embedded PDFs via Ghostscript; FY21-22 to FY24-25 from OCR of scanned statements. Balance sheet figures for FY17-18 to FY20-21 are manually transcribed from Canon-scanned PDFs (raw rupees converted to lakhs); FY21-22 to FY22-23 from iLovePDF scans. FY21-22 introduced an Ind-AS reclassification — roughly ₹40 Cr of deposits/advances moved from current assets to "Other Non-Current Assets" — creating a structural break; pre-FY21-22 figures are as originally reported. The `notes` column in the source CSV documents extraction method and any discrepancies per item.

---

## System Overview

```sql pnl_summary
SELECT
    COUNT(*) as years_covered,
    ROUND(SUM(-operating_profit_loss) / 100, 0) as total_operating_deficit_cr,
    ROUND(SUM(total_reimbursements) / 100, 0) as total_reimbursements_cr,
    ROUND(SUM(net_profit_loss) / 100, 1) as cumulative_net_pl_cr
FROM PMPML_Financial_PnL
```

<Grid cols=4>
<BigValue
    data={pnl_summary}
    value=years_covered
    title="Fiscal Years"
/>
<BigValue
    data={pnl_summary}
    value=total_operating_deficit_cr
    title="Cumulative Operating Deficit"
    fmt='"₹"#,##0" Cr"'
/>
<BigValue
    data={pnl_summary}
    value=total_reimbursements_cr
    title="Total Reimbursements Received"
    fmt='"₹"#,##0" Cr"'
/>
<BigValue
    data={pnl_summary}
    value=cumulative_net_pl_cr
    title="Net Position (8 Years)"
    fmt='"₹"#,##0.0" Cr"'
/>
</Grid>

---

## Revenue vs. Total Expenditure

Bus revenue has remained in the ₹550–650 Cr range across most years, with the COVID-year (FY20-21) exception. Total expenditure has grown continuously — driven almost entirely by employee benefit costs — creating a widening structural gap. Without municipal reimbursements, PMPML has been operationally insolvent in every year except FY22-23 and FY23-24.

<BarChart
    data={pnl_trend}
    x=fiscal_year
    y={['income_cr', 'expenses_cr']}
    title="Total Income vs. Total Expenditure (₹ Crores)"
    yAxisTitle="₹ Crores"
    yFmt='#,##0'
    labels=true
/>

<LineChart
    data={pnl_trend}
    x=fiscal_year
    y=operating_pl_cr
    title="Operating Profit / (Loss) Before Reimbursements (₹ Crores)"
    subtitle="Negative = operating deficit funded by municipal reimbursements"
    yAxisTitle="₹ Crores"
    yFmt='#,##0'
/>

---

## The Operating Deficit and How It Is Covered

PMPML's operating deficit is formally a reimbursable item — PMC and PCMC are legally obligated to compensate PMPML for providing public transport in their jurisdictions. PMRDA (Pune Metropolitan Region Development Authority) began contributing from FY23-24 onward. The reimbursements cover the *previous year's* losses, so a large deficit in year N appears as revenue in year N+1.

<BarChart
    data={reimbursements_breakdown}
    x=fiscal_year
    y={['pmc_cr', 'pcmc_cr', 'pmrda_cr']}
    type=stacked
    title="Municipal Reimbursements Received by Source (₹ Crores)"
    yAxisTitle="₹ Crores"
    yFmt='#,##0'
/>

<BarChart
    data={reimbursements_breakdown}
    x=fiscal_year
    y={['operating_deficit_cr', 'reimbursements_cr']}
    title="Operating Deficit vs. Reimbursements Received (₹ Crores)"
    subtitle="Gap between bars = deficit not covered, or surplus coverage from prior-year timing"
    yAxisTitle="₹ Crores"
    yFmt='#,##0'
/>

---

## Employee Costs: The Structural Driver

PMPML's employee benefit costs — salaries, pensions, provident fund contributions — have grown from ₹439 Cr in FY17-18 to ₹831 Cr in FY24-25 while the fleet expanded only modestly. As a share of bus revenue, employee costs rose from 75% to 140%. This ratio above 100% means PMPML cannot even cover its payroll from fare revenue alone.

<LineChart
    data={emp_ratio}
    x=fiscal_year
    y=emp_to_revenue_pct
    title="Employee Benefits as % of Bus Revenue"
    subtitle="Above 100% means payroll exceeds fare income — requires subsidy to break even"
    yAxisTitle="% of Bus Revenue"
    yFmt='#0.0"%"'
/>

<BarChart
    data={emp_ratio}
    x=fiscal_year
    y={['revenue_cr', 'employee_cr']}
    title="Bus Revenue vs. Employee Benefits (₹ Crores)"
    yAxisTitle="₹ Crores"
    yFmt='#,##0'
/>

---

## Expenditure Breakdown

Employee benefits dominate the cost structure, accounting for 50–70% of total expenditure across all years. "Other expenses" is the second-largest line — this covers contracts, maintenance, administrative costs, and other operational items. Fuel and consumables (cost of purchases) are relatively modest, reflecting the dependency on hired fleet that handles fuel independently.

<BarChart
    data={expense_breakdown}
    x=fiscal_year
    y={['employee_cr', 'other_cr', 'fuel_purchase_cr', 'depreciation_cr', 'finance_cr']}
    type=stacked
    title="Total Expenditure by Category (₹ Crores)"
    yAxisTitle="₹ Crores"
    yFmt='#,##0'
/>

---

## Net Profit / (Loss) After Reimbursements

After accounting for all reimbursements received, PMPML posted net profits in FY17-18 (small surplus from prior-year reimbursements), FY22-23, and FY23-24. FY24-25 returned to a net loss of ₹191 Cr — despite receiving ₹698 Cr in reimbursements — because the underlying operating deficit reached ₹889 Cr.

<BarChart
    data={pnl_trend}
    x=fiscal_year
    y=net_pl_cr
    title="Net Profit / (Loss) After Reimbursements (₹ Crores)"
    subtitle="This is the bottom-line figure after all income, expenses, and reimbursements"
    yAxisTitle="₹ Crores"
    yFmt='#,##0.0'
/>

---

## Balance Sheet: Eight-Year Trends

PMPML entered this period with no short-term debt and a strong cash position. The FY2019-20 surge in net fixed assets — from ₹82 Cr to ₹214 Cr in a single year — reflects large-scale capital investment, likely the BRT fleet expansion and early electric bus procurement. Since then, annual depreciation has outpaced new additions: net PPE has fallen 85% over six years to ₹32.8 Cr in FY2024-25, suggesting the 2019-20 vintage fleet is approaching full depreciation without comparable replacement. Cash reserves tracked an opposite arc — peaking at ₹93 Cr in FY2019-20, collapsing to ₹9.9 Cr by FY2022-23, and partially recovering since. Short-term borrowings were zero through FY2019-20, then rose as cash fell, reaching ₹34.3 Cr by FY2024-25.

*Note: FY2021-22 introduced an Ind-AS reclassification that moved ~₹40 Cr from current to non-current assets. Pre-FY2021-22 figures are as originally reported — the structural break appears most clearly in the "Other Non-Current Assets" line.*

```sql bs_trend
SELECT fiscal_year, item, ROUND(value_lakhs / 100, 1) as value_cr
FROM (
    SELECT 'FY2017-18' as fiscal_year, item, fy2017_18_lakhs as value_lakhs FROM PMPML_Balance_Sheet
    UNION ALL
    SELECT 'FY2018-19', item, fy2018_19_lakhs FROM PMPML_Balance_Sheet
    UNION ALL
    SELECT 'FY2019-20', item, fy2019_20_lakhs FROM PMPML_Balance_Sheet
    UNION ALL
    SELECT 'FY2020-21', item, fy2020_21_lakhs FROM PMPML_Balance_Sheet
    UNION ALL
    SELECT 'FY2021-22', item, fy2021_22_lakhs FROM PMPML_Balance_Sheet
    UNION ALL
    SELECT 'FY2022-23', item, fy2022_23_lakhs FROM PMPML_Balance_Sheet
    UNION ALL
    SELECT 'FY2023-24', item, fy2023_24_lakhs FROM PMPML_Balance_Sheet
    UNION ALL
    SELECT 'FY2024-25', item, fy2024_25_lakhs FROM PMPML_Balance_Sheet
) t
WHERE item IN (
    'Property Plant & Equipment (Net)',
    'Cash & Cash Equivalents',
    'Short-Term Borrowings',
    'Inventories'
)
ORDER BY fiscal_year, item
```

<LineChart
    data={bs_trend}
    x=fiscal_year
    y=value_cr
    series=item
    title="Key Balance Sheet Items — FY2017-18 to FY2024-25 (₹ Crores)"
    subtitle="PPE, cash, borrowings, and inventories over eight fiscal years"
    yAxisTitle="₹ Crores"
    yFmt='#,##0.0'
/>

---

## Balance Sheet Snapshot

*FY2024-25 with FY2023-24 comparatives. Values extracted from the annual balance sheet by OCR and cross-validated using consecutive-year previous-column matching. Figures in ₹ Crores.*

Three signals from the balance sheet: short-term borrowings grew 36% (₹25.2 Cr → ₹34.3 Cr), inventories (spare parts and consumables) nearly tripled (₹8.8 Cr → ₹20.2 Cr), and net fixed assets shrank 30% (₹46.6 Cr → ₹32.8 Cr) as depreciation outpaced capital additions. Cash remained essentially flat. The largest single asset — ₹112.8 Cr classified as "Other Non-Current Assets" — likely represents accumulated subsidy receivables from PMC and PCMC that have not yet been settled in cash, consistent with the reimbursement timing gap documented above.

```sql bs_snapshot
SELECT
    ROUND(MAX(CASE WHEN item = 'Cash & Cash Equivalents' THEN fy2024_25_lakhs END) / 100, 1) as cash_cr,
    ROUND(MAX(CASE WHEN item = 'Short-Term Borrowings' THEN fy2024_25_lakhs END) / 100, 1) as stborrowings_cr,
    ROUND(MAX(CASE WHEN item = 'Property Plant & Equipment (Net)' THEN fy2024_25_lakhs END) / 100, 1) as ppe_cr,
    ROUND(MAX(CASE WHEN item = 'Inventories' THEN fy2024_25_lakhs END) / 100, 1) as inventories_cr,
    ROUND(100.0 * (MAX(CASE WHEN item = 'Short-Term Borrowings' THEN fy2024_25_lakhs END) -
                   MAX(CASE WHEN item = 'Short-Term Borrowings' THEN fy2023_24_lakhs END)) /
          NULLIF(MAX(CASE WHEN item = 'Short-Term Borrowings' THEN fy2023_24_lakhs END), 0), 0) as borrowings_yoy_pct,
    ROUND(100.0 * (MAX(CASE WHEN item = 'Inventories' THEN fy2024_25_lakhs END) -
                   MAX(CASE WHEN item = 'Inventories' THEN fy2023_24_lakhs END)) /
          NULLIF(MAX(CASE WHEN item = 'Inventories' THEN fy2023_24_lakhs END), 0), 0) as inventories_yoy_pct,
    ROUND(100.0 * (MAX(CASE WHEN item = 'Property Plant & Equipment (Net)' THEN fy2024_25_lakhs END) -
                   MAX(CASE WHEN item = 'Property Plant & Equipment (Net)' THEN fy2023_24_lakhs END)) /
          NULLIF(MAX(CASE WHEN item = 'Property Plant & Equipment (Net)' THEN fy2023_24_lakhs END), 0), 0) as ppe_yoy_pct
FROM PMPML_Balance_Sheet
```

<Grid cols=4>
<BigValue
    data={bs_snapshot}
    value=cash_cr
    title="Cash (FY24-25)"
    fmt='"₹"#,##0.0" Cr"'
/>
<BigValue
    data={bs_snapshot}
    value=stborrowings_cr
    title="Short-Term Borrowings"
    fmt='"₹"#,##0.0" Cr"'
/>
<BigValue
    data={bs_snapshot}
    value=ppe_cr
    title="Net Fixed Assets (PPE)"
    fmt='"₹"#,##0.0" Cr"'
/>
<BigValue
    data={bs_snapshot}
    value=inventories_cr
    title="Inventories"
    fmt='"₹"#,##0.0" Cr"'
/>
</Grid>

```sql balance_sheet_compare
SELECT
    item,
    subcategory,
    'FY2023-24' as fiscal_year,
    ROUND(fy2023_24_lakhs / 100, 1) as value_cr
FROM PMPML_Balance_Sheet
WHERE item NOT IN ('Other Non-Current Assets', 'Other Current Assets', 'Other Non-Current Liabilities')
UNION ALL
SELECT
    item,
    subcategory,
    'FY2024-25' as fiscal_year,
    ROUND(fy2024_25_lakhs / 100, 1) as value_cr
FROM PMPML_Balance_Sheet
WHERE item NOT IN ('Other Non-Current Assets', 'Other Current Assets', 'Other Non-Current Liabilities')
ORDER BY subcategory DESC, item, fiscal_year
```

<BarChart
    data={balance_sheet_compare}
    x=item
    y=value_cr
    series=fiscal_year
    title="Key Balance Sheet Items — FY2023-24 vs FY2024-25 (₹ Crores)"
    subtitle="Inventories +129%, short-term borrowings +36%, PPE net −30%"
    yAxisTitle="₹ Crores"
    yFmt='#,##0.0'
    xLabelWrap=true
/>

---

## Reading the Arc

The eight-year trajectory is a story of structural dependency deepening on three fronts. On the revenue side: PMPML cannot cover its payroll from fare revenue alone — employee costs reached 140% of bus income in FY2024-25 — and that gap is widening, not closing. On the liquidity side: short-term borrowings that were zero through FY2019-20 have grown to ₹34 Cr, while cash reserves that peaked at ₹93 Cr in FY2019-20 have not recovered past ₹21 Cr. On the asset side: net fixed assets have depreciated 85% from their FY2019-20 peak without comparable reinvestment, meaning the fleet is aging without replacement capital in sight.

The system continues to function — but only because PMC and PCMC are legally obligated to cover the operating deficit each year, on a schedule set by their own budget cycles. Whether that arrangement scales to cover a deficit now approaching ₹900 Cr annually is a political question that lives outside the financial statements.

## See Also

- **[Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Monthly operational data: fleet utilization, ridership, and revenue by depot
- **[Annual Performance Report](/PCMC/Public%20Transport/Annual_Statistics)** — FY 2023-24 vs 2024-25 operational metrics
- **[Public Transport Overview](/PCMC/Public%20Transport)** — Three eras of bus transit in Pimpri-Chinchwad
- **[BRT Service Statistics](/PCMC/Public%20Transport/BRT)** — Dedicated BRT corridor operations: fleet, ridership, and efficiency
- **[E-Bus Service Statistics](/PCMC/Public%20Transport/EBus)** — Electric bus operations and KMPU energy efficiency tracking

---

*Data covers FY 2017-18 to FY 2024-25 (8 fiscal years). All figures in ₹ Crores (1 Cr = 10 lakhs). Source: [PMPML Annual Financial Statements](https://pmpml.org/financial_performance), Chief Accounts Officer. P&L extraction via Ghostscript (FY17-21) and EasyOCR (FY21-25); balance sheet FY17-21 manually transcribed from scanned documents, FY21-23 via OCR; all cross-validated across consecutive annual reports.*

---

## Data Queries

*SQL queries powering the visualizations above. Evidence.dev processes these at build time.*

```sql pnl_trend
SELECT
    fiscal_year,
    revenue_bus_ops / 100 as revenue_cr,
    total_income / 100 as income_cr,
    total_expenses / 100 as expenses_cr,
    operating_profit_loss / 100 as operating_pl_cr,
    total_reimbursements / 100 as reimbursements_cr,
    net_profit_loss / 100 as net_pl_cr
FROM PMPML_Financial_PnL
ORDER BY fiscal_year
```

```sql emp_ratio
SELECT
    fiscal_year,
    ROUND(employee_benefits / NULLIF(revenue_bus_ops, 0) * 100, 1) as emp_to_revenue_pct,
    employee_benefits / 100 as employee_cr,
    revenue_bus_ops / 100 as revenue_cr
FROM PMPML_Financial_PnL
ORDER BY fiscal_year
```

```sql reimbursements_breakdown
SELECT
    fiscal_year,
    pmc_reimbursement / 100 as pmc_cr,
    pcmc_reimbursement / 100 as pcmc_cr,
    pmrda_reimbursement / 100 as pmrda_cr,
    total_reimbursements / 100 as reimbursements_cr,
    -operating_profit_loss / 100 as operating_deficit_cr
FROM PMPML_Financial_PnL
ORDER BY fiscal_year
```

```sql expense_breakdown
SELECT
    fiscal_year,
    employee_benefits / 100 as employee_cr,
    other_expenses / 100 as other_cr,
    cost_purchases / 100 as fuel_purchase_cr,
    depreciation / 100 as depreciation_cr,
    finance_costs / 100 as finance_cr
FROM PMPML_Financial_PnL
ORDER BY fiscal_year
```
