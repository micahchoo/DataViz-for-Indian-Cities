---
title: DataViz for Indian Cities
description: Urban mobility data for Pimpri-Chinchwad — vehicles, buses, traffic, and road safety from 2000 to 2025
---

Pimpri-Chinchwad grew from 10 lakh residents in 2001 to over 17 lakh by 2011, making it one of India's fastest-growing urban areas. As the city expanded, its transport infrastructure — buses, roads, vehicle registrations — strained to keep pace. This project visualizes that story through public data. Private vehicle ownership multiplied nearly 9-fold between 2000 and 2018, crossing one registered vehicle per person by 2017-18. Over the same period, bus ridership per capita declined. This site documents that divergence — through vehicle registration records, bus ridership data, traffic surveys, and financial accounts spanning 2000 to 2025.

Narrative pages (City Context, Vehicle Registrations, Financial Performance) argue a point and can be read start to finish. Dashboard pages (Depotwise Reports, Traffic Surveys) let you filter and explore. Both draw from the same underlying data.

## Pimpri-Chinchwad

- **[City Overview](/PCMC)** — Ward map, zone structure, and data coverage
- **[City Growth Context](/PCMC/City_Context)** — Population, urban expansion, land use, and CMP 2008 transport demand projections
- **[Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018)** — Cumulative RTO registrations by type, 2000-2018
- **[Fleet Composition Trends](/PCMC/Fleet_Composition_Trends)** — Growth rates, market share shifts, and indexed comparisons
- **[Road Safety](/PCMC/Road_Accident_Statistics)** — Accident trends 2000-2007 and PMPML bus safety 2023-2025

### Public Transport
- **[Overview](/PCMC/Public%20Transport)** — Three eras of bus transit: PCMT, the merger, and PMPML today
- **[PCMT Before PMPML](/PCMC/Public%20Transport/PCMT_before_PMPML)** — Bus fleet operations 1995-2007
- **[PMPML Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Monthly fleet data across 17 depots, 2023-2025
- **[Depot Performance](/PCMC/Public%20Transport/Depot_Performance)** — Efficiency, fleet composition, and ridership by depot
- **[Ridership and Fares](/PCMC/Public%20Transport/Ridership_and_Fares)** — Pass types, fare tiers, and revenue mix
- **[BRT Corridor Demand](/PCMC/Public%20Transport/BRT_Corridors)** — CMP 2008 projections vs 2021 reality, with proposed route map
- **[COVID-Era Operations](/PCMC/Public%20Transport/COVID_Era)** — FY 2020-21: fleet utilization collapsed to 32%, ridership at 2.83 lakh/day
- **[Annual Performance Report](/PCMC/Public%20Transport/Annual_Statistics)** — FY 2023-24 vs 2024-25: fuel efficiency by propulsion type, accidents, workshop data

### Traffic
- **[Overview](/PCMC/Traffic)** — Traffic volume surveys in 2008 and 2021
- **[2008 Traffic Survey](/PCMC/Traffic/Pimpri_Chinchwad_Traffic_at_Locations)** — 15 locations across PCMC
- **[2021 Traffic Survey](/PCMC/Traffic/Pimpri_Chinchwad_Traffic_at_Locations_2021)** — 82 locations across Pune metro

---

## About

Built with [Evidence](https://docs.evidence.dev/) for data visualization and static site generation. Tables extracted from PDF reports using [gmft](https://github.com/conjuncts/gmft) ([extraction scripts](https://github.com/micahchoo/Jenga-Block-Archiving-Tools/tree/main/Extract%20tables%20from%20PDFs)), cleaned with [RKward](https://github.com/KDE/rkward). Data sourced from PCMC's Comprehensive Mobility Plan (2008), Open City Urban Data Portal, PMPML monthly statistical reports, and Pune Metro DPR traffic surveys. Open to data submissions from other Indian cities.
