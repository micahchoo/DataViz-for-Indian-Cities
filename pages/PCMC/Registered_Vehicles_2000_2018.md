---
title: What Vehicles are being registered - 2000 to 2018
---
<script>
    let myColors = [
        // Warm oranges and peaches
        '#de988a', // Pastel peach
        '#fae9c3', // Pale gold

        // Pinks and roses
        '#e0a8b5', // Light rose
        '#eba0c0', // Baby pink
        '#e3bcd9', // Lavender pink

        // Purples and lavenders
        '#D4B5FA', // Soft purple
        '#E2C6FA', // Pale violet
        '#FAF0FA', // Soft periwinkle

        // Blues and periwinkles
        '#B5D1FA', // Light sky blue
        '#C4DDFA', // Pale blue
        '#D1E5FA', // Soft azure
        '#E9F5FA', // Pale cerulean

        // Yellow tones
        '#faeaa7', // Soft butter
        '#f0e6c5', // Pale vanilla

        // Transitional hues
        '#FAD1E5', // Soft salmon pink
        '#FAE0EB', // Light coral pink
        '#FAEEF5', // Pale rose pink
        '#F5E6FA', // Soft lavender
        '#E6F0FA', // Pale sky blue
        '#F0F7FA'  // Light air blue
    ]
</script>


```sql view_options
select 'Overall' as view union all
select 'Two Wheelers' as view union all 
select 'Personal Vehicles' as view union all
select 'Commercial Vehicles' as view
```
```sql all_categories
WITH base_categories AS (
    SELECT Year,
    CASE 
        WHEN Vehicle_Type IN ('Motor_Cycles', 'Scooters', 'Moped') THEN 'Two Wheelers'
        WHEN Vehicle_Type IN ('Cars') THEN 'Cars'
        WHEN Vehicle_Type IN ('Jeeps', 'Stn_Wagons') THEN 'SUVs & Wagons'
        WHEN Vehicle_Type IN ('Taxi_w_meter', 'Luxury_Tourist_Cabs') THEN 'Taxi Services'
        WHEN Vehicle_Type IN ('Auto_rickshaw') THEN 'Auto Rickshaws'
        WHEN Vehicle_Type IN ('Stage_carriages', 'Mini_Bus') THEN 'Public Transport'
        WHEN Vehicle_Type IN ('School_Buses') THEN 'School Transport'
        WHEN Vehicle_Type IN ('Private Service Vehicles', 'Ambulances') THEN 'Service Vehicles'
        WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated/Multi.') THEN 'Heavy Transport'
        WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
        WHEN Vehicle_Type IN ('Delivery_Van_4_wheelers_', 'Delivery_Van_3_wheelers_') THEN 'Delivery Vehicles'
        WHEN Vehicle_Type IN ('Tractors', 'Trailers') THEN 'Agricultural Vehicles'
        ELSE 'Others'
    END as category,
    SUM(Count) as Count
    FROM vehicle_registrations_by_type_and_year
    GROUP BY Year, Vehicle_Type
)
SELECT 
    Year,
    category,
    SUM(Count) as Count
FROM base_categories
GROUP BY Year, category
ORDER BY Year ASC, category
```

```sql detailed_two_wheelers
SELECT
    Year,
    CASE 
        WHEN Vehicle_Type = 'Motor_Cycles' THEN 'Motorcycles'
        WHEN Vehicle_Type = 'Scooters' THEN 'Scooters'
        WHEN Vehicle_Type = 'Moped' THEN 'Mopeds'
    END as subcategory,
    Count
FROM vehicle_registrations_by_type_and_year
WHERE Vehicle_Type IN ('Motor_Cycles', 'Scooters', 'Moped')
ORDER BY Year ASC, subcategory
```

```sql detailed_personal
SELECT
    Year,
    CASE 
        WHEN Vehicle_Type = 'Cars' THEN 'Cars'
        WHEN Vehicle_Type = 'Jeeps' THEN 'Jeeps'
        WHEN Vehicle_Type = 'Stn_Wagons' THEN 'Station Wagons'
    END as subcategory,
    Count
FROM vehicle_registrations_by_type_and_year
WHERE Vehicle_Type IN ('Cars', 'Jeeps', 'Stn_Wagons')
ORDER BY Year ASC, subcategory
```

```sql detailed_commercial
SELECT
    Year,
    CASE 
        WHEN Vehicle_Type = 'Auto_rickshaw' THEN 'Auto Rickshaw'
        WHEN Vehicle_Type = 'Taxi_w_meter' THEN 'Metered Taxis'
        WHEN Vehicle_Type = 'Luxury_Tourist_Cabs' THEN 'Tourist Cabs'
        WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated/Multi.') THEN 'Heavy Transport'
        WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
        WHEN Vehicle_Type = 'Delivery_Van_4_wheelers_' THEN '4-Wheeler Delivery Vans'
        WHEN Vehicle_Type = 'Delivery_Van_3_wheelers_' THEN '3-Wheeler Delivery Vans'
        WHEN Vehicle_Type = 'School_Buses' THEN 'School Buses'
        WHEN Vehicle_Type IN ('Private Service Vehicles', 'Ambulances') THEN 'Service Vehicles'
        WHEN Vehicle_Type IN ('Tractors', 'Trailers') THEN 'Agricultural Vehicles'
        ELSE 'Others'
    END as subcategory,
    Count
FROM vehicle_registrations_by_type_and_year
WHERE Vehicle_Type IN ('Auto_rickshaw', 'Taxi_w_meter', 'Luxury_Tourist_Cabs', 
                      'Trucks/Lorries', 'Tanker', 'Delivery_Van_4_wheelers_', 'Delivery_Van_3_wheelers_')
ORDER BY Year ASC, subcategory
```


<ButtonGroup 
 name=selected_view 
 data={view_options}
 value=view
 title="Select Vehicle Category View"
 defaultValue="Overall"
 display=buttons
/>



{#if inputs.selected_view === "Overall"}
### Overall Vehicle Registration Distribution
<AreaChart
     data={all_categories}
     x=Year
     y=Count
     series=category
     type=stacked
     title="Vehicle Registrations"
     subtitle="Distribution across major vehicle categories"
     xAxisTitle="Year"
     fillOpacity=0.9
     connectGroup="vehicles"
     chartAreaHeight=300
     yGridLines=true
     sort=false
    colorPalette={myColors}
 />
<AreaChart
     data={all_categories}
     x=Year
     y=Count
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
    colorPalette={myColors}    
 />

 {:else if inputs.selected_view === "Two Wheelers"}
### Two Wheeler Registration Distribution
<AreaChart
     data={detailed_two_wheelers}
     x=Year
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
    colorPalette={myColors}
 />

 <AreaChart
     data={detailed_two_wheelers}
     x=Year
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
    colorPalette={myColors}
 />

 {:else if inputs.selected_view === "Personal Vehicles"}
### Personal Vehicle Registration Distribution
<AreaChart
     data={detailed_personal}
     x=Year
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
    colorPalette={myColors}
 />
<AreaChart
     data={detailed_personal}
     x=Year
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
    colorPalette={myColors}
 />

{:else}
### Commercial Vehicle Registration Distribution
<AreaChart
     data={detailed_commercial}
     x=Year
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
    colorPalette={myColors}
 />
 <AreaChart
     data={detailed_commercial}
     x=Year
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
    colorPalette={myColors}
 />
 {/if}

## Sources
- [Open City Urban Data Portal](https://data.opencity.in/dataset/maharashtra-vehicles-registration-data/resource/maharashtra-vehicles-registration-data---2001-2018)