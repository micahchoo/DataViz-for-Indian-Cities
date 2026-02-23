---
title: PMPML Depot Performance
description: Performance patterns across 17 depots — efficiency, fleet composition, ridership, and revenue
sidebar: show
---

## PMPML Depot Performance

Performance patterns across 17 depots — efficiency, fleet composition, ridership, and revenue. Each depot serves a different catchment area with different route profiles, fleet mixes, and rider demographics. These structural differences produce very different outcomes on the same metrics.

---

## 1. Depot Map

{#if depot_metrics_for_map.length > 0}

<PointMap
data={depot_metrics_for_map}
basemap={`https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png`}
attribution='&copy; OpenStreetMap contributors &copy; Carto'
lat=latitude
long=longitude
value=avg_fleet_size
pointName=depot
valueFmt="#,##0"
title="PMPML Depots — Bubble Size = Average Fleet Size"
tooltipType=hover
tooltip={[
{id: 'depot', showColumnName: false, valueClass: 'text-l font-semibold'},
{id: 'avg_fleet_size', title: 'Avg Fleet Size', fmt: 'num0'},
{id: 'avg_utilization_pct', title: 'Utilization %', fmt: '#0.0'},
{id: 'total_revenue_crores', title: 'Revenue (₹ Cr)', fmt: '#,##0.00'},
{id: 'avg_passengers_per_bus', title: 'Passengers/Bus/Day', fmt: 'num0'}
]}
opacity=0.8
size=20
height=700
legend=false
startingLat=18.56
startingLong=73.85
startingZoom=11
/>

{:else}

_The map will render once latitude/longitude values are added to `sources/CMP/depot_locations.csv`. The 17 depot coordinates are currently blank._

{/if}

---

## 2. The Efficiency Spectrum

How depots compare on the metrics that matter most: fleet utilization, earning per kilometer, passengers per bus, and fleet size. Small depots sometimes outperform large ones on efficiency — and vice versa.

<DataTable
    data={depot_efficiency_spectrum}
    rows=all
    search=true
>
    <Column id=Depot />
    <Column id=months_data title="Months" />
    <Column id=avg_fleet_size title="Fleet Size" fmt='#,##0' />
    <Column id=avg_utilization_pct title="Utilization %" fmt='#0.0' contentType=colorscale colorScale="#16a34a"/>
    <Column id=avg_epk title="₹/KM (EPK)" fmt='#,##0.00' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=avg_passengers_per_bus title="Pass/Bus/Day" fmt='#,##0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=avg_revenue_per_bus title="₹/Bus/Day" fmt='#,##0' contentType=colorscale colorScale="#16a34a"/>
</DataTable>

<BarChart
    data={top_bottom_utilization}
    x=Depot
    y=avg_utilization_pct
    swapXY=true
    title="Fleet Utilization % by Depot (All-Time Average)"
    yAxisTitle="Utilization %"
    yFmt='#0.0'
/>

Utilization measures the share of a depot's total fleet that is actually running scheduled routes on any given day. Depots with older fleets or more maintenance backlogs show lower utilization — buses sitting in workshops drag the percentage down. Compare fleet size with utilization: some smaller depots maintain tighter operations, while some large depots with big fleets still struggle to put their buses on the road.

---

## 3. Schedule Adherence

Each depot has a sanctioned schedule — the number of daily trips it is expected to operate. The gap between sanctioned and actually operated schedules reveals chronic under-delivery. A depot consistently falling short is either short on serviceable buses, short on crew, or both.

<BarChart
    data={schedule_adherence}
    x=Depot
    y={['avg_sanctioned', 'avg_operated']}
    swapXY=true
    title="Sanctioned vs. Operated Schedules per Day (Avg)"
    yAxisTitle="Schedules/Day"
    type=grouped
/>

<BarChart
    data={schedule_adherence}
    x=Depot
    y=avg_schedule_gap
    swapXY=true
    title="Average Daily Schedule Gap (Sanctioned minus Operated)"
    yAxisTitle="Missed Schedules/Day"
/>

<DataTable
    data={schedule_adherence}
    rows=all
>
    <Column id=Depot />
    <Column id=avg_sanctioned title="Sanctioned/Day" fmt='#,##0' />
    <Column id=avg_operated title="Operated/Day" fmt='#,##0' />
    <Column id=adherence_pct title="Adherence %" fmt='#0.0' contentType=colorscale colorScale="#16a34a"/>
    <Column id=avg_schedule_gap title="Daily Gap" fmt='#,##0' contentType=colorscale colorScale="#ef4444"/>
</DataTable>

Depots at the bottom of the adherence ranking are chronically missing their scheduled trips. When a depot's adherence is below 80%, it means riders on those routes are regularly experiencing cancelled services — longer waits, crowded buses on surviving trips, and eventual mode shift to private vehicles. The schedule gap is a leading indicator of service deterioration.

---

## 4. Own vs. PPP vs. Hired Fleet

PMPML's fleet is not a single entity. Depots operate a mix of PMPML-owned buses, PPP (Public-Private Partnership) vehicles from private operators, and hired buses. The ownership split has direct implications for cost control, service quality, and operational flexibility.

<BarChart
    data={fleet_composition}
    x=Depot
    y={['avg_own_on_road', 'avg_ppp_on_road', 'avg_hired_on_road']}
    type=stacked
    swapXY=true
    title="Fleet Composition on Road: Own / PPP / Hired (Avg Daily)"
    yAxisTitle="Vehicles on Road per Day"
/>

<DataTable
    data={fleet_composition}
    rows=all
    search=true
>
    <Column id=Depot />
    <Column id=avg_own_on_road title="Own" fmt='#,##0' />
    <Column id=avg_ppp_on_road title="PPP" fmt='#,##0' />
    <Column id=avg_hired_on_road title="Hired" fmt='#,##0' />
    <Column id=avg_total_on_road title="Total" fmt='#,##0' />
    <Column id=ppp_share_pct title="PPP %" fmt='#0.0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=hired_share_pct title="Hired %" fmt='#0.0' contentType=colorscale colorScale="#3b82f6"/>
</DataTable>

Some depots run almost entirely on hired or PPP vehicles. This creates a dependency: when private operators pull back (contract disputes, fleet age-outs), these depots have no fallback. Depots with a high own-fleet share have more direct control over service reliability, but also bear the full maintenance burden. The ideal balance depends on route economics — high-revenue trunk routes justify owned fleet investment; low-ridership peripheral routes may be better served through flexible hire arrangements.

---

## 5. Revenue vs. Ridership

Not all passengers are equal in revenue terms. A depot with high ridership but low per-passenger revenue is carrying mostly pass holders (student passes, monthly commuter passes, senior citizen concessions). A depot with lower ridership but higher fare per head is serving more ticket-buying, longer-distance passengers.

<BarChart
    data={revenue_vs_ridership}
    x=Depot
    y=avg_passengers_per_bus
    swapXY=true
    title="Average Passengers per Bus per Day by Depot"
    yAxisTitle="Passengers/Bus/Day"
/>

<BarChart
    data={revenue_vs_ridership}
    x=Depot
    y=avg_revenue_per_bus
    swapXY=true
    title="Average Revenue per Bus per Day by Depot (₹)"
    yAxisTitle="₹/Bus/Day"
    yFmt='#,##0'
/>

<DataTable
    data={revenue_vs_ridership}
    rows=all
    search=true
>
    <Column id=Depot />
    <Column id=avg_passengers_per_bus title="Pass/Bus/Day" fmt='#,##0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=avg_revenue_per_bus title="₹/Bus/Day" fmt='#,##0' contentType=colorscale colorScale="#16a34a"/>
    <Column id=avg_fare_per_passenger title="₹/Passenger" fmt='#,##0.00' contentType=colorscale colorScale="#16a34a"/>
    <Column id=avg_epk title="₹/KM (EPK)" fmt='#,##0.00' />
    <Column id=avg_fleet_size title="Fleet Size" fmt='#,##0' />
</DataTable>

<BarChart
    data={fare_per_passenger_chart}
    x=Depot
    y=avg_fare_per_passenger
    swapXY=true
    title="Average Revenue per Passenger by Depot (₹)"
    yAxisTitle="₹ per Passenger"
    yFmt='#,##0.00'
/>

The revenue-per-passenger gap across depots tells us about route mix and rider composition. Depots serving longer-distance intercity or suburban routes naturally earn more per passenger (distance-based fares). Depots in dense urban cores carry more passengers per bus but at lower per-trip fares — especially when pass holders dominate. A depot with high ridership but low fare realization is subsidizing mobility for pass-dependent commuters, which is socially valuable but financially challenging.

---

## 6. Monthly Trends by Depot

Select a depot to see its utilization and ridership trends over time. Seasonal patterns — monsoon dips, festive-season peaks, post-holiday recovery — vary by depot depending on their route mix and catchment area.

<Dropdown
  name=selected_depot
  data={depot_list}
  value=value
  label=label
  title="Select Depot"
  defaultValue="Swargate"
/>

### {inputs.selected_depot.value} — Fleet Utilization Over Time

<LineChart
    data={depot_monthly_trends}
    x=date_parsed
    y=utilization_pct
    title="{inputs.selected_depot.value}: Monthly Fleet Utilization %"
    yAxisTitle="Utilization %"
    yFmt='#0.0'
    connectGroup="depot-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

### {inputs.selected_depot.value} — Passengers per Bus per Day

<LineChart
    data={depot_monthly_trends}
    x=date_parsed
    y=passengers_per_bus
    title="{inputs.selected_depot.value}: Monthly Passengers per Bus per Day"
    yAxisTitle="Passengers/Bus/Day"
    yFmt='#,##0'
    connectGroup="depot-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

### {inputs.selected_depot.value} — Revenue per Bus per Day

<LineChart
    data={depot_monthly_trends}
    x=date_parsed
    y=revenue_per_bus
    title="{inputs.selected_depot.value}: Monthly Revenue per Bus (₹)"
    yAxisTitle="₹/Bus/Day"
    yFmt='#,##0'
    connectGroup="depot-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

### {inputs.selected_depot.value} — KMs per Bus per Day

<LineChart
    data={depot_monthly_trends}
    x=date_parsed
    y=km_per_bus
    title="{inputs.selected_depot.value}: Monthly Effective KMs per Bus per Day"
    yAxisTitle="KMs/Bus/Day"
    yFmt='#,##0.0'
    connectGroup="depot-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<DataTable
    data={depot_monthly_trends}
    rows=all
>
    <Column id=date_parsed title="Month" />
    <Column id=fleet_size title="Fleet" fmt='#,##0' />
    <Column id=utilization_pct title="Util %" fmt='#0.0' />
    <Column id=passengers_per_bus title="Pass/Bus" fmt='#,##0' />
    <Column id=revenue_per_bus title="₹/Bus" fmt='#,##0' />
    <Column id=km_per_bus title="KM/Bus" fmt='#,##0.0' />
</DataTable>

Monthly patterns typically show: monsoon months (June-September) see dips in ridership and utilization as flooding and waterlogging disrupt services; festive months (October-November around Diwali/Dussehra) sometimes show peaks from increased travel; and the January-March quarter tends to be the most stable operational period. However, these patterns vary significantly by depot — a depot serving industrial areas may see different seasonality than one near educational institutions.

---

## Data Queries

*SQL queries powering the visualizations above. Evidence.dev processes these at build time — position in the file does not affect rendering.*

```sql depot_metrics_for_map
SELECT
    d.depot,
    d.latitude,
    d.longitude,
    ROUND(AVG(TRY_CAST(e."Total Vehicles Per Day" AS DOUBLE)), 0) as avg_fleet_size,
    ROUND(AVG(TRY_CAST(e."% of Fleet Utilization(PMPML+PPP)" AS DOUBLE)), 1) as avg_utilization_pct,
    ROUND(SUM(TRY_CAST(e."All Traffic Earning (₹)" AS DOUBLE)) / 10000000, 2) as total_revenue_crores,
    ROUND(AVG(TRY_CAST(e."Avg Passenger per Bus per day on Traffic" AS DOUBLE)), 0) as avg_passengers_per_bus
FROM depot_locations d
LEFT JOIN extracted e ON d.depot = e.Depot
WHERE e.Date IS NOT NULL AND e.Depot IS NOT NULL
    AND d.latitude IS NOT NULL AND d.longitude IS NOT NULL
GROUP BY d.depot, d.latitude, d.longitude
ORDER BY avg_fleet_size DESC
```

```sql depot_efficiency_spectrum
SELECT
    Depot,
    COUNT(*) as months_data,
    ROUND(AVG(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0) as avg_fleet_size,
    ROUND(AVG(LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0)), 1) as avg_utilization_pct,
    ROUND(AVG(TRY_CAST("Earning per KMs in Rs.(EPK) (₹)" AS DOUBLE)), 2) as avg_epk,
    ROUND(AVG(TRY_CAST("Avg Passenger per Bus per day on Traffic" AS DOUBLE)), 0) as avg_passengers_per_bus,
    ROUND(AVG(TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE)), 0) as avg_revenue_per_bus
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
GROUP BY Depot
ORDER BY avg_utilization_pct DESC
```

```sql top_bottom_utilization
SELECT
    Depot,
    ROUND(AVG(LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0)), 1) as avg_utilization_pct
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
GROUP BY Depot
ORDER BY avg_utilization_pct DESC
```

```sql schedule_adherence
-- Jan 2023 and Mar 2023 data quality issue: the "Sanctioned" column contains only
-- PMPML-direct schedules (not PPP) while "Operated" contains the full PPP+hire total.
-- The columns are effectively swapped for 8 depots in those two months.
-- Fix: use GREATEST as the true sanctioned and LEAST as the true operated.
SELECT
    Depot,
    ROUND(AVG(true_sanctioned), 0) as avg_sanctioned,
    ROUND(AVG(true_operated), 0) as avg_operated,
    ROUND(AVG(true_operated) * 100.0 / NULLIF(AVG(true_sanctioned), 0), 1) as adherence_pct,
    ROUND(AVG(true_sanctioned) - AVG(true_operated), 0) as avg_schedule_gap
FROM (
    SELECT
        Depot,
        GREATEST(
            COALESCE(TRY_CAST("No.of Schedules Sanctioned Per Day (PMPML + PPP)" AS DOUBLE), 0),
            COALESCE(TRY_CAST("Average No.of Schedule operated Per Day (PMPML+PPP)" AS DOUBLE), 0)
        ) as true_sanctioned,
        LEAST(
            COALESCE(TRY_CAST("No.of Schedules Sanctioned Per Day (PMPML + PPP)" AS DOUBLE), 0),
            COALESCE(TRY_CAST("Average No.of Schedule operated Per Day (PMPML+PPP)" AS DOUBLE), 0)
        ) as true_operated
    FROM extracted
    WHERE Date IS NOT NULL AND Depot IS NOT NULL
)
GROUP BY Depot
ORDER BY adherence_pct ASC
```

```sql fleet_composition
SELECT
    Depot,
    ROUND(AVG(TRY_CAST("Avg. Vehicles On Road- PMPML Per Day (OWN)" AS DOUBLE)), 0) as avg_own_on_road,
    ROUND(AVG(TRY_CAST("On Road PPP Vehicles per day" AS DOUBLE)), 0) as avg_ppp_on_road,
    ROUND(AVG(TRY_CAST("On Road Hire Vehicles Per Day" AS DOUBLE)), 0) as avg_hired_on_road,
    ROUND(AVG(TRY_CAST("Total Avg.Veh- On Road Per Day" AS DOUBLE)), 0) as avg_total_on_road,
    ROUND(
        AVG(TRY_CAST("On Road PPP Vehicles per day" AS DOUBLE)) * 100.0 /
        NULLIF(AVG(TRY_CAST("Total Avg.Veh- On Road Per Day" AS DOUBLE)), 0)
    , 1) as ppp_share_pct,
    ROUND(
        AVG(TRY_CAST("On Road Hire Vehicles Per Day" AS DOUBLE)) * 100.0 /
        NULLIF(AVG(TRY_CAST("Total Avg.Veh- On Road Per Day" AS DOUBLE)), 0)
    , 1) as hired_share_pct
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
GROUP BY Depot
ORDER BY avg_total_on_road DESC
```

```sql revenue_vs_ridership
SELECT
    Depot,
    ROUND(AVG(TRY_CAST("Avg Passenger per Bus per day on Traffic" AS DOUBLE)), 0) as avg_passengers_per_bus,
    ROUND(AVG(TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE)), 0) as avg_revenue_per_bus,
    ROUND(
        AVG(TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE)) /
        NULLIF(AVG(TRY_CAST("Avg Passenger per Bus per day on Traffic" AS DOUBLE)), 0)
    , 2) as avg_fare_per_passenger,
    ROUND(AVG(TRY_CAST("Earning per KMs in Rs.(EPK) (₹)" AS DOUBLE)), 2) as avg_epk,
    ROUND(AVG(TRY_CAST("Total Vehicles Per Day" AS DOUBLE)), 0) as avg_fleet_size
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
GROUP BY Depot
ORDER BY avg_passengers_per_bus DESC
```

```sql fare_per_passenger_chart
SELECT
    Depot,
    ROUND(
        AVG(TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE)) /
        NULLIF(AVG(TRY_CAST("Avg Passenger per Bus per day on Traffic" AS DOUBLE)), 0)
    , 2) as avg_fare_per_passenger
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
GROUP BY Depot
ORDER BY avg_fare_per_passenger DESC
```

```sql depot_list
SELECT DISTINCT Depot as value, Depot as label
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
ORDER BY Depot
```

```sql depot_monthly_trends
SELECT
    Date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    Depot,
    LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0) as utilization_pct,
    TRY_CAST("Avg Passenger per Bus per day on Traffic" AS DOUBLE) as passengers_per_bus,
    TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE) as revenue_per_bus,
    TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE) as km_per_bus,
    TRY_CAST("Total Vehicles Per Day" AS DOUBLE) as fleet_size
FROM extracted
WHERE Date IS NOT NULL AND Depot IS NOT NULL
    AND Depot = '${inputs.selected_depot.value}'
ORDER BY date_parsed
```

---

## See Also

- **[Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Monthly fleet dashboard: vehicle deployment, kilometers, revenue, fuel efficiency, safety, and depot comparisons
- **[PCMT Before PMPML](/PCMC/Public%20Transport/PCMT_before_PMPML)** — Historical context: how PCMT operated before the 2007 merger

---

*Data covers Jan 2023 – Jun 2025 with gaps (Jan–Mar 2024, Nov 2024–Mar 2025 missing). Source: PMPML Chief Statistician monthly reports.*