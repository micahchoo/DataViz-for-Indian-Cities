---
title: PMPML Fleet Monthly Depotwise reports
description: Fleet data per depot per month across 22 months from January 2023 to June 2025 (with coverage gaps)
sidebar: show
---

## PMPML Fleet Monthly Depotwise reports
Fleet data per depot per month across 22 months from January 2023 to June 2025. Coverage is not continuous — Jan–Mar 2024 and Nov 2024–Mar 2025 are missing from the source reports. This period falls during post-COVID ridership recovery — PMPML ridership had collapsed during 2020-21 lockdowns and was still rebuilding toward pre-pandemic levels through 2023-2024.

This page lets you explore individual depot metrics over time. For a cross-depot comparison, see [Depot Performance](/PCMC/Public%20Transport/Depot_Performance).

**Known data quality notes:** February 2023 "All Traffic Earning" was corrupted in the source PDF extraction (tabula column shift); it has been imputed as ticket + pass + student earnings. December 2023 fleet utilization exceeded 100% at Pune Station (200%) and Nigadi (117%) — a source formula quirk; capped at 100% in all SQL. April 2023 ticket-only EPK was corrupted; imputed from earnings/km. January and March 2023: the "Sanctioned" and "Operated" schedule columns are swapped for 8 depots — schedule queries use GREATEST/LEAST to reconstruct the correct values. November 2023 Nigadi "Gross KMs per own bus" is anomalously high (541 km/bus/day vs. typical 150–200); the `Total Gross KMs (Diesel+CNG+E)` column is structurally unreliable and is not used in any visualisation here — use `Total Dead KMs (Diesel+CNG+E)` (which is independently recorded and reliable) if dead-km data is needed.
```sql summary_metrics
-- Each row is MONTHLY data for ONE DEPOT
-- To get system-wide metrics, we aggregate across ALL depots and months
SELECT 
    COUNT(DISTINCT Date) as total_months,
    COUNT(DISTINCT Depot) as total_depots,
    -- System-wide average daily fleet (average across all depot-months)
    ROUND(AVG(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0) as avg_fleet_per_depot,
    -- System-wide monthly average of daily passengers (sum across depots, then average across months)
    ROUND(AVG(monthly_passengers), 0) as avg_daily_passengers_system,
    -- Total revenue across all depots and months (in crores)
    ROUND(SUM(TRY_CAST("All Traffic Earning (₹)" AS DOUBLE)) / 10000000, 2) as total_revenue_crores,
    -- Average utilization rate across all depot-months
    ROUND(AVG(LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0)), 1) as avg_fleet_utilization_pct,
    -- Average km per bus across all depot-months
    ROUND(AVG(TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE)), 1) as avg_km_per_bus_per_day
FROM (
    SELECT 
        Date,
        Depot,
        "Total Vehicles Per Day",
        "% of Fleet Utilization(PMPML+PPP)",
        "Effective Km Per Bus Per day",
        "All Traffic Earning (₹)",
        SUM(TRY_CAST("Avg. Passenger per day on Traffic (including Ticket Sales, Commuters Passes, Student Passes, Monthly Passes & Casual Contract, Luxury Service, Mobile App etc.)" AS DOUBLE)) 
            OVER (PARTITION BY Date) as monthly_passengers
    FROM extracted
    WHERE Date IS NOT NULL
) e1
```

<Grid cols=4>
<BigValue
  data={summary_metrics}
  value=total_months
  title="Months Analyzed"
/>

<BigValue
  data={summary_metrics}
  value=avg_daily_passengers_system
  title="Avg Daily Passengers (System)"
  fmt='#,##0'
/>

<BigValue
  data={summary_metrics}
  value=total_revenue_crores
  title="Total Revenue (₹ Cr)"
  fmt='"₹"#,##0.00" Cr"'
/>

<BigValue
  data={summary_metrics}
  value=avg_fleet_utilization_pct
  title="Fleet Utilization %"
  fmt='#0.0"%"'
/>
</Grid>

---

## Fleet Operations Overview

### Vehicle Deployment Trends

```sql fleet_trends
-- Each date represents a MONTH, each row is one depot's monthly data
-- Sum across depots to get system-wide monthly averages
SELECT
        Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    -- System-wide monthly average daily metrics (sum all depots)
    SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) as system_avg_vehicles_per_day,
    SUM(TRY_CAST("Total Avg.Veh- On Road Per Day" AS DOUBLE)) as system_avg_on_road,
    SUM(TRY_CAST("Total Vehicles Off Road Per Day" AS DOUBLE)) as system_avg_off_road,
    SUM(TRY_CAST("Avg.Workshop Vehicles Per Day" AS DOUBLE)) as system_avg_workshop,
    -- Weighted average utilization by fleet size
    ROUND(
        SUM(LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as fleet_utilization_pct
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_year
ORDER BY date_parsed
```

<BarChart
data={fleet_trends}
x=date_parsed
y={['system_avg_on_road', 'system_avg_off_road']}
type=stacked
title="Monthly System-Wide Average Daily Vehicle Status"
yAxisTitle="Number of Vehicles (Daily Average)"
connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</BarChart>

<LineChart
 data={fleet_trends}
 x=date_parsed
 y=fleet_utilization_pct
 title="Monthly System Fleet Utilization Rate"
 yAxisTitle="Utilization %"
 yFmt='#0.0'
 connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

---

## Operational Efficiency

### Kilometers Operated

```sql km_trends
-- Monthly totals: sum across all depots for the month
SELECT 
    Date as month_date,
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    -- Monthly totals (sum across all depots for the month)
    SUM(TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)) / 100000 as monthly_effective_kms_lakhs,
    SUM(TRY_CAST("Total Dead KMs (Diesel+CNG+E)" AS DOUBLE)) / 100000 as monthly_dead_kms_lakhs,
    SUM(TRY_CAST("Total Cancelled KMs" AS DOUBLE)) / 100000 as monthly_cancelled_kms_lakhs,
    -- Average efficiency: weighted average across depots
    ROUND(
        SUM(TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as avg_km_per_bus_per_day
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_year
ORDER BY date_parsed
```

<AreaChart
    data={km_trends}
    x=date_parsed
    y={['monthly_effective_kms_lakhs', 'monthly_dead_kms_lakhs', 'monthly_cancelled_kms_lakhs']}
    type=stacked
    handleMissing=gap
    title="Monthly Kilometers by Type (System Total, lakhs)"
    yAxisTitle="Kilometers (lakhs)"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</AreaChart>

<LineChart
 data={km_trends}
 x=date_parsed
 y=avg_km_per_bus_per_day
 title="Monthly System-Wide Average KMs Per Bus Per Day"
 yAxisTitle="KMs/Bus/Day"
 connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

---

## Revenue Performance

### Earnings Analysis

```sql revenue_trends
-- Monthly revenue: sum across all depots
SELECT 
        Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    SUM(TRY_CAST("Passenger Earning (Sale of Ticket)(₹)" AS DOUBLE)) / 10000000 as ticket_sales_crores,
    SUM(TRY_CAST("All Traffic Earning (₹)" AS DOUBLE)) / 10000000 as total_revenue_crores,
    -- Weighted averages
    ROUND(
        SUM(TRY_CAST("Earning per KMs in Rs.(EPK) (₹)" AS DOUBLE) * 
            TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)), 0)
    , 2) as earning_per_km,
    ROUND(
        SUM(TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 0) as earning_per_vehicle,
    SUM(TRY_CAST("Avg. Passenger per day on Traffic (including Ticket Sales, Commuters Passes, Student Passes, Monthly Passes & Casual Contract, Luxury Service, Mobile App etc.)" AS DOUBLE)) as monthly_daily_passengers
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_year
ORDER BY date_parsed
```

<LineChart
    data={revenue_trends}
    x=date_parsed
    y={['ticket_sales_crores', 'total_revenue_crores']}
    title="Monthly Revenue Trends (₹ Crores)"
    yAxisTitle="Revenue (₹ Crores)"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

<LineChart
    data={revenue_trends}
    x=date_parsed
    y=earning_per_km
    title="Monthly System-Wide Earnings Per Kilometer"
    yAxisTitle="₹ per KM"
    yFmt='#,##0.00'
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

### Passenger Metrics

```sql passenger_metrics
SELECT 
        Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    -- Monthly system-wide daily passengers (sum across all depots)
    SUM(TRY_CAST("Avg. Passenger per day on Traffic (including Ticket Sales, Commuters Passes, Student Passes, Monthly Passes & Casual Contract, Luxury Service, Mobile App etc.)" AS DOUBLE)) as daily_passengers_system,
    -- Weighted average passengers per bus
    ROUND(
        SUM(TRY_CAST("Avg Passenger per Bus per day on Traffic" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 0) as passengers_per_bus,
    -- Weighted average load factor
    ROUND(
        SUM(TRY_CAST("% Load Factor on- 2. On Total Traffic Receipts i.e. (Earning from All types of Passes, Luxury, Monthly Contract, Casual Contract etc. as per Depotwise Eff. KM)" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as load_factor_pct
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_year
ORDER BY date_parsed
```

<LineChart
    data={passenger_metrics}
    x=date_parsed
    y=daily_passengers_system
    title="Monthly System-Wide Daily Passenger Count"
    yAxisTitle="Passengers (Daily Average)"
    yFmt='#,##0'
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<LineChart
    data={passenger_metrics}
    x=date_parsed
    y=load_factor_pct
    title="Monthly System Load Factor"
    yAxisTitle="Load Factor %"
    yFmt='#0.0'
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

### Pass Holder Share

```sql pass_holder_share
SELECT
    Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    SUM(TRY_CAST("Avg. Passenger travel per day (On Ticket Sale)" AS DOUBLE)) as ticket_passengers,
    SUM(TRY_CAST("Avg. Passenger per day on Traffic (including Ticket Sales, Commuters Passes, Student Passes, Monthly Passes & Casual Contract, Luxury Service, Mobile App etc.)" AS DOUBLE)) as total_passengers,
    ROUND((1 - SUM(TRY_CAST("Avg. Passenger travel per day (On Ticket Sale)" AS DOUBLE)) /
        NULLIF(SUM(TRY_CAST("Avg. Passenger per day on Traffic (including Ticket Sales, Commuters Passes, Student Passes, Monthly Passes & Casual Contract, Luxury Service, Mobile App etc.)" AS DOUBLE)), 0)) * 100, 1) as pass_holder_pct
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

<LineChart
    data={pass_holder_share}
    x=date_parsed
    y=pass_holder_pct
    title="Non-Ticket Riders as % of Total Passengers"
    subtitle="Non-ticket riders (pass holders, monthly commuters, mobile app) account for ~30-32% of traffic"
    yAxisTitle="Pass Holder Share (%)"
    yFmt='#0.0'
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

The growing share of non-ticket riders (passes, contracts, mobile app) indicates a maturing commuter base. This is a double-edged trend: regular commuters are good for ridership stability, but passes are typically discounted relative to tickets, compressing per-passenger revenue.

### Revenue Sources

```sql revenue_sources
-- Total revenue across all months and depots by source
SELECT 
    'Ticket Sales' as category,
    SUM(TRY_CAST("Passenger Earning (Sale of Ticket)(₹)" AS DOUBLE)) / 10000000 as revenue_crores
FROM extracted WHERE Date IS NOT NULL
UNION ALL
SELECT 
    'Student Passes',
    SUM(TRY_CAST("Amt. recd from Student Passes (₹)" AS DOUBLE)) / 10000000
FROM extracted WHERE Date IS NOT NULL
UNION ALL
SELECT 
    'Commuter Passes',
    SUM(TRY_CAST("Gr.Total (Daily+Monthly) (₹)" AS DOUBLE)) / 10000000
FROM extracted WHERE Date IS NOT NULL
ORDER BY revenue_crores DESC
```

<BarChart 
    data={revenue_sources}
    x=category
    y=revenue_crores
    swapXY=true
    title="Total Revenue by Source (₹ Crores)"
    yAxisTitle="Revenue (₹ Crores)"
/>

---

## Fuel & Energy Efficiency

### Fleet Composition by Fuel Type

```sql fuel_kms
-- Monthly KMs by fuel type (sum across all depots).
-- Diesel: the "Total Eff;km.Diesel (Own+PPP)" column is null for all 2024+ rows due
-- to a PDF extraction change. We back-calculate as KMPL × diesel_consumption_own
-- (own-fleet only, which is ~95%+ of diesel km based on 2023 data where both are available).
SELECT
    Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    SUM(COALESCE(
        NULLIF(TRY_CAST("Total Eff;km.Diesel (Own+PPP)" AS DOUBLE), 0),
        TRY_CAST("KMs per Litre of Diesel (KMPL)(Own)" AS DOUBLE) *
        TRY_CAST("Diesel Consumption in Litres- PMPML(Own)" AS DOUBLE)
    )) / 1000000 as diesel_kms_millions,
    SUM(TRY_CAST("Total Eff.km CNG (Own+PPP)" AS DOUBLE)) / 1000000 as cng_kms_millions,
    SUM(TRY_CAST("Total Eff.km E-Bus (Own)" AS DOUBLE)) / 1000000 as ebus_kms_millions
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_year
ORDER BY date_parsed
```

<AreaChart
    data={fuel_kms}
    x=date_parsed
    y={['cng_kms_millions', 'diesel_kms_millions', 'ebus_kms_millions']}
    type=stacked
    handleMissing=gap
    title="Monthly Kilometers by Fuel Type (Millions)"
    yAxisTitle="Kilometers (Millions)"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</AreaChart>

```sql fuel_kms_long
-- Same back-calculation for diesel as fuel_kms above.
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    'CNG' as fuel_type,
    SUM(TRY_CAST("Total Eff.km CNG (Own+PPP)" AS DOUBLE)) / 1000000 as kms
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, date_parsed
UNION ALL
SELECT
    STRPTIME(Date, '%b %Y'),
    'Diesel',
    SUM(COALESCE(
        NULLIF(TRY_CAST("Total Eff;km.Diesel (Own+PPP)" AS DOUBLE), 0),
        TRY_CAST("KMs per Litre of Diesel (KMPL)(Own)" AS DOUBLE) *
        TRY_CAST("Diesel Consumption in Litres- PMPML(Own)" AS DOUBLE)
    )) / 1000000
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, STRPTIME(Date, '%b %Y')
UNION ALL
SELECT
    STRPTIME(Date, '%b %Y'),
    'E-Bus',
    SUM(TRY_CAST("Total Eff.km E-Bus (Own)" AS DOUBLE)) / 1000000
FROM extracted WHERE Date IS NOT NULL GROUP BY Date, STRPTIME(Date, '%b %Y')
ORDER BY date_parsed, fuel_type
```

<AreaChart
    data={fuel_kms_long}
    x=date_parsed
    y=kms
    series=fuel_type
    type=stacked100
    handleMissing=gap
    title="Fuel Mix Share (%)"
    subtitle="Diesel share grew from ~5% (Jan 2023) to ~16% (Jun 2025) — 2024+ diesel estimated from consumption × efficiency"
    yAxisTitle="Share of Total KMs"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</AreaChart>

Counter to typical "green fleet" expectations, PMPML's own fleet is shifting *toward* diesel and *away* from CNG. Diesel's share grew from ~5% in early 2023 to ~16% by mid-2025. The source reports stopped including a direct diesel-km column after December 2023; 2024–2025 figures are estimated as `KMPL × diesel consumption (own fleet)` — a proxy that agreed within ~20% of the direct values in 2023. E-Bus km reads as zero here because the contracted e-bus fleet (Olectra Greentech) runs under a separate reporting stream — see the [E-Bus page](/PCMC/Public%20Transport/EBus).

### Fuel Efficiency Trends

Note: Diesel efficiency is in km/litre and CNG in km/kg — these are not directly comparable since diesel and CNG have different energy densities (~36 MJ/litre vs ~48 MJ/kg). These charts track each fuel type's efficiency trend over time, not relative performance between fuels.

```sql fuel_efficiency
-- Monthly weighted average efficiency
SELECT 
        Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    ROUND(AVG(TRY_CAST("KMs per Litre of Diesel (KMPL)(Own)" AS DOUBLE)), 2) as diesel_kmpl,
    ROUND(AVG(TRY_CAST("KMs per Kg.of CNG (KMPG)(Own)" AS DOUBLE)), 2) as cng_kmpg,
    ROUND(AVG(TRY_CAST("KMs per Unit of E-Bus(KMPU)(Own)" AS DOUBLE)), 2) as ebus_kmpu
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_year
ORDER BY date_parsed
```

<LineChart
    data={fuel_efficiency}
    x=date_parsed
    y=diesel_kmpl
    title="Monthly Average Diesel Efficiency (KMPL)"
    yAxisTitle="Kilometers per Litre"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

<LineChart
    data={fuel_efficiency}
    x=date_parsed
    y=cng_kmpg
    title="Monthly Average CNG Efficiency (KMPG)"
    yAxisTitle="Kilometers per Kg"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

---

## Safety & Maintenance

### Accident Metrics

```sql safety_metrics
-- Monthly system totals (sum across all depots)
SELECT 
        Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    SUM(TRY_CAST("No.of Accidents (PMPML) 1. Fatal" AS DOUBLE)) as fatal_accidents,
    SUM(TRY_CAST("No.of Accidents (PMPML) 2. Major" AS DOUBLE)) as major_accidents,
    SUM(TRY_CAST("No.of Accidents (PMPML) 3. Minor" AS DOUBLE)) as minor_accidents,
    SUM(TRY_CAST("No.of Accidents (PMPML) Total" AS DOUBLE)) as total_accidents,
    -- Weighted average accident rate
    ROUND(
        SUM(TRY_CAST("Rate of Accidents per 1 Lakh KMs (PMPML)" AS DOUBLE) *
            TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)) /
        NULLIF(SUM(TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)), 0)
    , 2) as accident_rate
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_year
ORDER BY date_parsed
```

<BarChart
    data={safety_metrics}
    x=date_parsed
    y={['fatal_accidents', 'major_accidents', 'minor_accidents']}
    type=stacked
    title="Monthly Accident Count by Severity (System Total)"
    yAxisTitle="Number of Accidents"
    connectGroup="system-monthly"
/>

### Breakdown Analysis

```sql breakdown_metrics
-- Monthly system totals
SELECT 
        Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    SUM(TRY_CAST("Total no.of Breakdown (PMPML Own)" AS DOUBLE)) as total_breakdowns,
    -- Weighted average breakdown rate
    ROUND(
        SUM(TRY_CAST("Breakdown rate per 10,000 KMs" AS DOUBLE) * 
            TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)), 0)
    , 2) as breakdown_rate
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_year
ORDER BY date_parsed
```

<LineChart
    data={breakdown_metrics}
    x=date_parsed
    y=total_breakdowns
    title="Monthly System-Wide Breakdowns"
    yAxisTitle="Number of Breakdowns"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

### Tyre Life

Average kilometers per new tyre measures how hard the fleet is being worked and how good the road/driving conditions are. Lower tyre life = more demanding routes or harder driving. Annual_Statistics shows tyre life improved from 65,595 km to 72,864 km (FY 2023-24 → 2024-25); the monthly view shows whether that improvement was gradual or step-change.

```sql tyre_life
SELECT
    Date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    SUM(TRY_CAST("No.of New Tyres removed for retreading" AS DOUBLE)) as new_tyres_pulled,
    ROUND(
        SUM(TRY_CAST("Avg. KMs per New Tyres" AS DOUBLE) * TRY_CAST("No.of New Tyres removed for retreading" AS DOUBLE)) /
        NULLIF(SUM(TRY_CAST("No.of New Tyres removed for retreading" AS DOUBLE)), 0)
    , 0) as avg_km_per_new_tyre
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

<LineChart
    data={tyre_life}
    x=date_parsed
    y=avg_km_per_new_tyre
    title="Monthly Average KMs per New Tyre (System Total)"
    subtitle="Higher = tyres last longer. Weighted by new tyres pulled per depot."
    yAxisTitle="Km per Tyre"
    yFmt='#,##0'
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

### Engine Oil Efficiency

Engine oil km/litre (km operated per litre of engine oil consumed) is a proxy for engine health: degrading engines consume oil faster and return lower km/litre. Higher values indicate better-maintained engines. Coverage is partial (~53% of depot-months have non-null values); months with no oil consumption recorded are excluded from the aggregate.

```sql engine_oil
SELECT
    Date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    -- Weighted average km/litre weighted by litres consumed (where available)
    ROUND(
        SUM(
            CASE WHEN TRY_CAST("Kilometer per Litre of Engine oil (Total)" AS DOUBLE) > 0
                      AND TRY_CAST("Engine Oil Cons.in Litres per day (Total)" AS DOUBLE) > 0
                 THEN TRY_CAST("Kilometer per Litre of Engine oil (Total)" AS DOUBLE) *
                      TRY_CAST("Engine Oil Cons.in Litres per day (Total)" AS DOUBLE)
                 ELSE NULL END
        ) / NULLIF(
            SUM(
                CASE WHEN TRY_CAST("Kilometer per Litre of Engine oil (Total)" AS DOUBLE) > 0
                          AND TRY_CAST("Engine Oil Cons.in Litres per day (Total)" AS DOUBLE) > 0
                     THEN TRY_CAST("Engine Oil Cons.in Litres per day (Total)" AS DOUBLE)
                     ELSE NULL END
            ), 0)
    , 0) as avg_kmpl_oil,
    SUM(TRY_CAST("Engine Oil Cons.in Litres per day (Total)" AS DOUBLE)) as total_litres_per_day
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
HAVING avg_kmpl_oil IS NOT NULL
ORDER BY date_parsed
```

<LineChart
    data={engine_oil}
    x=date_parsed
    y=avg_kmpl_oil
    title="Monthly Average Engine Oil Efficiency (Km/Litre)"
    subtitle="Weighted by litres consumed per depot. Months without oil records excluded."
    yAxisTitle="Km per Litre of Oil"
    yFmt='#,##0'
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

---

## Staff & Workforce

PMPML's prescribed staffing norm is 9.0 bus staff per vehicle (1.0 admin + 6.5 traffic + 1.5 workshop). The actual system-wide ratio runs around 4.0 — roughly half the norm. The traffic sub-ratio (drivers, conductors, supervisors) bears the most weight: actual ~3.1 vs norm 6.5. The admin sub-ratio is the most severely understaffed: actual ~0.17 vs norm 1.0. Workshop staffing sits at ~0.6 vs norm 1.5.

This persistent half-norm staffing constrains both operations (fewer drivers = fewer schedules can run) and safety oversight (fewer supervisors per bus). It is partly structural — PMPML relies on PPP and hired fleet whose drivers are not counted in PMPML's own staff ratios — and partly reflects recruitment/retention constraints within a corporation that cannot freely set salaries.

```sql staff_ratio
SELECT
    Date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    -- Fleet-weighted average actual staff per bus
    ROUND(
        SUM(
            TRY_CAST("Total Bus Staff ratio – Norm Total (A+B+C) - 9.00" AS DOUBLE) *
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)
        ) / NULLIF(
            SUM(CASE WHEN TRY_CAST("Total Bus Staff ratio – Norm Total (A+B+C) - 9.00" AS DOUBLE) > 0
                     THEN TRY_CAST("Total Vehicles Per Day" AS DOUBLE) END)
        , 0)
    , 2) as actual_ratio
FROM extracted
WHERE Date IS NOT NULL
  AND TRY_CAST("Total Bus Staff ratio – Norm Total (A+B+C) - 9.00" AS DOUBLE) > 0
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

<LineChart
    data={staff_ratio}
    x=date_parsed
    y=actual_ratio
    title="System-Wide Staff per Bus (Actual vs. Norm 9.0)"
    subtitle="Norm of 9.0 bus staff per vehicle (admin + traffic + workshop)"
    yAxisTitle="Staff per Bus"
    yFmt='#0.00'
    connectGroup="system-monthly"
>
    <ReferenceLine y=9 label="Norm (9.0)" color=warning lineType=dashed hideValue=true labelPosition=belowEnd/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

```sql depot_staff_ratio
SELECT
    Depot,
    ROUND(
        SUM(TRY_CAST("Total Bus Staff ratio – Norm Total (A+B+C) - 9.00" AS DOUBLE) *
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) /
        NULLIF(SUM(CASE WHEN TRY_CAST("Total Bus Staff ratio – Norm Total (A+B+C) - 9.00" AS DOUBLE) > 0
                        THEN TRY_CAST("Total Vehicles Per Day" AS DOUBLE) END), 0)
    , 2) as avg_actual_ratio,
    COUNT(*) as months_data
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
  AND TRY_CAST("Total Bus Staff ratio – Norm Total (A+B+C) - 9.00" AS DOUBLE) > 0
GROUP BY Depot
ORDER BY avg_actual_ratio DESC
```

<BarChart
    data={depot_staff_ratio}
    x=Depot
    y=avg_actual_ratio
    title="Average Staff per Bus by Depot (All-Time)"
    subtitle="Norm = 9.0 — all depots operate well below prescribed levels"
    yAxisTitle="Staff per Bus"
    yFmt='#0.00'
    swapXY=true
/>

---

## Depot Performance Comparison

### Top Depots by Revenue

```sql depot_revenue
-- Aggregate each depot across all months
SELECT 
    Depot,
    COUNT(*) as months_operated,
    ROUND(SUM(TRY_CAST("All Traffic Earning (₹)" AS DOUBLE)) / 10000000, 2) as total_revenue_crores,
    ROUND(AVG(TRY_CAST("Earning per KMs in Rs.(EPK) (₹)" AS DOUBLE)), 2) as avg_earning_per_km,
    ROUND(AVG(LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0)), 1) as avg_utilization_pct,
    ROUND(AVG(TRY_CAST("Avg Passenger per Bus per day on Traffic" AS DOUBLE)), 0) as avg_passengers_per_bus
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
GROUP BY Depot
ORDER BY total_revenue_crores DESC
LIMIT 10
```

<BarChart
    data={depot_revenue}
    x=Depot
    y=total_revenue_crores
    title="Top 10 Depots by Total Revenue (₹ Crores)"
    yAxisTitle="Revenue (₹ Crores)"
    swapXY=true
/>

### Depot Efficiency Metrics

```sql depot_efficiency
-- Average metrics per depot across all months
SELECT 
    Depot,
    COUNT(*) as months_data,
    ROUND(AVG(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0) as avg_fleet_size,
    ROUND(AVG(TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE)), 1) as avg_km_per_bus,
    ROUND(AVG(LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0)), 1) as avg_utilization,
    ROUND(AVG(TRY_CAST("Avg Passenger per Bus per day on Traffic" AS DOUBLE)), 0) as passengers_per_bus,
    ROUND(AVG(TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE)), 0) as revenue_per_bus
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
GROUP BY Depot
ORDER BY avg_utilization DESC
```

<DataTable
    data={depot_efficiency}
    rows=all
    search=true
>
    <Column id=Depot />
    <Column id=months_data title="Months"/>
    <Column id=avg_fleet_size title="Avg Fleet" fmt='#,##0'/>
    <Column id=avg_km_per_bus title="KM/Bus/Day" fmt='#,##0.0'/>
    <Column id=avg_utilization title="Util %" fmt='#0.0' contentType=colorscale colorScale="#16a34a"/>
    <Column id=passengers_per_bus title="Pass/Bus" fmt='#,##0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=revenue_per_bus title="₹/Bus" fmt='#,##0' contentType=colorscale colorScale="#3b82f6"/>
</DataTable>

---

## Monthly Trends Summary

### System-Wide Monthly Performance

```sql monthly_summary
-- Monthly system-wide metrics (sum across all depots)
SELECT 
    Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_label,
    -- System fleet (sum of daily averages across depots)
    ROUND(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0) as system_avg_fleet,
    -- Monthly total KMs (in thousands)
    ROUND(SUM(TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)) / 1000, 0) as total_kms_thousands,
    -- Monthly total revenue (in crores)
    ROUND(SUM(TRY_CAST("All Traffic Earning (₹)" AS DOUBLE)) / 10000000, 2) as revenue_crores,
    -- Monthly system-wide daily passengers
    SUM(TRY_CAST("Avg. Passenger per day on Traffic (including Ticket Sales, Commuters Passes, Student Passes, Monthly Passes & Casual Contract, Luxury Service, Mobile App etc.)" AS DOUBLE)) as daily_passengers_system,
    -- Weighted utilization
    ROUND(
        SUM(LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as avg_utilization_pct
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_label
ORDER BY date_parsed
```

<LineChart
    data={monthly_summary}
    x=date_parsed
    y=revenue_crores
    title="Monthly System Revenue (₹ Crores)"
    yAxisTitle="Revenue (₹Cr)"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

<LineChart
    data={monthly_summary}
    x=date_parsed
    y=daily_passengers_system
    title="Monthly System Daily Passenger Volume"
    yAxisTitle="Daily Passengers (Avg)"
    yFmt='#,##0'
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

<DataTable
    data={monthly_summary}
    rows=all
>
    <Column id=date_parsed title="Month"/>
    <Column id=system_avg_fleet title="Fleet Size" fmt='#,##0'/>
    <Column id=total_kms_thousands title="KMs (000s)" fmt='#,##0'/>
    <Column id=revenue_crores title="Revenue (₹Cr)" fmt='#,##0.00' contentType=colorscale colorScale="#16a34a"/>
    <Column id=daily_passengers_system title="Daily Pass" fmt='#,##0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=avg_utilization_pct title="Util %" fmt='#0.0'/>
</DataTable>

---

## Key Performance Indicators

### Overall System Performance (All-Time Averages)

```sql kpi_summary
-- System-wide averages across all depot-months
SELECT 
    -- Weighted averages by fleet size
    ROUND(AVG(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0) as avg_depot_fleet_size,
    ROUND(
        SUM(LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as fleet_utilization,
    ROUND(
        SUM(TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as km_per_bus_per_day,
    ROUND(
        SUM(TRY_CAST("Avg Passenger per Bus per day on Traffic" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 0) as passengers_per_bus,
    ROUND(
        SUM(TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 0) as revenue_per_bus_per_day,
    ROUND(
        SUM(TRY_CAST("Earning per KMs in Rs.(EPK) (₹)" AS DOUBLE) * 
            TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)), 0)
    , 2) as revenue_per_km,
    ROUND(
        SUM(TRY_CAST("% Load Factor on- 2. On Total Traffic Receipts i.e. (Earning from All types of Passes, Luxury, Monthly Contract, Casual Contract etc. as per Depotwise Eff. KM)" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as avg_load_factor,
    ROUND(AVG(TRY_CAST("KMs per Litre of Diesel (KMPL)(Own)" AS DOUBLE)), 2) as avg_diesel_kmpl,
    ROUND(AVG(TRY_CAST("KMs per Kg.of CNG (KMPG)(Own)" AS DOUBLE)), 2) as avg_cng_kmpg
FROM extracted
WHERE Date IS NOT NULL
```

<DataTable
    data={kpi_summary}
    rows=all
>
    <Column id=avg_depot_fleet_size title="Avg Depot Fleet" fmt='#,##0'/>
    <Column id=fleet_utilization title="Fleet Util %" fmt='#0.0'/>
    <Column id=km_per_bus_per_day title="KM/Bus/Day" fmt='#,##0.0'/>
    <Column id=passengers_per_bus title="Pass/Bus/Day" fmt='#,##0'/>
    <Column id=revenue_per_bus_per_day title="₹/Bus/Day" fmt='#,##0'/>
    <Column id=revenue_per_km title="₹/KM" fmt='#,##0.00'/>
    <Column id=avg_load_factor title="Load Factor %" fmt='#0.0'/>
    <Column id=avg_diesel_kmpl title="Diesel KMPL" fmt='#0.00'/>
    <Column id=avg_cng_kmpg title="CNG KMPG" fmt='#0.00'/>
</DataTable>

---

## Schedule Operations

### Sanctioned vs. Operated Schedules

```sql schedule_ops
-- Jan 2023 and Mar 2023: "Sanctioned" holds PMPML-only count; "Operated" holds full
-- PPP+hire total for 8 depots. Use GREATEST/LEAST to swap them back into the correct
-- columns before summing — otherwise those months show impossible adherence ratios.
SELECT
    Date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    sanctioned,
    operated,
    ROUND(operated / NULLIF(sanctioned, 0) * 100, 1) as adherence_pct
FROM (
    SELECT
        Date,
        SUM(GREATEST(
            COALESCE(TRY_CAST("No.of Schedules Sanctioned Per Day (PMPML + PPP)" AS DOUBLE), 0),
            COALESCE(TRY_CAST("Average No.of Schedule operated Per Day (PMPML+PPP)" AS DOUBLE), 0)
        )) as sanctioned,
        SUM(LEAST(
            COALESCE(TRY_CAST("No.of Schedules Sanctioned Per Day (PMPML + PPP)" AS DOUBLE), 0),
            COALESCE(TRY_CAST("Average No.of Schedule operated Per Day (PMPML+PPP)" AS DOUBLE), 0)
        )) as operated
    FROM extracted
    WHERE Date IS NOT NULL
    GROUP BY Date
)
ORDER BY date_parsed
```

<LineChart
    data={schedule_ops}
    x=date_parsed
    y={['sanctioned', 'operated']}
    title="Sanctioned vs. Operated Schedules Per Day"
    yAxisTitle="Number of Schedules"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<LineChart
    data={schedule_ops}
    x=date_parsed
    y=adherence_pct
    title="Schedule Adherence Rate (%)"
    yAxisTitle="Adherence %"
    yFmt='#0.0'
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

---

## Complaint & Default Trends

```sql complaint_trends
SELECT
    Date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    SUM(TRY_CAST("Total no. of Passenger Complaints received (including Telephone)" AS DOUBLE)) as complaints,
    SUM(TRY_CAST("Total no.of Default Cases Reported DEO" AS DOUBLE)) as defaults,
    SUM(TRY_CAST("Total Amount of Fine recovered by the Traffic Sup.Staff in Rs." AS DOUBLE)) as fines_recovered
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

<LineChart
    data={complaint_trends}
    x=date_parsed
    y={['complaints', 'defaults']}
    title="Monthly Passenger Complaints and Default Cases"
    yAxisTitle="Count"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<LineChart
    data={complaint_trends}
    x=date_parsed
    y=fines_recovered
    title="Monthly Fines Recovered by Traffic Supervisory Staff (₹)"
    yAxisTitle="Amount (₹)"
    yFmt='#,##0'
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' color=warning/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' color=warning/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' color=warning/>
</LineChart>

---

## Route Network

```sql route_coverage
SELECT
    Date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    SUM(TRY_CAST("Total Number of Routes" AS DOUBLE)) as total_routes,
    ROUND(AVG(TRY_CAST("Average Route Length in KMs" AS DOUBLE)), 1) as avg_route_length
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

<LineChart
    data={route_coverage}
    x=date_parsed
    y=total_routes
    title="Total Number of Routes Over Time"
    yAxisTitle="Number of Routes"
    connectGroup="system-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<DataTable
    data={route_coverage}
    rows=all
>
    <Column id=date_parsed title="Month"/>
    <Column id=total_routes title="Total Routes" fmt='#,##0'/>
    <Column id=avg_route_length title="Avg Route Length (KM)" fmt='#,##0.0'/>
</DataTable>

---

## See Also

- **[PCMT Before PMPML](/PCMC/Public%20Transport/PCMT_before_PMPML)** — Historical context: how PCMT operated before the 2007 merger
- **[Depot Performance](/PCMC/Public%20Transport/Depot_Performance)** — Narrative analysis of depot-level efficiency, schedule adherence, and revenue patterns
- **[Financial Performance](/PCMC/Public%20Transport/Financial_Performance)** — Annual P&L 2017-18 to 2024-25: the growing structural deficit and municipal reimbursements

---

*Data covers Jan 2023 – Dec 2025 with gaps (Jan–Mar 2024, Nov 2024–Mar 2025, Jul–Sep 2025 missing). 25 months of data, 15–17 depots per month, 385 records. Source: [PMPML Chief Statistician monthly reports](https://pmpml.org/statistics).*

## Data Queries
