---
title: Public Transport in Pimpri-Chinchwad
description: Three eras of bus transit — PCMT standalone operations, the 2007 merger, and PMPML today
---

Pimpri-Chinchwad's public bus system has passed through three distinct eras, each with its own operational character and challenges.

## PCMT: The Standalone Years (1995-2007)

Pimpri Chinchwad Municipal Transport (PCMT) operated as an independent city bus service from the mid-1990s. Starting with 248 buses serving 1.31 lakh daily passengers in 1995-96, the system suffered a sharp decline — by 2001-02, daily ridership had crashed 58% to just 54,684. A genuine recovery followed: by 2006-07, PCMT had rebuilt ridership to 1.08 lakh daily passengers with fewer buses (212 vs 248), achieving better productivity through higher utilization.

**[Read the full PCMT story](/PCMC/Public%20Transport/PCMT_before_PMPML)**

## The 2007 Merger

On 15 October 2007, PCMT merged with Pune Municipal Transport (PMT) to form Pune Mahanagar Parivahan Mahamandal Ltd (PMPML). The merger aimed to eliminate route overlaps between the twin cities and consolidate operations under a single entity serving the entire Pune metropolitan area.

## PMPML Today (2023-2025)

```sql summary_metrics
SELECT
    COUNT(DISTINCT Date) as total_months,
    COUNT(DISTINCT Depot) as total_depots,
    ROUND(SUM(TRY_CAST("All Traffic Earning (₹)" AS DOUBLE)) / 10000000, 2) as total_revenue_crores,
    ROUND(AVG(LEAST(TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE), 100.0)), 1) as avg_fleet_utilization_pct
FROM extracted
WHERE Date IS NOT NULL
```

<Grid cols=4>
<BigValue
  data={summary_metrics}
  value=total_months
  title="Months of Data"
/>

<BigValue
  data={summary_metrics}
  value=total_depots
  title="Depots"
/>

<BigValue
  data={summary_metrics}
  value=total_revenue_crores
  title="Total Revenue (₹ Cr)"
  fmt='"₹"#,##0.00" Cr"'
/>

<BigValue
  data={summary_metrics}
  value=avg_fleet_utilization_pct
  title="Avg Fleet Utilization"
  fmt='#0.0"%"'
/>
</Grid>

PMPML now operates across 17 depots with a fleet of ~2,000 buses. Monthly depot-level data from January 2023 to June 2025 (with some coverage gaps) provides granular insight into fleet operations, revenue, ridership, and safety.

- **[Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Monthly fleet dashboard: vehicle deployment, kilometers, revenue, fuel efficiency, safety, and depot comparisons
- **[Depot Performance](/PCMC/Public%20Transport/Depot_Performance)** — How depots compare on efficiency, schedule adherence, fleet ownership, and revenue patterns
- **[Ridership and Fares](/PCMC/Public%20Transport/Ridership_and_Fares)** — Pass types, fare tiers, student ridership, and the shifting revenue mix
- **[BRT Service Statistics](/PCMC/Public%20Transport/BRT)** — Dedicated B.R.T. corridor operations: fleet, ridership, and efficiency across 15–17 depots
- **[BRT Corridor Demand](/PCMC/Public%20Transport/BRT_Corridors)** — CMP 2008 projections vs 2021 observed corridor traffic, with proposed route map
- **[COVID-Era Operations](/PCMC/Public%20Transport/COVID_Era)** — FY 2020-21: 32% fleet utilization, 2.83 lakh daily passengers, 13-depot breakdown
- **[Annual Performance Report](/PCMC/Public%20Transport/Annual_Statistics)** — FY 2023-24 vs FY 2024-25: fleet, ridership, revenue, fuel efficiency by propulsion type, safety, workshop
- **[E-Bus Service Statistics](/PCMC/Public%20Transport/EBus)** — Electric bus operations at dedicated depots, including KMPU energy efficiency tracking

---

*Data covers Jan 2023 – Jun 2025 with gaps (Jan–Mar 2024, Nov 2024–Mar 2025 missing). Source: PMPML Chief Statistician monthly reports.*
