```sql wards_list
select * from pcmc
order by wardnum
```

<DataTable data={wards_list} rows=20/>


<AreaMap 
 data={wards_list}
 areaCol=name
 geoJsonUrl=https://raw.githubusercontent.com/micahchoo/DataViz-for-Indian-Cities/refs/heads/master/pcmc.geojson
 geoId=name
 value=dummy
 title="PCMC Wards by Zone"
 height=600
/>