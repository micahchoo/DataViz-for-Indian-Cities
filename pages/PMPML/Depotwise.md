---
title: PMPML Depot Operations - Historical Dashboard
---

# PMPML Operations Overview

```sql latest_date
WITH data_prep AS (
    SELECT 
        TRY_CAST(Date AS DATE) as date,
        CASE 
            WHEN Particulars IN ('Upper\nDepot', 'Upper Depot') THEN 'Upper Depot'
            WHEN Particulars IN ('Pune\nStation', 'Pune Station') THEN 'Pune Station'
            WHEN Particulars IN ('Bhekraina\ngar', 'Bhekrai-\nnagar', 'Bhekrai\nnagar') THEN 'Bhekrainagar'
            WHEN Particulars IN ('Shewalwa\ndi', 'Shewale-\nwadi', 'Shewal\nwadi') THEN 'Shewalwadi'
            ELSE Particulars 
        END as depot
    FROM extracted
    WHERE Date IS NOT NULL AND Particulars IS NOT NULL
)
SELECT MAX(date) as latest_date FROM data_prep
```

```sql depot_list
WITH data_prep AS (
    SELECT 
        CASE 
            WHEN Particulars IN ('Upper\nDepot', 'Upper Depot') THEN 'Upper Depot'
            WHEN Particulars IN ('Pune\nStation', 'Pune Station') THEN 'Pune Station'
            WHEN Particulars IN ('Bhekraina\ngar', 'Bhekrai-\nnagar', 'Bhekrai\nnagar') THEN 'Bhekrainagar'
            WHEN Particulars IN ('Shewalwa\ndi', 'Shewale-\nwadi', 'Shewal\nwadi') THEN 'Shewalwadi'
            ELSE Particulars 
        END as depot
    FROM extracted
    WHERE Particulars IS NOT NULL
)
SELECT DISTINCT depot FROM data_prep ORDER BY depot
```

## 📊 System-Wide Performance

```sql system_totals
WITH data_prep AS (
    SELECT 
        TRY_CAST(Date AS DATE) as date,
        CASE 
            WHEN Particulars IN ('Upper\nDepot', 'Upper Depot') THEN 'Upper Depot'
            WHEN Particulars IN ('Pune\nStation', 'Pune Station') THEN 'Pune Station'
            WHEN Particulars IN ('Bhekraina\ngar', 'Bhekrai-\nnagar', 'Bhekrai\nnagar') THEN 'Bhekrainagar'
            WHEN Particulars IN ('Shewalwa\ndi', 'Shewale-\nwadi', 'Shewal\nwadi') THEN 'Shewalwadi'
            ELSE Particulars 
        END as depot,
        TRY_CAST("Avg. Vehicles Held - Per Day PMPML" AS INTEGER) as vehicles_held_pmpml,
        TRY_CAST("Total Avg.Veh- On Road Per Day" AS INTEGER) as vehicles_on_road,
        TRY_CAST("Total Vehicles Off Road Per Day" AS INTEGER) as vehicles_off_road,
        TRY_CAST("Total Eff.Km (Own+Hire)" AS BIGINT) as total_effective_km,
        TRY_CAST("Passenger Earning (Sale of Ticket)(₹)" AS BIGINT) as ticket_revenue,
        TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS INTEGER) as daily_passengers,
        TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE) as fleet_utilization_pct,
        TRY_CAST("Total no.of Breakdown (PMPML Own)" AS INTEGER) as breakdowns,
        TRY_CAST("No.of Accidents (PMPML) Total" AS INTEGER) as accidents_pmpml
    FROM extracted
    WHERE Date IS NOT NULL AND Particulars IS NOT NULL
)
SELECT 
    date,
    MONTHNAME(date) || ' ' || YEAR(date) as period,
    SUM(vehicles_held_pmpml) as total_fleet,
    SUM(vehicles_on_road) as total_on_road,
    SUM(vehicles_off_road) as total_off_road,
    SUM(total_effective_km) as total_km,
    SUM(ticket_revenue) as total_ticket_revenue,
    SUM(daily_passengers) as total_passengers,
    ROUND(AVG(fleet_utilization_pct), 2) as avg_utilization,
    SUM(breakdowns) as total_breakdowns,
    SUM(accidents_pmpml) as total_accidents
FROM data_prep
GROUP BY date, period
ORDER BY date DESC
```

### Current Month Snapshot

<BigValue 
    data={system_totals} 
    value=total_on_road
    title="Vehicles On Road"
    fmt="#,##0"
/>

<BigValue 
    data={system_totals} 
    value=total_passengers
    title="Daily Passengers"
    fmt="#,##0"
/>

<BigValue 
    data={system_totals} 
    value=total_ticket_revenue
    title="Ticket Revenue"
    fmt="₹#,##0"
/>

<BigValue 
    data={system_totals} 
    value=avg_utilization
    title="Fleet Utilization"
    fmt="#,##0.0'%'"
/>

### Historical Trends

<LineChart 
    data={system_totals}
    x=period
    y=total_on_road
    yAxisTitle="Number of Vehicles"
    title="Vehicles On Road - Trend"
/>

<LineChart 
    data={system_totals}
    x=period
    y=total_passengers
    yAxisTitle="Daily Passengers"
    title="Daily Passenger Volume"
    yFmt="#,##0"
/>

<LineChart 
    data={system_totals}
    x=period
    y=total_ticket_revenue
    yAxisTitle="Revenue (₹)"
    title="Ticket Revenue Trend"
    yFmt="₹#,##0"
/>

## 🚌 Fleet Operations

```sql fleet_trends
WITH data_prep AS (
    SELECT 
        TRY_CAST(Date AS DATE) as date,
        TRY_CAST("Total Vehicles Per Day" AS INTEGER) as total_vehicles,
        TRY_CAST("Total Avg.Veh- On Road Per Day" AS INTEGER) as vehicles_on_road,
        TRY_CAST("Total Vehicles Off Road Per Day" AS INTEGER) as vehicles_off_road,
        TRY_CAST("Avg.Workshop Vehicles Per Day" AS INTEGER) as vehicles_in_workshop,
        TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE) as fleet_utilization_pct
    FROM extracted
    WHERE Date IS NOT NULL AND Particulars IS NOT NULL
)
SELECT 
    date,
    MONTHNAME(date) || ' ' || YEAR(date) as period,
    SUM(total_vehicles) as total_fleet,
    SUM(vehicles_on_road) as on_road,
    SUM(vehicles_off_road) as off_road,
    SUM(vehicles_in_workshop) as in_workshop,
    ROUND(AVG(fleet_utilization_pct), 2) as utilization_pct
FROM data_prep
GROUP BY date, period
ORDER BY date
```

<AreaChart
    data={fleet_trends}
    x=period
    y={['on_road', 'off_road', 'in_workshop']}
    type=stacked
    title="Fleet Distribution Over Time"
    yAxisTitle="Number of Vehicles"
/>

<LineChart
    data={fleet_trends}
    x=period
    y=utilization_pct
    title="Fleet Utilization Rate (%)"
    yAxisTitle="Utilization %"
/>

## 📍 Depot Comparison

```sql depot_performance
WITH data_prep AS (
    SELECT 
        TRY_CAST(Date AS DATE) as date,
        CASE 
            WHEN Particulars IN ('Upper\nDepot', 'Upper Depot') THEN 'Upper Depot'
            WHEN Particulars IN ('Pune\nStation', 'Pune Station') THEN 'Pune Station'
            WHEN Particulars IN ('Bhekraina\ngar', 'Bhekrai-\nnagar', 'Bhekrai\nnagar') THEN 'Bhekrainagar'
            WHEN Particulars IN ('Shewalwa\ndi', 'Shewale-\nwadi', 'Shewal\nwadi') THEN 'Shewalwadi'
            ELSE Particulars 
        END as depot,
        TRY_CAST("Total Avg.Veh- On Road Per Day" AS INTEGER) as vehicles_on_road,
        TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS INTEGER) as daily_passengers,
        TRY_CAST("Average daily earning in Rs." AS INTEGER) as daily_revenue,
        TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE) as revenue_per_vehicle,
        TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE) as fleet_utilization_pct,
        TRY_CAST("Passenger Per Bus Per day" AS INTEGER) as passengers_per_bus,
        TRY_CAST("Total no.of Breakdown (PMPML Own)" AS INTEGER) as breakdowns,
        TRY_CAST("No.of Accidents (PMPML) Total" AS INTEGER) as accidents_pmpml,
        TRY_CAST("No.of Accidents (HIRED) Total" AS INTEGER) as accidents_hired
    FROM extracted
    WHERE Date IS NOT NULL AND Particulars IS NOT NULL
)
SELECT 
    depot,
    COUNT(DISTINCT date) as months_active,
    ROUND(AVG(vehicles_on_road), 0) as avg_vehicles_on_road,
    ROUND(AVG(daily_passengers), 0) as avg_daily_passengers,
    ROUND(AVG(daily_revenue), 0) as avg_daily_revenue,
    ROUND(AVG(revenue_per_vehicle), 2) as avg_revenue_per_vehicle,
    ROUND(AVG(fleet_utilization_pct), 2) as avg_fleet_utilization,
    ROUND(AVG(passengers_per_bus), 0) as avg_passengers_per_bus,
    SUM(breakdowns) as total_breakdowns,
    SUM(accidents_pmpml + COALESCE(accidents_hired, 0)) as total_accidents
FROM data_prep
GROUP BY depot
ORDER BY avg_daily_revenue DESC
```

### Top Performing Depots

<BarChart
    data={depot_performance}
    x=depot
    y=avg_daily_revenue
    swapXY=true
    title="Average Daily Revenue by Depot"
    yAxisTitle="Revenue (₹)"
    yFmt="₹#,##0"
/>

<BarChart
    data={depot_performance}
    x=depot
    y=avg_daily_passengers
    swapXY=true
    title="Average Daily Passengers by Depot"
    yAxisTitle="Passengers"
    yFmt="#,##0"
/>

<BarChart
    data={depot_performance}
    x=depot
    y=avg_fleet_utilization
    swapXY=true
    title="Fleet Utilization by Depot"
    yAxisTitle="Utilization %"
/>

### Depot Performance Table

<DataTable data={depot_performance} rows=15>
    <Column id=depot/>
    <Column id=avg_vehicles_on_road title="Avg Vehicles" fmt="#,##0"/>
    <Column id=avg_daily_passengers title="Avg Daily Passengers" fmt="#,##0"/>
    <Column id=avg_daily_revenue title="Avg Daily Revenue" fmt="₹#,##0"/>
    <Column id=avg_revenue_per_vehicle title="Revenue/Vehicle" fmt="₹#,##0"/>
    <Column id=avg_fleet_utilization title="Utilization %" fmt="#0.0'%'"/>
    <Column id=total_breakdowns title="Breakdowns" fmt="#,##0"/>
    <Column id=total_accidents title="Accidents" fmt="#,##0"/>
</DataTable>

## 📈 Revenue Analysis

```sql revenue_trends
WITH data_prep AS (
    SELECT 
        TRY_CAST(Date AS DATE) as date,
        TRY_CAST("Passenger Earning (Sale of Ticket)(₹)" AS BIGINT) as ticket_revenue,
        TRY_CAST("All Traffic Earning (₹)" AS BIGINT) as total_traffic_revenue,
        TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE) as revenue_per_vehicle,
        TRY_CAST("Earning per KMs in Rs.(EPK) (₹)" AS DOUBLE) as revenue_per_km,
        TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS INTEGER) as daily_passengers
    FROM extracted
    WHERE Date IS NOT NULL AND Particulars IS NOT NULL
)
SELECT 
    date,
    MONTHNAME(date) || ' ' || YEAR(date) as period,
    SUM(ticket_revenue) as ticket_revenue,
    SUM(total_traffic_revenue) as total_revenue,
    ROUND(AVG(revenue_per_vehicle), 2) as avg_revenue_per_vehicle,
    ROUND(AVG(revenue_per_km), 2) as avg_revenue_per_km,
    SUM(daily_passengers) as total_passengers
FROM data_prep
GROUP BY date, period
ORDER BY date
```

<LineChart
    data={revenue_trends}
    x=period
    y={['ticket_revenue', 'total_revenue']}
    title="Revenue Comparison: Tickets vs Total Traffic"
    yAxisTitle="Revenue (₹)"
    yFmt="₹#,##0,,'M'"
/>

<LineChart
    data={revenue_trends}
    x=period
    y=avg_revenue_per_vehicle
    title="Average Revenue per Vehicle"
    yAxisTitle="Revenue (₹)"
    yFmt="₹#,##0"
/>

## 🛣️ Operational Efficiency

```sql efficiency_trends
WITH data_prep AS (
    SELECT 
        TRY_CAST(Date AS DATE) as date,
        TRY_CAST("Total Eff.Km (Own+Hire)" AS BIGINT) as total_effective_km,
        TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE) as km_per_bus,
        TRY_CAST("Total Cancelled KMs" AS INTEGER) as cancelled_kms,
        TRY_CAST("KMs per Litre of Diesel (KMPL)(Own)" AS DOUBLE) as diesel_efficiency
    FROM extracted
    WHERE Date IS NOT NULL AND Particulars IS NOT NULL
)
SELECT 
    date,
    MONTHNAME(date) || ' ' || YEAR(date) as period,
    SUM(total_effective_km) / 1000000.0 as total_km_millions,
    ROUND(AVG(km_per_bus), 2) as avg_km_per_bus,
    SUM(cancelled_kms) / 1000000.0 as cancelled_km_millions,
    ROUND(AVG(diesel_efficiency), 2) as avg_diesel_kmpl
FROM data_prep
GROUP BY date, period
ORDER BY date
```

<LineChart
    data={efficiency_trends}
    x=period
    y=total_km_millions
    title="Total Effective Kilometers (Millions)"
    yAxisTitle="Million KMs"
/>

<LineChart
    data={efficiency_trends}
    x=period
    y=avg_km_per_bus
    title="Average KM per Bus per Day"
    yAxisTitle="KM per Bus"
/>

<LineChart
    data={efficiency_trends}
    x=period
    y=avg_diesel_kmpl
    title="Diesel Fuel Efficiency (KMPL)"
    yAxisTitle="KM per Litre"
/>

## 🔧 Maintenance & Safety

```sql maintenance_trends
WITH data_prep AS (
    SELECT 
        TRY_CAST(Date AS DATE) as date,
        TRY_CAST("Avg.Workshop Vehicles Per Day" AS INTEGER) as vehicles_in_workshop,
        TRY_CAST("% of Workshop Vehicles" AS DOUBLE) as workshop_pct,
        TRY_CAST("Total no.of Breakdown (PMPML Own)" AS INTEGER) as breakdowns,
        TRY_CAST("No.of Accidents (PMPML) Total" AS INTEGER) as accidents_pmpml,
        TRY_CAST("No.of Accidents (HIRED) Total" AS INTEGER) as accidents_hired
    FROM extracted
    WHERE Date IS NOT NULL AND Particulars IS NOT NULL
)
SELECT 
    date,
    MONTHNAME(date) || ' ' || YEAR(date) as period,
    SUM(vehicles_in_workshop) as vehicles_in_workshop,
    ROUND(AVG(workshop_pct), 2) as workshop_pct,
    SUM(breakdowns) as total_breakdowns,
    SUM(accidents_pmpml) as pmpml_accidents,
    SUM(COALESCE(accidents_hired, 0)) as hired_accidents
FROM data_prep
GROUP BY date, period
ORDER BY date
```

<LineChart
    data={maintenance_trends}
    x=period
    y=vehicles_in_workshop
    title="Vehicles in Workshop"
    yAxisTitle="Number of Vehicles"
/>

<LineChart
    data={maintenance_trends}
    x=period
    y=total_breakdowns
    title="Monthly Breakdowns"
    yAxisTitle="Number of Breakdowns"
/>

<AreaChart
    data={maintenance_trends}
    x=period
    y={['pmpml_accidents', 'hired_accidents']}
    type=stacked
    title="Accidents: PMPML vs Hired Vehicles"
    yAxisTitle="Number of Accidents"
/>

## 🔍 Depot Deep Dive

```sql depot_monthly
WITH data_prep AS (
    SELECT 
        TRY_CAST(Date AS DATE) as date,
        CASE 
            WHEN Particulars IN ('Upper\nDepot', 'Upper Depot') THEN 'Upper Depot'
            WHEN Particulars IN ('Pune\nStation', 'Pune Station') THEN 'Pune Station'
            WHEN Particulars IN ('Bhekraina\ngar', 'Bhekrai-\nnagar', 'Bhekrai\nnagar') THEN 'Bhekrainagar'
            WHEN Particulars IN ('Shewalwa\ndi', 'Shewale-\nwadi', 'Shewal\nwadi') THEN 'Shewalwadi'
            ELSE Particulars 
        END as depot,
        TRY_CAST("Total Avg.Veh- On Road Per Day" AS INTEGER) as vehicles_on_road,
        TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS INTEGER) as daily_passengers,
        TRY_CAST("Average daily earning in Rs." AS INTEGER) as daily_revenue,
        TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE) as fleet_utilization_pct,
        TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE) as km_per_bus,
        TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE) as revenue_per_vehicle,
        TRY_CAST("Passenger Per Bus Per day" AS INTEGER) as passengers_per_bus
    FROM extracted
    WHERE Date IS NOT NULL AND Particulars IS NOT NULL
)
SELECT 
    date,
    MONTHNAME(date) || ' ' || YEAR(date) as period,
    depot,
    vehicles_on_road,
    daily_passengers,
    daily_revenue,
    fleet_utilization_pct,
    km_per_bus,
    revenue_per_vehicle,
    passengers_per_bus
FROM data_prep
ORDER BY date DESC, depot
```

<LineChart
    data={depot_monthly}
    x=period
    y=daily_revenue
    series=depot
    title="Daily Revenue by Depot Over Time"
    yAxisTitle="Revenue (₹)"
/>

<LineChart
    data={depot_monthly}
    x=period
    y=daily_passengers
    series=depot
    title="Daily Passengers by Depot Over Time"
    yAxisTitle="Passengers"
/>

<LineChart
    data={depot_monthly}
    x=period
    y=fleet_utilization_pct
    series=depot
    title="Fleet Utilization by Depot Over Time"
    yAxisTitle="Utilization %"
/>

## 📋 Detailed Records

```sql all_records
WITH data_prep AS (
    SELECT 
        TRY_CAST(Date AS DATE) as date,
        CASE 
            WHEN Particulars IN ('Upper\nDepot', 'Upper Depot') THEN 'Upper Depot'
            WHEN Particulars IN ('Pune\nStation', 'Pune Station') THEN 'Pune Station'
            WHEN Particulars IN ('Bhekraina\ngar', 'Bhekrai-\nnagar', 'Bhekrai\nnagar') THEN 'Bhekrainagar'
            WHEN Particulars IN ('Shewalwa\ndi', 'Shewale-\nwadi', 'Shewal\nwadi') THEN 'Shewalwadi'
            ELSE Particulars 
        END as depot,
        TRY_CAST("Total Avg.Veh- On Road Per Day" AS INTEGER) as vehicles_on_road,
        TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS INTEGER) as daily_passengers,
        TRY_CAST("Average daily earning in Rs." AS INTEGER) as daily_revenue,
        TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE) as revenue_per_vehicle,
        TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE) as fleet_utilization_pct,
        TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE) as km_per_bus,
        TRY_CAST("Passenger Per Bus Per day" AS INTEGER) as passengers_per_bus,
        TRY_CAST("Total no.of Breakdown (PMPML Own)" AS INTEGER) as breakdowns,
        TRY_CAST("No.of Accidents (PMPML) Total" AS INTEGER) as accidents_pmpml
    FROM extracted
    WHERE Date IS NOT NULL AND Particulars IS NOT NULL
)
SELECT 
    date,
    depot,
    vehicles_on_road,
    daily_passengers,
    daily_revenue,
    revenue_per_vehicle,
    fleet_utilization_pct,
    km_per_bus,
    passengers_per_bus,
    breakdowns,
    accidents_pmpml
FROM data_prep
ORDER BY date DESC, depot
```

<DataTable data={all_records} rows=20 search=true>
    <Column id=date/>
    <Column id=depot/>
    <Column id=vehicles_on_road title="On Road" fmt="#,##0"/>
    <Column id=daily_passengers title="Passengers" fmt="#,##0"/>
    <Column id=daily_revenue title="Revenue" fmt="₹#,##0"/>
    <Column id=revenue_per_vehicle title="Rev/Vehicle" fmt="₹#,##0"/>
    <Column id=fleet_utilization_pct title="Utilization" fmt="#0.0'%'"/>
    <Column id=km_per_bus title="KM/Bus" fmt="#,##0"/>
    <Column id=passengers_per_bus title="Pass/Bus" fmt="#,##0"/>
    <Column id=breakdowns/>
    <Column id=accidents_pmpml title="Accidents"/>
</DataTable>

---

**Data Source:** PMPML Monthly Depot Operations | **Last Updated:** {latest_date[0].latest_date}