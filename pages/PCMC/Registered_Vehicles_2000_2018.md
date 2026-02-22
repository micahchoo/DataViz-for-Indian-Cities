---
title: What Vehicles are being registered
description: Cumulative vehicle registrations by type with the RTO from 2000 to 2018
---
This data shows the cumulative vehicle registrations by type with the Pimpri-Chinchwad RTO from 2000 to 2018. These are total on-road fleet counts (not annual new registrations), so rising numbers reflect the growing vehicle population over time.

```sql view_options
SELECT 'Overall' as view 
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
            WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated_Multi_') THEN 'Heavy Transport'
            WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
            WHEN Vehicle_Type IN ('Delivery_Van_4_wheelers_', 'Delivery_Van_3_wheelers_') THEN 'Delivery Vehicles'
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
    SPLIT_PART(Year, '-', 1) as display_year,
    CASE 
        WHEN Vehicle_Type = 'Auto_rickshaw' THEN 'Auto Rickshaw'
        WHEN Vehicle_Type = 'Taxi_w_meter' THEN 'Metered Taxis'
        WHEN Vehicle_Type = 'Luxury_Tourist_Cabs' THEN 'Tourist Cabs'
        WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated_Multi_') THEN 'Heavy Transport'
        WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
        WHEN Vehicle_Type = 'Delivery_Van_4_wheelers_' THEN '4-Wheeler Delivery Vans'
        WHEN Vehicle_Type = 'Delivery_Van_3_wheelers_' THEN '3-Wheeler Delivery Vans'
        WHEN Vehicle_Type = 'School_Buses' THEN 'School Buses'
        WHEN Vehicle_Type IN ('Private_Service_Vehicles', 'Ambulances') THEN 'Service Vehicles'
        WHEN Vehicle_Type IN ('Tractors', 'Trailers') THEN 'Agricultural Vehicles'
        ELSE 'Others'
    END as subcategory,
    Count
FROM vehicle_registrations_by_type_and_year
WHERE Vehicle_Type IN ('Auto_rickshaw', 'Taxi_w_meter', 'Luxury_Tourist_Cabs',
                      'Trucks/Lorries', 'Articulated_Multi_', 'Tanker', 'Delivery_Van_4_wheelers_',
                      'Delivery_Van_3_wheelers_', 'Private_Service_Vehicles', 'Ambulances',
                      'Tractors', 'Trailers', 'School_Buses')
ORDER BY display_year ASC, subcategory
```


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
<AreaChart
    data={all_categories}
    x=display_year
    y=count
    series=category
    type=stacked
    title="Vehicle Registrations"
    subtitle="Distribution across major vehicle categories"
    xAxisTitle="Year"
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

 {:else if inputs.selected_view === "Two Wheelers"}
### Two Wheeler Registration Distribution
<AreaChart
    data={detailed_two_wheelers}
    x=display_year
    y=Count
    series=subcategory
    type=stacked
    title="Two Wheeler Registrations"
    subtitle="Distribution of motorcycles, scooters, and mopeds"
    xAxisTitle="Year"
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
<AreaChart
     data={detailed_personal}
     x=display_year
     y=Count
     series=subcategory
     type=stacked
     title="Personal Vehicle Registrations"
     subtitle="Distribution of cars, jeeps, and station wagons"
     xAxisTitle="Year"
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
<AreaChart
     data={detailed_commercial}
     x=display_year
     y=Count
     series=subcategory
     type=stacked
     title="Commercial Vehicle Registrations"
     subtitle="Distribution across transport and goods vehicles"
     xAxisTitle="Year"
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

## Sources
- [Open City Urban Data Portal](https://data.opencity.in/dataset/maharashtra-vehicles-registration-data/resource/maharashtra-vehicles-registration-data---2001-2018)
