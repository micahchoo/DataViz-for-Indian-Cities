---
title: Pimpri-Chinchwad Overview
description: Pimpri-Chinchwad Municipal Corporation — city context, ward map, and data coverage
---

Pimpri-Chinchwad is the industrial twin city of Pune, home to major automobile and manufacturing plants (Tata Motors, Bajaj Auto, Force Motors) that have shaped its growth trajectory since the 1960s. The city grew from a population of 10.06 lakh (Census 2001) to 17.28 lakh (Census 2011), driven by industrial employment and spillover from Pune's expanding IT sector.

The municipal corporation is organized into 6 administrative zones (A through F), covering 181 sq km with 32 electoral wards. The zones run roughly north-south: Zone A (Nigdi-Akurdi) and Zone B (Pimpri-Chinchwad core) form the industrial heartland, while Zones E and F (Wakad, Moshi) represent newer residential expansion areas.

## Ward Map

```sql wards_list
select * from pcmc
order by wardnum
```

<AreaMap
 data={wards_list}
 areaCol=name
 geoJsonUrl=https://raw.githubusercontent.com/micahchoo/DataViz-for-Indian-Cities/refs/heads/master/static/pcmcg.geojson
 geoId=name
 value=zone
 title="PCMC Wards by Zone"
 height=600
 opacity=0.5
 borderWidth=1
 legend=true
 tooltip={[
    {id: 'zone', title: 'Ward Zone'},
    {id: 'wardnum', title: 'Ward Number'}
]}
/>

<DataTable data={wards_list} rows=20/>

## Data Coverage

| Dataset | Period | Granularity | Source |
|---------|--------|-------------|--------|
| Vehicle Registrations | 2000-2018 | Annual, by vehicle type | Open City Urban Data Portal |
| Road Accident Statistics | 2000-2007 | Annual | PCMC CMP 2008 |
| PCMT Bus Fleet | 1995-2007 | Annual | PCMC CMP 2008 |
| PMPML Depot Reports | Jan 2023 - Jun 2025 | Monthly, per depot | PMPML Chief Statistician |
| Traffic Volumes (PCMC) | 2008 | 15 locations | PCMC CMP 2008 |
| Traffic Volumes (Metro) | 2021 | 82 locations | Pune Metro DPR |

Taken together, these datasets span 70 years of planning and operations — but with uneven coverage. The strongest continuous record is the PMPML monthly data from 2023 onward. The longest gap is 2007–2022, PMPML's formative 15 years. Readers who see findings from different time periods on the same page should consult the source notes — the data periods do not overlap.

## Explore

- **[City Growth Context](/PCMC/City_Context)** — Population, urban expansion, land use, and CMP 2008 transport demand projections
- **[Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018)** — What vehicles are on PCMC's roads: cumulative RTO data by type
- **[Fleet Composition Trends](/PCMC/Fleet_Composition_Trends)** — Growth rates, market share shifts, and indexed comparisons across vehicle categories
- **[Pune vs PCMC Vehicles](/PCMC/Pune_PCMC_Comparison)** — How PCMC's registered fleet compares to Pune's across 18 years
- **[Road Safety](/PCMC/Road_Accident_Statistics)** — Accident severity trends and per-vehicle fatality rates
- **[Public Transport](/PCMC/Public%20Transport)** — From PCMT's 248 buses in 1995 to PMPML's 2,000+ fleet today
- **[Traffic Surveys](/PCMC/Traffic)** — How vehicle volumes shifted between 2008 and 2021

*Sources: Ward boundary data from PCMC GIS. Population from Census 2001 (10.06 lakh) and Census 2011 (17.28 lakh).*
