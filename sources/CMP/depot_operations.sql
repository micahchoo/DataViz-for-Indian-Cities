-- PMPML Data Transformation Script
-- This script converts the wide-format extracted.csv into normalized depot_operations table
-- Run this as a source query in Evidence: sources/CMP/transform_depot_data.sql

WITH normalized_data AS (
    SELECT 
        -- Parse date properly
        TRY_CAST(Date AS DATE) as date,
        
        -- Normalize depot names (remove line breaks and standardize)
        CASE 
            WHEN REPLACE(REPLACE(Particulars, '\n', ''), ' ', '') LIKE '%UpperDepot%' 
                THEN 'Upper Depot'
            WHEN REPLACE(REPLACE(Particulars, '\n', ''), ' ', '') LIKE '%PuneStation%' 
                THEN 'Pune Station'
            WHEN REPLACE(REPLACE(Particulars, '\n', ''), '-', '') LIKE '%Bhekrai%' 
                THEN 'Bhekrainagar'
            WHEN REPLACE(REPLACE(Particulars, '\n', ''), '-', '') LIKE '%Shewal%' 
                THEN 'Shewalwadi'
            ELSE TRIM(REPLACE(Particulars, '\n', ' '))
        END as depot,
        
        -- Fleet Metrics
        TRY_CAST("Avg. Vehicles Held - Per Day PMPML" AS INTEGER) as vehicles_held_pmpml,
        TRY_CAST("Total Avg.Veh- On Road Per Day" AS INTEGER) as vehicles_on_road,
        TRY_CAST("Total Vehicles Off Road Per Day" AS INTEGER) as vehicles_off_road,
        TRY_CAST("Avg.Workshop Vehicles Per Day" AS INTEGER) as vehicles_in_workshop,
        TRY_CAST("% of Fleet Utilization(PMPML+PPP)" AS DOUBLE) as fleet_utilization_pct,
        
        -- Distance Metrics
        TRY_CAST("Total Eff.Km (Own+Hire)" AS BIGINT) as total_effective_km,
        TRY_CAST("Effective Km Per Bus Per day" AS DOUBLE) as km_per_bus,
        TRY_CAST("Total Cancelled KMs" AS INTEGER) as cancelled_kms,
        
        -- Revenue Metrics
        TRY_CAST("Passenger Earning (Sale of Ticket)(₹)" AS BIGINT) as ticket_revenue,
        TRY_CAST("All Traffic Earning (₹)" AS BIGINT) as total_traffic_revenue,
        TRY_CAST("Earning Per Vehicle Per day in Rs." AS DOUBLE) as revenue_per_vehicle,
        TRY_CAST("Earning per KMs in Rs.(EPK) (₹)" AS DOUBLE) as revenue_per_km,
        TRY_CAST("Average daily earning in Rs." AS INTEGER) as daily_revenue,
        
        -- Passenger Metrics
        TRY_CAST("Avg. Passenger travel per day (On\nTicket Sale)" AS INTEGER) as daily_passengers,
        TRY_CAST("Passenger Per Bus Per day" AS INTEGER) as passengers_per_bus,
        TRY_CAST("Avg Passenger per day (Passes, CC,\nAaram Bus)" AS INTEGER) as pass_passengers_per_day,
        
        -- Safety Metrics
        TRY_CAST("Total no.of Breakdown (PMPML Own)" AS INTEGER) as breakdowns,
        TRY_CAST("No.of Accidents (PMPML) Total" AS INTEGER) as accidents_pmpml,
        TRY_CAST("No.of Accidents (HIRED) Total" AS INTEGER) as accidents_hired,
        TRY_CAST("Breakdown rate per 10,000 KMs" AS DOUBLE) as breakdown_rate_per_10k,
        
        -- Fuel Efficiency
        TRY_CAST("KMs per Litre of Diesel (KMPL)(Own)" AS DOUBLE) as diesel_efficiency_kmpl,
        TRY_CAST("KMs per Kg.of CNG (KMPG)(Own)" AS DOUBLE) as cng_efficiency_kmpg,
        TRY_CAST("Total KMPG (Own+PPP)" AS DOUBLE) as total_cng_efficiency,
        
        -- Fuel Consumption
        TRY_CAST("Total Diesel  (PMPML\nOwn+PPP)" AS INTEGER) as total_diesel_litres,
        TRY_CAST("Total CNG (PMPML Own+PPP)" AS INTEGER) as total_cng_kg,
        
        -- Load Factors
        TRY_CAST("% Load Factor on- 1. Sale of Tickets" AS DOUBLE) as load_factor_tickets_pct,
        
        -- Additional Metrics
        TRY_CAST("Total Number of Routes" AS INTEGER) as total_routes,
        TRY_CAST("Average Route Length in KMs" AS DOUBLE) as avg_route_length_km,
        TRY_CAST("Total no. of Passenger Complaints\nreceived (including Telephone)" AS INTEGER) as passenger_complaints
        
    FROM extracted
    WHERE Date IS NOT NULL 
        AND Particulars IS NOT NULL
        AND TRY_CAST(Date AS DATE) IS NOT NULL
)

SELECT *
FROM normalized_data
WHERE depot IS NOT NULL
ORDER BY date DESC, depot;