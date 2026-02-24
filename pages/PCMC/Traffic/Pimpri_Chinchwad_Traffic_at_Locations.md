---
title: Traffic Volume Survey across PCMC 2008
description: Traffic volumes measured at 15 locations across Pimpri-Chinchwad as part of the 2008 Comprehensive Mobility Plan
---
The 2008 CMP traffic survey measured daily vehicle volumes at 15 locations across Pimpri-Chinchwad. This data predates the 2021 metro-wide survey by 13 years and covers only PCMC (not PMC).

### Key Patterns

**NH-4 corridor dominates**: Dapodi Bridge (1,20,527 vehicles, 4,66,672 passengers) and the parallel Bopodi bridge (46,540 vehicles) together carried the heaviest traffic, serving as the primary north-south connector between PCMC and Pune. The 3.87 passengers-per-vehicle ratio at Dapodi — compared to ~1.3 on local roads — reflects the heavy bus and shared-vehicle traffic on this arterial.

**Two-wheeler dominance on internal roads**: Locations like KSB Chowk–NH-50 (28,096 two-wheelers out of 51,843 vehicles = 54%) and Kalewadi–Dange Chowk (19,183 of 37,266 = 51%) show how internal PCMC roads were overwhelmingly two-wheeler territory in 2008, consistent with the [vehicle registration data](/PCMC/Registered_Vehicles_2000_2018) showing two-wheelers as ~70% of the fleet.

**Expressway is car-heavy**: The Mumbai-Pune Expressway point (21,784 four-wheelers out of 28,935 = 75%) has a completely different vehicle mix from the rest of PCMC — very few two-wheelers or autos, reflecting its limited-access design.

**Sparse northern periphery**: Dehu-Alandi Road (9,228 vehicles) and Nigdi–Dehu connector (12,595) show the low-density northern edge of PCMC in 2008 — areas that have since seen significant development.



```sql traffic_locations
select 
    location_detail as pointName,
    latitude as lat,
    longitude as long,
    total_passengers as passengers,
    total_vehicles as vehicles,
    -- Category aggregations
    four_wheelers as cars,
    two_wheelers as two_wheelers,
    cycles as cycles,
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
{id: 'two_wheelers', title: '2-Wheelers', fmt: 'num0'},
{id: 'cycles', title: 'Cycles', fmt: 'num0'},
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


## Aggregate Mode Share

```sql mode_share
SELECT 'Two-Wheelers' as mode, SUM(two_wheelers) as vehicles,
    ROUND(SUM(two_wheelers) * 100.0 / NULLIF(SUM(total_vehicles), 0), 1) as share_pct,
    ROUND(SUM(total_passengers) * 1.0 / NULLIF(SUM(total_vehicles), 0), 2) as pax_per_vehicle
FROM Pimpri_Chinchwad_Traffic_at_Locations
UNION ALL
SELECT 'Four-Wheelers', SUM(four_wheelers),
    ROUND(SUM(four_wheelers) * 100.0 / NULLIF(SUM(total_vehicles), 0), 1), null
FROM Pimpri_Chinchwad_Traffic_at_Locations
UNION ALL
SELECT 'Auto Rickshaws', SUM(auto_rickshaws),
    ROUND(SUM(auto_rickshaws) * 100.0 / NULLIF(SUM(total_vehicles), 0), 1), null
FROM Pimpri_Chinchwad_Traffic_at_Locations
UNION ALL
SELECT 'Buses', SUM(minibuses + local_buses + intercity_buses),
    ROUND(SUM(minibuses + local_buses + intercity_buses) * 100.0 / NULLIF(SUM(total_vehicles), 0), 1), null
FROM Pimpri_Chinchwad_Traffic_at_Locations
UNION ALL
SELECT 'Cycles', SUM(cycles),
    ROUND(SUM(cycles) * 100.0 / NULLIF(SUM(total_vehicles), 0), 1), null
FROM Pimpri_Chinchwad_Traffic_at_Locations
ORDER BY vehicles DESC
```

<BarChart
    data={mode_share}
    x=mode
    y=share_pct
    swapXY=true
    title="Vehicle Mode Share Across All 15 Locations"
    subtitle="Two-wheelers dominate at 43%, followed by four-wheelers at 31%"
    yAxisTitle="Share of Total Vehicles (%)"
/>

Across all 15 survey points, the overall passengers-per-vehicle ratio was 2.97 — meaning each vehicle carried about 3 people on average. But this varies enormously: the Mumbai-Pune Expressway averaged just 3.0 (cars with drivers), while Aundh Bridge hit 4.74 (heavy bus traffic inflating the ratio). Buses made up only 6% of vehicles but carried a disproportionate share of passengers.

## See Also

- **[Vehicle Registrations](/PCMC/Registered_Vehicles_2000_2018)** — The vehicle fleet growth behind these traffic volumes

## Sources
- [PCMC CMP 2008](https://www.pcmcindia.gov.in/admin/cms_upload/submission/2388046091386320509.pdf)

## Data Queries
