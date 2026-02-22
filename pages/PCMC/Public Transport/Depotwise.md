---
title: PMPML Fleet Monthly Depotwise reports
description: Historical fleet data per depot per month from January 2023 to January 2025
sidebar: show
---

## PMPML Fleet Monthly Depotwise reports
Historical fleet data per depot per month from January 2023 to January 2025
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
    ROUND(AVG(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE)), 1) as avg_fleet_utilization_pct,
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
        SUM(TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS DOUBLE)) 
            OVER (PARTITION BY Date) as monthly_passengers
    FROM extracted
    WHERE Date IS NOT NULL
) e1
```

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
        SUM(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE) * 
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
title="Monthly System-Wide Average Daily Vehicle Status"
yAxisTitle="Number of Vehicles (Daily Average)"
/>

<LineChart 
 data={fleet_trends}
 x=date_parsed
 y=fleet_utilization_pct
 title="Monthly System Fleet Utilization Rate"
 yAxisTitle="Utilization %"
 yFmt='#0.0'
/>

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
title="Monthly Kilometers by Type (System Total, lakhs)"
yAxisTitle="Kilometers (lakhs)"
/>

<LineChart 
 data={km_trends}
 x=date_parsed
 y=avg_km_per_bus_per_day
 title="Monthly System-Wide Average KMs Per Bus Per Day"
 yAxisTitle="KMs/Bus/Day"
/>

---

## Revenue Performance

### Earnings Analysis

```sql revenue_trends
-- Monthly revenue: sum across all depots
SELECT 
        Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    SUM(TRY_CAST("Passenger Earning (Sale of Ticket)(₹)" AS DOUBLE)) / 100000 as ticket_sales_lakhs,
    SUM(TRY_CAST("All Traffic Earning (₹)" AS DOUBLE)) / 100000 as total_revenue_lakhs,
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
    SUM(TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS DOUBLE)) as monthly_daily_passengers
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed, month_year
ORDER BY date_parsed
```

<LineChart 
    data={revenue_trends}
    x=date_parsed
    y={['ticket_sales_lakhs', 'total_revenue_lakhs']}
    title="Monthly Revenue Trends (₹ Lakhs)"
    yAxisTitle="Revenue (₹ Lakhs)"
/>

<LineChart 
    data={revenue_trends}
    x=date_parsed
    y=earning_per_km
    title="Monthly System-Wide Earnings Per Kilometer"
    yAxisTitle="₹ per KM"
    yFmt='#,##0.00'
/>

### Passenger Metrics

```sql passenger_metrics
SELECT 
        Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    -- Monthly system-wide daily passengers (sum across all depots)
    SUM(TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS DOUBLE)) as daily_passengers_system,
    -- Weighted average passengers per bus
    ROUND(
        SUM(TRY_CAST("Passenger Per Bus Per day" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 0) as passengers_per_bus,
    -- Weighted average load factor
    ROUND(
        SUM(TRY_CAST("% Load Factor on- 1. Sale of Tickets" AS DOUBLE) * 
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
/>

<LineChart 
    data={passenger_metrics}
    x=date_parsed
    y=load_factor_pct
    title="Monthly System Load Factor"
    yAxisTitle="Load Factor %"
    yFmt='#0.0'
/>

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
UNION ALL
SELECT 
    'Casual Contracts',
    SUM(TRY_CAST("Casual Contract Amount (₹)" AS DOUBLE)) / 10000000
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
-- Monthly KMs by fuel type (sum across all depots)
SELECT
        Date as month_date,
    STRPTIME(Date, '%b %Y') as date_parsed,  -- Add this for proper sorting
    STRFTIME(STRPTIME(Date, '%b %Y'), '%b %Y') as month_year,
    SUM(TRY_CAST("Total Eff;km.Diesel (Own+PPP)" AS DOUBLE)) / 1000000 as diesel_kms_millions,
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
    y={['diesel_kms_millions', 'cng_kms_millions', 'ebus_kms_millions']}
    title="Monthly Kilometers by Fuel Type (Millions)"
    yAxisTitle="Kilometers (Millions)"
/>

### Fuel Efficiency Trends

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
/>

<LineChart 
    data={fuel_efficiency}
    x=date_parsed
    y=cng_kmpg
    title="Monthly Average CNG Efficiency (KMPG)"
    yAxisTitle="Kilometers per Kg"
/>

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
        SUM(TRY_CAST("Rate of Accidents per 1 Lakh KMs" AS DOUBLE) * 
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
    title="Monthly Accident Count by Severity (System Total)"
    yAxisTitle="Number of Accidents"
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
/>

---

## Depot Performance Comparison

### Top Depots by Revenue

```sql depot_revenue
-- Aggregate each depot across all months
SELECT 
    Depot,
    COUNT(*) as months_operated,
    ROUND(SUM(TRY_CAST("All Traffic Earning (₹)" AS DOUBLE)) / 1000000, 2) as total_revenue_millions,
    ROUND(AVG(TRY_CAST("Earning per KMs in Rs.(EPK) (₹)" AS DOUBLE)), 2) as avg_earning_per_km,
    ROUND(AVG(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE)), 1) as avg_utilization_pct,
    ROUND(AVG(TRY_CAST("Passenger Per Bus Per day" AS DOUBLE)), 0) as avg_passengers_per_bus
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
GROUP BY Depot
ORDER BY total_revenue_millions DESC
LIMIT 10
```

<BarChart 
    data={depot_revenue}
    x=Depot
    y=total_revenue_millions
    title="Top 10 Depots by Total Revenue (₹M)"
    yAxisTitle="Revenue (₹M)"
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
    ROUND(AVG(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE)), 1) as avg_utilization,
    ROUND(AVG(TRY_CAST("Passenger Per Bus Per day" AS DOUBLE)), 0) as passengers_per_bus,
    ROUND(AVG(TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE)), 0) as revenue_per_bus
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
GROUP BY Depot
ORDER BY avg_utilization DESC
```

<DataTable 
    data={depot_efficiency}
    rows=all
>
    <Column id=Depot />
    <Column id=months_data title="Months"/>
    <Column id=avg_fleet_size title="Avg Fleet" fmt='#,##0'/>
    <Column id=avg_km_per_bus title="KM/Bus/Day" fmt='#,##0.0'/>
    <Column id=avg_utilization title="Util %" fmt='#0.0'/>
    <Column id=passengers_per_bus title="Pass/Bus" fmt='#,##0'/>
    <Column id=revenue_per_bus title="₹/Bus" fmt='#,##0'/>
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
    SUM(TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS DOUBLE)) as daily_passengers_system,
    -- Weighted utilization
    ROUND(
        SUM(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as avg_utilization_pct
FROM extracted
WHERE Date IS NOT NULL
GROUP BY date_parsed, month_label
ORDER BY date_parsed
```

<LineChart 
    data={monthly_summary}
    x=date_parsed
    y=revenue_crores
    title="Monthly System Revenue (₹ Crores)"
    yAxisTitle="Revenue (₹Cr)"
/>

<LineChart 
    data={monthly_summary}
    x=date_parsed
    y=daily_passengers_system
    title="Monthly System Daily Passenger Volume"
    yAxisTitle="Daily Passengers (Avg)"
    yFmt='#,##0'
/>

<DataTable 
    data={monthly_summary}
    rows=all
>
    <Column id=date_parsed title="Month"/>
    <Column id=system_avg_fleet title="Fleet Size" fmt='#,##0'/>
    <Column id=total_kms_thousands title="KMs (000s)" fmt='#,##0'/>
    <Column id=revenue_crores title="Revenue (₹Cr)" fmt='#,##0.00'/>
    <Column id=daily_passengers_system title="Daily Pass" fmt='#,##0'/>
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
        SUM(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as fleet_utilization,
    ROUND(
        SUM(TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE) * 
            TRY_CAST("Total Vehicles Per Day" AS DOUBLE)) / 
        NULLIF(SUM(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0)
    , 1) as km_per_bus_per_day,
    ROUND(
        SUM(TRY_CAST("Passenger Per Bus Per day" AS DOUBLE) * 
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
        SUM(TRY_CAST("% Load Factor on- 1. Sale of Tickets" AS DOUBLE) * 
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

*Dashboard last updated: January 2025*
*Data structure: Monthly aggregated reports per depot (Jan 2023 – Jan 2025, ~15-17 depots per month, 397 records)*
