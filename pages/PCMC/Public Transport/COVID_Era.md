---
title: PMPML During COVID — FY 2020-21
description: Fleet utilization collapsed to 32%, ridership fell to 2.83 lakh/day — how the pandemic reshaped bus operations across 13 Pune depots
---

FY 2020-21 was the pandemic year. Maharashtra's lockdowns from March 2020 cut PMPML's daily ridership to just 2.83 lakh passengers. Of 2,259 buses across 13 depots, only 728 were on road — a fleet utilization rate of 32%, compared to 74% in FY 2023-24. Revenue fell to ₹37 lakh per day system-wide.

This annual depot-level report is the only structured snapshot of PMPML operations during the COVID period. It shows not just the system-wide collapse but which depots were most affected — and how the balance of own vs. hired buses shifted.

---

## System at a Glance

<Grid cols=4>
<BigValue
  data={covid_headline}
  value=total_on_road
  title="Buses On Road (Daily Avg)"
  fmt='#,##0'
/>
<BigValue
  data={covid_headline}
  value=fleet_utilization_pct
  title="Fleet Utilization"
  fmt='#0.0"%"'
/>
<BigValue
  data={covid_headline}
  value=daily_ridership
  title="Daily Ridership"
  fmt='#,##0'
/>
<BigValue
  data={covid_headline}
  value=daily_revenue_lakh
  title="Daily Revenue (₹ Lakh)"
  fmt='#,##0.0'
/>
</Grid>

*FY 2023-24 comparison: 1,658 buses on road, 74.4% utilization, 12.08 lakh daily passengers.*

Note: 4 depots that exist today — Baner, Charholi, Maan, Wagholi — were not yet operational or not yet included in this report.

---

## Fleet Utilization by Depot

Only 3 depots exceeded 40% utilization. The peri-urban depots with large hired fleets (Nigadi, Bhekrai Nagar) had the most buses sitting idle — contractors fielded vehicles even as passenger demand evaporated.

<BarChart
  data={covid_by_depot}
  x=Depot
  y=utilization_pct
  title="Fleet Utilization by Depot — FY 2020-21"
  subtitle="Buses on road ÷ total buses held"
  yAxisTitle="Fleet Utilization %"
  swapXY=true
  yFmt='#0.0"%"'
  colorPalette={['#cd4063']}
/>

---

## Daily Ridership by Depot

Ridership distribution during COVID did not simply mirror fleet size. Nigadi led despite low own-fleet utilization because it had 182 hired buses providing peri-urban Pune coverage. Balewadi, running only its 83 PMPML-owned buses with zero hired vehicles, had the lowest ridership.

<BarChart
  data={covid_by_depot}
  x=Depot
  y=Ridership_Daily
  title="Daily Ridership by Depot — FY 2020-21"
  subtitle="Sorted by ridership descending"
  yAxisTitle="Daily Passengers"
  swapXY=true
  yFmt='#,##0'
/>

---

## Own vs. Hired Buses On Road

System-wide, hired buses were 26% of all vehicles on road — far lower than their 65%+ share in FY 2023-24. Balewadi and Swargate operated with zero hired vehicles during this period.

<BarChart
  data={covid_fleet_stack}
  x=Depot
  y={['Own_On_Road', 'Hire_On_Road', 'Idle_Buses']}
  type=stacked
  title="Fleet Composition by Depot — FY 2020-21"
  subtitle="Own on road, Hired on road, and total idle (held but not deployed)"
  yAxisTitle="Buses"
  swapXY=true
  yFmt='#,##0'
/>

---

## Schedule Adherence

Schedules sanctioned but not operated reflect both reduced demand and COVID-era service disruptions. Most depots operated close to their (already reduced) sanctions.

<BarChart
  data={covid_schedule}
  x=Depot
  y={['Total_Schedules_Sanctioned', 'Total_Schedules_Operated']}
  type=grouped
  title="Schedules Sanctioned vs. Operated — FY 2020-21"
  yAxisTitle="Schedules per Day"
  swapXY=true
  yFmt='#,##0'
/>

---

## Full Depot Data

<DataTable
  data={covid_full_table}
  rows=all
>
  <Column id=Depot title="Depot"/>
  <Column id=Total_Buses_Held title="Buses Held" fmt='#,##0'/>
  <Column id=Total_On_Road title="On Road" fmt='#,##0'/>
  <Column id=utilization_pct title="Utilization %" fmt='#0.0"%"'/>
  <Column id=Ridership_Daily title="Ridership/Day" fmt='#,##0'/>
  <Column id=Revenue_Daily title="Revenue/Day (₹)" fmt='#,##0'/>
  <Column id=Total_Schedules_Sanctioned title="Sanctioned" fmt='#,##0'/>
  <Column id=Total_Schedules_Operated title="Operated" fmt='#,##0'/>
</DataTable>

---

## See Also

- **[Annual Performance Report](/PCMC/Public%20Transport/Annual_Statistics)** — FY 2023-24 vs 2024-25: the post-COVID recovery baseline
- **[Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Monthly depot data from Jan 2023–Dec 2025
- **[PCMT Before PMPML](/PCMC/Public%20Transport/PCMT_before_PMPML)** — Pre-merger bus operations 1995-2007

---

*Source: [PMPML Annual Statistical Report FY 2020-2021](https://pmpml.org/statistics). Covers 13 depots active at the time. Baner, Charholi, Maan, and Wagholi depots were not included. "Upper Depot" is listed as "Marketyard" in the source document.*

---

## Data Queries

```sql covid_headline
SELECT
    SUM(Total_On_Road) as total_on_road,
    ROUND(100.0 * SUM(Total_On_Road) / NULLIF(SUM(Total_Buses_Held), 0), 1) as fleet_utilization_pct,
    SUM(Ridership_Daily) as daily_ridership,
    ROUND(SUM(Revenue_Daily) / 100000.0, 1) as daily_revenue_lakh
FROM Depot_Stats_COVID_2020_2021
```

```sql covid_by_depot
SELECT
    Depot,
    Total_Buses_Held,
    Total_On_Road,
    ROUND(100.0 * Total_On_Road / NULLIF(Total_Buses_Held, 0), 1) as utilization_pct,
    Total_Schedules_Sanctioned,
    Total_Schedules_Operated,
    Ridership_Daily,
    Revenue_Daily
FROM Depot_Stats_COVID_2020_2021
ORDER BY Ridership_Daily DESC
```

```sql covid_fleet_stack
SELECT
    Depot,
    PMPML_On_Road as Own_On_Road,
    Hire_On_Road,
    (Total_Buses_Held - Total_On_Road) as Idle_Buses
FROM Depot_Stats_COVID_2020_2021
ORDER BY Total_On_Road DESC
```

```sql covid_schedule
SELECT
    Depot,
    Total_Schedules_Sanctioned,
    Total_Schedules_Operated
FROM Depot_Stats_COVID_2020_2021
ORDER BY Total_Schedules_Sanctioned DESC
```

```sql covid_full_table
SELECT
    Depot,
    Total_Buses_Held,
    Total_On_Road,
    ROUND(100.0 * Total_On_Road / NULLIF(Total_Buses_Held, 0), 1) as utilization_pct,
    Ridership_Daily,
    Revenue_Daily,
    Total_Schedules_Sanctioned,
    Total_Schedules_Operated
FROM Depot_Stats_COVID_2020_2021
ORDER BY Ridership_Daily DESC
```
