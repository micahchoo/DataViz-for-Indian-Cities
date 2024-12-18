---
title: Traffic Chokepoints across Pune 2021
---




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
basemap={`https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.{ext}`}
attribution='© CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | © <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> © <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
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
{id: 'pointName', showColumnName: false, valueClass: 'text-xl font-semibold'},
{id: 'vehicles', title: 'Total Vehicles', fmt: 'num0'},
{id: 'PCUs', title: 'Passenger Car Units', fmt: 'num0'},
{id: 'ratio', title: 'PCU/Vehicle Ratio', fmt: '0.00'},
{id: 'ratio_interpretation', title: 'Vehicle Mix', showColumnName: false, valueClass: 'text-sm text-gray-600 italic'}
]}
colorPalette={['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026']}
size=15
opacity=0.7
height=900
legendPosition=topLeft
startingZoom=12
/>


## Sources
- [UPDATED DETAILED PROJECT REPORT(PCMC TO NIGDI –Corridor 1A)- 24/08/2021](https://www.punemetrorail.org/download/PCMC-Nigdi_Revised_updated.pdf)