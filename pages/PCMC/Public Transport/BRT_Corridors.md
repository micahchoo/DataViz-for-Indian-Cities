---
title: BRT Corridor Demand — CMP 2008 vs 2021 Reality
description: How the PCMC Comprehensive Mobility Plan's 2008 BRT demand projections compared to actual 2021 traffic observations on the same corridors
---

The 2008 PCMC Comprehensive Mobility Plan proposed a network of BRT corridors to handle growing cross-city demand. For each corridor, the CMP modelled peak-hour passenger flows. Thirteen years later, the 2021 Pune Metro DPR traffic surveys measured actual demand on many of the same corridors — providing a rare opportunity to evaluate how accurate the CMP forecasts were.

The results are uneven: some corridors (NH-50 Nashik Phata–Moshi, Nashik Phata–Wakad) saw demand roughly double the 2008 projections by 2021. Others held closer to forecast. The CMP's 2008 corridor map also proposed specific sections with start/end coordinates and per-section trip estimates.

---

## Corridor Overview

```sql brt_corridor_summary
SELECT
    COUNT(DISTINCT Corridor) as total_corridors,
    SUM(CASE WHEN Year = 2008 THEN TRY_CAST("Corridor Peak Passengers per Direction" AS DOUBLE) END) as total_demand_2008,
    SUM(CASE WHEN Year = 2021 THEN TRY_CAST("Corridor Peak Passengers per Direction" AS DOUBLE) END) as total_demand_2021
FROM Estimated_vs_Actual_Bus_Passenger_trips_along_BRTS_corridors
```

<Grid cols=3>
<BigValue
    data={brt_corridor_summary}
    value=total_corridors
    title="Corridors Tracked"
/>
<BigValue
    data={brt_corridor_summary}
    value=total_demand_2008
    title="Total Peak Demand 2008"
    fmt='#,##0'
/>
<BigValue
    data={brt_corridor_summary}
    value=total_demand_2021
    title="Total Peak Demand 2021"
    fmt='#,##0'
/>
</Grid>

---

## 2008 Projections vs 2021 Observations

The NH-4 (Old Highway) corridor recorded the highest projected demand in 2008 at 189,427 — not included in the 2021 comparison data. For corridors where both years are available, NH-50 (Nashik Phata–Moshi) and Nashik Phata–Wakad show the largest absolute growth: both roughly doubled between 2008 and 2021, reflecting the northward expansion of PCMC's residential and commercial footprint.

<BarChart
    data={corridor_comparison}
    x=Corridor
    y=peak_passengers
    series=Year
    type=grouped
    title="Peak Passengers per Direction: 2008 Projected vs 2021 Observed"
    subtitle="Corridors with data for both years only"
    yAxisTitle="Peak Passengers / Direction"
    yFmt='#,##0'
    swapXY=true
/>

<DataTable
    data={corridor_all}
    rows=all
>
    <Column id=Corridor title="Corridor"/>
    <Column id=Year title="Year"/>
    <Column id=peak_passengers title="Peak Passengers/Direction" fmt='#,##0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=peak_hour_traffic title="Peak Hour Traffic" fmt='#,##0' contentType=colorscale colorScale="#16a34a"/>
</DataTable>

---

## Proposed Route Map

The CMP proposed 30 specific route sections across 8 BRT corridors. Each section has defined start and end coordinates and a projected passenger demand. The map below shows the midpoint of each section, with bubble size proportional to projected daily trips.

<PointMap
    data={brt_route_sections}
    lat=mid_lat
    long=mid_lng
    value=projected_trips
    valueFmt='#,##0'
    pointName=section_name
    title="Proposed BRT Sections — CMP 2008 (Bubble = Projected Trips/Day)"
    height=500
    basemap={`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`}
    tooltipType=hover
    colorPalette={['#00dc54', '#ffe256', '#cd4063']}
/>

<DataTable
    data={brt_route_sections}
    rows=all
    search=true
>
    <Column id=brt_section title="BRT Corridor"/>
    <Column id=section_name title="Section"/>
    <Column id=projected_trips title="Projected Trips/Day" fmt='#,##0' contentType=colorscale colorScale="#3b82f6"/>
</DataTable>

---

## See Also

- **[PMPML BRT Service Statistics](/PCMC/Public%20Transport/BRT)** — Actual PMPML BRT operations 2023–2025: fleet, ridership, revenue
- **[Traffic Surveys](/PCMC/Traffic)** — 2008 baseline and 2021 metropolitan surveys
- **[PCMC Growth Context](/PCMC/City_Context)** — Population, urban expansion, and CMP transport demand projections
- **[Public Transport Overview](/PCMC/Public%20Transport)** — Three eras of bus transit

---

*Data sources: PCMC Comprehensive Mobility Plan (2008) for projected BRT corridor demand and route sections; Pune Metro DPR traffic surveys (2021) for observed corridor traffic.*

---

## Data Queries

*SQL queries powering the visualizations above.*

```sql brt_corridor_summary
SELECT
    COUNT(DISTINCT Corridor) as total_corridors,
    SUM(CASE WHEN Year = 2008 THEN TRY_CAST("Corridor Peak Passengers per Direction" AS DOUBLE) END) as total_demand_2008,
    SUM(CASE WHEN Year = 2021 THEN TRY_CAST("Corridor Peak Passengers per Direction" AS DOUBLE) END) as total_demand_2021
FROM Estimated_vs_Actual_Bus_Passenger_trips_along_BRTS_corridors
```

```sql corridor_comparison
SELECT
    Corridor,
    Year,
    TRY_CAST("Corridor Peak Passengers per Direction" AS DOUBLE) as peak_passengers
FROM Estimated_vs_Actual_Bus_Passenger_trips_along_BRTS_corridors
WHERE Corridor IN (
    SELECT Corridor
    FROM Estimated_vs_Actual_Bus_Passenger_trips_along_BRTS_corridors
    GROUP BY Corridor
    HAVING COUNT(DISTINCT Year) = 2
)
ORDER BY Corridor, Year
```

```sql corridor_all
SELECT
    Corridor,
    Year,
    TRY_CAST("Corridor Peak Passengers per Direction" AS DOUBLE) as peak_passengers,
    TRY_CAST("Corridor Peak Hour Peak Direction Traffic" AS DOUBLE) as peak_hour_traffic
FROM Estimated_vs_Actual_Bus_Passenger_trips_along_BRTS_corridors
ORDER BY Corridor, Year
```

```sql brt_route_sections
SELECT
    "BRT Section" as brt_section,
    "Section of corridor" as section_name,
    (TRY_CAST(SPLIT_PART("From", ', ', 1) AS DOUBLE) + TRY_CAST(SPLIT_PART("To", ', ', 1) AS DOUBLE)) / 2.0 as mid_lat,
    (TRY_CAST(SPLIT_PART("From", ', ', 2) AS DOUBLE) + TRY_CAST(SPLIT_PART("To", ', ', 2) AS DOUBLE)) / 2.0 as mid_lng,
    TRY_CAST("Projected Bus trips for 2008 (passenger trips per day)" AS DOUBLE) as projected_trips
FROM Proposed_BRT_Routes_Data
WHERE "From" IS NOT NULL AND "To" IS NOT NULL
ORDER BY TRY_CAST("S.No." AS INTEGER)
```
