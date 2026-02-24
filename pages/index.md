---
title: DataViz for Indian Cities
description: Urban mobility data for Pimpri-Chinchwad — vehicles, buses, traffic, and road safety from 2000 to 2025
---

Pimpri-Chinchwad grew from 10 lakh residents in 2001 to over 17 lakh by 2011, making it one of India's fastest-growing urban areas. As the city expanded, its transport infrastructure — buses, roads, vehicle registrations — strained to keep pace. This project visualizes that story through public data. Private vehicle ownership multiplied nearly 9-fold between 2000 and 2018, crossing one registered vehicle per person by 2017-18. Over the same period, bus ridership per capita declined. This site documents that divergence — through vehicle registration records, bus ridership data, traffic surveys, and financial accounts spanning 2000 to 2025.

Narrative pages (City Context, Vehicle Registrations, Financial Performance) argue a point and can be read start to finish. Dashboard pages (Depotwise Reports, Traffic Surveys) let you filter and explore. Both draw from the same underlying data.

## Pimpri-Chinchwad

- **[City Overview](/PCMC)** — Ward map, zone structure, and data coverage
- **[City Growth Context](/PCMC/City_Context)** — Population, land use, and the 2008 CMP transport projections — and how reality diverged from them
- **[Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018)** — 2.38 lakh to 21.27 lakh in 18 years: who registered what, and when the composition shifted
- **[Fleet Composition Trends](/PCMC/Fleet_Composition_Trends)** — Despite 18 years of growth, two-wheelers still dominate at 70%: the fleet that didn't diversify
- **[Pune vs PCMC Vehicles](/PCMC/Pune_PCMC_Comparison)** — PCMC's fleet grew from a fifth the size of Pune's to nearly 40% — category by category
- **[Road Safety](/PCMC/Road_Accident_Statistics)** — Per-vehicle fatality rates fell as the fleet grew, but absolute deaths rose: the safety paradox of rapid motorization

### Public Transport
- **[Overview](/PCMC/Public%20Transport)** — Three eras of bus transit: PCMT's decline, the 2007 merger, and PMPML today
- **[PCMT Before PMPML](/PCMC/Public%20Transport/PCMT_before_PMPML)** — A 58% ridership crash by 2001-02 and a genuine recovery — what the pre-merger data shows
- **[PMPML Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Monthly fleet data across 17 depots, 2023-2025: explore and filter
- **[Depot Performance](/PCMC/Public%20Transport/Depot_Performance)** — Three structural depot clusters: why 0% utilization doesn't mean a depot is broken
- **[Ridership and Fares](/PCMC/Public%20Transport/Ridership_and_Fares)** — Ticket revenue declining, pass revenue growing: how the revenue mix is shifting
- **[Financial Performance](/PCMC/Public%20Transport/Financial_Performance)** — Employee costs at 140% of fare revenue, PPE down 85%: the 8-year financial arc
- **[BRT Corridor Demand](/PCMC/Public%20Transport/BRT_Corridors)** — CMP 2008 projections vs 2021 reality, with proposed route map
- **[COVID-Era Operations](/PCMC/Public%20Transport/COVID_Era)** — FY 2020-21: fleet utilization collapsed to 32%, ridership at 2.83 lakh/day
- **[Annual Performance Report](/PCMC/Public%20Transport/Annual_Statistics)** — Ridership fell 7%, accidents nearly halved, e-bus efficiency up 24%: the two-year operational trajectory

### Traffic
- **[Overview](/PCMC/Traffic)** — Traffic volume surveys in 2008 and 2021
- **[2008 Traffic Survey](/PCMC/Traffic/Pimpri_Chinchwad_Traffic_at_Locations)** — 15 PCMC locations: the pre-BRT baseline
- **[2021 Traffic Survey](/PCMC/Traffic/Pimpri_Chinchwad_Traffic_at_Locations_2021)** — 82 metro locations: who grew, who shrank, and what the redistribution means

---

## Suggested Reading Path

For the full story in sequence: [City Context](/PCMC/City_Context) → [Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018) → [Public Transport Overview](/PCMC/Public%20Transport) → [PCMT Before PMPML](/PCMC/Public%20Transport/PCMT_before_PMPML) → [Financial Performance](/PCMC/Public%20Transport/Financial_Performance) → [Depot Performance](/PCMC/Public%20Transport/Depot_Performance). Each page adds a layer to the same argument: private vehicles multiplied while public transport strained to keep pace.

---

## About

Built with [Evidence](https://docs.evidence.dev/) for data visualization and static site generation. Tables extracted from PDF reports using [gmft](https://github.com/conjuncts/gmft) ([extraction scripts](https://github.com/micahchoo/Jenga-Block-Archiving-Tools/tree/main/Extract%20tables%20from%20PDFs)), cleaned with [RKward](https://github.com/KDE/rkward). Data sourced from PCMC's Comprehensive Mobility Plan (2008), Open City Urban Data Portal, PMPML monthly statistical reports, and Pune Metro DPR traffic surveys. Open to data submissions from other Indian cities.
