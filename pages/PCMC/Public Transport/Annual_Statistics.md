---
title: PMPML Annual Performance Report
description: Year-on-year comparison for FY 2023-24 and FY 2024-25 — fleet, ridership, revenue, fuel efficiency, safety, and workshop performance
---

PMPML's annual statistical reports compress a full year of operations into a single comparable table. This page draws on the FY 2023-24 and FY 2024-25 reports (issued June 2025) to track year-on-year changes and highlight metrics that the monthly depot data doesn't surface at system level: **fuel efficiency by propulsion type**, workshop reliability, tyre life, and staff ratios.

The headline story across both years: ridership and revenue both fell roughly 7%, accidents nearly halved (41 → 20 for PMPML own fleet), and e-bus fuel efficiency improved sharply (KMPU 1.10 → 1.36 km/unit). Hired fleet contraction is the structural trend — hired buses declined from 1,071 to 932 held while PMPML own fleet remained stable.

---

## Year-on-Year Headlines

<Grid cols=4>
<BigValue
    data={annual_headline}
    value=passengers_per_day_m
    title="Avg Passengers / Day (lakhs)"
    fmt='#,##0.0" L"'
/>
<BigValue
    data={annual_headline}
    value=total_earning_cr
    title="Total Earning (₹ Cr)"
    fmt='"₹"#,##0.0" Cr"'
/>
<BigValue
    data={annual_headline}
    value=fleet_utilization
    title="Fleet Utilization %"
    fmt='#0.0"%"'
/>
<BigValue
    data={annual_headline}
    value=accidents_total
    title="Total Accidents (PMPML+Hired)"
    fmt='#,##0'
/>
</Grid>

*BigValues show FY 2024-25 values.*

<BarChart
    data={annual_compare}
    x=Particular
    y=pct_change
    title="Year-on-Year % Change: FY 2023-24 → FY 2024-25"
    subtitle="Negative = declined, positive = improved. Accidents and breakdowns declining is good."
    swapXY=true
    yFmt='#0.0"%"'
    colorPalette={['#cd4063']}
    connectGroup="annual"
/>

---

## Fleet

The PMPML own fleet held steady (~944 → 951 vehicles), while the hired fleet contracted significantly (1,071 → 932 per day). PPP fleet remained capped at 50. Total vehicles on road fell from 1,658 to 1,558.

<BarChart
    data={fleet_composition}
    x=Particular
    y={['FY2023_24', 'FY2024_25']}
    type=grouped
    title="Fleet Composition: FY 2023-24 vs FY 2024-25"
    subtitle="PMPML Own, PPP, and Hired vehicles — held and on road"
    swapXY=true
    yFmt='#,##0'
    connectGroup="annual"
/>

<BarChart
    data={fleet_utilization_pct}
    x=Particular
    y={['FY2023_24', 'FY2024_25']}
    type=grouped
    title="Fleet Off-Road Breakdown (%)"
    subtitle="Share of fleet in spare vs workshop maintenance"
    yFmt='#0.0"%"'
    connectGroup="annual"
/>

---

## Ridership and Revenue

Total passengers per day fell from 12.08 lakh to 11.25 lakh (−6.8%). The pass-passenger share held steady at 30–31%, indicating the core commuter base remains intact. Revenue fell proportionally — ₹669 Cr → ₹625 Cr total earning, with earning per passenger barely moving (₹15.15 → ₹15.22), suggesting the ridership decline is volume-driven rather than fare-driven.

<Grid cols=2>
<BarChart
    data={ridership_compare}
    x=Particular
    y={['FY2023_24', 'FY2024_25']}
    type=grouped
    title="Ridership Metrics"
    swapXY=true
    yFmt='#,##0'
    connectGroup="annual"
/>
<BarChart
    data={revenue_compare}
    x=Particular
    y={['FY2023_24_cr', 'FY2024_25_cr']}
    type=grouped
    title="Revenue (₹ Crores)"
    swapXY=true
    yFmt='"₹"#,##0.0'
    connectGroup="annual"
/>
</Grid>

---

## Fuel Efficiency by Propulsion Type

This is the data the monthly reports don't provide at system level. Three fleets, three fuels, three efficiency metrics:

| Metric | FY 2023-24 | FY 2024-25 | Direction |
|--------|-----------|-----------|-----------|
| KMPL Diesel (Own) | 3.48 | 3.55 | ↑ improved |
| KMPG CNG (Own+PPP) | 2.96 | 2.89 | ↓ declined |
| KMPU E-Bus (Own) | 1.10 | 1.36 | ↑ improved (+24%) |

The e-bus KMPU jump from 1.10 to 1.36 is notable — as the e-bus fleet expanded (from 8,512 to 30,114 annual effective KMs), the per-unit efficiency improved, likely reflecting newer vehicles and better route matching.

<BarChart
    data={fuel_efficiency}
    x=Particular
    y={['FY2023_24', 'FY2024_25']}
    type=grouped
    title="Fuel Efficiency by Propulsion Type"
    subtitle="KMPL diesel, KMPG CNG (Own+PPP), KMPU E-Bus (Own)"
    yFmt='#0.0'
    connectGroup="annual"
/>

<BarChart
    data={fuel_consumption_perbus}
    x=Particular
    y={['FY2023_24', 'FY2024_25']}
    type=grouped
    title="Fuel Consumption Per Bus Per Day"
    subtitle="Litres (diesel), Kg (CNG), Units (E-Bus) — intensity of use"
    yFmt='#0.0'
    connectGroup="annual"
/>

---

## Safety

Accidents fell dramatically in 2024-25: PMPML own fleet down from 41 to 20, hired fleet down from 77 to 33. The accident rate per lakh km also halved — this is not just a KMs-denominator effect, it reflects genuine safety improvement. The complete elimination of insignificant accidents in the PMPML fleet (14 → 0) is the starkest signal.

<BarChart
    data={accidents_by_severity}
    x=Particular
    y={['FY2023_24', 'FY2024_25']}
    type=grouped
    title="Accidents by Severity: PMPML Own Fleet"
    subtitle="Fatal, Major, Minor, Insignificant"
    swapXY=true
    yFmt='#,##0'
    connectGroup="annual"
/>

<BarChart
    data={accidents_hired}
    x=Particular
    y={['FY2023_24', 'FY2024_25']}
    type=grouped
    title="Accidents by Severity: Hired Fleet (Olectra E-Bus + CNG Hire)"
    swapXY=true
    yFmt='#,##0'
    connectGroup="annual"
/>

---

## Workshop and Reliability

Breakdowns fell from 7,705 to 6,145 (−20%) and the breakdown rate improved from 1.51 to 1.22 per 10,000 km. Tyre performance also improved — average KMs per new tyre rose from 65,595 to 72,864.

<BarChart
    data={workshop_compare}
    x=Particular
    y={['FY2023_24', 'FY2024_25']}
    type=grouped
    title="Workshop Performance"
    subtitle="Breakdowns and tyre life"
    swapXY=true
    yFmt='#,##0'
    connectGroup="annual"
/>

---

## Passes and Commuter Profile

<DataTable
    data={passes_compare}
    rows=all
>
    <Column id=Particular title="Metric"/>
    <Column id=FY2023_24 title="FY 2023-24" fmt='#,##0'/>
    <Column id=FY2024_25 title="FY 2024-25" fmt='#,##0'/>
</DataTable>

---

## See Also

- **[Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Monthly system-wide dashboard, Jan 2023–Jun 2025
- **[Depot Performance](/PCMC/Public%20Transport/Depot_Performance)** — How individual depots compare on efficiency
- **[Ridership and Fares](/PCMC/Public%20Transport/Ridership_and_Fares)** — Monthly pass type breakdown and revenue mix
- **[E-Bus Statistics](/PCMC/Public%20Transport/EBus)** — KMPU energy efficiency tracked monthly
- **[Road Safety](/PCMC/Road_Accident_Statistics)** — City-wide accident trends and PMPML safety in context

---

*Source: PMPML Statistical Report for FY 2023-2024 & 2024-25, STAT Department, dated 18/06/2025. Note: FY 2024-25 Balance Sheet (cost per KM, row 14) not yet finalised at time of report.*

---

## Data Queries

*SQL queries powering the visualizations above.*

```sql annual_headline
SELECT
    (SELECT TRY_CAST(FY2024_25 AS DOUBLE) / 100000
     FROM Annual_Statistics_2023_2025 WHERE Particular = 'Total Avg Passengers Per Day') as passengers_per_day_m,
    (SELECT TRY_CAST(FY2024_25 AS DOUBLE) / 10000000
     FROM Annual_Statistics_2023_2025 WHERE Particular = 'Total Earning incl Concessional Passes') as total_earning_cr,
    (SELECT TRY_CAST(FY2024_25 AS DOUBLE)
     FROM Annual_Statistics_2023_2025 WHERE Particular = 'Fleet Utilization PMPML+PPP') as fleet_utilization,
    (SELECT TRY_CAST(a1.FY2024_25 AS DOUBLE) + TRY_CAST(a2.FY2024_25 AS DOUBLE)
     FROM Annual_Statistics_2023_2025 a1
     JOIN Annual_Statistics_2023_2025 a2
       ON a1.Particular = 'PMPML Accidents Total'
      AND a2.Particular = 'Hired Accidents Total') as accidents_total
```

```sql annual_compare
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25,
    ROUND(100.0 * (TRY_CAST(FY2024_25 AS DOUBLE) - TRY_CAST(FY2023_24 AS DOUBLE)) /
        NULLIF(TRY_CAST(FY2023_24 AS DOUBLE), 0), 1) as pct_change
FROM Annual_Statistics_2023_2025
WHERE Particular IN (
    'Total Avg Vehicles On Road',
    'Total Schedules Operated Per Day',
    'Total Avg Passengers Per Day',
    'Total Effective KM Own+Hire',
    'PMPML Accidents Total',
    'Hired Accidents Total',
    'Total Breakdowns PMPML Own'
)
ORDER BY pct_change
```

```sql fleet_composition
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25
FROM Annual_Statistics_2023_2025
WHERE Category = 'Fleet'
  AND Particular IN (
    'Avg PMPML Own Vehicles Held',
    'PPP Vehicles Held',
    'Hire Vehicles Per Day',
    'Avg PMPML Own Vehicles On Road',
    'PPP Vehicles On Road',
    'Hire Vehicles On Road',
    'Total Avg Vehicles On Road'
  )
ORDER BY Particular
```

```sql fleet_utilization_pct
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25
FROM Annual_Statistics_2023_2025
WHERE Particular IN (
    'Fleet Utilization PMPML+PPP',
    'Pct Spare Vehicles',
    'Pct Workshop Vehicles'
)
ORDER BY Particular
```

```sql ridership_compare
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25
FROM Annual_Statistics_2023_2025
WHERE Particular IN (
    'Total Avg Passengers Per Day',
    'Avg Ticket Passengers Per Day',
    'Ticket Passengers Per Bus Per Day',
    'Total Passengers Per Bus Per Day'
)
ORDER BY Particular
```

```sql revenue_compare
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) / 10000000 as FY2023_24_cr,
    TRY_CAST(FY2024_25 AS DOUBLE) / 10000000 as FY2024_25_cr
FROM Annual_Statistics_2023_2025
WHERE Particular IN (
    'Passenger Earning Ticket',
    'All Traffic Earning',
    'Total Earning incl Concessional Passes',
    'Commuter Pass Earning',
    'Student Pass Earning'
)
ORDER BY FY2023_24_cr DESC
```

```sql fuel_efficiency
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25
FROM Annual_Statistics_2023_2025
WHERE Particular IN (
    'KMPL Diesel Own',
    'KMPG CNG Own+PPP',
    'KMPU E-Bus Own'
)
ORDER BY Particular
```

```sql fuel_consumption_perbus
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25
FROM Annual_Statistics_2023_2025
WHERE Particular IN (
    'Diesel Per Bus Per Day Own',
    'CNG Per Bus Per Day PMPML+PPP',
    'E-Bus Per Bus Per Day Own'
)
ORDER BY Particular
```

```sql accidents_by_severity
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25
FROM Annual_Statistics_2023_2025
WHERE Category = 'Safety'
  AND Particular LIKE 'PMPML Accidents%'
  AND Particular != 'PMPML Accident Rate Per Lakh KM'
ORDER BY
    CASE Particular
        WHEN 'PMPML Accidents Fatal' THEN 1
        WHEN 'PMPML Accidents Major' THEN 2
        WHEN 'PMPML Accidents Minor' THEN 3
        WHEN 'PMPML Accidents Insignificant' THEN 4
        WHEN 'PMPML Accidents Total' THEN 5
    END
```

```sql accidents_hired
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25
FROM Annual_Statistics_2023_2025
WHERE Category = 'Safety'
  AND Particular LIKE 'Hired Accidents%'
  AND Particular != 'Hired Accident Rate Per Lakh KM'
ORDER BY
    CASE Particular
        WHEN 'Hired Accidents Fatal' THEN 1
        WHEN 'Hired Accidents Major' THEN 2
        WHEN 'Hired Accidents Minor' THEN 3
        WHEN 'Hired Accidents Insignificant' THEN 4
        WHEN 'Hired Accidents Total' THEN 5
    END
```

```sql workshop_compare
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25
FROM Annual_Statistics_2023_2025
WHERE Category = 'Workshop'
ORDER BY Particular
```

```sql passes_compare
SELECT
    Particular,
    TRY_CAST(FY2023_24 AS DOUBLE) as FY2023_24,
    TRY_CAST(FY2024_25 AS DOUBLE) as FY2024_25
FROM Annual_Statistics_2023_2025
WHERE Particular IN (
    'Student Passes Issued',
    'Commuter Passes Issued',
    'Pass Passengers Per Day',
    'Pct Pass Passengers',
    'Total Passenger Complaints',
    'Total Default Cases DEO'
)
ORDER BY Particular
```
