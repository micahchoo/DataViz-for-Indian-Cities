---
title: Traffic Chokepoints across Pune Metro 2021
description: Traffic intensity mapped across different spots in the Pune metropolitan region including PCMC, PMC, and surrounding areas
---

The 2021 traffic survey covered 83 locations across the Pune metropolitan area as part of the Metro Rail DPR update. Unlike the [2008 PCMC-only survey](/PCMC/Traffic/Pimpri_Chinchwad_Traffic_at_Locations), this dataset includes locations across PMC, PCMC, and outlying areas.

The PCU/Vehicle ratio reveals the vehicle mix at each location - ratios above 1.0 indicate heavier vehicles (trucks, buses), while ratios below 0.85 indicate two-wheeler dominant traffic.




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
        WHEN ratio >= 0.92 AND ratio < 1.0 THEN 'Cars & two-wheelers mix'
        WHEN ratio >= 0.85 AND ratio < 0.92 THEN 'Two-wheeler dominant'
        ELSE 'High two-wheeler proportion'
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


## Sources
- [UPDATED DETAILED PROJECT REPORT(PCMC TO NIGDI –Corridor 1A)- 24/08/2021](https://www.punemetrorail.org/download/PCMC-Nigdi_Revised_updated.pdf)
