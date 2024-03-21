-- Calculate lifespan and list bands with Glam rock as their main style, ranked by longevity

SELECT  band_name,(ifnull(split,2020) - ifnull(formed,0)) lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC 
