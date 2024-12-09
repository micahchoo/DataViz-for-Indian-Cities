# The Story of Pimpri-Chinchwad's Bus Fleet Before PMPML

The Comprehensive Mobility Plan (CMP) from 2008 gives us a fascinating glimpse into Pimpri Chinchwad Municipal Transport's (PCMT) operations right before a major transition. Looking at the data visualization above, we can trace PCMT's journey from 1995 to 2007 - a period marked by both challenges and resilience.

The most striking aspect is how PCMT managed its fleet efficiency. In 1995-96, with 248 buses in total, they kept 158 on the road daily serving about 130,000 passengers. Fast forward to 2006-07, they were operating with a smaller fleet of 212 buses but maintained 160 buses on the road - a notable improvement in fleet utilization from 63.7% to 75.5%.

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
    ROUND(CAST("Buses on Road" AS FLOAT) / "No. of Buses" * 100, 1) as Fleet_Utilization_Rate
FROM Bus_Fleet_Statistics
ORDER BY Sort_Year
```


<LineChart
    data={Bus_Fleet_Statistics}
    x=Display_Year
    y=Active_Buses
    y2=Daily_Passengers
    y2SeriesType=bar
    yAxisTitle="Number of Buses / Passengers"
    title="Bus Fleet Performance Over Time"
    subtitle="Tracking fleet size, utilization and passenger volume"
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
/>

## The Merger and Birth of PMPML

On 15 October 2007, a significant change occurred - PCMT merged with Pune Municipal Transport (PMT) to form Pune Mahanagar Parivahan Mahamandal Ltd (PMPML). This merger aimed to eliminate route overlaps and improve financial performance.

The transformation of PMPML's fleet size over the years tells an interesting story:
- 2010: 1,454 buses operating on 271 routes
- 2012: 1,745 buses (including 327 hired from private operators) serving 12.3 lakh daily passengers
- 2014: Fleet size of 1,523 with 1,198 buses on the road (78.66% Fleet Utilisation)
- 2015: Fleet size of 2,100 
- 2023: Fleet size of 2,066 with 1,658 buses in actual utilization (77.27% Fleet Utilisation) serving 387
- 2024: Fleet size of 1,880 with 1,602 buses in actual utilization (77.27% Fleet Utilisation) serving 11,47,702 Daily Passengers

## Gaps in Understanding

What's particularly intriguing is the gap in data between 2008 and 2010. The CMP captured PCMT's final years, but we don't have granular data about the immediate post-merger period. This leaves several questions unanswered about how the transition was managed and how quickly the integrated service scaled up.
Recently, there is more data about daily bus breakdown rates but that is also patchy

## Sources
- [PCMC CMP 2008](https://www.pcmcindia.gov.in/admin/cms_upload/submission/2388046091386320509.pdf)
- [PMC BRTS System Report 2010](https://www.pmc.gov.in/informpdf/BRTS/System_Spec_Report.pdf)
- [PMC City Development Plan 2012](https://www.pmc.gov.in/sites/default/files/project-glimpses/City_Development_Plan_Executive_Summary.pdf)
- [ITDP Report 2024](https://itdp.org/wp-content/uploads/2024/04/Pimpri-Chinchwad-Citys-Data-Driven-Approach_Shekhar-Singh.pdf)
- [PMC okays PMPML de-merger](https://punemirror.com/pune/cover-story/pmc-okays-pmpml-de-merger/cid5102540.htm)
- [Team PMPML gets specific tasks](https://timesofindia.indiatimes.com/city/pune/team-pmpml-gets-specific-tasks/articleshow/45846248.cms)
- [PMPML website](https://pmpml.org/statistics)

We would need year-by-year data between 2008-2024 to truly understand how the merged entity evolved and whether it achieved its goals of better coordination and improved service delivery. The available snapshots show growth in fleet size, but the full story of service quality, route optimization, and operational efficiency remains to be told.
PMPML has been publishing statistical reports every month but the historical data is not available