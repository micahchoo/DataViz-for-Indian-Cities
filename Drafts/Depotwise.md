---
title: PMPML Depot Operations Dashboard
---

# PMPML Operations Overview

<DateRange 
    name=date_range 
    title="Select Date Range"
/>

<Dropdown 
    name=depot_filter 
    title="Filter by Depot" 
    data={depot_list} 
    value=depot
    defaultValue="All Depots"
/>

```sql depot_list
SELECT depot, value
FROM (
    SELECT DISTINCT 
        depot,
        depot as value
    FROM depot_operations
    WHERE depot IS NOT NULL

    UNION ALL

    SELECT 
        'All Depots' as depot,
        'All Depots' as value
) AS combined
ORDER BY depot
```

```sql base_data
SELECT 
    date,
    depot,
    vehicles_held_pmpml,
    vehicles_on_road,
    vehicles_off_road,
    vehicles_in_workshop,
    total_effective_km,
    ticket_revenue,
    total_traffic_revenue,
    daily_passengers,
    fleet_utilization_pct,
    revenue_per_vehicle,
    revenue_per_km,
    km_per_bus,
    passengers_per_bus,
    breakdowns,
    accidents_pmpml,
    accidents_hired,
    diesel_efficiency_kmpl,
    cancelled_kms
FROM depot_operations
WHERE date IS NOT NULL
  AND depot IS NOT NULL
  ${inputs.date_range.start ? "AND date >= '" + inputs.date_range.start + "'" : ''}
  ${inputs.date_range.end   ? "AND date <= '" + inputs.date_range.end   + "'" : ''}
  ${inputs.depot_filter && inputs.depot_filter !== 'All Depots'
       ? "AND depot = '" + inputs.depot_filter + "'" : ''}
```

```sql data_quality_check
SELECT 
    COUNT(*) as total_records,
    COUNT(CASE WHEN vehicles_on_road IS NULL THEN 1 END) as missing_vehicles,
    COUNT(CASE WHEN daily_passengers IS NULL THEN 1 END) as missing_passengers,
    COUNT(CASE WHEN ticket_revenue IS NULL THEN 1 END) as missing_revenue,
    COUNT(CASE WHEN fleet_utilization_pct > 100 THEN 1 END) as invalid_utilization,
    COUNT(CASE WHEN revenue_per_vehicle < 0 THEN 1 END) as negative_revenue
FROM ${base_data}
```

```sql data_quality_issues
SELECT 
    (${data_quality_check[0].missing_vehicles} +
     ${data_quality_check[0].missing_passengers} +
     ${data_quality_check[0].missing_revenue} +
     ${data_quality_check[0].invalid_utilization} +
     ${data_quality_check[0].negative_revenue}) as total_issues
```

{#if data_quality_issues[0].total_issues > 0}
<Alert status="warning">
**Data Quality Alert:** Found {data_quality_issues[0].total_issues} data quality issues. 
Missing vehicles: {data_quality_check[0].missing_vehicles}, 
Missing passengers: {data_quality_check[0].missing_passengers}, 
Invalid utilization: {data_quality_check[0].invalid_utilization}
</Alert>
{/if}

```sql latest_period
SELECT 
    MAX(date) as latest_date,
    DATE_TRUNC('month', MAX(date)) as latest_month
FROM ${base_data}
```

```sql current_month_kpis
SELECT 
    SUM(vehicles_on_road) as total_vehicles,
    SUM(daily_passengers) as total_passengers,
    SUM(ticket_revenue) as total_revenue,
    ROUND(AVG(fleet_utilization_pct), 1) as avg_utilization,
    SUM(breakdowns) as total_breakdowns,
    SUM(accidents_pmpml + COALESCE(accidents_hired, 0)) as total_accidents
FROM ${base_data}
WHERE DATE_TRUNC('month', date) = (SELECT latest_month FROM ${latest_period})
```

```sql prev_month_kpis
SELECT 
    SUM(vehicles_on_road) as total_vehicles,
    SUM(daily_passengers) as total_passengers,
    SUM(ticket_revenue) as total_revenue,
    ROUND(AVG(fleet_utilization_pct), 1) as avg_utilization,
    SUM(breakdowns) as total_breakdowns,
    SUM(accidents_pmpml + COALESCE(accidents_hired, 0)) as total_accidents
FROM ${base_data}
WHERE DATE_TRUNC('month', date) = (
    SELECT DATE_TRUNC('month', MAX(date)) - INTERVAL '1 month'
    FROM ${base_data}
)
```

```sql kpi_comparison
SELECT 
    c.total_vehicles,
    c.total_passengers,
    c.total_revenue,
    c.avg_utilization,
    c.total_breakdowns,
    c.total_accidents,
    p.total_vehicles as prev_vehicles,
    p.total_passengers as prev_passengers,
    p.total_revenue as prev_revenue,
    p.avg_utilization as prev_utilization,
    CASE 
        WHEN p.total_vehicles > 0 
        THEN ROUND(((c.total_vehicles - p.total_vehicles) / p.total_vehicles::FLOAT) * 100, 1)
        ELSE 0 
    END as vehicles_change_pct,
    CASE 
        WHEN p.total_passengers > 0 
        THEN ROUND(((c.total_passengers - p.total_passengers) / p.total_passengers::FLOAT) * 100, 1)
        ELSE 0 
    END as passengers_change_pct,
    CASE 
        WHEN p.total_revenue > 0 
        THEN ROUND(((c.total_revenue - p.total_revenue) / p.total_revenue::FLOAT) * 100, 1)
        ELSE 0 
    END as revenue_change_pct,
    (c.avg_utilization - p.avg_utilization) as utilization_change_pp
FROM ${current_month_kpis} c
CROSS JOIN ${prev_month_kpis} p
```

## Executive Summary

**Period:** {latest_period[0].latest_month}

<Grid cols=4 colsPhone=1 colsTablet=2>
    <BigValue 
        data={kpi_comparison} 
        value=total_vehicles
        comparison=prev_vehicles
        comparisonTitle="vs Last Month"
        title="Vehicles On Road"
        fmt="#,##0"
    />
    <BigValue 
        data={kpi_comparison} 
        value=total_passengers
        comparison=prev_passengers
        comparisonTitle="vs Last Month"
        title="Daily Passengers"
        fmt="#,##0"
    />
    <BigValue 
        data={kpi_comparison} 
        value=total_revenue
        comparison=prev_revenue
        comparisonTitle="vs Last Month"
        title="Ticket Revenue"
        fmt="₹#,##0,,'M'"
    />
    <BigValue 
        data={kpi_comparison} 
        value=avg_utilization
        comparison=prev_utilization
        comparisonTitle="vs Last Month"
        title="Fleet Utilization"
        fmt="#0.0'%'"
    />
</Grid>

```sql anomaly_breakdowns
SELECT 
    depot,
    SUM(breakdowns) as breakdown_count,
    (SELECT AVG(monthly_breakdowns) 
     FROM (
         SELECT SUM(breakdowns) as monthly_breakdowns 
         FROM ${base_data} 
         WHERE DATE_TRUNC('month', date) < (SELECT latest_month FROM ${latest_period})
         GROUP BY depot, DATE_TRUNC('month', date)
     ) sub
    ) as avg_historical_breakdowns
FROM ${base_data}
WHERE DATE_TRUNC('month', date) = (SELECT latest_month FROM ${latest_period})
GROUP BY depot
HAVING SUM(breakdowns) > (
    SELECT AVG(monthly_breakdowns) * 1.5
    FROM (
        SELECT SUM(breakdowns) as monthly_breakdowns 
        FROM ${base_data} 
        WHERE DATE_TRUNC('month', date) < (SELECT latest_month FROM ${latest_period})
        GROUP BY depot, DATE_TRUNC('month', date)
    ) sub
)
ORDER BY breakdown_count DESC
```

{#if anomaly_breakdowns.length > 0}
<Alert status="error">
**⚠️ High Breakdown Alert:** {anomaly_breakdowns[0].depot} has {anomaly_breakdowns[0].breakdown_count} breakdowns this month, 
significantly above the historical average of {Math.round(anomaly_breakdowns[0].avg_historical_breakdowns)}.
</Alert>
{/if}

```sql anomaly_utilization
SELECT 
    depot,
    ROUND(AVG(fleet_utilization_pct), 1) as current_utilization,
    (SELECT ROUND(AVG(fleet_utilization_pct), 1)
     FROM ${base_data} 
     WHERE DATE_TRUNC('month', date) < (SELECT latest_month FROM ${latest_period})
    ) as avg_historical_utilization
FROM ${base_data}
WHERE DATE_TRUNC('month', date) = (SELECT latest_month FROM ${latest_period})
GROUP BY depot
HAVING AVG(fleet_utilization_pct) < 60
ORDER BY current_utilization ASC
```

{#if anomaly_utilization.length > 0}
<Alert status="warning">
**📉 Low Utilization Alert:** {anomaly_utilization[0].depot} has only {anomaly_utilization[0].current_utilization}% fleet utilization this month.
System average: {anomaly_utilization[0].avg_historical_utilization}%
</Alert>
{/if}

---

## 📊 Performance Trends

```sql monthly_trends
SELECT 
    DATE_TRUNC('month', date) as period,
    SUM(vehicles_on_road) as total_on_road,
    SUM(daily_passengers) as total_passengers,
    SUM(ticket_revenue) as total_revenue,
    SUM(total_traffic_revenue) as all_traffic_revenue,
    ROUND(AVG(fleet_utilization_pct), 1) as avg_utilization,
    SUM(total_effective_km) / 1000000.0 as total_km_millions,
    ROUND(AVG(revenue_per_vehicle), 0) as avg_revenue_per_vehicle,
    SUM(breakdowns) as total_breakdowns,
    SUM(accidents_pmpml + COALESCE(accidents_hired, 0)) as total_accidents
FROM ${base_data}
GROUP BY period
ORDER BY period DESC
LIMIT 12
```

<Tabs>
    <Tab label="Operations">
        <LineChart 
            data={monthly_trends}
            x=period
            y=total_on_road
            xFmt="mmm yyyy"
            yAxisTitle="Vehicles"
            title="Vehicles On Road - Monthly Trend"
            chartAreaHeight=300
        />
        
        <LineChart 
            data={monthly_trends}
            x=period
            y=total_passengers
            xFmt="mmm yyyy"
            yAxisTitle="Passengers"
            yFmt="#,##0"
            title="Daily Passenger Volume - Monthly Trend"
            chartAreaHeight=300
        />
    </Tab>
    
    <Tab label="Revenue">
        <LineChart 
            data={monthly_trends}
            x=period
            y={['total_revenue', 'all_traffic_revenue']}
            xFmt="mmm yyyy"
            yAxisTitle="Revenue (₹)"
            yFmt="₹#,##0,,'M'"
            title="Revenue Comparison: Tickets vs All Traffic"
            chartAreaHeight=300
            labels={['Ticket Revenue', 'Total Traffic Revenue']}
        />
        
        <LineChart 
            data={monthly_trends}
            x=period
            y=avg_revenue_per_vehicle
            xFmt="mmm yyyy"
            yAxisTitle="Revenue per Vehicle (₹)"
            yFmt="₹#,##0"
            title="Average Revenue per Vehicle - Monthly Trend"
            chartAreaHeight=300
        />
    </Tab>
    
    <Tab label="Efficiency">
        <LineChart 
            data={monthly_trends}
            x=period
            y=avg_utilization
            xFmt="mmm yyyy"
            yAxisTitle="Utilization %"
            title="Fleet Utilization Rate - Monthly Trend"
            chartAreaHeight=300
        />
        
        <LineChart 
            data={monthly_trends}
            x=period
            y=total_km_millions
            xFmt="mmm yyyy"
            yAxisTitle="Million KM"
            title="Total Effective Kilometers - Monthly Trend"
            chartAreaHeight=300
        />
    </Tab>
    
    <Tab label="Safety">
        <LineChart 
            data={monthly_trends}
            x=period
            y=total_breakdowns
            xFmt="mmm yyyy"
            yAxisTitle="Breakdowns"
            title="Monthly Breakdowns"
            chartAreaHeight=300
        />
        
        <LineChart 
            data={monthly_trends}
            x=period
            y=total_accidents
            xFmt="mmm yyyy"
            yAxisTitle="Accidents"
            title="Total Accidents (PMPML + Hired)"
            chartAreaHeight=300
        />
    </Tab>
</Tabs>

---

## 🚌 Depot Performance Comparison

```sql depot_performance
SELECT 
    depot,
    COUNT(DISTINCT DATE_TRUNC('month', date)) as months_active,
    ROUND(AVG(vehicles_on_road), 0) as avg_vehicles_on_road,
    ROUND(AVG(daily_passengers), 0) as avg_daily_passengers,
    ROUND(AVG(ticket_revenue), 0) as avg_daily_revenue,
    ROUND(AVG(revenue_per_vehicle), 0) as avg_revenue_per_vehicle,
    ROUND(AVG(fleet_utilization_pct), 1) as avg_fleet_utilization,
    ROUND(AVG(passengers_per_bus), 0) as avg_passengers_per_bus,
    ROUND(AVG(km_per_bus), 0) as avg_km_per_bus,
    SUM(breakdowns) as total_breakdowns,
    SUM(accidents_pmpml + COALESCE(accidents_hired, 0)) as total_accidents,
    ROUND(SUM(breakdowns) / NULLIF(SUM(total_effective_km / 10000), 0), 2) as breakdown_rate_per_10k_km,
    ROUND(AVG(diesel_efficiency_kmpl), 2) as avg_diesel_kmpl
FROM ${base_data}
GROUP BY depot
ORDER BY avg_daily_revenue DESC
```

### Revenue Performance

<BarChart
    data={depot_performance}
    x=depot
    y=avg_daily_revenue
    swapXY=true
    title="Average Daily Revenue by Depot"
    yAxisTitle="Revenue (₹)"
    yFmt="₹#,##0"
    chartAreaHeight=400
/>

### Operational Metrics

<Grid cols=2 colsPhone=1>
    <BarChart
        data={depot_performance}
        x=depot
        y=avg_daily_passengers
        swapXY=true
        title="Average Daily Passengers"
        yFmt="#,##0"
        chartAreaHeight=350
    />
    
    <BarChart
        data={depot_performance}
        x=depot
        y=avg_fleet_utilization
        swapXY=true
        title="Fleet Utilization %"
        chartAreaHeight=350
    />
</Grid>

### Detailed Depot Comparison

<DataTable data={depot_performance} rows=all search=true>
    <Column id=depot title="Depot" />
    <Column id=avg_vehicles_on_road title="Avg Vehicles" fmt="#,##0" align=right />
    <Column id=avg_daily_passengers title="Avg Passengers" fmt="#,##0" align=right />
    <Column id=avg_daily_revenue title="Daily Revenue" fmt="₹#,##0" align=right />
    <Column id=avg_revenue_per_vehicle title="Rev/Vehicle" fmt="₹#,##0" align=right />
    <Column id=avg_fleet_utilization title="Utilization" fmt="#0.0'%'" align=right />
    <Column id=avg_passengers_per_bus title="Pass/Bus" fmt="#,##0" align=right />
    <Column id=avg_km_per_bus title="KM/Bus" fmt="#,##0" align=right />
    <Column id=total_breakdowns title="Breakdowns" fmt="#,##0" align=right />
    <Column id=breakdown_rate_per_10k_km title="Breakdown Rate" fmt="#0.00" align=right />
    <Column id=total_accidents title="Accidents" fmt="#,##0" align=right />
    <Column id=avg_diesel_kmpl title="Diesel KMPL" fmt="#0.00" align=right />
</DataTable>

---

## 📈 Depot-wise Historical Trends

```sql depot_monthly_trends
SELECT 
    DATE_TRUNC('month', date) as period,
    depot,
    ROUND(AVG(vehicles_on_road), 0) as vehicles_on_road,
    ROUND(AVG(daily_passengers), 0) as daily_passengers,
    SUM(ticket_revenue) as monthly_revenue,
    ROUND(AVG(fleet_utilization_pct), 1) as fleet_utilization,
    ROUND(AVG(revenue_per_vehicle), 0) as revenue_per_vehicle,
    SUM(breakdowns) as breakdowns,
    SUM(accidents_pmpml + COALESCE(accidents_hired, 0)) as accidents
FROM ${base_data}
GROUP BY period, depot
ORDER BY period DESC, depot
```

<Tabs>
    <Tab label="Revenue">
        <LineChart
            data={depot_monthly_trends}
            x=period
            y=monthly_revenue
            series=depot
            xFmt="mmm yyyy"
            yAxisTitle="Revenue (₹)"
            yFmt="₹#,##0,,'M'"
            title="Monthly Revenue by Depot"
            chartAreaHeight=350
        />
    </Tab>
    
    <Tab label="Passengers">
        <LineChart
            data={depot_monthly_trends}
            x=period
            y=daily_passengers
            series=depot
            xFmt="mmm yyyy"
            yAxisTitle="Passengers"
            yFmt="#,##0"
            title="Daily Passengers by Depot"
            chartAreaHeight=350
        />
    </Tab>
    
    <Tab label="Utilization">
        <LineChart
            data={depot_monthly_trends}
            x=period
            y=fleet_utilization
            series=depot
            xFmt="mmm yyyy"
            yAxisTitle="Utilization %"
            title="Fleet Utilization by Depot"
            chartAreaHeight=350
        />
    </Tab>
    
    <Tab label="Safety">
        <LineChart
            data={depot_monthly_trends}
            x=period
            y=breakdowns
            series=depot
            xFmt="mmm yyyy"
            yAxisTitle="Breakdowns"
            title="Monthly Breakdowns by Depot"
            chartAreaHeight=350
        />
    </Tab>
</Tabs>

---

## 🔍 Detailed Records

<Details title="View All Records">

```sql detailed_records
SELECT 
    date,
    depot,
    vehicles_on_road,
    daily_passengers,
    ticket_revenue,
    revenue_per_vehicle,
    fleet_utilization_pct,
    km_per_bus,
    passengers_per_bus,
    breakdowns,
    accidents_pmpml,
    accidents_hired,
    diesel_efficiency_kmpl
FROM ${base_data}
ORDER BY date DESC, depot
```

<DataTable data={detailed_records} rows=50 search=true downloadable=true>
    <Column id=date fmt="yyyy-mm-dd" />
    <Column id=depot />
    <Column id=vehicles_on_road title="On Road" fmt="#,##0" align=right />
    <Column id=daily_passengers title="Passengers" fmt="#,##0" align=right />
    <Column id=ticket_revenue title="Revenue" fmt="₹#,##0" align=right />
    <Column id=revenue_per_vehicle title="Rev/Veh" fmt="₹#,##0" align=right />
    <Column id=fleet_utilization_pct title="Util %" fmt="#0.0'%'" align=right />
    <Column id=km_per_bus title="KM/Bus" fmt="#,##0" align=right />
    <Column id=passengers_per_bus title="Pass/Bus" fmt="#,##0" align=right />
    <Column id=breakdowns fmt="#,##0" align=right />
    <Column id=accidents_pmpml title="Acc (Own)" fmt="#,##0" align=right />
    <Column id=accidents_hired title="Acc (Hired)" fmt="#,##0" align=right />
    <Column id=diesel_efficiency_kmpl title="KMPL" fmt="#0.00" align=right />
</DataTable>

</Details>

---

**Last Updated:** {latest_period[0].latest_date}

**Data Quality:** {data_quality_check[0].total_records - data_quality_issues[0].total_issues} of {data_quality_check[0].total_records} records validated