---
title: Traffic Chokepoints across PCMC 2008
description: The 2008 traffic survey across Pimpri Chinchwad revealed significant variations in traffic patterns across 15 key locations. Here are the main insights
---
The 2008 traffic survey across Pimpri Chinchwad revealed significant variations in traffic patterns across 15 key locations. Here are the main insights:

### High Traffic Corridors
Dapodi Bridge emerged as the busiest corridor with 120,527 vehicles daily, also handling the highest passenger volume (466,672 passengers)
Aundh Bridge recorded the second-highest traffic with 87,087 vehicles and 413,078 passengers
Between Pimpri Junction & Kasarwadi Junction saw 79,216 vehicles, highlighting its importance as a major transit point

### Moderate Traffic Areas
The Mumbai-Pune Expressway point recorded 28,935 vehicles
Nashik Highway before the toll plaza showed moderate vehicle count (41,495) but significant passenger movement (149,451)
The corridor Between Nigdi Junction & Chinchwad Junction handled 66,439 vehicles

### Lower Traffic Zones
Dehu-Alandi Road showed the lowest traffic volumes with 9,228 vehicles
The connection from Nigdi Junction to Dehu-Alandi Road recorded 12,595 vehicles
These areas primarily serve local traffic rather than major transit routes

### Passenger-to-Vehicle Ratio Analysis
Major highways and bridges show higher passenger-to-vehicle ratios, indicating greater use of public transport and shared vehicles
Dapodi Bridge shows approximately 3.87 passengers per vehicle
Local roads show lower ratios, suggesting more private vehicle usage



```sql traffic_locations
select 
    location_detail as pointName,
    latitude as lat,
    longitude as long,
    total_passengers as passengers,
    total_vehicles as vehicles,
    -- Category aggregations
    four_wheelers as cars,
    (two_wheelers + cycles) as motorcycles,
    auto_rickshaws as autos,
    (minibuses + local_buses + intercity_buses) as total_buses
from Pimpri_Chinchwad_Traffic_at_Locations
```




<PointMap
data={traffic_locations}
basemap={`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`}
attribution= '© OpenStreetMap © OpenStreetMap contributors © Carto '
lat=lat
long=long
value=vehicles
pointName=pointName
valueFmt="#,##0"
title="Vehicle Traffic Volume at Key Locations in 2008"
tooltipType=hover
tooltip={[
{id: 'pointName', showColumnName: false, valueClass: 'text-l font-semibold'},
{id: 'cars', title: '4-Wheelers', fmt: 'num0'},
{id: 'motorcycles', title: '2-Wheelers', fmt: 'num0'},
{id: 'autos', title: 'Auto Rickshaws', fmt: 'num0'},
{id: 'total_buses', title: 'Buses', fmt: 'num0'},
{id: 'vehicles', title: 'Total Vehicles', fmt: 'num0'},
{id: 'passengers', title: 'Total Passengers', fmt: 'num0'}
]}
size=15
opacity=0.6
height=900
legend=false
legendPosition=topLeft
startingZoom=12
borderColor=#00000000
selectedBorderColor=#00ffff
/>


## Sources
- [PCMC CMP 2008](https://www.pcmcindia.gov.in/admin/cms_upload/submission/2388046091386320509.pdf)
