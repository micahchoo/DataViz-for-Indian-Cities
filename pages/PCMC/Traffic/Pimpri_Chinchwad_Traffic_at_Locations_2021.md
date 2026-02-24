---
title: Traffic Volume Survey across Pune Metro 2021
description: Traffic volume and vehicle mix measured at 82 locations across the Pune metropolitan region including PCMC, PMC, and surrounding areas
---

The 2021 traffic survey measured vehicle volumes at 82 locations across the Pune metropolitan area as part of the Metro Rail DPR update. Unlike the [2008 PCMC-only survey](/PCMC/Traffic/Pimpri_Chinchwad_Traffic_at_Locations), this dataset includes locations across PMC, PCMC, and outlying areas. Note: these are volume counts at survey points, not congestion metrics — a high-volume road may still flow freely if it has sufficient capacity.

The PCU/Vehicle ratio reveals the vehicle mix at each location. PCU (Passenger Car Unit) normalizes different vehicle types to a common unit (car=1, two-wheeler≈0.5, bus≈3). Ratios above 1.0 indicate heavier vehicles (trucks, buses) are prevalent, while ratios below 0.85 indicate two-wheeler dominant traffic.




```sql traffic_locations
select 
    location_detail as pointName,
    latitude as lat,
    longitude as long,
    Passenger_Car_Units as PCUs,
    total_vehicles as vehicles,
    ratio as ratio,
    CASE 
        WHEN ratio >= 1.1 THEN 'Heavy vehicle corridor (trucks & buses dominant)'
        WHEN ratio >= 1.0 AND ratio < 1.1 THEN 'Cars & heavy vehicles mix'
        WHEN ratio >= 0.92 AND ratio < 1.0 THEN 'Balanced mix (cars & two-wheelers)'
        WHEN ratio >= 0.85 AND ratio < 0.92 THEN 'Two-wheeler leaning'
        ELSE 'Heavily two-wheeler (>60% likely)'
    END as ratio_interpretation
from Pimpri_Chinchwad_Traffic_at_Locations_2021
```




<PointMap
data={traffic_locations}
basemap={`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`}
attribution= '© OpenStreetMap © OpenStreetMap contributors © Carto '
lat=lat
long=long
startingLat=18.6142011464405
startingLong=73.8070402184475
value=vehicles
pointName=pointName
valueFmt="#,##0"
title="Vehicle Traffic Volume at Key Locations in 2021"
tooltipType=hover
tooltip={[
{id: 'pointName', showColumnName: false, valueClass: 'text-l font-semibold'},
{id: 'vehicles', title: 'Total Vehicles', fmt: 'num0'},
{id: 'PCUs', title: 'Passenger Car Units', fmt: 'num0'},
{id: 'ratio', title: 'PCU/Vehicle Ratio', fmt: '0.00'},
{id: 'ratio_interpretation', title: 'Vehicle Mix', showColumnName: false, valueClass: 'text-sm text-gray-600 italic'}
]}
size=15
opacity=0.7
height=900
legendPosition=topLeft
startingZoom=12
borderColor=#00000000
selectedBorderColor=#00ffff
legend=true
/>


## Comparing 2008 and 2021

Four locations from the [2008 PCMC traffic survey](/PCMC/Traffic/Pimpri_Chinchwad_Traffic_at_Locations) can be matched to nearby 2021 survey points (within 500m). The results suggest traffic redistribution rather than uniform growth.

```sql comparison_2008_2021
WITH matches AS (
    SELECT * FROM (VALUES
        ('Dapodi Bridge', 'V1', 'SL41'),
        ('Harris Bridge (Bopodi)', 'V15', 'SL53'),
        ('Aundh Bridge', 'V2', 'SL50'),
        ('Nashik Phata', 'V5', 'SL39')
    ) AS t(location, loc_2008, loc_2021)
)
SELECT
    m.location,
    t08.total_vehicles as vehicles_2008,
    t21.total_vehicles as vehicles_2021,
    ROUND((t21.total_vehicles - t08.total_vehicles) * 100.0 / t08.total_vehicles, 0) as change_pct
FROM matches m
JOIN Pimpri_Chinchwad_Traffic_at_Locations t08 ON t08.location_no = m.loc_2008
JOIN Pimpri_Chinchwad_Traffic_at_Locations_2021 t21 ON t21.location_no = m.loc_2021
ORDER BY change_pct
```

<DataTable data={comparison_2008_2021} rows=all/>

Dapodi Bridge's 58% drop is striking — NH-4 traffic has likely redistributed to parallel routes including the adjacent Harris Bridge (+265%) and the wider Aundh-Ravet corridor (+31%). Nashik Phata's +65% growth reflects the general traffic increase in PCMC's developing northern corridor.

---

*Data from the 2021 Traffic and Transportation Study for Pune Metropolitan Region, covering 82 locations across PCMC, PMC, and surrounding areas. Source: PMPML/PMRDA Traffic Study 2021.*

## See Also

- **[2008 Traffic Survey](/PCMC/Traffic/Pimpri_Chinchwad_Traffic_at_Locations)** — 15-location PCMC baseline, 13 years before this survey
- **[Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018)** — The growing vehicle fleet that generated this traffic
- **[Traffic Section Overview](/PCMC/Traffic)** — Both surveys in context

## Sources
- [UPDATED DETAILED PROJECT REPORT(PCMC TO NIGDI –Corridor 1A)- 24/08/2021](https://www.punemetrorail.org/download/PCMC-Nigdi_Revised_updated.pdf)

## Data Queries
