---
title: PMPML BRT Service Statistics
description: B.R.T. Bus Rapid Transit operations 2023–2025 — fleet performance, corridor efficiency, and ridership trends
---

PMPML's B.R.T. (Bus Rapid Transit) network operates on designated high-capacity corridors linking Pune and Pimpri-Chinchwad. BRT buses run on priority lanes and serve backbone routes — the system is distinct from PMPML's mixed urban fleet in that it targets higher throughput per corridor, with correspondingly stricter fleet utilization targets.

Between 2023 and 2025, the BRT network expanded from 759 to 927 buses (by late 2023), then contracted. Fleet utilization, which opened above 94%, declined to the low 80s by 2025. Ridership peaked in mid-2023 and dropped sharply — a pattern consistent with metro line openings drawing away cross-city commuters who once depended on BRT.

**Note on depot naming:** The M.Yard depot appears in 2023 data. From April 2024 onward, this operational base is listed as Upper Depot. Both refer to the same location.

**Note on data coverage:** BRT data runs February 2023 – June 2025. January 2023 is absent because the source report was not available for download — the BRT service existed but the monthly PDF was not published online. The same two coverage gaps affect all PMPML report types: January–March 2024 and November 2024–March 2025.

---

## System Overview

```sql brt_summary
SELECT
    COUNT(DISTINCT Date) as total_months,
    SUM(TRY_CAST(buses_held AS DOUBLE)) / NULLIF(COUNT(DISTINCT Date), 0) as avg_buses_held,
    ROUND(AVG(TRY_CAST(fleet_utilization_pct AS DOUBLE)), 1) as avg_utilization_pct,
    ROUND(SUM(TRY_CAST(all_traffic_earning AS DOUBLE)) / 10000000, 1) as total_revenue_cr
FROM brt_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
```

<Grid cols=4>
<BigValue
    data={brt_summary}
    value=total_months
    title="Months of Data"
/>
<BigValue
    data={brt_summary}
    value=avg_buses_held
    title="Avg Buses Held"
    fmt='#,##0'
/>
<BigValue
    data={brt_summary}
    value=avg_utilization_pct
    title="Avg Fleet Utilization"
    fmt='#0.0"%"'
/>
<BigValue
    data={brt_summary}
    value=total_revenue_cr
    title="Total Revenue (₹ Cr)"
    fmt='"₹"#,##0.0" Cr"'
/>
</Grid>

---

## Fleet Operations

The BRT fleet expanded through 2023 — reaching 927 buses by November — before contracting. Off-road buses (in maintenance or reserve) track inversely with utilization: when depots struggle to put buses on road, the off-road count spikes.

<BarChart
    data={brt_fleet}
    x=date_parsed
    y={['avg_on_road', 'avg_off_road']}
    type=stacked
    title="BRT Fleet: On Road vs Off Road (System Total)"
    yAxisTitle="Number of Buses"
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</BarChart>

<LineChart
    data={brt_fleet}
    x=date_parsed
    y=fleet_utilization_pct
    title="Fleet Utilization % (System Total)"
    subtitle="BRT consistently outperforms the mixed fleet — but the gap has narrowed since 2023"
    yAxisTitle="Utilization %"
    yMin=70
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Kilometers and Schedule Adherence

Planned kilometers represent what PMPML scheduled — effective kilometers are what was actually operated. The gap between them, expressed as cancelled KM percentage, reveals how reliably depots execute their schedules. BRT's cancellation rate is typically lower than the mixed fleet, but spikes during driver shortages and breakdown peaks.

<AreaChart
    data={brt_km}
    x=date_parsed
    y={['effective_km', 'cancelled_km']}
    type=stacked
    title="Effective vs Cancelled Kilometers (System Total)"
    yAxisTitle="Kilometers"
    yFmt='#,##0'
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</AreaChart>

<LineChart
    data={brt_km}
    x=date_parsed
    y=km_per_bus_per_day
    title="Km Per Bus Per Day (System Total)"
    subtitle="Vehicle utilization intensity — how hard each bus is worked"
    yAxisTitle="Km/Bus/Day"
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Revenue

BRT revenue peaked in late 2023 before declining into 2025. The earning per kilometer (EPK) is a key efficiency metric — a falling EPK means either fares are unchanged while passengers drop, or the route mix has shifted toward lower-yield corridors.

<LineChart
    data={brt_revenue}
    x=date_parsed
    y=all_traffic_earning_cr
    title="Monthly All-Traffic Earning (₹ Crores)"
    yAxisTitle="Revenue (₹ Cr)"
    yFmt='#,##0.0'
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<LineChart
    data={brt_revenue}
    x=date_parsed
    y={['epk_total', 'epk_ticket']}
    title="Earning Per Kilometer (EPK)"
    subtitle="Total EPK vs ticket-only EPK — the gap represents non-ticket revenue"
    yAxisTitle="₹ per KM"
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Ridership

BRT ridership peaked at over 600,000 passengers per day in August 2023, then declined sharply into 2025. By mid-2025, the BRT network was carrying fewer passengers than in its February 2023 baseline — on a larger fleet. This compression of passengers-per-bus is the clearest signal of ridership loss.

<LineChart
    data={brt_ridership}
    x=date_parsed
    y=passengers_per_day
    title="Total Passengers Per Day (System Total)"
    yAxisTitle="Passengers / Day"
    yFmt='#,##0'
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<LineChart
    data={brt_ridership}
    x=date_parsed
    y=avg_passengers_per_bus_per_day
    title="Average Passengers Per Bus Per Day"
    subtitle="Falling passengers/bus signals either ridership loss or fleet overcapacity"
    yAxisTitle="Passengers / Bus / Day"
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Safety

BRT accident data is reported by severity: fatal, major, minor, and insignificant. BRT's safety record has historically been better than the citywide road accident baseline — dedicated lanes reduce conflict points with other vehicles.

<BarChart
    data={brt_accidents}
    x=date_parsed
    y={['accidents_fatal', 'accidents_major', 'accidents_minor', 'accidents_insignificant']}
    type=stacked
    title="Monthly BRT Accidents by Severity (System Total)"
    yAxisTitle="Number of Accidents"
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</BarChart>

<LineChart
    data={brt_accidents}
    x=date_parsed
    y=accident_rate_per_lakh_km
    title="Accident Rate per 1 Lakh KMs"
    yAxisTitle="Accidents per 1 Lakh KMs"
    connectGroup="brt-monthly"
>
    <ReferenceArea xMin='2023-01-01' xMax='2023-01-31' label="Jan 2023 missing" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Depot Comparison

<DataTable
    data={brt_depot_summary}
    rows=all
    search=true
>
    <Column id=Depot title="Depot"/>
    <Column id=months_present title="Months"/>
    <Column id=avg_utilization title="Avg Utilization %" fmt='#0.0' contentType=colorscale colorScale="#16a34a"/>
    <Column id=avg_km_per_bus title="Km/Bus/Day" fmt='#,##0.0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=avg_passengers_per_bus title="Pass/Bus/Day" fmt='#,##0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=avg_epk title="EPK (₹/Km)" fmt='#,##0.00' contentType=colorscale colorScale="#16a34a"/>
</DataTable>

<BarChart
    data={brt_depot_utilization}
    x=Depot
    y=avg_utilization
    title="Average Fleet Utilization % by Depot"
    subtitle="Ranked highest to lowest across all available months"
    yAxisTitle="Utilization %"
    swapXY=true
/>

---

## See Also

- **[PMPML E-Bus Statistics](/PCMC/Public%20Transport/EBus)** — Electric bus operations at 6–7 dedicated depots
- **[Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — System-wide monthly fleet dashboard covering all PMPML operations
- **[Road Safety](/PCMC/Road_Accident_Statistics)** — BRT safety in context of city-wide accident trends

---

*Data covers Feb 2023 – Jun 2025 with gaps (Jan–Mar 2024, Nov 2024–Mar 2025 missing). Source: PMPML B.R.T. Bus Service Statistical Reports (monthly), Chief Statistician.*

---

## Data Queries

*SQL queries powering the visualizations above. Evidence.dev processes these at build time — position in the file does not affect rendering.*

```sql brt_fleet
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(buses_held AS DOUBLE) as buses_held,
    TRY_CAST(avg_on_road AS DOUBLE) as avg_on_road,
    TRY_CAST(avg_off_road AS DOUBLE) as avg_off_road,
    TRY_CAST(fleet_utilization_pct AS DOUBLE) as fleet_utilization_pct
FROM brt_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql brt_km
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(effective_km AS DOUBLE) as effective_km,
    TRY_CAST(cancelled_km AS DOUBLE) as cancelled_km,
    TRY_CAST(km_per_bus_per_day AS DOUBLE) as km_per_bus_per_day,
    TRY_CAST(pct_cancelled_km AS DOUBLE) as pct_cancelled_km
FROM brt_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql brt_revenue
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(all_traffic_earning AS DOUBLE) / 10000000 as all_traffic_earning_cr,
    TRY_CAST(ticket_sale_earning AS DOUBLE) / 10000000 as ticket_earning_cr,
    TRY_CAST(epk_total AS DOUBLE) as epk_total,
    TRY_CAST(epk_ticket AS DOUBLE) as epk_ticket,
    TRY_CAST(earning_per_bus_per_day AS DOUBLE) as earning_per_bus_per_day
FROM brt_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql brt_ridership
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(passengers_per_day AS DOUBLE) as passengers_per_day,
    TRY_CAST(avg_passengers_per_bus_per_day AS DOUBLE) as avg_passengers_per_bus_per_day,
    TRY_CAST(ticket_passengers_per_day AS DOUBLE) as ticket_passengers_per_day,
    TRY_CAST(earning_per_passenger_per_day AS DOUBLE) as earning_per_passenger
FROM brt_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql brt_accidents
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(accidents_fatal AS DOUBLE) as accidents_fatal,
    TRY_CAST(accidents_major AS DOUBLE) as accidents_major,
    TRY_CAST(accidents_minor AS DOUBLE) as accidents_minor,
    TRY_CAST(accidents_insignificant AS DOUBLE) as accidents_insignificant,
    TRY_CAST(accidents_total AS DOUBLE) as accidents_total,
    TRY_CAST(accident_rate_per_lakh_km AS DOUBLE) as accident_rate_per_lakh_km
FROM brt_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql brt_depot_summary
SELECT
    Depot,
    COUNT(DISTINCT Date) as months_present,
    ROUND(AVG(TRY_CAST(fleet_utilization_pct AS DOUBLE)), 1) as avg_utilization,
    ROUND(AVG(TRY_CAST(km_per_bus_per_day AS DOUBLE)), 1) as avg_km_per_bus,
    ROUND(AVG(TRY_CAST(avg_passengers_per_bus_per_day AS DOUBLE)), 0) as avg_passengers_per_bus,
    ROUND(AVG(TRY_CAST(epk_total AS DOUBLE)), 2) as avg_epk
FROM brt_extracted
WHERE Date IS NOT NULL AND Depot != 'System Total'
GROUP BY Depot
ORDER BY avg_utilization DESC
```

```sql brt_depot_utilization
SELECT
    Depot,
    ROUND(AVG(TRY_CAST(fleet_utilization_pct AS DOUBLE)), 1) as avg_utilization
FROM brt_extracted
WHERE Date IS NOT NULL AND Depot != 'System Total'
GROUP BY Depot
ORDER BY avg_utilization DESC
```
