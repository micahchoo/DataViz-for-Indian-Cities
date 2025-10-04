```sql wards_list
SELECT 
    json_extract_string(feature, '$.properties.wardnum')::INTEGER as wardnum,
    json_extract_string(feature, '$.properties.name') as name,
    json_extract_string(feature, '$.properties.zone') as zone,
    1 as dummy_value
FROM (
    SELECT unnest(features) as feature
    FROM read_json('pcmc.geojson', format='auto')
)
```
<AreaMap 
    data={wards_list} 
    areaCol=wardnum
    geoJsonUrl="/pcmc.geojson"
    basemap={`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`}
    attribution= '© OpenStreetMap © OpenStreetMap contributors © Carto '
    geoId=wardnum
    value=dummy_value
    height=600
    title="PCMC Ward Boundaries"
/>
