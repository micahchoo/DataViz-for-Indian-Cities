# Table Analysis
[Download CSV file](Existing%20vs%20New%20Vehicle%20Registrations%20by%20Type%20and%20Year.csv)

1. This table contains data on the existing and new registrations of different types of vehicles in India FROM 2002 to 2007, including two-wheelers, auto cars/light motor vehicles (LMVs), heavy vehicles, and others. 

1. Key insights:
Existing
- Two-wheelers had the highest production volume and the second-highest AACGR (13.31%), indicating a significant demand for affordable personal transportation.
- Heavy vehicles had the highest AACGR (16.57%), suggesting a growing demand for commercial transportation and infrastructure development.
New
- Two Wheelers (motorcycles, scooters, etc.) dominate the production numbers, consistently accounting for the highest share across all years.
- There is a significant increase in the production of Heavy Vehicles, FROM 470 units in 2002-03 to 4,048 units in 2006-07, indicating a growing demand for commercial vehicles.


I'll create a comprehensive set of SQL queries and stacked area charts for all vehicle categories, maintaining the same structure for each category.

```sql all_vehicle_categories
WITH base_categories AS (
  SELECT 
    Year,
    'Two Wheelers' as category,
    CASE WHEN Vehicle_Type IN ('Motor_Cycles', 'Scooters', 'Moped') THEN Count ELSE 0 END as Count
  FROM vehicle_registrations_by_type_and_year
  
  UNION ALL
  
  SELECT 
    Year,
    'Personal Vehicles' as category,
    CASE WHEN Vehicle_Type IN ('Cars', 'Jeeps', 'Stn_Wagons') THEN Count ELSE 0 END as Count
  FROM vehicle_registrations_by_type_and_year
  
  UNION ALL
  
  SELECT 
    Year,
    'Commercial Passenger' as category,
    CASE WHEN Vehicle_Type IN ('Auto_rickshaw', 'Stage_carriages', 'Mini_Bus', 'School_Buses', 'Taxi_w_meter', 'Luxury_Tourist_Cabs') 
        THEN Count ELSE 0 END as Count
  FROM vehicle_registrations_by_type_and_year
  
  UNION ALL
  
  SELECT 
    Year,
    'Commercial Goods' as category,
    CASE WHEN Vehicle_Type IN ('Trucks/Lorries', 'Tanker', 'Delivery_Van_4_wheelers_', 'Delivery_Van_3_wheelers_') 
        THEN Count ELSE 0 END as Count
  FROM vehicle_registrations_by_type_and_year
)
SELECT 
  Year,
  category,
  SUM(Count) as Count
FROM base_categories
GROUP BY Year, category
ORDER BY Year ASC, category;
```


# Overall Vehicle Distribution

<AreaChart
    data={all_vehicle_categories}
    x=Year
    y=Count
    series=category
    type=stacked
    title="Overall Vehicle Registration Distribution"
    subtitle="Counts across major vehicle categories"
    yAxisLabels=true
    xAxisTitle="Year"
    fillOpacity=0.9
    connectGroup="A"
    chartAreaHeight=200
    yGridLines=true
    sort=false
/>



```sql two_wheelers
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

ORDER BY Year ASC, subcategory;
```



# Two Wheeler Distribution

<AreaChart
 data={two_wheelers}
 x=Year
 y=Count
 series=subcategory
 type=stacked
 title="Two Wheeler Registration Distribution"
 subtitle="Percentage breakdown of two-wheeler vehicle types"
 yAxisTitle="Percentage of Two Wheelers"
 xAxisTitle="Year"
 fillOpacity=0.8
 connectGroup="A"
 sort="false"
/>

