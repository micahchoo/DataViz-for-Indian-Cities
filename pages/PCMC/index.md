---
title: PCMC Ward Map
description: Pimpri-Chinchwad Municipal Corporation wards organized by administrative zones (A-F)
---

```sql wards_list
select * from pcmc
order by wardnum
```

<DataTable data={wards_list} rows=20/>


<AreaMap
 data={wards_list}
 areaCol=name
 geoJsonUrl=https://raw.githubusercontent.com/micahchoo/DataViz-for-Indian-Cities/refs/heads/master/static/pcmcg.geojson
 geoId=name
 value=zone
 title="PCMC Wards by Zone"
 height=600
 opacity=0.5
 borderWidth=1
 legend=true
 tooltip={[
    {id: 'zone', title: 'Ward Zone'},
    {id: 'wardnum', title: 'Ward Number'}
]}
/>
