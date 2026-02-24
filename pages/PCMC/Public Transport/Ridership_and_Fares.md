---
title: PMPML Ridership and Fare Structure
description: Pass types, fare tiers, and how the revenue mix is shifting
---

PMPML offers a layered fare system with daily passes, monthly passes, and subsidized student passes. Each tier serves a different segment of the city's commuter population. This page breaks down who buys what, how many, and where the money comes from.

> **Fare revision note:** PMPML revised pass prices during the data period. The column labels in the source data reflect the original (2023) prices. By mid-2025, the Punyadasham pass went from Rs 10 to Rs 20, the combined municipal pass from Rs 50 to Rs 70, the all-route daily pass from Rs 120 to Rs 150, and the monthly both-corporation pass from Rs 1,200 to Rs 1,500. The within-PMC and within-PCMC Rs 40 daily passes were consolidated. Read pass labels as approximate cohort identifiers (low-income daily rider, commuter, long-distance) rather than exact price points — the prices changed partway through the data period.

---

## Daily Pass Landscape

Who buys which pass? PMPML's daily pass structure maps onto income and geography. The Punyadasham pass (originally Rs 10, now Rs 20) serves the lowest-income riders — a deliberate social inclusion measure. The Rs 40 passes serve senior citizens and single-city commuters. The combined municipal pass (originally Rs 50, now Rs 70) covers travel across both PMC and PCMC, while the all-route pass (originally Rs 120, now Rs 150) serves cross-city commuters who need full network access.

<AreaChart
    data={daily_passes}
    x=date_parsed
    y={['pass_10_punyadasham', 'pass_40_sr_citizen', 'pass_40_pmc', 'pass_40_pcmc', 'pass_50_both', 'pass_120_all_route']}
    type=stacked
    title="Daily Passes Sold by Type (System Total per Month)"
    yAxisTitle="Number of Passes"
    yFmt='#,##0'
    connectGroup="ridership-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</AreaChart>

<DataTable
    data={daily_passes}
    rows=all
>
    <Column id=date_parsed title="Month"/>
    <Column id=pass_10_punyadasham title="Rs 10 Punyadasham" fmt='#,##0'/>
    <Column id=pass_40_sr_citizen title="Rs 40 Sr.Citizen" fmt='#,##0'/>
    <Column id=pass_40_pmc title="Rs 40 PMC" fmt='#,##0'/>
    <Column id=pass_40_pcmc title="Rs 40 PCMC" fmt='#,##0'/>
    <Column id=pass_50_both title="Rs 50 Both" fmt='#,##0'/>
    <Column id=pass_120_all_route title="Rs 120 All Route" fmt='#,##0'/>
</DataTable>

The volume distribution tells a story about PMPML's ridership base. The Rs 10 Punyadasham pass exists for social welfare — providing basic mobility to those who cannot afford even Rs 40. The within-city Rs 40 passes dominate in volume, reflecting the reality that most bus trips are within a single municipal boundary. The Rs 120 all-route pass, despite its higher price, captures commuters whose daily patterns span the full PMC-PCMC corridor.

---

## Monthly Pass Subscribers

Monthly pass holders are the commuter core — the riders who have made a deliberate decision to use PMPML as their primary mode of transport. The ratio of monthly to daily pass holders is a useful indicator of how many riders treat the bus as a regular commute tool versus an occasional fallback.

<AreaChart
    data={monthly_passes}
    x=date_parsed
    y={['monthly_500_sr_citizen', 'monthly_700_corp_employee', 'monthly_900_one_corp', 'monthly_1200_both_corp', 'monthly_2700_all_route']}
    type=stacked
    title="Monthly Pass Subscribers by Type (System Total)"
    yAxisTitle="Number of Pass Holders"
    yFmt='#,##0'
    connectGroup="ridership-monthly"
/>

<AreaChart
    data={monthly_passes_long}
    x=date_parsed
    y=passes
    series=pass_type
    type=stacked100
    title="Monthly Pass Mix (Share of Total)"
    yAxisTitle="Share %"
    connectGroup="ridership-monthly"
/>

<DataTable
    data={monthly_passes}
    rows=all
>
    <Column id=date_parsed title="Month"/>
    <Column id=monthly_500_sr_citizen title="Rs 500 Sr.Citizen" fmt='#,##0'/>
    <Column id=monthly_700_corp_employee title="Rs 700 Corp.Employee" fmt='#,##0'/>
    <Column id=monthly_900_one_corp title="Rs 900 One Corp" fmt='#,##0'/>
    <Column id=monthly_1200_both_corp title="Rs 1200 Both Corp" fmt='#,##0'/>
    <Column id=monthly_2700_all_route title="Rs 2700 All Route" fmt='#,##0'/>
</DataTable>

The Rs 700 municipal corporation employee pass is notable — it represents a captive institutional ridership channel. The single-corporation pass (originally Rs 900, later revised to Rs 1,500 for both corporations combined) tends to dominate, reinforcing the pattern seen in daily passes: most PMPML ridership is intra-city, not cross-city. The Rs 2,700 all-route monthly pass, despite being the most expensive, captures regular long-distance commuters for whom no alternative is affordable. The percentage view reveals whether any segment is growing faster than others — a shift toward higher-value passes would indicate growing cross-city demand.

---

## Student Ridership

Student passes are a distinct category: subsidized, seasonal, and large in volume. PMPML issues student passes at concessional rates, making the academic calendar visible in the ridership data.

<LineChart
    data={student_ridership}
    x=date_parsed
    y=student_passes_issued
    title="Student Passes Issued per Month (System Total)"
    yAxisTitle="Number of Passes"
    yFmt='#,##0'
    connectGroup="ridership-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

<LineChart
    data={student_ridership}
    x=date_parsed
    y=student_revenue_lakhs
    title="Revenue from Student Passes (Rs Lakhs per Month)"
    yAxisTitle="Revenue (Rs Lakhs)"
    yFmt='#,##0.0'
    connectGroup="ridership-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

<DataTable
    data={student_ridership}
    rows=all
>
    <Column id=date_parsed title="Month"/>
    <Column id=student_passes_issued title="Passes Issued" fmt='#,##0'/>
    <Column id=student_revenue_lakhs title="Revenue (Rs Lakhs)" fmt='#,##0.0'/>
</DataTable>

The seasonal pattern should mirror the academic calendar — dips during summer vacations (April-May) and Diwali breaks (October-November), with peaks during exam months. The revenue per pass indicates the effective subsidy rate. Student passes represent a significant social investment by PMPML: high ridership volume at heavily discounted fares. The scale of this subsidy — potentially tens of thousands of passes per month across all depots — is worth tracking because it directly affects per-passenger revenue metrics even as it fulfils an important public service mandate.

---

## Revenue Composition Over Time

Where does the money come from? PMPML earns revenue from three primary streams: ticket sales (pay-per-ride), commuter passes (daily + monthly combined), and student passes. The balance between these streams reveals how the system's financial structure is evolving.

<AreaChart
    data={revenue_composition}
    x=date_parsed
    y={['ticket_earnings_cr', 'pass_earnings_cr', 'student_earnings_cr']}
    type=stacked
    title="Monthly Revenue by Source (Rs Crores)"
    yAxisTitle="Revenue (Rs Crores)"
    yFmt='#,##0.00'
    connectGroup="ridership-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</AreaChart>

<AreaChart
    data={revenue_composition_long}
    x=date_parsed
    y=revenue_cr
    series=source
    type=stacked100
    title="Revenue Mix (Share of Total)"
    subtitle="How the balance between tickets, passes, and student fares is shifting"
    yAxisTitle="Share %"
    connectGroup="ridership-monthly"
/>

<DataTable
    data={revenue_composition}
    rows=all
>
    <Column id=date_parsed title="Month"/>
    <Column id=ticket_earnings_cr title="Ticket Sales (Rs Cr)" fmt='#,##0.00'/>
    <Column id=pass_earnings_cr title="Passes D+M (Rs Cr)" fmt='#,##0.00'/>
    <Column id=student_earnings_cr title="Student (Rs Cr)" fmt='#,##0.00'/>
    <Column id=total_earnings_cr title="Total (Rs Cr)" fmt='#,##0.00'/>
</DataTable>

A system that depends heavily on ticket sales is one where most riders are occasional users — they pay full fare each time because they do not ride often enough to justify a pass. As the pass share grows, it signals a shift toward a committed commuter base: financially more predictable, but at lower per-ride revenue since passes are inherently discounted. The ideal balance is debatable — passes improve ridership stability but compress margins. If the pass share is growing while total revenue is also growing, the system is successfully converting occasional riders into regular users without sacrificing aggregate income.

---

## Tourism Services

PMPML operates two niche tourism services: Pune Darshan Seva (city sightseeing) and Pune Parytan (extended tours). These are not core transit services but they serve a visibility and public engagement function.

<LineChart
    data={tourism}
    x=date_parsed
    y={['pune_darshan', 'pune_parytan']}
    title="Tourism Services (Monthly Counts, System Total)"
    yAxisTitle="Count"
    yFmt='#,##0'
    connectGroup="ridership-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

Tourism services are a small fraction of PMPML's overall operations, but they indicate institutional ambition beyond basic commuter transport. Pune Darshan in particular is a recognizable brand in the city. Seasonal patterns here — peaks during school holidays and the October-November festival season — would confirm that these services cater primarily to leisure and visiting populations rather than regular commuters.

---

## Data Queries

*SQL queries powering the visualizations above. Evidence.dev processes these at build time — position in the file does not affect rendering.*

```sql daily_passes
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    Date as month_label,
    SUM(TRY_CAST("One Day Passes ₹ 10 (Punyadasham)" AS DOUBLE)) as pass_10_punyadasham,
    SUM(TRY_CAST("One Day Passes ₹ 40 (Sr.Citizen)" AS DOUBLE)) as pass_40_sr_citizen,
    SUM(TRY_CAST("One Day Passes ₹ 40 (within PMC Limit)" AS DOUBLE)) as pass_40_pmc,
    SUM(TRY_CAST("One Day Passes ₹ 40 (within PCMC Limit)" AS DOUBLE)) as pass_40_pcmc,
    SUM(TRY_CAST("One Day Passes ₹ 50 (within Both Municipal limit)" AS DOUBLE)) as pass_50_both,
    SUM(TRY_CAST("One Day Passes ₹ 120 (All Route)" AS DOUBLE)) as pass_120_all_route
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

```sql monthly_passes
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    Date as month_label,
    SUM(TRY_CAST("Monthly Passes ₹ 500 (Sr.Citizens)" AS DOUBLE)) as monthly_500_sr_citizen,
    SUM(TRY_CAST("Monthly Passes ₹ 700 (Mun.Corpn.Employees)" AS DOUBLE)) as monthly_700_corp_employee,
    SUM(TRY_CAST("Monthly Passes ₹ 900 (within One Mun.Corpn.)" AS DOUBLE)) as monthly_900_one_corp,
    SUM(TRY_CAST("Monthly Passes ₹ 1200 (within Both Mun.Corpn.)" AS DOUBLE)) as monthly_1200_both_corp,
    SUM(TRY_CAST("Monthly Passes ₹ 2700 (All Route)" AS DOUBLE)) as monthly_2700_all_route
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

```sql monthly_passes_long
SELECT STRPTIME(Date, '%b %Y') as date_parsed, '₹500 Sr.Citizen' as pass_type,
    SUM(TRY_CAST("Monthly Passes ₹ 500 (Sr.Citizens)" AS DOUBLE)) as passes
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, date_parsed
UNION ALL
SELECT STRPTIME(Date, '%b %Y'), '₹700 Corp.Employee',
    SUM(TRY_CAST("Monthly Passes ₹ 700 (Mun.Corpn.Employees)" AS DOUBLE))
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, STRPTIME(Date, '%b %Y')
UNION ALL
SELECT STRPTIME(Date, '%b %Y'), '₹900 One Corp',
    SUM(TRY_CAST("Monthly Passes ₹ 900 (within One Mun.Corpn.)" AS DOUBLE))
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, STRPTIME(Date, '%b %Y')
UNION ALL
SELECT STRPTIME(Date, '%b %Y'), '₹1200 Both Corp',
    SUM(TRY_CAST("Monthly Passes ₹ 1200 (within Both Mun.Corpn.)" AS DOUBLE))
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, STRPTIME(Date, '%b %Y')
UNION ALL
SELECT STRPTIME(Date, '%b %Y'), '₹2700 All Route',
    SUM(TRY_CAST("Monthly Passes ₹ 2700 (All Route)" AS DOUBLE))
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, STRPTIME(Date, '%b %Y')
ORDER BY date_parsed, pass_type
```

```sql student_ridership
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    Date as month_label,
    SUM(TRY_CAST("Total no.of Student Passes issued" AS DOUBLE)) as student_passes_issued,
    SUM(TRY_CAST("Amt. recd from Student Passes (₹)" AS DOUBLE)) / 100000 as student_revenue_lakhs
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

```sql revenue_composition
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    Date as month_label,
    SUM(TRY_CAST("Passenger Earning (Sale of Ticket)(₹)" AS DOUBLE)) / 10000000 as ticket_earnings_cr,
    SUM(TRY_CAST("Gr.Total (Daily+Monthly) (₹)" AS DOUBLE)) / 10000000 as pass_earnings_cr,
    SUM(TRY_CAST("Amt. recd from Student Passes (₹)" AS DOUBLE)) / 10000000 as student_earnings_cr,
    SUM(TRY_CAST("All Traffic Earning (₹)" AS DOUBLE)) / 10000000 as total_earnings_cr
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

```sql revenue_composition_long
SELECT STRPTIME(Date, '%b %Y') as date_parsed, 'Ticket Sales' as source,
    SUM(TRY_CAST("Passenger Earning (Sale of Ticket)(₹)" AS DOUBLE)) / 10000000 as revenue_cr
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, date_parsed
UNION ALL
SELECT STRPTIME(Date, '%b %Y'), 'Commuter Passes',
    SUM(TRY_CAST("Gr.Total (Daily+Monthly) (₹)" AS DOUBLE)) / 10000000
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, STRPTIME(Date, '%b %Y')
UNION ALL
SELECT STRPTIME(Date, '%b %Y'), 'Student Passes',
    SUM(TRY_CAST("Amt. recd from Student Passes (₹)" AS DOUBLE)) / 10000000
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, STRPTIME(Date, '%b %Y')
ORDER BY date_parsed, source
```

```sql tourism
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    Date as month_label,
    SUM(TRY_CAST("Pune Darshan Seva" AS DOUBLE)) as pune_darshan,
    SUM(TRY_CAST("Pune Parytan" AS DOUBLE)) as pune_parytan
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

## See Also

- **[Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Monthly fleet dashboard: vehicle deployment, kilometers, revenue, fuel efficiency, safety, and depot comparisons
- **[PCMT Before PMPML](/PCMC/Public%20Transport/PCMT_before_PMPML)** — Historical context: how PCMT operated before the 2007 merger

---

*Data covers Jan 2023 – Dec 2025 with gaps (Jan–Mar 2024, Nov 2024–Mar 2025, Jul–Sep 2025 missing). Source: [PMPML Chief Statistician monthly reports](https://pmpml.org/statistics).*
