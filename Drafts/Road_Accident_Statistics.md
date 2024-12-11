# Table Analysis
[Download CSV file](Road%20Accident%20Statistics.csv)
```sql accidents
-- First level: Years to Accident Types
select 
    Year || ' Total' as source,
    'Fatal Accidents' as target,
    cast("Fatal accidents" as int) as value
from road_accident_statistics

union all

select 
    Year || ' Total' as source,
    'Major Accidents' as target,
    cast("Major accidents" as int) as value
from road_accident_statistics

-- Second level: Accident Types to Outcomes
union all
select 
    'Fatal Accidents' as source,
    'Deaths' as target,
    sum(cast("Deaths" as int)) as value
from road_accident_statistics

union all
select 
    'Major Accidents' as source,
    'Injured Persons' as target,
    sum(cast("Injured persons" as int)) as value
from road_accident_statistics
```

<SankeyDiagram
    data={accidents}
    title="Road Accident Flow by Year (2000-2007)"
    subtitle="From yearly totals through accident types to casualties"
    sourceCol=source
    targetCol=target
    valueCol=value
    linkColor=gradient
    linkLabels=percent
    nodeAlign=justify
    height=500
    colorPalette={['#e88a87', '#eb5752', '#cf0d06', '#960906', '#6e0d06']}
/>