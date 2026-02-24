---
title: PCMC Growth Context
description: Population trajectories, urban expansion, land use, and transport demand projections from the 2008 Comprehensive Mobility Plan
---

Pimpri-Chinchwad's story is one of rapid industrial urbanization. What began as a cluster of villages adjacent to Pune grew into a million-plus city in under two decades — driven by automobile manufacturing, a favorable position on national highways, and overflow from Pune's IT expansion. The city's 2008 Comprehensive Mobility Plan (CMP) documented this growth and projected where it was headed. This page draws on that CMP data to provide context for the transport statistics elsewhere on this site.

---

## Population Growth

PCMC's population grew from 26,367 in 1951 to over 10 lakh by 2001 — a 38-fold increase in 50 years, with the steepest acceleration occurring between 1971 and 1991 as industrial employment drew workers from across Maharashtra. The CMP projected continued growth toward 29 lakh by 2031.

<BarChart
    data={population_growth}
    x=census_year
    y={['actual_population', 'projected_population']}
    type=grouped
    title="PCMC Population Growth 1951–2031"
    subtitle="Actual census data (1951–2001) vs CMP 2008 projections (2011–2031)"
    yAxisTitle="Population"
    yFmt='#,##0'
    labels=true
/>

<LineChart
    data={population_growth}
    x=census_year
    y=growth_rate_pct
    title="Decadal Population Growth Rate (%)"
    subtitle="Growth rate decelerating from 155% (1971–81) toward more moderate projections"
    yAxisTitle="Growth Rate %"
    connectGroup="city-context"
/>

---

## Urban Expansion

Between 1989 and 2007, PCMC's built-up area more than doubled — from 151 sq km to 332 sq km. The 84.68% expansion between 2000 and 2007 reflects a period when new residential and industrial zones spread rapidly into agricultural land at the city's periphery.

<DataTable
    data={urban_sprawl}
>
    <Column id=Stage title="Stage"/>
    <Column id=data_source title="Data Source"/>
    <Column id=area_sq_km title="Area (sq km)" fmt='#,##0.0'/>
    <Column id=pct_increase title="% Increase" fmt='#,##0.0"%"'/>
</DataTable>

---

## Land Use (2008)

The 2008 CMP mapped PCMC's developed land into 15 categories. Residential uses dominate — low-income housing (R_C), middle-income (R_B), and high-income (R_A) together account for nearly 70% of developed area. Industrial zones (IND_A and IND_B) make up about 19%.

<BarChart
    data={landuse}
    x=Description
    y=Developed_Area_Sq_Km
    title="Developed Area by Land Use Type (2008)"
    subtitle="All categories sorted by area"
    yAxisTitle="Area (sq km)"
    swapXY=true
/>

<DataTable
    data={landuse}
    rows=all
>
    <Column id=Description title="Land Use"/>
    <Column id=Type title="Type"/>
    <Column id=Developed_Area_Sq_Km title="Area (sq km)" fmt='#,##0.00' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=Percent_of_Total title="% of Total" fmt='#,##0.00' contentType=colorscale colorScale="#16a34a"/>
</DataTable>

---

## Household Profile (2008 Survey)

The CMP household survey covered 4,896 households. Nearly two-thirds owned their homes; independent houses dominated the housing stock. Most households occupied under 500 sq m — reflecting the dense industrial township character of PCMC's older neighborhoods.

<Grid cols=3>
<BarChart
    data={household_ownership}
    x=Category
    y=pct
    title="Housing Tenure"
    yAxisTitle="%"
    yFmt='#0.0"%"'
/>
<BarChart
    data={household_building}
    x=Category
    y=pct
    title="Building Type"
    yAxisTitle="%"
    yFmt='#0.0"%"'
/>
<BarChart
    data={household_area}
    x=Category
    y=pct
    title="Residence Area"
    yAxisTitle="%"
    yFmt='#0.0"%"'
/>
</Grid>

---

## Transport Demand Projections

The CMP projected total trip demand to grow 7-fold between 2008 and 2031 (from 21 lakh to 1.46 crore trips per day). Public transport's share was expected to grow from 26% in 2008 to 32% in 2031 — reflecting planned BRT and metro investments. The actual trajectory diverged significantly with metro construction and changing land use patterns.

<BarChart
    data={transport_demand}
    x=Year
    y={['pt_trips', 'total_trips']}
    type=grouped
    title="Total Trips vs Public Transport Trips by Planning Horizon"
    subtitle="CMP 2008 projected demand — all modes vs public transport"
    yAxisTitle="Trips per Day"
    yFmt='#,##0'
    connectGroup="city-context"
/>

<LineChart
    data={transport_demand}
    x=Year
    y=pt_share_pct
    title="Public Transport's Projected Modal Share (%)"
    subtitle="CMP 2008 target: grow PT share from 26% (2008) to 32% (2031)"
    yAxisTitle="%"
    yFmt='#0.0"%"'
    connectGroup="city-context"
/>

---

## See Also

- **[Ward Map and City Overview](/PCMC)** — Administrative zones and ward structure
- **[Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018)** — Cumulative RTO data 2000–2018
- **[BRT Corridor Demand](/PCMC/Public%20Transport/BRT_Corridors)** — How the CMP's BRT corridor projections compared to 2021 reality
- **[Traffic Surveys](/PCMC/Traffic)** — 2008 and 2021 traffic volume measurements
- **[Public Transport Overview](/PCMC/Public%20Transport)** — Three eras of bus transit in Pimpri-Chinchwad

---

*Data source: PCMC Comprehensive Mobility Plan (2008). Population projections prepared for CMP planning horizon. Urban sprawl measurements from TM/ETM/Google Image satellite comparisons.*

---

## Data Queries

*SQL queries powering the visualizations above. Evidence.dev processes these at build time — position in the file does not affect rendering.*

```sql population_growth
SELECT
    "Census Year" as census_year,
    NULLIF(TRY_CAST("Actual Population" AS DOUBLE), 0) as actual_population,
    NULLIF(TRY_CAST("Projected Population (at 2008)" AS DOUBLE), 0) as projected_population,
    TRY_CAST("Decadal Growth Rate (%)" AS DOUBLE) as growth_rate_pct
FROM Projected_Decadal_Population_Growth_at_2008
ORDER BY census_year
```

```sql urban_sprawl
SELECT
    Stage,
    "Data Source \nImage" as data_source,
    TRY_CAST("Sq. km" AS DOUBLE) as area_sq_km,
    TRY_CAST(REPLACE(COALESCE(NULLIF("% increase", '-'), '0'), '%', '') AS DOUBLE) as pct_increase
FROM "PCMC_Urban_Sprawl_Increase_1989_-_2007"
ORDER BY Stage
```

```sql landuse
SELECT
    Description,
    Type,
    "Sub Type" as sub_type,
    TRY_CAST(Developed_Area_Sq_Km AS DOUBLE) as Developed_Area_Sq_Km,
    TRY_CAST(Percent_of_Total AS DOUBLE) as Percent_of_Total
FROM Landuse_Type_by_Developed_Area_2008
ORDER BY Developed_Area_Sq_Km DESC
```

```sql household_ownership
SELECT
    Category,
    TRY_CAST(REPLACE(Percent, '%', '') AS DOUBLE) as pct
FROM Household_Survey_Data
WHERE "Statistics Type" = 'Ownership'
ORDER BY pct DESC
```

```sql household_building
SELECT
    Category,
    TRY_CAST(REPLACE(Percent, '%', '') AS DOUBLE) as pct
FROM Household_Survey_Data
WHERE "Statistics Type" = 'Type of Building'
ORDER BY pct DESC
```

```sql household_area
SELECT
    Category,
    TRY_CAST(REPLACE(Percent, '%', '') AS DOUBLE) as pct
FROM Household_Survey_Data
WHERE "Statistics Type" = 'Residence Area (sq. m)'
ORDER BY pct DESC
```

```sql transport_demand
SELECT
    Year,
    CAST(REPLACE("Total Trips", ',', '') AS BIGINT) as total_trips,
    CAST(REPLACE("PT Trips", ',', '') AS BIGINT) as pt_trips,
    ROUND(100.0 * CAST(REPLACE("PT Trips", ',', '') AS DOUBLE) /
        NULLIF(CAST(REPLACE("Total Trips", ',', '') AS DOUBLE), 0), 1) as pt_share_pct
FROM Estimated_increase_in_Total_trips_to_Public_Transport_trips
WHERE "S. No." IS NOT NULL
ORDER BY Year
```
