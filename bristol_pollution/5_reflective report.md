# <u>Task 6</u>
## <u>Reflective Report</u>

I initially completed Script 1 using Python's CSV module. My prototype code (Appendix A) used a loop with various conditional statements to achieve the crop and cleanse. Though successful, I also took the opportunity to experiment with Pandas. I preferred the compact nature of Pandas code and achieved the crop in only 2 lines:    
![](https://i.imgur.com/047skEB.png)    
To clean the file, I initially concatenated the SiteID and Location columns of the main dataframe and sites dictionary dataframe into single columns that could then be compared against each other. This was convoluted and so I refined the process by creating a filter mask by mapping SiteID to the relevant column in the sites dictionary:    
![](https://i.imgur.com/DwoXf2H.png)    
I utilised SQLAlchemy for Script 2 given its readable and succinct code. Tables and data types were defined prior to pushing data using the **to_sql()** method. I realise it is possible to pass the various names and dtypes as arguments to this method but I preferred to do so in advance as it enabled me to specify relationships in the same statement. For example:    
![](https://i.imgur.com/7MV8er1.png)    
Table specific dataframes were created and pushed to the database. I experimented with modifying chunk size and connection method but found no performance differences:    
![](https://i.imgur.com/P3Fm8cs.png)    
Some confusion was experienced when inserting sites data. The unique primary key caused an error when using the **if_exists="append"** argument. This was rectified by dropping duplicates from the dataframe. The same could be achieved using **if_exists="replace"** but dropping duplicates meant less data to insert.    

Initial queries of the database occurred without complication. I executed query 1 by sorting all NOx values into descending order then limiting to 1. This approach was used because of unexpected functioning of the MAX() function. I subsequently realised to place **MAX()** in a sub-selection for expected results:   
![Query A](https://i.imgur.com/b9yMNuz.png)  

**AVG()** function for query 2 and 3 raised an interesting issue. I noticed that, depending on whether I had used **dropna(0)** during database creation, my results would vary. The **AVG()** aggregate function calculated the values differently because NULL values are ignored in the calculation. I opted to leave NULL values to maintain flexibility in choosing how to manage NULL values according to use case. Defining NULL values as 0 at the point of implementation would have precluded this and would disguise which readings were NULL and which were actual zero. Replacing NULL in **AVG()** calculations was achieved using **IFNULL()**.     
![QueryB](https://i.imgur.com/yHIGaCi.png)    
I also noted that some sites did not appear in these calculations (i.e. IKEA M32). Further investigation revealed that these sites contained no data in the readings table for the given time frame.    

In Script 4, I took the time to ensure that geographical and datetime data were correctly imported to enable full functionality of the database. Geopandas dataframes can be merged with relevant shape files to enable geographic plotting through Geoplot. This would enable various readings metrics to be assigned to plot aesthetics, i.e. hue. Geographic scatter charts or heatmaps would be most appropriate given the scale of the geographic region depicted in the dataset. Iterating through readings according to datetime would enable the creation of sequential visualisations in Geoplot that could then be animated to create GIfs using Imageio. The following plot of NO2 levels in Bristol was created by piping the full dataset to Mongo Atlas in order to experiment with geospatial plotting:    
![](https://i.imgur.com/c0PzM8Q.png)    

## <u>Summary Reflections</u>   
Prior to this project, I had little to no experience using the tools involved. Despite this, I achieved success in all learning objectives as I successfully learned to use the required technologies. I demonstrated proficiency modelling, cleansing, normalising and implementing a SQL database with accurate referential integrity using Python scripts. I constructed and executed accurate SQL queries to extract data from that database and demonstrated my understanding through multiple approaches to these queries. A functioning NoSQL database was designed, implemented and populated using Python scripts and effective queries were constructed and executed upon it. Care was taken to ensure that data integrity was maintained so that more advanced query and plotting features could be used.

## <u>Appendices</u>
**Appendices A - Task 1a Prototype Code**    
![Prototype code 1](https://i.imgur.com/7xgYoQ7.png)   
![Prototype code 2](https://i.imgur.com/ajbOzVQ.png)    
**Appendices B - Task 1a Crop.py**    
![crop.py](https://i.imgur.com/KpE2jAq.png)    
**Appendices C - Task 1b Clean.py**    
![clean.py](https://i.imgur.com/Tc7Lla1.png)    
**Appendices D - Task 3a Populate.py**    
![populate.py 1](https://i.imgur.com/KtveWzj.png)    
![populate.py 2](https://i.imgur.com/gCTIrkO.png)    
**Appendices E - Task 3b Insert-100.py**     
![insert100](https://i.imgur.com/lD1zTwi.png)  
