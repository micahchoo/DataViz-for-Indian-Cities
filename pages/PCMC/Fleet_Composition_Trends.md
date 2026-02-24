---
title: "How the Fleet Changed: Shifting Vehicle Mix, 2000–2018"
description: "How registered vehicle composition in Pimpri-Chinchwad shifted 2000–2018: growth rates, share changes, and emerging categories"
---

The [previous page](/PCMC/Registered_Vehicles_2000_2018) showed total vehicle growth by category. This page asks a different question: is Pimpri-Chinchwad's fleet becoming more or less diverse? The answer matters because a fleet dominated by two-wheelers signals different infrastructure needs than one balanced between two-wheelers and cars. Note: these are cumulative active registrations (the total stock on the RTO's books), not annual new sales — growth rates here reflect net fleet expansion, not single-year purchase patterns.

```sql view_options
SELECT 'Growth Rates' as value
UNION ALL SELECT 'Market Share'
UNION ALL SELECT 'Indexed Growth'
UNION ALL SELECT 'Emerging Categories'
UNION ALL SELECT 'Two-Wheeler Battle'
UNION ALL SELECT 'Commercial vs Personal'
UNION ALL SELECT 'Stagnating & Displaced'
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
      WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated_Multi') THEN 'Heavy Transport'
      WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
      WHEN Vehicle_Type IN ('Delivery_Van_4_wheelers', 'Delivery_Van_3_wheelers') THEN 'Delivery Vehicles'
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
      WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated_Multi') THEN 'Heavy Transport'
      WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
      WHEN Vehicle_Type IN ('Delivery_Van_4_wheelers', 'Delivery_Van_3_wheelers') THEN 'Delivery Vehicles'
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
      WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated_Multi') THEN 'Heavy Transport'
      WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
      WHEN Vehicle_Type IN ('Delivery_Van_4_wheelers', 'Delivery_Van_3_wheelers') THEN 'Delivery Vehicles'
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
      WHEN Vehicle_Type IN ('Trucks/Lorries', 'Articulated_Multi') THEN 'Heavy Transport'
      WHEN Vehicle_Type IN ('Tanker') THEN 'Tankers'
      WHEN Vehicle_Type IN ('Delivery_Van_4_wheelers', 'Delivery_Van_3_wheelers') THEN 'Delivery Vehicles'
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
    WHEN Vehicle_Type = 'Delivery_Van_3_wheelers' THEN '3-Wheeler Delivery Vans'
    WHEN Vehicle_Type = 'Delivery_Van_4_wheelers' THEN '4-Wheeler Delivery Vans'
    WHEN Vehicle_Type = 'Ambulances' THEN 'Ambulances'
  END as subcategory,
  Count
FROM vehicle_registrations_by_type_and_year
WHERE Vehicle_Type IN ('Luxury_Tourist_Cabs', 'Delivery_Van_3_wheelers', 
                       'Delivery_Van_4_wheelers', 'Ambulances')
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
  WHERE Vehicle_Type IN ('Moped', 'Taxi_w_meter', 'Stn_Wagons')
)
SELECT
  display_year,
  CASE
    WHEN Vehicle_Type = 'Moped' THEN 'Mopeds'
    WHEN Vehicle_Type = 'Taxi_w_meter' THEN 'Metered Taxis'
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

### Year-over-Year Fleet Growth Rates

How fast each category's registrations grew compared to the previous year.

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
WHERE display_year >= '${inputs.growth_year_filter.value || '2000'}'
  AND (
    ${!inputs.growth_categories || inputs.growth_categories.length === 0 || inputs.growth_categories.includes('All Categories') ? '1=1' : 
      'category IN (' + inputs.growth_categories.map(c => "'" + c + "'").join(',') + ')'
    }
  )
```

{#if inputs.growth_chart_type.value === "Line Chart"}
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
{:else if inputs.growth_chart_type.value === "Area Chart"}
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

**Key Insights:** Motorcycles and Cars consistently show the highest absolute growth rates (15-25% annually in early years, tapering to 6-10% by 2017). Smaller categories like School Buses or Ambulances show volatile spikes but from tiny bases. Note the across-the-board growth slowdown around 2008-09, coinciding with the global financial crisis.

{:else if inputs.selected_view === "Market Share"}

### Fleet Composition Share

How each category's share of the total registered fleet has shifted over time. Note: this reflects the accumulated stock of registrations, not the share of new vehicles being registered each year.

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
WHERE display_year >= '${inputs.share_year_filter.value || '2000'}'
  AND (
    ${!inputs.share_categories || inputs.share_categories.length === 0 || inputs.share_categories.includes('All Categories') ? '1=1' : 
      'category IN (' + inputs.share_categories.map(c => "'" + c + "'").join(',') + ')'
    }
  )
```

{#if inputs.share_metric.value === "Percentage"}
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
     yAxisTitle="Share (%)"
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

**Key Insights:** A category's share of the fleet can shrink even while its absolute numbers grow, if other categories are growing faster. Two-wheelers dominate the fleet (~70%), but their share has been slowly eroded by the growth in Cars.

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
WHERE display_year >= '${inputs.index_year_filter.value || '2000'}'
  AND index_value >= ${inputs.index_threshold || 0}
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

**Key Insights:** Cars grew to ~17x their 2000 base by 2018, outpacing even Motorcycles (~11x). The fastest-growing categories by index (Ambulances, School Transport) started from negligible bases. Use the threshold slider to filter out slow-growing categories and focus on the high-growth ones.

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
WHERE display_year >= '${inputs.emerging_year_filter.value || '2000'}'
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
- **Luxury Tourist Cabs:** Appears in 2007-08 exactly when Metered Taxis drops to zero — this is an RTO reclassification, not organic tourism growth. Subsequent growth reflects the broader taxi/cab market expansion
- **Delivery Vans:** Steady growth tracks Pimpri-Chinchwad's industrial and commercial expansion (auto manufacturing, IT parks). Late-period acceleration may partly reflect e-commerce logistics
- **Ambulances:** Growth from 206 to 1,693 likely reflects the 108 emergency service rollout and private hospital expansion

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
WHERE display_year >= '${inputs.twowheeler_year_filter.value || '2000'}'
```

{#if inputs.twowheeler_metric.value === "Percentage"}
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
     yAxisTitle="Share (%)"
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

**Key Insights:** Motorcycles dominated throughout, but scooters staged a dramatic comeback around 2013-14 (from 93,528 to 2,79,645 by 2017-18). This coincides with the gearless automatic scooter revolution (Honda Activa, TVS Jupiter) which broadened scooter appeal across demographics. Meanwhile, Mopeds flatlined entirely after 2011 — a category that simply stopped growing.

{:else if inputs.selected_view === "Commercial vs Personal"}

### Commercial vs Personal Vehicle Balance

A simplified split: "Personal" includes cars, two-wheelers, jeeps, and station wagons. "Commercial" groups everything else — passenger transport (autos, taxis, buses), goods transport (trucks, delivery vans, tankers), agricultural (tractors, trailers), and service vehicles (ambulances). This binary view shows the broad balance but masks very different economic activities within "commercial."

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
WHERE display_year >= '${inputs.ratio_year_filter.value || '2000'}'
```

{#if inputs.ratio_display.value === "Percentage"}
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
{:else if inputs.ratio_display.value === "Split"}
<AreaChart
     data={filtered_ratio}
     x=display_year
     y={['personal', 'commercial']}
     type=stacked100
     title="Personal vs Commercial Vehicle Split"
     subtitle="Distribution of vehicle registrations by usage type"
     xAxisTitle="Year"
     yAxisTitle="Share (%)"
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

**Key Insights:** The commercial share stays relatively stable at ~10-12%, suggesting personal vehicle growth (especially motorcycles and cars) is the dominant driver of fleet expansion. To understand what's happening within the commercial segment, use the Growth Rates or Emerging Categories views to compare specific vehicle types.

{:else}

### Stagnating & Displaced Categories

Vehicle types that plateaued or were displaced by regulatory or market shifts.

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
WHERE display_year >= '${inputs.decline_year_filter.value || '2000'}'
```

{#if inputs.decline_chart_type === "Line Chart"}
<LineChart
     data={filtered_decline}
     x=display_year
     y=Count
     series=subcategory
     title="Stagnating & Displaced Categories"
     subtitle="Vehicle types that plateaued or were displaced by regulatory/market shifts"
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
     title="Stagnating & Displaced Categories"
     subtitle="Vehicle types that plateaued or were displaced by regulatory/market shifts"
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
- **Mopeds:** Plateau at ~37,600 from 2011 onward — no new registrations, suggesting the category was fully superseded by motorcycles and gearless scooters
- **Metered Taxis:** Drops to zero in 2007-08 — not a market decline but an RTO reclassification to "Luxury Tourist Cabs" (see Emerging Categories view)
- **Station Wagons:** Negligible numbers throughout (60-78 vehicles) — essentially a legacy category on the books, not a meaningful market segment

{/if}

## See Also

- **[Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018)** — Raw registration counts by category and year
- **[Pune vs PCMC Vehicles](/PCMC/Pune_PCMC_Comparison)** — How PCMC's fleet size and composition compare to Pune city
- **[Road Safety](/PCMC/Road_Accident_Statistics)** — Accident trends as the fleet grew 2000-2007
- **[PCMC Overview](/PCMC)** — City context and data coverage

---

*Data: cumulative vehicle registrations with the Pimpri-Chinchwad RTO, 2000-2001 to 2017-2018. Source: Maharashtra state RTO registration data, as compiled in the CMP baseline.*

## Sources
- [Open City Urban Data Portal](https://data.opencity.in/dataset/maharashtra-vehicles-registration-data/resource/maharashtra-vehicles-registration-data---2001-2018)

## Data Queries
