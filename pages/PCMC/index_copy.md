---
title: Test
---

```sql wards_list
select * from pcmc
order by wardnum
```

<DataTable data={wards_list} rows=20/>

# Static Files bug
<AreaMap 
 data={wards_list}
 areaCol=name
 geoJsonUrl="/pcmcg.geojson"
 geoId=name
 value=zone
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

<Image 
    url="/wordmark-gray-800.png"
    description="Sample placeholder image"
    height=80
/>

# Legend Bug
<AreaMap 
 data={wards_list}
 areaCol=name
 geoJsonUrl=https://raw.githubusercontent.com/micahchoo/DataViz-for-Indian-Cities/refs/heads/master/static/pcmcg.geojson
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

<AreaMap 
 data={wards_list}
 areaCol=name
 geoJsonUrl=https://raw.githubusercontent.com/micahchoo/DataViz-for-Indian-Cities/refs/heads/master/static/pcmcg.geojson
 geoId=name
 value=wardnum
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