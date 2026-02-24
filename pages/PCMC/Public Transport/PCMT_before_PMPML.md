---
title: The Story of Pimpri-Chinchwad's Bus Fleet Before PMPML
description: The Comprehensive Mobility Plan (CMP) from 2008 gives us a fascinating glimpse into Pimpri Chinchwad Municipal Transport's (PCMT) operations right during a major transition.
---
Looking at the data visualization below, we can trace PCMT's journey from 1995 to 2007 — a story of collapse and recovery, not steady progress.

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

On 15 October 2007, a significant change occurred - PCMT merged with Pune Municipal Transport (PMT) to form Pune Mahanagar Parivahan Mahamandal Ltd (PMPML). This merger aimed to eliminate route overlaps and improve financial performance.

The transformation of PMPML's fleet size over the years tells an interesting story:
- 2010: 1,454 buses operating on 271 routes
- 2012: 1,745 buses (including 327 hired from private operators) serving 12.3 lakh daily passengers
- 2014: Fleet size of 1,523 with 1,198 buses on the road (78.66% Fleet Utilisation)
- 2015: Fleet size of 2,100
- 2023-24: Fleet size of 2,066 with 1,658 on road daily (74.4% fleet utilization), serving 8,34,764 daily passengers on ticket sales and 12,07,737 total daily traffic. 387 routes averaging 21.2 KM each. _(Source: PMPML Yearly Statistical Report 2023-25)_
- 2024-25: Fleet size of 1,933 with 1,558 on road daily (71.0% fleet utilization), serving 7,70,353 daily passengers on ticket sales and 11,25,440 total daily traffic. 382 routes averaging 21.8 KM each. _(Source: PMPML Yearly Statistical Report 2023-25)_

Note: Some secondary sources report different figures for this period — the ITDP Report 2024 cites a fleet of 1,880 with 85.2% utilization, and the PMPML website previously showed 3,87,000 daily passengers for 2023. These discrepancies likely reflect different reporting dates, definitions (e.g. utilization calculated as on-road/held vs. the weighted metric in PMPML's statistical reports), or the difference between ticket-only and total traffic counts.

## Gaps in Understanding

What's particularly intriguing is the gap in data between 2008 and 2010. The CMP captured PCMT's final years, but we don't have granular data about the immediate post-merger period. This leaves several questions unanswered about how the transition was managed and how quickly the integrated service scaled up.
Recently, there is more data about daily bus breakdown rates but that is also patchy. We would need year-by-year data between 2008-2024 to truly understand how the merged entity evolved and whether it achieved its goals of better coordination and improved service delivery. The available snapshots show growth in fleet size, but the full story of service quality, route optimization, and operational efficiency remains to be told.
PMPML has been publishing statistical reports every month but the historical data is not available

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
