---
title: Test
---

```sql wards_list
select * from pcmc
order by wardnum
```

<DataTable data={wards_list} rows=20/>


<AreaMap 
 data={wards_list}
 areaCol=name
 geoJsonUrl="/pcmcg.geojson"
 geoId=name
 value=wardnum
 title="PCMC Wards by Zone"
 height=600
 opacity=0.5
 borderWidth=1
 legend=false
 tooltip={[
    {id: 'zone', title: 'Ward Zone'},
    {id: 'wardnum', title: 'Ward Number'}
]}
/>