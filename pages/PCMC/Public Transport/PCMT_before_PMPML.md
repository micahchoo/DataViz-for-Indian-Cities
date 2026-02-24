---
title: The Story of Pimpri-Chinchwad's Bus Fleet Before PMPML
description: "PCMT 1995–2007: collapse and recovery in Pimpri-Chinchwad's bus system, from the CMP 2008 baseline data"
---
PCMC ran its own municipal bus service for over a decade before handing it to Pune — and what the data shows is not a smooth handover but a decade of collapse and partial recovery.

In 1995-96, PCMT operated 248 buses with 158 on the road daily, serving about 1,31,000 passengers — 829 passengers per bus, a strong productivity figure. But by 2001-02, the system had deteriorated sharply: daily passengers had crashed to just 54,684 (a 58% drop), passengers per bus halved to 452, only 121 of 239 buses were on the road, and utilization had fallen to 50.6%. The data gap between 1996 and 1999 hides the onset of this decline, but by 1999-2000 passengers had already halved to 60,727.

The recovery from this low point is the real story. Between 2002-03 and 2006-07, PCMT rebuilt ridership from 59,192 to 1,08,209 daily passengers while actually shrinking the total fleet from 239 to 212 buses — getting more from less. By 2006-07, 160 buses were on the road with 75.5% utilization, a genuine turnaround from the early-2000s nadir.

```sql Bus_Fleet_Statistics
SELECT
    CASE 
        WHEN Year LIKE '%-%' THEN SPLIT_PART(Year, '-', 1)  -- For years like "2006-07"
        WHEN Year LIKE 'Upto%' THEN '2007'                  -- For "Upto Oct 2007"
        ELSE Year 
    END as Sort_Year,
    Year as Display_Year,
    "No. of Buses" as Total_Fleet_Size,
    "Buses on Road" as Active_Buses,
    "Avg No. of Passengers / Day" as Daily_Passengers,
    ROUND(TRY_CAST("Buses on Road" AS DOUBLE) / "No. of Buses" * 100, 1) as Fleet_Utilization_Rate,
    ROUND(TRY_CAST("Avg No. of Passengers / Day" AS DOUBLE) / "Buses on Road", 0) as Passengers_Per_Bus
FROM Bus_Fleet_Statistics
ORDER BY Sort_Year
```


<LineChart
    data={Bus_Fleet_Statistics}
    x=Display_Year
    y=Active_Buses
    y2=Daily_Passengers
    y2SeriesType=bar
    yAxisTitle="Active Buses"
    y2AxisTitle="Avg Daily Passengers"
    title="Bus Fleet Performance Over Time"
    subtitle="Tracking active fleet (line) and daily passengers (bars)"
    sort=Sort_Year
/>

<LineChart
    data={Bus_Fleet_Statistics}
    x=Display_Year
    y=Fleet_Utilization_Rate
    sort=Sort_Year
    title="Fleet Utilization Rate"
    subtitle="Percentage of total fleet actively deployed on road"
    yAxisTitle="Utilization Rate (%)"
    connectGroup="fleet-metrics"
    baseline="40.0"
/>

<LineChart
    data={Bus_Fleet_Statistics}
    x=Display_Year
    y=Passengers_Per_Bus
    sort=Sort_Year
    title="Passengers Per Bus On Road"
    subtitle="From 829 in 1995-96 to 430 in 2000-01 — a productivity collapse, not just a ridership dip"
    yAxisTitle="Daily Passengers / Active Bus"
    connectGroup="fleet-metrics"
/>

## The Merger and Birth of PMPML

On 15 October 2007, PCMT merged with Pune Municipal Transport (PMT) to form Pune Mahanagar Parivahan Mahamandal Ltd (PMPML), aiming to eliminate route overlaps and consolidate operations under a single entity serving the entire Pune metropolitan area.

In the three years after the merger, the combined fleet grew from roughly 1,400 to nearly 1,750 vehicles — a 25% increase PCMT's declining finances could never have supported independently. By 2014, PMPML was running both cities' routes under unified ticketing, though the ex-PCMC depots retained their separate operational character, as the [depot-level data](/PCMC/Public%20Transport/Depot_Performance) makes clear.

By 2023-24, PMPML operated a fleet of 2,066 buses with 1,658 on the road daily (74.4% utilization), serving 12.08 lakh total daily passengers on 387 routes averaging 21.2 km. By 2024-25, the fleet had consolidated to 1,933 buses with 11.25 lakh daily passengers on 382 routes. _(Source: PMPML Yearly Statistical Report 2023-25)_

Note: Some secondary sources report different figures for this period — the ITDP Report 2024 cites a fleet of 1,880 with 85.2% utilization, and the PMPML website previously showed 3,87,000 daily passengers for 2023. These discrepancies likely reflect different reporting dates, definitions (e.g. utilization calculated as on-road/held vs. the weighted metric in PMPML's statistical reports), or the difference between ticket-only and total traffic counts.

## Data Limitations

PCMT's operational records for 1975–2007 have not been digitized or released publicly. The figures on this page are reconstructed from CMP 2008 summary tables — treat fleet-size numbers as approximate and ridership figures as CMP estimates rather than audited actuals. The 15-year gap between the 2007 merger and PMPML's monthly reports (beginning January 2023) reflects the limits of available public data, not of the city's history.

---

*Data from the 2008 Comprehensive Mobility Plan, Table on PCMT operations 1995-2007. Source: CMP 2008, PCMC Transport Department.*

## See Also

- **[PMPML Depotwise Reports](/PCMC/Public%20Transport/Depotwise)** — Current PMPML operations across 17 depots (2023-2025)
- **[Depot Performance](/PCMC/Public%20Transport/Depot_Performance)** — How today's depots compare on efficiency, ridership, and revenue

## Sources
- [PCMC CMP 2008](https://www.pcmcindia.gov.in/admin/cms_upload/submission/2388046091386320509.pdf)
- [PMC BRTS System Report 2010](https://www.pmc.gov.in/informpdf/BRTS/System_Spec_Report.pdf)
- [PMC City Development Plan 2012](https://www.pmc.gov.in/sites/default/files/project-glimpses/City_Development_Plan_Executive_Summary.pdf)
- [ITDP Report 2024](https://itdp.org/wp-content/uploads/2024/04/Pimpri-Chinchwad-Citys-Data-Driven-Approach_Shekhar-Singh.pdf)
- [PMC okays PMPML de-merger](https://punemirror.com/pune/cover-story/pmc-okays-pmpml-de-merger/cid5102540.htm)
- [Team PMPML gets specific tasks](https://timesofindia.indiatimes.com/city/pune/team-pmpml-gets-specific-tasks/articleshow/45846248.cms)
- [PMPML website](https://pmpml.org/statistics)
