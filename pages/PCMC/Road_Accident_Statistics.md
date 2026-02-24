---
title: Road Safety in Pimpri-Chinchwad
description: Accident trends 2000-2007 and PMPML bus safety 2023-2025
---

As Pimpri-Chinchwad's vehicle fleet more than doubled between 2000 and 2007, road safety became a growing concern. The 2008 Comprehensive Mobility Plan recorded both fatal and major accidents across the city, revealing a tension between improving per-vehicle safety rates and rising absolute casualty counts driven by sheer traffic volume growth. Fatal accidents and deaths track almost 1:1 (by definition — a fatal accident is one where someone dies), so the key trends to watch are the overall trajectory and the ratio of fatal to major accidents.

## Accident Trends (2000-2007)

<BarChart
    data={accident_trends}
    x=Year
    y={['fatal_accidents', 'major_accidents']}
    title="Accidents by Severity (2000-2007)"
    subtitle="Fatal and major accidents both trend upward"
    yAxisTitle="Number of Accidents"
    xFmt='####'
    type=stacked
/>

<LineChart
    data={accident_trends}
    x=Year
    y={['deaths', 'injured_persons']}
    title="Casualties Over Time (2000-2007)"
    subtitle="Deaths rose 33% while injuries remained volatile"
    yAxisTitle="Number of People"
    xFmt='####'
/>

<LineChart
    data={accident_ratios}
    x=Year
    y=fatal_share_pct
    title="Fatal Accidents as Share of Total (%)"
    subtitle="Rising from 53% to 56% — a higher proportion of accidents are deadly"
    yAxisTitle="Fatal Accident Share (%)"
    xFmt='####'
/>

<DataTable
    data={accident_trends}
    rows=all
/>

## Per-Vehicle Accident Rate

Absolute accident counts are misleading without accounting for the growing vehicle fleet. By cross-referencing with [PCMC vehicle registration data](/PCMC/Registered_Vehicles_2000_2018), we can compute accident rates per 10,000 registered vehicles.

<LineChart
    data={per_vehicle_rate}
    x=Year
    y={['deaths_per_10k_vehicles', 'accidents_per_10k_vehicles']}
    title="Accident Rate Per 10,000 Registered Vehicles"
    subtitle="Per-vehicle fatality rate dropped sharply even as absolute deaths rose 33%"
    yAxisTitle="Per 10,000 Vehicles"
    xFmt='####'
/>

Despite a 33% rise in absolute deaths (118 to 157) between 2000 and 2007, the fatality rate per 10,000 registered vehicles fell sharply as the vehicle fleet more than doubled. Roads were getting safer per vehicle — but the sheer volume growth meant more total deaths. This is a common pattern in rapidly motorizing cities: safety improvements per trip are overwhelmed by the explosion in total trips.

## Bus Safety: PMPML Operations 2023-2025

Between 2007 and 2023, there is a 16-year gap in this accident data. The Comprehensive Mobility Plan captured PCMC's road safety through the pre-merger era, while PMPML's monthly depot reports pick up the story from January 2023. While these datasets are not directly comparable — one records city-wide road accidents across all vehicle types, the other tracks bus-specific incidents within PMPML operations — the depot data lets us examine bus safety specifically, offering a focused lens on public transport's safety record during the post-COVID recovery period.

<BarChart
    data={pmpml_accidents}
    x=date_parsed
    y={['fatal', 'major', 'minor']}
    title="Monthly PMPML Accidents by Severity"
    subtitle="Stacked view: fatal, major, and minor bus incidents"
    yAxisTitle="Number of Accidents"
    type=stacked
    connectGroup="pmpml-safety"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</BarChart>

<LineChart
    data={pmpml_accidents}
    x=date_parsed
    y=accident_rate_per_lakh_km
    title="PMPML Accident Rate per Lakh KMs"
    subtitle="Weighted average across all depots"
    yAxisTitle="Accidents per 1 Lakh KMs"
    connectGroup="pmpml-safety"
>
    <ReferenceArea xMin='2024-01-01' xMax='2024-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2024-11-01' xMax='2025-03-31' label="Data gap" color=warning labelPosition=bottom/>
    <ReferenceArea xMin='2025-07-01' xMax='2025-09-30' label="Data gap" color=warning labelPosition=bottom/>
</LineChart>

### Own Fleet vs. Hired Vehicles

<BarChart
    data={own_vs_hired_accidents}
    x=fleet_type
    y={['fatal', 'major', 'minor']}
    title="Total Accidents: PMPML Own vs. Hired Fleet (All Months)"
    yAxisTitle="Number of Accidents"
    type=stacked
/>

<DataTable
    data={own_vs_hired_accidents}
    rows=all
>
    <Column id=fleet_type title="Fleet Type"/>
    <Column id=fatal title="Fatal"/>
    <Column id=major title="Major"/>
    <Column id=minor title="Minor"/>
    <Column id=total title="Total"/>
    <Column id=avg_rate_per_lakh_km title="Rate per Lakh KM" fmt='#,##0.00'/>
</DataTable>

The own-fleet vs. hired comparison should be read with caution. The hired fleet operates fewer total kilometers, so even small absolute accident counts can produce volatile rate figures. The rate columns in the source data (`Rate of Accidents per 1 Lakh KMs (PMPML)` and `Rate of Accidents per 1 Lakh KMs (HIRED)`) are reported per depot per month, so the weighted averages above smooth out some of that noise — but the hired fleet's smaller denominator means its rate is inherently less stable. What matters most is whether one fleet type shows a consistently higher severity mix (more fatal/major vs. minor) rather than just comparing raw rates.

The direction of travel, despite these caveats, is clear: total bus accident burden across both own and hired fleet roughly halved between FY2023-24 and FY2024-25. The [Annual Performance Report](/PCMC/Public%20Transport/Annual_Statistics) shows the year-on-year figures in full context.

---

## Data Queries

*SQL queries powering the visualizations above. Evidence.dev processes these at build time — position in the file does not affect rendering.*

```sql accident_trends
select
    Year,
    cast("Fatal accidents" as int) as fatal_accidents,
    cast("Major accidents" as int) as major_accidents,
    cast("Deaths" as int) as deaths,
    cast("Injured persons" as int) as injured_persons,
    cast("Fatal accidents" as int) + cast("Major accidents" as int) as total_accidents
from road_accident_statistics
order by Year
```

```sql accident_ratios
select
    Year,
    cast("Fatal accidents" as int) as fatal,
    cast("Major accidents" as int) as major,
    ROUND(cast("Fatal accidents" as DOUBLE) / (cast("Fatal accidents" as DOUBLE) + cast("Major accidents" as DOUBLE)) * 100, 1) as fatal_share_pct
from road_accident_statistics
order by Year
```

```sql per_vehicle_rate
WITH vehicle_totals AS (
    SELECT
        CAST(SPLIT_PART(Year, '-', 1) AS INT) as year_num,
        SUM(Count) as total_vehicles
    FROM vehicle_registrations_by_type_and_year
    GROUP BY year_num
),
accidents AS (
    SELECT
        Year as year_num,
        cast("Deaths" as int) as deaths,
        cast("Fatal accidents" as int) + cast("Major accidents" as int) as total_accidents
    FROM road_accident_statistics
)
SELECT
    a.year_num as Year,
    a.deaths,
    a.total_accidents,
    v.total_vehicles,
    ROUND(a.deaths * 10000.0 / v.total_vehicles, 2) as deaths_per_10k_vehicles,
    ROUND(a.total_accidents * 10000.0 / v.total_vehicles, 2) as accidents_per_10k_vehicles
FROM accidents a
JOIN vehicle_totals v ON a.year_num = v.year_num
ORDER BY a.year_num
```

```sql pmpml_accidents
SELECT
    Date,
    STRPTIME(Date, '%b %Y') as date_parsed,
    SUM(TRY_CAST("No.of Accidents (PMPML) 1. Fatal" AS DOUBLE)) as fatal,
    SUM(TRY_CAST("No.of Accidents (PMPML) 2. Major" AS DOUBLE)) as major,
    SUM(TRY_CAST("No.of Accidents (PMPML) 3. Minor" AS DOUBLE)) as minor,
    SUM(TRY_CAST("No.of Accidents (PMPML) Total" AS DOUBLE)) as total,
    ROUND(
        SUM(TRY_CAST("Rate of Accidents per 1 Lakh KMs (PMPML)" AS DOUBLE) *
            TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)) /
        NULLIF(SUM(TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)), 0)
    , 2) as accident_rate_per_lakh_km
FROM extracted
WHERE Date IS NOT NULL
GROUP BY Date, date_parsed
ORDER BY date_parsed
```

```sql own_vs_hired_accidents
SELECT
    'PMPML Own Fleet' as fleet_type,
    SUM(TRY_CAST("No.of Accidents (PMPML) 1. Fatal" AS DOUBLE)) as fatal,
    SUM(TRY_CAST("No.of Accidents (PMPML) 2. Major" AS DOUBLE)) as major,
    SUM(TRY_CAST("No.of Accidents (PMPML) 3. Minor" AS DOUBLE)) as minor,
    SUM(TRY_CAST("No.of Accidents (PMPML) Total" AS DOUBLE)) as total,
    ROUND(
        SUM(TRY_CAST("Rate of Accidents per 1 Lakh KMs (PMPML)" AS DOUBLE) *
            TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)) /
        NULLIF(SUM(TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)), 0)
    , 2) as avg_rate_per_lakh_km
FROM extracted
WHERE Date IS NOT NULL
UNION ALL
SELECT
    'Hired Vehicles' as fleet_type,
    SUM(TRY_CAST("No.of Accidents (HIRED) 1. Fatal" AS DOUBLE)) as fatal,
    SUM(TRY_CAST("No.of Accidents (HIRED) 2. Major" AS DOUBLE)) as major,
    SUM(TRY_CAST("No.of Accidents (HIRED) 3. Minor" AS DOUBLE)) as minor,
    SUM(TRY_CAST("No.of Accidents (HIRED) Total" AS DOUBLE)) as total,
    ROUND(
        SUM(TRY_CAST("Rate of Accidents per 1 Lakh KMs (HIRED)" AS DOUBLE) *
            TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)) /
        NULLIF(SUM(TRY_CAST("Total Eff.Km (Own+Hire)" AS DOUBLE)), 0)
    , 2) as avg_rate_per_lakh_km
FROM extracted
WHERE Date IS NOT NULL
```

---

*Data covers 2000–2007 (CMP road accidents) and January 2023–December 2025 (PMPML depot safety records, with gaps in Jan–Mar 2024, Nov 2024–Mar 2025, Jul–Sep 2025). Source: [PMPML Chief Statistician monthly reports](https://pmpml.org/statistics); accident data 2000-2007 from the 2008 Comprehensive Mobility Plan.*

## See Also

- **[Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018)** — The vehicle fleet growth behind accident rate changes
- **[PMPML Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Full operational dashboard including safety metrics
