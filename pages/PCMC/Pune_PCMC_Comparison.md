---
title: Pune vs Pimpri-Chinchwad — Vehicle Fleet Comparison
description: How PCMC's registered vehicle fleet grew relative to Pune city 2000–2018, by category
---

Pimpri-Chinchwad and Pune share roads, borders, and eventually a merged transit authority — but their vehicle fleets have grown at very different rates. At the turn of the millennium, PCMC's fleet was roughly a fifth the size of Pune's. By 2017-18, it was approaching **40%**. This page traces that convergence across all major vehicle categories.

Both cities draw on the same Maharashtra RTO dataset: cumulative registrations on the books — not necessarily vehicles currently on the road, and not annual new registrations.

---

## Fleet Size Over Time

<Grid cols=4>
<BigValue
    data={fleet_summary}
    value=pcmc_2000
    title="PCMC Fleet — 2000-01"
    fmt='#,##0'
/>
<BigValue
    data={fleet_summary}
    value=pune_2000
    title="Pune Fleet — 2000-01"
    fmt='#,##0'
/>
<BigValue
    data={fleet_summary}
    value=pcmc_2018
    title="PCMC Fleet — 2017-18"
    fmt='#,##0'
/>
<BigValue
    data={fleet_summary}
    value=pune_2018
    title="Pune Fleet — 2017-18"
    fmt='#,##0'
/>
</Grid>

<LineChart
    data={total_fleet}
    x=display_year
    y={['pune_total', 'pcmc_total']}
    title="Total Registered Vehicles: Pune vs Pimpri-Chinchwad"
    subtitle="PCMC's fleet grew faster — narrowing the gap from 5:1 to under 3:1"
    yAxisTitle="Registered Vehicles"
    xAxisTitle="Year"
    yFmt='#,##0'
    xLabelWrap=true
    chartAreaHeight=350
/>

<LineChart
    data={total_fleet}
    x=display_year
    y=pcmc_share_pct
    title="PCMC Fleet as % of Pune Fleet"
    subtitle="Rose from ~20% in 2000-01 to ~38% by 2017-18"
    yAxisTitle="PCMC as % of Pune"
    xAxisTitle="Year"
    yFmt='#0.0"%"'
    xLabelWrap=true
/>

---

## Two-Wheelers: The Dominant Category

Two-wheelers — motorcycles, scooters, and mopeds — account for roughly 60–65% of all registered vehicles in both cities. PCMC's two-wheeler fleet grew at nearly twice Pune's rate, driven by workers commuting from dense residential zones (Pimpri, Bhosari, Charholi) to factory corridors.

<LineChart
    data={two_wheelers}
    x=display_year
    y={['pune_2w', 'pcmc_2w']}
    title="Two-Wheeler Registrations: Pune vs PCMC"
    subtitle="Motorcycles + scooters + moped. PCMC crossed 1.2 million by 2017-18."
    yAxisTitle="Registrations"
    xAxisTitle="Year"
    yFmt='#,##0'
    xLabelWrap=true
/>

<LineChart
    data={two_wheelers}
    x=display_year
    y=pcmc_2w_share_pct
    title="PCMC Two-Wheelers as % of Pune Two-Wheelers"
    yAxisTitle="PCMC as % of Pune"
    xAxisTitle="Year"
    yFmt='#0.0"%"'
    xLabelWrap=true
/>

---

## Cars and Personal Transport

Cars represent the second-largest personal vehicle category. PCMC started with ~21% of Pune's car fleet in 2000-01; by 2017-18 that share had grown to ~44%. Auto-rickshaws, heavily regulated in both cities, remained a smaller category dominated by Pune.

<LineChart
    data={personal_vehicles}
    x=display_year
    y={['pune_cars', 'pcmc_cars']}
    title="Car Registrations: Pune vs PCMC"
    yAxisTitle="Registrations"
    xAxisTitle="Year"
    yFmt='#,##0'
    xLabelWrap=true
/>

<LineChart
    data={personal_vehicles}
    x=display_year
    y={['pune_autos', 'pcmc_autos']}
    title="Auto-Rickshaw Registrations: Pune vs PCMC"
    subtitle="Pune dominated auto-rickshaw registrations throughout"
    yAxisTitle="Registrations"
    xAxisTitle="Year"
    yFmt='#,##0'
    xLabelWrap=true
/>

---

## Growth Rates Compared

PCMC's fleet grew faster in every major category. The strongest differential was in cars (+1,682% vs Pune's +682%) and two-wheelers (+700% vs +369%). Both cities show the classic Indian motorization arc — rapid growth through the 2000s, continuing through the 2010s.

<DataTable
    data={growth_rates}
    rows=all
>
    <Column id=category title="Vehicle Category"/>
    <Column id=pcmc_2000 title="PCMC 2000-01" fmt='#,##0'/>
    <Column id=pcmc_2018 title="PCMC 2017-18" fmt='#,##0'/>
    <Column id=pcmc_growth_pct title="PCMC Growth %" fmt='#,##0"%"'/>
    <Column id=pune_2000 title="Pune 2000-01" fmt='#,##0'/>
    <Column id=pune_2018 title="Pune 2017-18" fmt='#,##0'/>
    <Column id=pune_growth_pct title="Pune Growth %" fmt='#,##0"%"'/>
</DataTable>

---

## See Also

- **[PCMC Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018)** — PCMC-only data with detailed sub-category breakdown and per-capita analysis
- **[Fleet Composition Trends](/PCMC/Fleet_Composition_Trends)** — Growth rates, market share shifts, and indexed comparisons across PCMC categories
- **[Road Safety](/PCMC/Road_Accident_Statistics)** — Accident rates as both fleets expanded

---

*Data: cumulative vehicle registrations with the Pimpri-Chinchwad and Pune RTOs, 2000-2001 to 2017-2018. Source: Maharashtra state RTO registration data via [Open City Urban Data Portal](https://data.opencity.in/dataset/maharashtra-vehicles-registration-data/).*

---

## Data Queries

*SQL queries powering the visualizations above.*

```sql total_fleet
WITH totals AS (
    SELECT
        year,
        SPLIT_PART(year, '-', 1) as display_year,
        city,
        TRY_CAST(motor_cycles AS BIGINT) + TRY_CAST(scooters AS BIGINT) + TRY_CAST(moped AS BIGINT)
        + TRY_CAST(cars AS BIGINT) + TRY_CAST(jeeps AS BIGINT) + TRY_CAST(stn_wagons AS BIGINT)
        + TRY_CAST(taxis AS BIGINT) + TRY_CAST(luxury_tourist AS BIGINT)
        + TRY_CAST(auto_rickshaws AS BIGINT) + TRY_CAST(stage_carriages AS BIGINT)
        + TRY_CAST(contract_minibus AS BIGINT) + TRY_CAST(school_buses AS BIGINT)
        + TRY_CAST(psv AS BIGINT) + TRY_CAST(ambulances AS BIGINT)
        + TRY_CAST(articulated AS BIGINT) + TRY_CAST(trucks_lorries AS BIGINT)
        + TRY_CAST(tanker AS BIGINT) + TRY_CAST(delivery_van_4w AS BIGINT)
        + TRY_CAST(delivery_van_3w AS BIGINT) + TRY_CAST(tractors AS BIGINT)
        + TRY_CAST(trailers AS BIGINT) + TRY_CAST(others AS BIGINT) as total
    FROM pune_vehicle_registrations
)
SELECT
    p.display_year,
    p.total as pune_total,
    c.total as pcmc_total,
    ROUND(c.total * 100.0 / NULLIF(p.total, 0), 1) as pcmc_share_pct
FROM totals p
JOIN totals c ON p.year = c.year AND p.city = 'Pune' AND c.city = 'Pimpri-Chinchwad'
ORDER BY p.display_year
```

```sql fleet_summary
WITH totals AS (
    SELECT
        year,
        city,
        TRY_CAST(motor_cycles AS BIGINT) + TRY_CAST(scooters AS BIGINT) + TRY_CAST(moped AS BIGINT)
        + TRY_CAST(cars AS BIGINT) + TRY_CAST(jeeps AS BIGINT) + TRY_CAST(stn_wagons AS BIGINT)
        + TRY_CAST(taxis AS BIGINT) + TRY_CAST(luxury_tourist AS BIGINT)
        + TRY_CAST(auto_rickshaws AS BIGINT) + TRY_CAST(stage_carriages AS BIGINT)
        + TRY_CAST(contract_minibus AS BIGINT) + TRY_CAST(school_buses AS BIGINT)
        + TRY_CAST(psv AS BIGINT) + TRY_CAST(ambulances AS BIGINT)
        + TRY_CAST(articulated AS BIGINT) + TRY_CAST(trucks_lorries AS BIGINT)
        + TRY_CAST(tanker AS BIGINT) + TRY_CAST(delivery_van_4w AS BIGINT)
        + TRY_CAST(delivery_van_3w AS BIGINT) + TRY_CAST(tractors AS BIGINT)
        + TRY_CAST(trailers AS BIGINT) + TRY_CAST(others AS BIGINT) as total
    FROM pune_vehicle_registrations
)
SELECT
    MAX(CASE WHEN city = 'Pimpri-Chinchwad' AND year = '2000-2001' THEN total END) as pcmc_2000,
    MAX(CASE WHEN city = 'Pune'             AND year = '2000-2001' THEN total END) as pune_2000,
    MAX(CASE WHEN city = 'Pimpri-Chinchwad' AND year = '2017-2018' THEN total END) as pcmc_2018,
    MAX(CASE WHEN city = 'Pune'             AND year = '2017-2018' THEN total END) as pune_2018
FROM totals
```

```sql two_wheelers
SELECT
    SPLIT_PART(p.year, '-', 1) as display_year,
    TRY_CAST(p.motor_cycles AS BIGINT) + TRY_CAST(p.scooters AS BIGINT) + TRY_CAST(p.moped AS BIGINT) as pune_2w,
    TRY_CAST(c.motor_cycles AS BIGINT) + TRY_CAST(c.scooters AS BIGINT) + TRY_CAST(c.moped AS BIGINT) as pcmc_2w,
    ROUND(
        (TRY_CAST(c.motor_cycles AS DOUBLE) + TRY_CAST(c.scooters AS DOUBLE) + TRY_CAST(c.moped AS DOUBLE)) * 100.0 /
        NULLIF(TRY_CAST(p.motor_cycles AS DOUBLE) + TRY_CAST(p.scooters AS DOUBLE) + TRY_CAST(p.moped AS DOUBLE), 0)
    , 1) as pcmc_2w_share_pct
FROM pune_vehicle_registrations p
JOIN pune_vehicle_registrations c ON p.year = c.year
WHERE p.city = 'Pune' AND c.city = 'Pimpri-Chinchwad'
ORDER BY display_year
```

```sql personal_vehicles
SELECT
    SPLIT_PART(p.year, '-', 1) as display_year,
    TRY_CAST(p.cars AS BIGINT) as pune_cars,
    TRY_CAST(c.cars AS BIGINT) as pcmc_cars,
    TRY_CAST(p.auto_rickshaws AS BIGINT) as pune_autos,
    TRY_CAST(c.auto_rickshaws AS BIGINT) as pcmc_autos
FROM pune_vehicle_registrations p
JOIN pune_vehicle_registrations c ON p.year = c.year
WHERE p.city = 'Pune' AND c.city = 'Pimpri-Chinchwad'
ORDER BY display_year
```

```sql growth_rates
SELECT
    'Two-Wheelers' as category,
    TRY_CAST(c00.motor_cycles AS BIGINT) + TRY_CAST(c00.scooters AS BIGINT) + TRY_CAST(c00.moped AS BIGINT) as pcmc_2000,
    TRY_CAST(c18.motor_cycles AS BIGINT) + TRY_CAST(c18.scooters AS BIGINT) + TRY_CAST(c18.moped AS BIGINT) as pcmc_2018,
    ROUND(100.0 * (TRY_CAST(c18.motor_cycles AS DOUBLE) + TRY_CAST(c18.scooters AS DOUBLE) + TRY_CAST(c18.moped AS DOUBLE)
        - TRY_CAST(c00.motor_cycles AS DOUBLE) - TRY_CAST(c00.scooters AS DOUBLE) - TRY_CAST(c00.moped AS DOUBLE)) /
        NULLIF(TRY_CAST(c00.motor_cycles AS DOUBLE) + TRY_CAST(c00.scooters AS DOUBLE) + TRY_CAST(c00.moped AS DOUBLE), 0), 0) as pcmc_growth_pct,
    TRY_CAST(p00.motor_cycles AS BIGINT) + TRY_CAST(p00.scooters AS BIGINT) + TRY_CAST(p00.moped AS BIGINT) as pune_2000,
    TRY_CAST(p18.motor_cycles AS BIGINT) + TRY_CAST(p18.scooters AS BIGINT) + TRY_CAST(p18.moped AS BIGINT) as pune_2018,
    ROUND(100.0 * (TRY_CAST(p18.motor_cycles AS DOUBLE) + TRY_CAST(p18.scooters AS DOUBLE) + TRY_CAST(p18.moped AS DOUBLE)
        - TRY_CAST(p00.motor_cycles AS DOUBLE) - TRY_CAST(p00.scooters AS DOUBLE) - TRY_CAST(p00.moped AS DOUBLE)) /
        NULLIF(TRY_CAST(p00.motor_cycles AS DOUBLE) + TRY_CAST(p00.scooters AS DOUBLE) + TRY_CAST(p00.moped AS DOUBLE), 0), 0) as pune_growth_pct
FROM pune_vehicle_registrations c00
JOIN pune_vehicle_registrations c18 ON c18.year = '2017-2018' AND c18.city = 'Pimpri-Chinchwad'
JOIN pune_vehicle_registrations p00 ON p00.year = '2000-2001' AND p00.city = 'Pune'
JOIN pune_vehicle_registrations p18 ON p18.year = '2017-2018' AND p18.city = 'Pune'
WHERE c00.year = '2000-2001' AND c00.city = 'Pimpri-Chinchwad'
UNION ALL
SELECT
    'Cars',
    TRY_CAST(c00.cars AS BIGINT), TRY_CAST(c18.cars AS BIGINT),
    ROUND(100.0 * (TRY_CAST(c18.cars AS DOUBLE) - TRY_CAST(c00.cars AS DOUBLE)) / NULLIF(TRY_CAST(c00.cars AS DOUBLE), 0), 0),
    TRY_CAST(p00.cars AS BIGINT), TRY_CAST(p18.cars AS BIGINT),
    ROUND(100.0 * (TRY_CAST(p18.cars AS DOUBLE) - TRY_CAST(p00.cars AS DOUBLE)) / NULLIF(TRY_CAST(p00.cars AS DOUBLE), 0), 0)
FROM pune_vehicle_registrations c00
JOIN pune_vehicle_registrations c18 ON c18.year = '2017-2018' AND c18.city = 'Pimpri-Chinchwad'
JOIN pune_vehicle_registrations p00 ON p00.year = '2000-2001' AND p00.city = 'Pune'
JOIN pune_vehicle_registrations p18 ON p18.year = '2017-2018' AND p18.city = 'Pune'
WHERE c00.year = '2000-2001' AND c00.city = 'Pimpri-Chinchwad'
UNION ALL
SELECT
    'Auto-Rickshaws',
    TRY_CAST(c00.auto_rickshaws AS BIGINT), TRY_CAST(c18.auto_rickshaws AS BIGINT),
    ROUND(100.0 * (TRY_CAST(c18.auto_rickshaws AS DOUBLE) - TRY_CAST(c00.auto_rickshaws AS DOUBLE)) / NULLIF(TRY_CAST(c00.auto_rickshaws AS DOUBLE), 0), 0),
    TRY_CAST(p00.auto_rickshaws AS BIGINT), TRY_CAST(p18.auto_rickshaws AS BIGINT),
    ROUND(100.0 * (TRY_CAST(p18.auto_rickshaws AS DOUBLE) - TRY_CAST(p00.auto_rickshaws AS DOUBLE)) / NULLIF(TRY_CAST(p00.auto_rickshaws AS DOUBLE), 0), 0)
FROM pune_vehicle_registrations c00
JOIN pune_vehicle_registrations c18 ON c18.year = '2017-2018' AND c18.city = 'Pimpri-Chinchwad'
JOIN pune_vehicle_registrations p00 ON p00.year = '2000-2001' AND p00.city = 'Pune'
JOIN pune_vehicle_registrations p18 ON p18.year = '2017-2018' AND p18.city = 'Pune'
WHERE c00.year = '2000-2001' AND c00.city = 'Pimpri-Chinchwad'
UNION ALL
SELECT
    'Trucks & Lorries',
    TRY_CAST(c00.trucks_lorries AS BIGINT), TRY_CAST(c18.trucks_lorries AS BIGINT),
    ROUND(100.0 * (TRY_CAST(c18.trucks_lorries AS DOUBLE) - TRY_CAST(c00.trucks_lorries AS DOUBLE)) / NULLIF(TRY_CAST(c00.trucks_lorries AS DOUBLE), 0), 0),
    TRY_CAST(p00.trucks_lorries AS BIGINT), TRY_CAST(p18.trucks_lorries AS BIGINT),
    ROUND(100.0 * (TRY_CAST(p18.trucks_lorries AS DOUBLE) - TRY_CAST(p00.trucks_lorries AS DOUBLE)) / NULLIF(TRY_CAST(p00.trucks_lorries AS DOUBLE), 0), 0)
FROM pune_vehicle_registrations c00
JOIN pune_vehicle_registrations c18 ON c18.year = '2017-2018' AND c18.city = 'Pimpri-Chinchwad'
JOIN pune_vehicle_registrations p00 ON p00.year = '2000-2001' AND p00.city = 'Pune'
JOIN pune_vehicle_registrations p18 ON p18.year = '2017-2018' AND p18.city = 'Pune'
WHERE c00.year = '2000-2001' AND c00.city = 'Pimpri-Chinchwad'
```
