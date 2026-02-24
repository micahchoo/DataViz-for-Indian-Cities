---
title: "A City on Two Wheels: Vehicle Registrations in Pimpri-Chinchwad, 2000–2018"
description: Cumulative vehicle registrations by type with the RTO from 2000 to 2018
---
This data shows cumulative vehicle registrations by type with the Pimpri-Chinchwad RTO from 2000 to 2018. These are active registrations on the RTO's books — not annual new registrations, and not necessarily vehicles currently on the road (some may be scrapped, idle, or relocated). Rising numbers primarily reflect new registrations outpacing de-registrations. Small drops in some categories (e.g. Scooters, Mopeds) indicate occasional data revisions or de-registrations.

<ButtonGroup
 name=selected_view
 data={view_options}
 value=view
 title="Select Vehicle Category View"
 defaultValue="Overall"
 display=buttons
 colorScale=custom
/>



{#if inputs.selected_view === "Overall"}
### Overall Vehicle Registration Distribution

Between 2000-01 and 2017-18, PCMC's registered vehicle fleet grew from 2.38 lakh to 21.27 lakh — a nearly 9-fold increase. Two-wheelers account for around 70% of all registrations throughout the period, a dominance that has barely shifted even as cars have grown faster in proportional terms. Use the category buttons above to explore the composition in detail.

<AreaChart
    data={all_categories}
    x=display_year
    y=count
    series=category
    type=stacked
    title="Vehicle Registrations"
    subtitle="Distribution across major vehicle categories"
    xAxisTitle="Year"
    yAxisTitle="Registrations"
    fillOpacity=0.9
    connectGroup="vehicles"
    chartAreaHeight=300
    sort=false
    handleMissing=gap
    xLabelWrap=true
    xGridlines=true
    xTickMarks=true
    colorScale=custom
 />
<AreaChart
    data={all_categories}
    x=display_year
    y=count
    series=category
    type=stacked100
    title="Vehicle Registrations"
    subtitle="As a share of all Vehicles on Road"
    xAxisTitle="Year"
    yAxisTitle="Share of All Vehicles (%)"
    fillOpacity=0.9
    connectGroup="vehicles"
    chartAreaHeight=300
    yGridLines=true
    sort=false
    xLabelWrap=true
    xGridlines=true
    xTickMarks=true
    colorScale=custom
 />

 {:else if inputs.selected_view === "New Registrations"}
### Annual New Registrations (Year-over-Year Change)

Derived from cumulative data — the difference between consecutive years shows how many new vehicles were registered each year. New registrations accelerated from ~31,000/year in 2001 to ~162,000/year by 2018.

<BarChart
    data={new_registrations}
    x=display_year
    y=new_registrations
    series=category
    type=stacked
    title="Annual New Vehicle Registrations"
    subtitle="Year-over-year increase in cumulative registrations"
    xAxisTitle="Year"
    yAxisTitle="New Registrations"
    chartAreaHeight=300
    sort=false
    xLabelWrap=true
    xGridlines=true
    xTickMarks=true
/>

<LineChart
    data={new_registrations_total}
    x=display_year
    y=yoy_growth_pct
    title="Rate of Change in New Registrations"
    subtitle="Year-over-year growth rate of total new registrations"
    xAxisTitle="Year"
    yAxisTitle="YoY Growth (%)"
    chartAreaHeight=300
    sort=false
    yGridLines=true
    xLabelWrap=true
    xGridlines=true
    xTickMarks=true
/>

 {:else if inputs.selected_view === "Per Capita"}
### Vehicles Per 1,000 Population

By 2017-18, PCMC had crossed 1,000 registered vehicles per 1,000 people — effectively one vehicle per person, including children. Population estimates use linear interpolation between Census 2001 (10.06 lakh) and Census 2011 (17.28 lakh).

<LineChart
    data={per_capita}
    x=display_year
    y={['vehicles_per_1000', 'two_wheelers_per_1000', 'four_wheelers_per_1000']}
    title="Registered Vehicles Per 1,000 Population"
    subtitle="PCMC crossed 1,000 vehicles per 1,000 people by 2017-18"
    xAxisTitle="Year"
    yAxisTitle="Vehicles per 1,000 people"
    chartAreaHeight=300
    yGridLines=true
    xLabelWrap=true
    xGridlines=true
    xTickMarks=true
    labels=true
/>

 {:else if inputs.selected_view === "Two Wheelers"}
### Two Wheeler Registration Distribution

The six-year scooter plateau (2007–2013) broke sharply in 2013-14 with a 19% jump in one year — the arrival of gearless automatics (Honda Activa, TVS Jupiter) that broadened two-wheeler appeal across age groups and genders. Mopeds, by contrast, simply stopped growing after 2011 and have flatlined since — the category was superseded.

<AreaChart
    data={detailed_two_wheelers}
    x=display_year
    y=Count
    series=subcategory
    type=stacked
    title="Two Wheeler Registrations"
    subtitle="Distribution of motorcycles, scooters, and mopeds"
    xAxisTitle="Year"
    yAxisTitle="Registrations"
    fillOpacity=0.9
    connectGroup="vehicles"
    chartAreaHeight=300
    yGridLines=true
    sort=false
    xLabelWrap=true
    xGridlines=true
    xTickMarks=true
    colorScale=custom
 />

 <AreaChart
    data={detailed_two_wheelers}
    x=display_year
    y=Count
    series=subcategory
    type=stacked100
    title="Two Wheeler Registrations"
    subtitle="As a share of other Two Wheelers on Road"
    xAxisTitle="Year"
    yAxisTitle="Share of Two Wheelers (%)"
    fillOpacity=0.9
    connectGroup="vehicles"
    chartAreaHeight=300
    yGridLines=true
    sort=false
    xLabelWrap=true
    xGridlines=true
    xTickMarks=true
    colorScale=custom
 />

 {:else if inputs.selected_view === "Personal Vehicles"}
### Personal Vehicle Registration Distribution

Car registrations accelerated after 2010, growing their share of the total fleet even as two-wheelers also grew in absolute numbers. The shift toward four-wheelers tracks the income growth documented in the CMP 2008 household surveys — what was once aspirational became reachable.

<AreaChart
     data={detailed_personal}
     x=display_year
     y=Count
     series=subcategory
     type=stacked
     title="Personal Vehicle Registrations"
     subtitle="Distribution of cars, jeeps, and station wagons"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     fillOpacity=0.9
     connectGroup="vehicles"
     chartAreaHeight=300
     yGridLines=true
    sort=false
        xLabelWrap=true
    xGridlines=true
    xTickMarks=true
 />
<AreaChart
     data={detailed_personal}
     x=display_year
     y=Count
     series=subcategory
     type=stacked100
     title="Personal Vehicle Registrations"
     subtitle="As a share of other Personal Vehicles on the Road"
     xAxisTitle="Year"
     yAxisTitle="Share of Personal Vehicles (%)"
     fillOpacity=0.9
     connectGroup="vehicles"
     chartAreaHeight=300
     yGridLines=true
    sort=false
        xLabelWrap=true
    xGridlines=true
    xTickMarks=true
 />

{:else}
### Commercial Vehicle Registration Distribution

Metered taxis disappear from the data in 2007-08 — not because taxis vanished, but because the RTO reclassified them as 'Luxury Tourist Cabs.' The rising delivery van count from 2012 onward tracks the expansion of e-commerce logistics alongside Pimpri-Chinchwad's existing industrial supply chains.

<AreaChart
     data={detailed_commercial}
     x=display_year
     y=Count
     series=subcategory
     type=stacked
     title="Commercial Vehicle Registrations"
     subtitle="Distribution across transport and goods vehicles"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     fillOpacity=0.9
     connectGroup="vehicles"
     chartAreaHeight=300
     yGridLines=true
     sort=false
        xLabelWrap=true
    xGridlines=true
    xTickMarks=true
 />
 <AreaChart
     data={detailed_commercial}
     x=display_year
     y=Count
     series=subcategory
     type=stacked100
     title="Commercial Vehicle Registrations"
     subtitle="As a share of other commercial vehicles on the road"
     xAxisTitle="Year"
     yAxisTitle="Share of Commercial Vehicles (%)"
     fillOpacity=0.9
     connectGroup="vehicles"
     chartAreaHeight=300
     yGridLines=true
     sort=false
        xLabelWrap=true
    xGridlines=true
    xTickMarks=true
 />
 {/if}

## Data Queries

*SQL queries powering the visualizations above. Evidence.dev processes these at build time — position in the file does not affect rendering.*

```sql view_options
SELECT 'Overall' as view
UNION ALL SELECT 'New Registrations' as view
UNION ALL SELECT 'Per Capita' as view
UNION ALL SELECT 'Two Wheelers' as view
UNION ALL SELECT 'Personal Vehicles' as view
UNION ALL SELECT 'Commercial Vehicles' as view
```

```sql all_categories
WITH base_categories AS (
    SELECT
        SPLIT_PART(Year, '-', 1) as display_year,
        Year as original_year,
        Vehicle_Type,
        Count as vehicle_count
    FROM vehicle_registrations_by_type_and_year
),
categorized AS (
    SELECT
        display_year,
        CASE
            WHEN Vehicle_Type IN ('Motor_Cycles', 'Scooters', 'Moped') THEN 'Two Wheelers'
            WHEN Vehicle_Type IN ('Cars') THEN 'Cars'
            WHEN Vehicle_Type IN ('Jeeps', 'Stn_Wagons') THEN 'SUVs & Wagons'
            WHEN Vehicle_Type IN ('Taxi_w_meter', 'Luxury_Tourist_Cabs') THEN 'Taxi Services'
            WHEN Vehicle_Type IN ('Auto_rickshaw') THEN 'Auto Rickshaws'
            WHEN Vehicle_Type IN ('Stage_carriages', 'Mini_Bus') THEN 'Public Transport'
            WHEN Vehicle_Type IN ('School_Buses') THEN 'School Transport'
            WHEN Vehicle_Type IN ('Private_Service_Vehicles', 'Ambulances') THEN 'Service Vehicles'
            WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated_Multi') THEN 'Heavy Transport'
            WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
            WHEN Vehicle_Type IN ('Delivery_Van_4_wheelers', 'Delivery_Van_3_wheelers') THEN 'Delivery Vehicles'
            WHEN Vehicle_Type IN ('Tractors', 'Trailers') THEN 'Agricultural Vehicles'
            ELSE 'Others'
        END as category,
        vehicle_count
    FROM base_categories
)
SELECT
    display_year,
    category,
    SUM(vehicle_count) as count
FROM categorized
GROUP BY display_year, category
ORDER BY display_year ASC, category
```

```sql detailed_two_wheelers
SELECT
    SPLIT_PART(Year, '-', 1) as display_year,
    CASE
        WHEN Vehicle_Type = 'Motor_Cycles' THEN 'Motorcycles'
        WHEN Vehicle_Type = 'Scooters' THEN 'Scooters'
        WHEN Vehicle_Type = 'Moped' THEN 'Mopeds'
    END as subcategory,
    Count
FROM vehicle_registrations_by_type_and_year
WHERE Vehicle_Type IN ('Motor_Cycles', 'Scooters', 'Moped')
ORDER BY display_year ASC, subcategory
```

```sql detailed_personal
SELECT
    SPLIT_PART(Year, '-', 1) as display_year,
    CASE
        WHEN Vehicle_Type = 'Cars' THEN 'Cars'
        WHEN Vehicle_Type = 'Jeeps' THEN 'Jeeps'
        WHEN Vehicle_Type = 'Stn_Wagons' THEN 'Station Wagons'
    END as subcategory,
    Count
FROM vehicle_registrations_by_type_and_year
WHERE Vehicle_Type IN ('Cars', 'Jeeps', 'Stn_Wagons')
ORDER BY display_year ASC, subcategory
```

```sql detailed_commercial
SELECT
    display_year,
    subcategory,
    SUM(Count) as Count
FROM (
    SELECT
        SPLIT_PART(Year, '-', 1) as display_year,
        CASE
            WHEN Vehicle_Type = 'Auto_rickshaw' THEN 'Auto Rickshaw'
            WHEN Vehicle_Type IN ('Taxi_w_meter', 'Luxury_Tourist_Cabs') THEN 'Taxi Services'
            WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated_Multi') THEN 'Heavy Transport'
            WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
            WHEN Vehicle_Type IN ('Delivery_Van_4_wheelers', 'Delivery_Van_3_wheelers') THEN 'Delivery Vehicles'
            WHEN Vehicle_Type = 'School_Buses' THEN 'School Buses'
            WHEN Vehicle_Type IN ('Private_Service_Vehicles', 'Ambulances') THEN 'Service Vehicles'
            WHEN Vehicle_Type IN ('Tractors', 'Trailers') THEN 'Agricultural Vehicles'
        END as subcategory,
        Count
    FROM vehicle_registrations_by_type_and_year
    WHERE Vehicle_Type IN ('Auto_rickshaw', 'Taxi_w_meter', 'Luxury_Tourist_Cabs',
                          'Trucks/Lorries', 'Articulated_Multi', 'Tanker', 'Delivery_Van_4_wheelers',
                          'Delivery_Van_3_wheelers', 'Private_Service_Vehicles', 'Ambulances',
                          'Tractors', 'Trailers', 'School_Buses')
)
GROUP BY display_year, subcategory
ORDER BY display_year ASC, subcategory
```

```sql new_registrations
WITH yearly_totals AS (
    SELECT
        SPLIT_PART(Year, '-', 1) as display_year,
        CASE
            WHEN Vehicle_Type IN ('Motor_Cycles', 'Scooters', 'Moped') THEN 'Two Wheelers'
            WHEN Vehicle_Type IN ('Cars', 'Jeeps', 'Stn_Wagons') THEN 'Cars & SUVs'
            ELSE 'Commercial & Others'
        END as category,
        SUM(Count) as cumulative
    FROM vehicle_registrations_by_type_and_year
    GROUP BY display_year, category
),
with_prev AS (
    SELECT
        display_year,
        category,
        cumulative,
        LAG(cumulative) OVER (PARTITION BY category ORDER BY display_year) as prev_cumulative
    FROM yearly_totals
)
SELECT
    display_year,
    category,
    cumulative - COALESCE(prev_cumulative, 0) as new_registrations
FROM with_prev
WHERE prev_cumulative IS NOT NULL
ORDER BY display_year ASC, category
```

```sql new_registrations_total
WITH yearly_totals AS (
    SELECT
        SPLIT_PART(Year, '-', 1) as display_year,
        SUM(Count) as cumulative
    FROM vehicle_registrations_by_type_and_year
    GROUP BY display_year
),
with_prev AS (
    SELECT
        display_year,
        cumulative,
        LAG(cumulative) OVER (ORDER BY display_year) as prev_cumulative
    FROM yearly_totals
)
SELECT
    display_year,
    cumulative - prev_cumulative as new_registrations,
    ROUND((cumulative - prev_cumulative) * 100.0 / prev_cumulative, 1) as yoy_growth_pct
FROM with_prev
WHERE prev_cumulative IS NOT NULL
ORDER BY display_year ASC
```

```sql per_capita
WITH yearly AS (
    SELECT
        SPLIT_PART(Year, '-', 1) as display_year,
        CAST(SPLIT_PART(Year, '-', 1) AS INT) as start_year,
        SUM(CASE WHEN Vehicle_Type IN ('Motor_Cycles', 'Scooters', 'Moped') THEN Count ELSE 0 END) as two_wheelers,
        SUM(CASE WHEN Vehicle_Type IN ('Cars', 'Jeeps', 'Stn_Wagons') THEN Count ELSE 0 END) as four_wheelers,
        SUM(Count) as total
    FROM vehicle_registrations_by_type_and_year
    GROUP BY display_year, start_year
)
SELECT
    display_year,
    -- Census 2001: 1006417, Census 2011: 1727692, linear interpolation
    ROUND(total / (CASE
        WHEN start_year <= 2001 THEN 1006417
        WHEN start_year >= 2011 THEN 1727692
        ELSE 1006417 + (1727692.0 - 1006417) * (start_year - 2001) / 10.0
    END) * 1000, 0) as vehicles_per_1000,
    ROUND(two_wheelers / (CASE
        WHEN start_year <= 2001 THEN 1006417
        WHEN start_year >= 2011 THEN 1727692
        ELSE 1006417 + (1727692.0 - 1006417) * (start_year - 2001) / 10.0
    END) * 1000, 0) as two_wheelers_per_1000,
    ROUND(four_wheelers / (CASE
        WHEN start_year <= 2001 THEN 1006417
        WHEN start_year >= 2011 THEN 1727692
        ELSE 1006417 + (1727692.0 - 1006417) * (start_year - 2001) / 10.0
    END) * 1000, 0) as four_wheelers_per_1000
FROM yearly
ORDER BY display_year
```

## See Also

- **[Fleet Composition Trends](/PCMC/Fleet_Composition_Trends)** — Growth rates, indexed comparisons, and market share analysis of the same registration data
- **[Pune vs PCMC Vehicles](/PCMC/Pune_PCMC_Comparison)** — PCMC's registered fleet in context: how it compares to Pune across 18 years
- **[Road Safety](/PCMC/Road_Accident_Statistics)** — How the growing vehicle fleet affected accident rates

## Sources
- [Open City Urban Data Portal](https://data.opencity.in/dataset/maharashtra-vehicles-registration-data/resource/maharashtra-vehicles-registration-data---2001-2018)

*Data: cumulative vehicle registrations with the Pimpri-Chinchwad RTO, 2000-2001 to 2017-2018. Source: Maharashtra state RTO registration data.*
