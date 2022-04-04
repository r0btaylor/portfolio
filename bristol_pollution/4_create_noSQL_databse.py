# This scripts accepts cleaned csv file ('clean.csv')
# A noSQL database using mongoDB is created
# Database is structured using a single document with site information embedded as a nested doument in each reading
# Script currently instantites only a single site but line 27 can be removed for entire dataset

from pymongo import MongoClient, errors, GEOSPHERE
import pandas as pd
from geopandas import geopandas, GeoDataFrame
import shapely

try:
    #create client instance
    client = MongoClient('mongodb://localhost:27017/')

    #drop db if exists
    client.drop_database("pollution")

    #Create db and collections
    db=client["pollution"]
    readings=db["readings"]

    #read csv & rename columns to remove decimal in names
    df = pd.read_csv("clean.csv", sep=",",low_memory=False,parse_dates=['DateTime','DateEnd','DateStart'])
    df.rename(columns={'NVPM2.5':'NVPM2_5', 'PM2.5':'PM2_5','VPM2.5':'VPM2_5'}, inplace=True)

    #Filter for specific site
    df = df.loc[(df["SiteID"] == 452)]

    #Check for missing datetime values (NaN type), convert to None type to avoid insert errors
    df["DateTime"] = df["DateTime"].astype(object).where(df["DateTime"].notnull(), None)
    df["DateStart"] = df["DateStart"].astype(object).where(df["DateStart"].notnull(), None)
    df["DateEnd"] = df["DateEnd"].astype(object).where(df["DateEnd"].notnull(), None)

    #set relevant dataframes
    readings_df = df.loc[:,~df.columns.isin(["SiteID","Location","geo_point_2d"])]
    sites_df = df[["SiteID","Location"]]

    #split geo_point_2d column into lon and lat, set as df_geo
    geo = df["geo_point_2d"].str.split(",",expand=True)

    #create geospatial object from coordinates and combine with sites_df
    geo_df = GeoDataFrame(sites_df,geometry=geopandas.points_from_xy(geo[1],geo[0]))
    #rename columns correctly
    geo_df.columns = ["SiteID", "Location","geo_point_2d"]
    #use lambda function to convert shapely point to GeoJson object
    geo_df["geo_point_2d"]=geo_df["geo_point_2d"].apply(lambda x:shapely.geometry.mapping(x))

    #convert dataframes into dictionaries
    readings_dict = readings_df.to_dict("records")
    sites_dict = geo_df.to_dict("records")
    
    #embed site info as nested dictionary in each readings dictionary
    index = 0
    for n in readings_dict:
        n["Site"] = sites_dict[index] 
        index+=1

    #insert all to db
    readings.insert_many(readings_dict)

    #set SiteID as index
    readings.create_index("Site.SiteID") 
    readings.create_index([("Site.geo_point_2d",GEOSPHERE)])   

except errors.ConnectionFailure:
    print("DataBase Connection Error: There was a problem connecting to the database")
except errors.OperationFailure:
    print("DataBase Operation Error: A datatbase operation has failed")
except FileNotFoundError:
        print("File Error: Check the file name and path are correct")
except:
        print("Error: Something went wrong")