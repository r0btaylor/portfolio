-- This script contains examples of SQL queries

-- 1.) Return the date/time, station name and the highest recorded value of nitrogen oxide (NOx) found in the dataset for the year 2019

-- Aggregate function in subselect 
SELECT `readings`.`DateTime`,`sites`.`Location`, `readings`.`NOx`
FROM `readings`
JOIN `sites` ON `readings`.`SiteID`=`sites`.`SiteID`
WHERE YEAR(`readings`.`DateTime`)='2019'
AND `readings`.`NOx` = (SELECT MAX(`NOx`) FROM `readings` WHERE YEAR(`readings`.`DateTime`)='2019');
-- 2019-01-24   09:00:00    Colston Avenue 1403.5

-- Order by with limit
SELECT `readings`.`DateTime`,`sites`.`Location`, `readings`.`NOx` 
FROM `readings`
JOIN `sites` ON `readings`.`SiteID`=`sites`.`SiteID`
WHERE YEAR(`readings`.`DateTime`)='2019'
ORDER BY `readings`.`NOx` DESC
LIMIT 1;
-- 2019-01-24   09:00:00    Colston Avenue 1403.5


-- 2.)  Return the mean values of PM2.5 (particulate matter <2.5 micron diameter) & VPM2.5 (volatile particulate matter <2.5 micron diameter) by each station for the year 2019 for readings taken on or near 08:00 hours (peak traffic intensity)

-- with nulls untouched, ignored in calculations
SELECT AVG(`readings`.`PM2.5`),AVG(`readings`.`VPM2.5`), `readings`.`SiteID`,`sites`.`Location` 
FROM `readings` 
JOIN `sites` ON `readings`.`SiteID`=`sites`.`SiteID` 
WHERE YEAR(`DateTime`)='2019' AND HOUR(`DateTime`) = '08.00'
GROUP BY `sites`.`Location`;

-- 10.963870994506344		452	AURN St Pauls
-- 		                    203	Brislington Depot
-- 		                    501	Colston Avenue
-- 		                    463	Fishponds Road
-- 11.870881795883179		215	Parson Street School
-- 		                    500	Temple Way
-- 		                    270	Wells Road

-- nulls replaced with 0 used in calculations
SELECT AVG(IFNULL(`PM2.5`,0)),AVG(IFNULL(`VPM2.5`,0)),`readings`.`SiteID`,`sites`.`Location`
FROM `readings` 
JOIN `sites` ON `readings`.`SiteID`=`sites`.`SiteID`
WHERE YEAR(`DateTime`)='2019' AND HOUR(`DateTime`)='08:00'
GROUP BY `sites`.`Location`

-- 9.311780844649224	0	452	AURN St Pauls
-- 0	                0	203	Brislington Depot
-- 0	                0	501	Colston Avenue
-- 0	                0	463	Fishponds Road
-- 1.7887630103385612	0	215	Parson Street School
-- 0	                0	500	Temple Way
-- 0	                0	270	Wells Road

-- 3.) Previous query extended to show values for all stations in the years 2010 to 2019

-- with nulls untocuhed, ignored in calculations
SELECT AVG(`readings`.`PM2.5`),AVG(`readings`.`VPM2.5`), `readings`.`SiteID`,`sites`.`Location` 
FROM `readings` 
JOIN `sites` ON `readings`.`SiteID`=`sites`.`SiteID` 
WHERE YEAR(`DateTime`) BETWEEN '2010' AND '2019' AND HOUR(`DateTime`) = '08.00'
GROUP BY `sites`.`Location`;

-- 12.462487524489651	2.9587650798430376	452	AURN St Pauls
-- 		                                    447	Bath Road
-- 		                                    203	Brislington Depot
-- 		                                    459	Cheltenham Road \ Station Road
-- 		                                    501	Colston Avenue
-- 		                                    481	CREATE Centre Roof
-- 		                                    463	Fishponds Road
-- 		                                    375	Newfoundland Road Police Station
-- 		                                    213	Old Market
-- 11.870881795883179		                215	Parson Street School
-- 		                                    206	Rupert Street
-- 		                                    395	Shiner's Garage
-- 		                                    500	Temple Way
-- 		                                    270	Wells Road

-- null replaced with 0, included in calculations
SELECT AVG(IFNULL(`PM2.5`,0)),AVG(IFNULL(`VPM2.5`,0)),`readings`.`SiteID`,`sites`.`Location`
FROM `readings` 
JOIN `sites` ON `readings`.`SiteID`=`sites`.`SiteID`
WHERE YEAR(`DateTime`) BETWEEN '2010' AND '2019' AND HOUR(`DateTime`) = '08.00'
GROUP BY `sites`.`Location`

-- 10.67433214036244	2.283077764238138	452	AURN St Pauls
-- 0	                0	                447	Bath Road
-- 0	                0	                203	Brislington Depot
-- 0	                0	                459	Cheltenham Road \ Station Road
-- 0	                0	                501	Colston Avenue
-- 0	                0	                481	CREATE Centre Roof
-- 0	                0	                463	Fishponds Road
-- 0	                0	                375	Newfoundland Road Police Station
-- 0	                0	                213	Old Market
-- 0.17877834029944548	0	                215	Parson Street School
-- 0	                0	                206	Rupert Street
-- 0	                0	                395	Shiner's Garage
-- 0	                0	                500	Temple Way
-- 0	                0	                270	Wells Road
