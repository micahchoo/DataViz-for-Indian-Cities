---
title: PMPML E-Bus Service Statistics
description: Electric bus operations 2023–2025 — fleet performance, energy efficiency, and the KMPU story
---

PMPML's electric bus fleet is a small but high-performing segment of the network. Operated under contract with Olectra Greentech (hence the "Hired Buses" label in accident data), the e-buses run at consistently higher fleet utilization than the diesel/CNG fleet — regularly above 95%. They serve six dedicated depots across both municipal areas.

The e-bus data carries a metric absent from every other PMPML report: **KMPU** (kilometers per unit of electricity). This is the electric equivalent of fuel efficiency — how far each kilowatt-hour takes the bus. Tracking KMPU alongside ridership and revenue makes it possible to estimate the cost of each kilometer served and each passenger carried, in energy terms.

**Note on depot coverage:** January 2023 data comes from a renamed PDF that escaped alphabetical sorting. From April 2025 onward, Hadapsar depot exited the e-bus operation and two new depots (Charholi, Maan) were added — the fleet count held at 490 but the geographic coverage shifted.

---

## System Overview

```sql ebus_summary
SELECT
    COUNT(DISTINCT Date) as total_months,
    ROUND(AVG(TRY_CAST(buses_held AS DOUBLE)), 0) as avg_buses_held,
    ROUND(AVG(TRY_CAST(fleet_utilization_pct AS DOUBLE)), 1) as avg_utilization_pct,
    ROUND(SUM(TRY_CAST(all_traffic_earning AS DOUBLE)) / 10000000, 1) as total_revenue_cr
FROM ebus_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
```

<Grid cols=4>
<BigValue
    data={ebus_summary}
    value=total_months
    title="Months of Data"
/>
<BigValue
    data={ebus_summary}
    value=avg_buses_held
    title="Avg Buses Held"
    fmt='#,##0'
/>
<BigValue
    data={ebus_summary}
    value=avg_utilization_pct
    title="Avg Fleet Utilization"
    fmt='#0.0"%"'
/>
<BigValue
    data={ebus_summary}
    value=total_revenue_cr
    title="Total Revenue (₹ Cr)"
    fmt='"₹"#,##0.0" Cr"'
/>
</Grid>

---

## Fleet Operations

The e-bus fleet has been exceptionally stable: 458 buses from launch through mid-2023, stepping up to 473 in October 2023, then 490 from August 2024. Unlike the diesel/CNG fleet where utilization swings with maintenance cycles, electric bus utilization has stayed consistently above 93% — reflecting both better vehicle reliability and stricter contractual targets with the operator.

<BarChart
    data={ebus_fleet}
    x=date_parsed
    y={['avg_on_road', 'avg_off_road']}
    type=stacked
    title="E-Bus Fleet: On Road vs Off Road (System Total)"
    yAxisTitle="Number of Buses"
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</BarChart>

<LineChart
    data={ebus_fleet}
    x=date_parsed
    y=fleet_utilization_pct
    title="Fleet Utilization % (System Total)"
    subtitle="E-bus consistently outperforms the diesel/CNG network — typically 93–97%"
    yAxisTitle="Utilization %"
    yMin=80
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Kilometers and Schedule Adherence

<AreaChart
    data={ebus_km}
    x=date_parsed
    y={['effective_km', 'cancelled_km']}
    type=stacked
    title="Effective vs Cancelled Kilometers (System Total)"
    yAxisTitle="Kilometers"
    yFmt='#,##0'
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</AreaChart>

<LineChart
    data={ebus_km}
    x=date_parsed
    y=km_per_bus_per_day
    title="Km Per Bus Per Day (System Total)"
    subtitle="E-bus vehicles are worked at roughly 200–220 km/day — comparable to BRT"
    yAxisTitle="Km/Bus/Day"
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Energy Efficiency: The KMPU Story

KMPU (kilometers per unit of electricity) is the e-bus equivalent of fuel efficiency. A bus that covers more kilometers per unit is more efficiently operated — whether through smoother driving, better route conditions, or reduced AC load. KMPU started high (0.81 in January 2023) and settled into a tighter band of 0.64–0.75 as operations normalized.

<LineChart
    data={ebus_energy}
    x=date_parsed
    y=kmpu
    title="Km Per Unit of Electricity (KMPU) — System Total"
    subtitle="Higher is better: more km covered per kWh consumed"
    yAxisTitle="Km/Unit"
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<LineChart
    data={ebus_energy}
    x=date_parsed
    y=electricity_per_day
    title="Electricity Consumption Per Day (Units)"
    subtitle="Monthly total divided by days — tracks fleet size and intensity of use"
    yAxisTitle="Units/Day"
    yFmt='#,##0'
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Revenue

<LineChart
    data={ebus_revenue}
    x=date_parsed
    y=all_traffic_earning_cr
    title="Monthly All-Traffic Earning (₹ Crores)"
    yAxisTitle="Revenue (₹ Cr)"
    yFmt='#,##0.0'
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<LineChart
    data={ebus_revenue}
    x=date_parsed
    y={['epk_total', 'epk_ticket']}
    title="Earning Per Kilometer (EPK)"
    subtitle="Total EPK vs ticket-only EPK"
    yAxisTitle="₹ per KM"
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Ridership

<LineChart
    data={ebus_ridership}
    x=date_parsed
    y=passengers_per_day
    title="Total Passengers Per Day (System Total)"
    yAxisTitle="Passengers / Day"
    yFmt='#,##0'
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

<LineChart
    data={ebus_ridership}
    x=date_parsed
    y=avg_passengers_per_bus_per_day
    title="Average Passengers Per Bus Per Day"
    yAxisTitle="Passengers / Bus / Day"
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

---

## Safety

E-bus accidents are categorized as "Hired Bus" accidents because the fleet is operated under contract with Olectra Greentech, not owned by PMPML. The safety record is generally strong — the dedicated corridors and newer vehicles contribute to lower accident rates.

<BarChart
    data={ebus_accidents}
    x=date_parsed
    y={['accidents_fatal', 'accidents_major', 'accidents_minor', 'accidents_insignificant']}
    type=stacked
    title="Monthly E-Bus Accidents by Severity (System Total)"
    yAxisTitle="Number of Accidents"
    connectGroup="ebus-monthly"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
</BarChart>

---

## Depot Comparison

<DataTable
    data={ebus_depot_summary}
    rows=all
    search=true
>
    <Column id=Depot title="Depot"/>
    <Column id=months_present title="Months"/>
    <Column id=avg_utilization title="Avg Utilization %" fmt='#0.0' contentType=colorscale colorScale="#16a34a"/>
    <Column id=avg_km_per_bus title="Km/Bus/Day" fmt='#,##0.0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=avg_passengers_per_bus title="Pass/Bus/Day" fmt='#,##0' contentType=colorscale colorScale="#3b82f6"/>
    <Column id=avg_kmpu title="Avg KMPU" fmt='#0.00' contentType=colorscale colorScale="#16a34a"/>
    <Column id=avg_epk title="EPK (₹/Km)" fmt='#,##0.00' contentType=colorscale colorScale="#16a34a"/>
</DataTable>

---

## See Also

- **[PMPML BRT Statistics](/PCMC/Public%20Transport/BRT)** — Dedicated BRT corridor operations across 15–17 depots
- **[Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — System-wide monthly fleet dashboard covering all PMPML operations
- **[Public Transport Overview](/PCMC/Public%20Transport)** — Three eras of bus transit in Pimpri-Chinchwad

---

*Data covers Jan 2023 – Jun 2025 with gaps (Jan–Mar 2024, Nov 2024–Mar 2025 missing). Source: PMPML E-Bus Service Statistical Reports (monthly), Chief Statistician.*

---

## Data Queries

*SQL queries powering the visualizations above. Evidence.dev processes these at build time — position in the file does not affect rendering.*

```sql ebus_fleet
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(buses_held AS DOUBLE) as buses_held,
    TRY_CAST(avg_on_road AS DOUBLE) as avg_on_road,
    TRY_CAST(avg_off_road AS DOUBLE) as avg_off_road,
    TRY_CAST(fleet_utilization_pct AS DOUBLE) as fleet_utilization_pct
FROM ebus_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql ebus_km
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(effective_km AS DOUBLE) as effective_km,
    TRY_CAST(cancelled_km AS DOUBLE) as cancelled_km,
    TRY_CAST(km_per_bus_per_day AS DOUBLE) as km_per_bus_per_day,
    TRY_CAST(pct_cancelled_km AS DOUBLE) as pct_cancelled_km
FROM ebus_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql ebus_energy
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(electricity_units AS DOUBLE) as electricity_units,
    TRY_CAST(electricity_per_day AS DOUBLE) as electricity_per_day,
    TRY_CAST(kmpu AS DOUBLE) as kmpu
FROM ebus_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql ebus_revenue
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(all_traffic_earning AS DOUBLE) / 10000000 as all_traffic_earning_cr,
    TRY_CAST(ticket_sale_earning AS DOUBLE) / 10000000 as ticket_earning_cr,
    TRY_CAST(epk_total AS DOUBLE) as epk_total,
    TRY_CAST(epk_ticket AS DOUBLE) as epk_ticket,
    TRY_CAST(earning_per_bus_per_day AS DOUBLE) as earning_per_bus_per_day
FROM ebus_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql ebus_ridership
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(passengers_per_day AS DOUBLE) as passengers_per_day,
    TRY_CAST(avg_passengers_per_bus_per_day AS DOUBLE) as avg_passengers_per_bus_per_day,
    TRY_CAST(ticket_passengers_per_day AS DOUBLE) as ticket_passengers_per_day,
    TRY_CAST(earning_per_passenger_per_day AS DOUBLE) as earning_per_passenger
FROM ebus_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql ebus_accidents
SELECT
    STRPTIME(Date, '%b %Y') as date_parsed,
    TRY_CAST(accidents_fatal AS DOUBLE) as accidents_fatal,
    TRY_CAST(accidents_major AS DOUBLE) as accidents_major,
    TRY_CAST(accidents_minor AS DOUBLE) as accidents_minor,
    TRY_CAST(accidents_insignificant AS DOUBLE) as accidents_insignificant,
    TRY_CAST(accidents_total AS DOUBLE) as accidents_total,
    TRY_CAST(accident_rate_per_lakh_km AS DOUBLE) as accident_rate_per_lakh_km
FROM ebus_extracted
WHERE Date IS NOT NULL AND Depot = 'System Total'
ORDER BY date_parsed
```

```sql ebus_depot_summary
SELECT
    Depot,
    COUNT(DISTINCT Date) as months_present,
    ROUND(AVG(TRY_CAST(fleet_utilization_pct AS DOUBLE)), 1) as avg_utilization,
    ROUND(AVG(TRY_CAST(km_per_bus_per_day AS DOUBLE)), 1) as avg_km_per_bus,
    ROUND(AVG(TRY_CAST(avg_passengers_per_bus_per_day AS DOUBLE)), 0) as avg_passengers_per_bus,
    ROUND(AVG(TRY_CAST(kmpu AS DOUBLE)), 2) as avg_kmpu,
    ROUND(AVG(TRY_CAST(epk_total AS DOUBLE)), 2) as avg_epk
FROM ebus_extracted
WHERE Date IS NOT NULL AND Depot != 'System Total'
GROUP BY Depot
ORDER BY avg_utilization DESC
```
