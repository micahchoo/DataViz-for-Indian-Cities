---
title: Vehicle Registration Insights - Market Dynamics
description: Revealing the interesting stories hidden in vehicle registration data through growth rates, market share shifts, and emerging trends
---

This analysis reveals market dynamics and compositional changes in vehicle registrations from 2000 to 2018, going beyond simple growth to uncover the real stories in the data.

```sql view_options
SELECT 'Growth Rates' as value
UNION ALL SELECT 'Market Share'
UNION ALL SELECT 'Indexed Growth'
UNION ALL SELECT 'Emerging Categories'
UNION ALL SELECT 'Two-Wheeler Battle'
UNION ALL SELECT 'Commercial vs Personal'
UNION ALL SELECT 'Declining Categories'
```

```sql year_range_options
SELECT '2000' as value, 'Full Period (2000-2017)' as label
UNION ALL SELECT '2005', '2000-2005'
UNION ALL SELECT '2010', '2005-2010'
UNION ALL SELECT '2017', '2010-2017'
UNION ALL SELECT '2008', 'Last Decade (2008-2017)'
```

```sql category_options
SELECT 'All Categories' as value
UNION ALL SELECT 'Two Wheelers'
UNION ALL SELECT 'Cars'
UNION ALL SELECT 'SUVs & Wagons'
UNION ALL SELECT 'Taxi Services'
UNION ALL SELECT 'Auto Rickshaws'
UNION ALL SELECT 'Public Transport'
UNION ALL SELECT 'School Transport'
UNION ALL SELECT 'Service Vehicles'
UNION ALL SELECT 'Heavy Transport'
UNION ALL SELECT 'Tankers'
UNION ALL SELECT 'Delivery Vehicles'
UNION ALL SELECT 'Agricultural Vehicles'
UNION ALL SELECT 'Others'
```

```sql chart_type_options
SELECT 'Line Chart' as value
UNION ALL SELECT 'Area Chart'
UNION ALL SELECT 'Bar Chart'
```

```sql metric_options
SELECT 'Percentage' as value, 'Market Share (%)' as label
UNION ALL SELECT 'Absolute', 'Absolute Count'
```

```sql yoy_growth_by_category
WITH yearly_data AS (
  SELECT 
    SPLIT_PART(Year, '-', 1) as display_year,
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
    Count as vehicle_count
  FROM vehicle_registrations_by_type_and_year
),
aggregated AS (
  SELECT 
    display_year,
    category,
    SUM(vehicle_count) as count
  FROM yearly_data
  GROUP BY display_year, category
),
with_lag AS (
  SELECT 
    display_year,
    category,
    count,
    LAG(count) OVER (PARTITION BY category ORDER BY display_year) as prev_count
  FROM aggregated
)
SELECT 
  display_year,
  category,
  count,
  CASE 
    WHEN prev_count > 0 AND prev_count IS NOT NULL
    THEN ROUND(((count - prev_count) * 100.0 / prev_count), 2)
    ELSE NULL
  END as yoy_growth_pct
FROM with_lag
WHERE prev_count IS NOT NULL
ORDER BY display_year ASC, category
```

```sql market_share_evolution
WITH yearly_totals AS (
  SELECT 
    SPLIT_PART(Year, '-', 1) as display_year,
    SUM(Count) as total_count
  FROM vehicle_registrations_by_type_and_year
  GROUP BY display_year
),
categorized AS (
  SELECT 
    SPLIT_PART(Year, '-', 1) as display_year,
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
    Count as vehicle_count
  FROM vehicle_registrations_by_type_and_year
),
category_totals AS (
  SELECT 
    display_year,
    category,
    SUM(vehicle_count) as count
  FROM categorized
  GROUP BY display_year, category
)
SELECT 
  c.display_year,
  c.category,
  c.count,
  ROUND((c.count * 100.0 / t.total_count), 2) as market_share_pct
FROM category_totals c
JOIN yearly_totals t ON c.display_year = t.display_year
ORDER BY c.display_year ASC, c.category
```

```sql indexed_growth
WITH base_year AS (
  SELECT 
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
    SUM(Count) as base_count
  FROM vehicle_registrations_by_type_and_year
  WHERE Year = '2000-2001'
  GROUP BY category
),
all_years AS (
  SELECT 
    SPLIT_PART(Year, '-', 1) as display_year,
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
    SUM(Count) as count
  FROM vehicle_registrations_by_type_and_year
  GROUP BY display_year, category
)
SELECT 
  a.display_year,
  a.category,
  a.count,
  ROUND((a.count * 100.0 / b.base_count), 1) as index_value
FROM all_years a
JOIN base_year b ON a.category = b.category
WHERE b.base_count > 0
ORDER BY a.display_year ASC, a.category
```

```sql emerging_categories
SELECT 
  SPLIT_PART(Year, '-', 1) as display_year,
  CASE 
    WHEN Vehicle_Type = 'Luxury_Tourist_Cabs' THEN 'Luxury Tourist Cabs'
    WHEN Vehicle_Type = 'Delivery_Van_3_wheelers_' THEN '3-Wheeler Delivery Vans'
    WHEN Vehicle_Type = 'Delivery_Van_4_wheelers_' THEN '4-Wheeler Delivery Vans'
    WHEN Vehicle_Type = 'Ambulances' THEN 'Ambulances'
  END as subcategory,
  Count
FROM vehicle_registrations_by_type_and_year
WHERE Vehicle_Type IN ('Luxury_Tourist_Cabs', 'Delivery_Van_3_wheelers_', 
                       'Delivery_Van_4_wheelers_', 'Ambulances')
ORDER BY display_year ASC, subcategory
```

```sql two_wheeler_composition
WITH two_wheeler_total AS (
  SELECT 
    SPLIT_PART(Year, '-', 1) as display_year,
    SUM(Count) as total_two_wheelers
  FROM vehicle_registrations_by_type_and_year
  WHERE Vehicle_Type IN ('Motor_Cycles', 'Scooters', 'Moped')
  GROUP BY display_year
)
SELECT 
  SPLIT_PART(v.Year, '-', 1) as display_year,
  CASE 
    WHEN v.Vehicle_Type = 'Motor_Cycles' THEN 'Motorcycles'
    WHEN v.Vehicle_Type = 'Scooters' THEN 'Scooters'
    WHEN v.Vehicle_Type = 'Moped' THEN 'Mopeds'
  END as subcategory,
  v.Count,
  ROUND((v.Count * 100.0 / t.total_two_wheelers), 2) as share_of_two_wheelers
FROM vehicle_registrations_by_type_and_year v
JOIN two_wheeler_total t ON SPLIT_PART(v.Year, '-', 1) = t.display_year
WHERE v.Vehicle_Type IN ('Motor_Cycles', 'Scooters', 'Moped')
ORDER BY display_year ASC, subcategory
```

```sql commercial_personal_ratio
WITH categorized AS (
  SELECT 
    SPLIT_PART(Year, '-', 1) as display_year,
    CASE 
      WHEN Vehicle_Type IN ('Cars', 'Jeeps', 'Stn_Wagons', 'Motor_Cycles', 'Scooters', 'Moped') 
      THEN 'Personal'
      ELSE 'Commercial'
    END as usage_type,
    Count
  FROM vehicle_registrations_by_type_and_year
)
SELECT 
  display_year,
  SUM(CASE WHEN usage_type = 'Personal' THEN Count ELSE 0 END) as personal,
  SUM(CASE WHEN usage_type = 'Commercial' THEN Count ELSE 0 END) as commercial,
  ROUND(SUM(CASE WHEN usage_type = 'Commercial' THEN Count ELSE 0 END) * 100.0 / 
    (SUM(CASE WHEN usage_type = 'Personal' THEN Count ELSE 0 END) + 
     SUM(CASE WHEN usage_type = 'Commercial' THEN Count ELSE 0 END)), 2) as commercial_pct
FROM categorized
GROUP BY display_year
ORDER BY display_year
```

```sql declining_categories
WITH yearly_data AS (
  SELECT 
    SPLIT_PART(Year, '-', 1) as display_year,
    Vehicle_Type,
    Count
  FROM vehicle_registrations_by_type_and_year
  WHERE Vehicle_Type IN ('Moped', 'Stage_carriages', 'Stn_Wagons')
)
SELECT 
  display_year,
  CASE 
    WHEN Vehicle_Type = 'Moped' THEN 'Mopeds'
    WHEN Vehicle_Type = 'Stage_carriages' THEN 'Stage Carriages'
    WHEN Vehicle_Type = 'Stn_Wagons' THEN 'Station Wagons'
  END as subcategory,
  Count
FROM yearly_data
ORDER BY display_year ASC, subcategory
```

<ButtonGroup 
 name=selected_view 
 data={view_options}
 value=value
 title="Select Analysis View"
 defaultValue="Growth Rates"
 display=buttons
/>

{#if inputs.selected_view === "Growth Rates"}

### Year-over-Year Growth Rates

Understanding market dynamics through growth velocity rather than absolute size.

<Dropdown
  name=growth_year_filter
  data={year_range_options}
  value=value
  label=label
  title="Select Time Period"
  defaultValue="2000"
/>

<Dropdown
  name=growth_chart_type
  data={chart_type_options}
  value=value
  title="Chart Type"
  defaultValue="Line Chart"
/>

<Dropdown
  name=growth_categories
  data={category_options}
  value=value
  title="Filter Categories"
  defaultValue="All Categories"
  multiple=true
/>

```sql filtered_growth
SELECT *
FROM ${yoy_growth_by_category}
WHERE display_year >= '${inputs.growth_year_filter}'
  AND (
    ${!inputs.growth_categories || inputs.growth_categories.length === 0 || inputs.growth_categories.includes('All Categories') ? '1=1' : 
      'category IN (' + inputs.growth_categories.map(c => "'" + c + "'").join(',') + ')'
    }
  )
```

{#if inputs.growth_chart_type === "Line Chart"}
<LineChart
     data={filtered_growth}
     x=display_year
     y=yoy_growth_pct
     series=category
     title="Annual Growth Rate by Category"
     subtitle="Revealing which categories are accelerating or decelerating"
     xAxisTitle="Year"
     yAxisTitle="YoY Growth (%)"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{:else if inputs.growth_chart_type === "Area Chart"}
<AreaChart
     data={filtered_growth}
     x=display_year
     y=yoy_growth_pct
     series=category
     title="Annual Growth Rate by Category"
     subtitle="Revealing which categories are accelerating or decelerating"
     xAxisTitle="Year"
     yAxisTitle="YoY Growth (%)"
     chartAreaHeight=450
     fillOpacity=0.6
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{:else}
<BarChart
     data={filtered_growth}
     x=display_year
     y=yoy_growth_pct
     series=category
     title="Annual Growth Rate by Category"
     subtitle="Revealing which categories are accelerating or decelerating"
     xAxisTitle="Year"
     yAxisTitle="YoY Growth (%)"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{/if}

<DataTable
  data={filtered_growth}
  search=true
  rows=10
/>

**Key Insights:** This chart shows the velocity of change rather than just size. Categories with volatile growth rates may indicate market disruption, while steady growth suggests mature, stable markets.

{:else if inputs.selected_view === "Market Share"}

### Market Share Evolution

How the composition of vehicle registrations has shifted over time.

<Dropdown
  name=share_year_filter
  data={year_range_options}
  value=value
  label=label
  title="Select Time Period"
  defaultValue="2000"
/>

<Dropdown
  name=share_metric
  data={metric_options}
  value=value
  label=label
  title="Display Metric"
  defaultValue="Percentage"
/>

<Dropdown
  name=share_categories
  data={category_options}
  value=value
  title="Filter Categories"
  defaultValue="All Categories"
  multiple=true
/>

```sql filtered_share
SELECT *
FROM ${market_share_evolution}
WHERE display_year >= '${inputs.share_year_filter}'
  AND (
    ${!inputs.share_categories || inputs.share_categories.length === 0 || inputs.share_categories.includes('All Categories') ? '1=1' : 
      'category IN (' + inputs.share_categories.map(c => "'" + c + "'").join(',') + ')'
    }
  )
```

{#if inputs.share_metric === "Percentage"}
<LineChart
     data={filtered_share}
     x=display_year
     y=market_share_pct
     series=category
     title="Market Share by Category"
     subtitle="The changing composition of registered vehicles"
     xAxisTitle="Year"
     yAxisTitle="Market Share (%)"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />

<AreaChart
     data={filtered_share}
     x=display_year
     y=market_share_pct
     series=category
     type=stacked100
     title="Market Share Distribution"
     subtitle="100% stacked view of category composition"
     xAxisTitle="Year"
     fillOpacity=0.9
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{:else}
<LineChart
     data={filtered_share}
     x=display_year
     y=count
     series=category
     title="Absolute Registrations by Category"
     subtitle="Total vehicle registrations over time"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{/if}

<DataTable
  data={filtered_share}
  search=true
  rows=10
/>

**Key Insights:** Market share reveals winners and losers. Even if absolute numbers are growing, a declining market share indicates relative underperformance.

{:else if inputs.selected_view === "Indexed Growth"}

### Indexed Growth (Base Year 2000 = 100)

Compare growth trajectories across categories of different sizes.

<Dropdown
  name=index_year_filter
  data={year_range_options}
  value=value
  label=label
  title="Select Time Period"
  defaultValue="2000"
/>

<Dropdown
  name=index_categories
  data={category_options}
  value=value
  title="Compare Categories"
  defaultValue="All Categories"
  multiple=true
/>

<Slider
  name=index_threshold
  title="Show categories with index above:"
  min=0
  max=1000
  defaultValue=0
  step=50
/>

```sql filtered_index
SELECT *
FROM ${indexed_growth}
WHERE display_year >= '${inputs.index_year_filter}'
  AND index_value >= ${inputs.index_threshold}
  AND (
    ${!inputs.index_categories || inputs.index_categories.length === 0 || inputs.index_categories.includes('All Categories') ? '1=1' : 
      'category IN (' + inputs.index_categories.map(c => "'" + c + "'").join(',') + ')'
    }
  )
```

<LineChart
     data={filtered_index}
     x=display_year
     y=index_value
     series=category
     title="Growth Index by Category"
     subtitle="All categories start at 100 in year 2000 for easy comparison"
     xAxisTitle="Year"
     yAxisTitle="Index (2000 = 100)"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />

<DataTable
  data={filtered_index}
  search=true
  rows=10
/>

**Key Insights:** Indexed growth makes it easy to compare percentage growth regardless of category size. A small category growing from 100 to 500 (5x) is more impressive than a large category growing from 100 to 150 (1.5x).

{:else if inputs.selected_view === "Emerging Categories"}

### Emerging Categories

Small but potentially high-growth categories that tell economic stories.

<Dropdown
  name=emerging_year_filter
  data={year_range_options}
  value=value
  label=label
  title="Select Time Period"
  defaultValue="2000"
/>

<Dropdown
  name=emerging_chart_type
  data={chart_type_options}
  value=value
  title="Chart Type"
  defaultValue="Line Chart"
/>

```sql filtered_emerging
SELECT *
FROM ${emerging_categories}
WHERE display_year >= '${inputs.emerging_year_filter}'
```

{#if inputs.emerging_chart_type === "Line Chart"}
<LineChart
     data={filtered_emerging}
     x=display_year
     y=Count
     series=subcategory
     title="Emerging Vehicle Categories"
     subtitle="Tracking tourism, delivery, and healthcare vehicle growth"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{:else if inputs.emerging_chart_type === "Area Chart"}
<AreaChart
     data={filtered_emerging}
     x=display_year
     y=Count
     series=subcategory
     title="Emerging Vehicle Categories"
     subtitle="Tracking tourism, delivery, and healthcare vehicle growth"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     chartAreaHeight=450
     fillOpacity=0.7
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{:else}
<BarChart
     data={filtered_emerging}
     x=display_year
     y=Count
     series=subcategory
     title="Emerging Vehicle Categories"
     subtitle="Tracking tourism, delivery, and healthcare vehicle growth"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{/if}

<DataTable
  data={filtered_emerging}
  search=true
  rows=10
/>

**Key Insights:**
- **Luxury Tourist Cabs:** Reflects growth in tourism industry
- **Delivery Vans:** Early signals of e-commerce and logistics growth
- **Ambulances:** Healthcare infrastructure development

{:else if inputs.selected_view === "Two-Wheeler Battle"}

### The Two-Wheeler Market: Motorcycles vs Scooters

Who's winning the battle for two-wheeler dominance?

<Dropdown
  name=twowheeler_year_filter
  data={year_range_options}
  value=value
  label=label
  title="Select Time Period"
  defaultValue="2000"
/>

<Dropdown
  name=twowheeler_metric
  data={metric_options}
  value=value
  label=label
  title="Display Metric"
  defaultValue="Percentage"
/>

```sql filtered_twowheeler
SELECT *
FROM ${two_wheeler_composition}
WHERE display_year >= '${inputs.twowheeler_year_filter}'
```

{#if inputs.twowheeler_metric === "Percentage"}
<LineChart
     data={filtered_twowheeler}
     x=display_year
     y=share_of_two_wheelers
     series=subcategory
     title="Two-Wheeler Market Share"
     subtitle="Composition of motorcycles, scooters, and mopeds"
     xAxisTitle="Year"
     yAxisTitle="Share of Two-Wheelers (%)"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />

<AreaChart
     data={filtered_twowheeler}
     x=display_year
     y=share_of_two_wheelers
     series=subcategory
     type=stacked100
     title="Two-Wheeler Market Composition"
     subtitle="100% stacked view"
     xAxisTitle="Year"
     fillOpacity=0.9
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{:else}
<LineChart
     data={filtered_twowheeler}
     x=display_year
     y=Count
     series=subcategory
     title="Two-Wheeler Registrations"
     subtitle="Absolute numbers by type"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{/if}

<DataTable
  data={filtered_twowheeler}
  search=true
  rows=10
/>

**Key Insights:** The shift between motorcycles and scooters can indicate changing consumer preferences, urbanization patterns, or demographic shifts (scooters are often preferred by women and in urban areas).

{:else if inputs.selected_view === "Commercial vs Personal"}

### Commercial vs Personal Vehicle Balance

How the ratio of commercial to personal vehicles reveals economic activity.

<Dropdown
  name=ratio_year_filter
  data={year_range_options}
  value=value
  label=label
  title="Select Time Period"
  defaultValue="2000"
/>

<Dropdown
  name=ratio_display
  title="Display View"
  defaultValue="Percentage"
>
  <DropdownOption value="Percentage" valueLabel="Commercial % Only" />
  <DropdownOption value="Split" valueLabel="Split View" />
  <DropdownOption value="Both" valueLabel="Both Metrics" />
</Dropdown>

```sql filtered_ratio
SELECT *
FROM ${commercial_personal_ratio}
WHERE display_year >= '${inputs.ratio_year_filter}'
```

{#if inputs.ratio_display === "Percentage"}
<LineChart
     data={filtered_ratio}
     x=display_year
     y=commercial_pct
     title="Commercial Vehicle Penetration"
     subtitle="Commercial vehicles as a percentage of total registrations"
     xAxisTitle="Year"
     yAxisTitle="Commercial Vehicle %"
     chartAreaHeight=450
     yGridLines=true
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{:else if inputs.ratio_display === "Split"}
<AreaChart
     data={filtered_ratio}
     x=display_year
     y={['personal', 'commercial']}
     type=stacked100
     title="Personal vs Commercial Vehicle Split"
     subtitle="Distribution of vehicle registrations by usage type"
     xAxisTitle="Year"
     fillOpacity=0.9
     chartAreaHeight=450
     yGridLines=true
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{:else}
<LineChart
     data={filtered_ratio}
     x=display_year
     y=commercial_pct
     title="Commercial Vehicle Penetration"
     subtitle="Commercial vehicles as a percentage of total registrations"
     xAxisTitle="Year"
     yAxisTitle="Commercial Vehicle %"
     chartAreaHeight=400
     yGridLines=true
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />

<LineChart
     data={filtered_ratio}
     x=display_year
     y={['personal', 'commercial']}
     title="Personal vs Commercial Vehicle Counts"
     subtitle="Absolute numbers by usage type"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     chartAreaHeight=400
     yGridLines=true
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{/if}

<DataTable
  data={filtered_ratio}
  search=true
  rows=10
/>

**Key Insights:** Rising commercial vehicle share indicates increased economic activity, logistics growth, and business expansion. Personal vehicle dominance suggests consumer-driven growth.

{:else}

### Declining Categories

Categories losing ground in the modern vehicle landscape.

<Dropdown
  name=decline_year_filter
  data={year_range_options}
  value=value
  label=label
  title="Select Time Period"
  defaultValue="2000"
/>

<Dropdown
  name=decline_chart_type
  data={chart_type_options}
  value=value
  title="Chart Type"
  defaultValue="Line Chart"
/>

```sql filtered_decline
SELECT *
FROM ${declining_categories}
WHERE display_year >= '${inputs.decline_year_filter}'
```

{#if inputs.decline_chart_type === "Line Chart"}
<LineChart
     data={filtered_decline}
     x=display_year
     y=Count
     series=subcategory
     title="Categories in Decline"
     subtitle="Traditional vehicle types being replaced by modern alternatives"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     chartAreaHeight=450
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{:else}
<AreaChart
     data={filtered_decline}
     x=display_year
     y=Count
     series=subcategory
     title="Categories in Decline"
     subtitle="Traditional vehicle types being replaced by modern alternatives"
     xAxisTitle="Year"
     yAxisTitle="Registrations"
     chartAreaHeight=450
     fillOpacity=0.7
     yGridLines=true
     sort=false
     xLabelWrap=true
     xGridlines=true
     xTickMarks=true
 />
{/if}

<DataTable
  data={filtered_decline}
  search=true
  rows=10
/>

**Key Insights:**
- **Mopeds:** Being replaced by motorcycles and scooters with better performance
- **Stage Carriages:** Traditional public transport losing to private vehicles and modern buses
- **Station Wagons:** Shifting preference toward SUVs and crossovers

{/if}

## Interactive Features Guide

This dashboard includes several interactive controls to help you explore the data:

**Time Period Filters:** Select different time ranges to focus on specific periods of interest. Compare early growth (2000-2005) vs recent trends (2010-2017).

**Chart Type Selectors:** Switch between line charts, area charts, and bar charts to see which visualization best reveals patterns.

**Category Filters:** Use multi-select dropdowns to compare specific categories of interest. Great for benchmarking or competitive analysis.

**Metric Toggles:** Switch between percentages and absolute numbers to see both relative and absolute performance.

**Range Sliders:** Filter data based on growth thresholds to focus on high performers or outliers.

**Data Tables:** Every view includes a searchable data table below the charts for detailed exploration and validation.

## Why These Views Matter

Traditional stacked area charts showing absolute growth can be misleading because they:
- Make large categories dominate visually
- Hide relative performance and market dynamics
- Miss acceleration/deceleration patterns
- Obscure interesting stories in smaller categories

These alternative views reveal:
- **Market momentum** through growth rates
- **Competitive dynamics** through market share shifts
- **Relative performance** through indexed comparisons
- **Economic signals** through commercial/personal ratios
- **Emerging opportunities** through small but fast-growing categories

## Sources
- [Open City Urban Data Portal](https://data.opencity.in/dataset/maharashtra-vehicles-registration-data/resource/maharashtra-vehicles-registration-data---2001-2018)