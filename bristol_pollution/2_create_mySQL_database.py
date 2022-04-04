# This scripts accepts cleaned csv file ('clean.csv')
# A mySQL database of 3 entities is created:
        # sites - holds site ID, location and geospatial coordinates
        # readings - holds all reading data
        # schema - holds defnitions of each metric recorded
# Accruate metadeta is created fro each entity before population from .csv file

import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Float, Boolean, ForeignKey, REAL, exc
from sqlalchemy_utils import database_exists, drop_database, create_database

try:       
        #create engine and connect to DB
        dbaddress= "mysql://root:@127.0.0.1:3306/polution"
        engine = create_engine(dbaddress)

        #drop any existing database
        if database_exists(dbaddress):
                drop_database(dbaddress)
        create_database(dbaddress)

        #create tables and define
        metadata_obj=MetaData()
        sites = Table("sites", metadata_obj,
                Column("SiteID",Integer, primary_key=True, nullable=False,autoincrement=False,unique=True,index=True),
                Column("Location",String(48)),
                Column("geo_point_2d", String(150)),
                )
        readings = Table("readings", metadata_obj,
                Column("ReadingID", Integer, primary_key=True,nullable=False,autoincrement=True,unique=True,index=True),
                Column("DateTime", DateTime),
                Column("NOx",Float),
                Column("NO2",Float),
                Column("NO",Float),
                Column("SiteID", Integer, ForeignKey("sites.SiteID"),nullable=False, index=True),
                Column("PM10",Float),
                Column("NVPM10",Float),
                Column("VPM10",Float,),
                Column("NVPM2.5",Float),
                Column("PM2.5",Float),
                Column("VPM2.5",Float),
                Column("CO",Float),
                Column("O3",Float),
                Column("SO2",Float),
                Column("Temperature",REAL),
                Column("RH",Integer),
                Column("AirPressure",Integer),
                Column("DateStart",DateTime),
                Column("DateEnd",DateTime),
                Column("Current",Boolean),
                Column("InstrumentType",String(45)),
                )
        reference = Table("schema", metadata_obj,
                Column("Measure",String(45), primary_key=True,nullable=False,index=True),
                Column("Description",String(150)),
                Column("Unit", String(10)),
                )
        metadata_obj.create_all(engine)

        #read in csv 
        df = pd.read_csv("clean.csv", sep=",",low_memory=False)

        #set sites df
        dfsites=df[["SiteID", "Location", "geo_point_2d"]].drop_duplicates()

        #set readings df
        dfreadings=df[["DateTime","NOx","NO2","NO","PM10","NVPM10","VPM10","NVPM2.5","PM2.5","VPM2.5","CO","O3","SO2","Temperature","RH",
        "AirPressure","InstrumentType","DateStart","DateEnd","Current","SiteID"]]

        #create definitions dictionary
        schema = {"measure":  ["DateTime","NOx","NO2","NO","SiteID","PM10","NVPM10","VPM10","NVPM2.5","PM2.5","VPM2.5","CO","O3","SO2","Temperature",
        "RH","AirPressure","Location","geo_point_2d","DateStart","DateEnd","Current","InstrumentType"],
        "description": ["Date and time of measurement","Concentration of oxides of nitrogen","Concentration of nitrogen dioxide",
        "Concentration of nitric oxide","Site ID for the station","Concentration of particulate matter <10 micron diameter",
        "Concentration of non - volatile particulate matter <10 micron diameter","Concentration of volatile particulate matter <10 micron diameter",
        "Concentration of non volatile particulate matter <2.5 micron diameter","Concentration of particulate matter <2.5 micron diameter",
        "Concentration of volatile particulate matter <2.5 micron diameter","Concentration of carbon monoxide","Concentration of ozone",
        "Concentration of sulphur dioxide","Air temperature","Relative Humidity","Air Pressure","Text description of location","Latitude and longitude",
        "The date monitoring started","The date monitoring ended","Is the monitor currently operating","Classification of the instrument"],
        "unit": ["datetime","μg/m3","μg/m3","μg/m3","integer","μg/m3","μg/m3","μg/m3","μg/m3","μg/m3","μg/m3","μg/m3","μg/m3","μg/m3","°C","%","mbar","text",
        "geo point","datetime","datetime","text","text"]
                }
        #set reference df
        dfref=pd.DataFrame(schema)

        #push all data to database
        dfsites.to_sql(name="sites",con=engine,index=False,if_exists="append",chunksize=20000)
        dfreadings.to_sql(name="readings",con=engine,index=False,if_exists="append",chunksize=20000)
        dfref.to_sql(name="schema",con=engine,index=False,if_exists="append",chunksize=20000)

except exc.OperationalError:
        print("DataBase Error: There was a problem connecting to the database")
except FileNotFoundError:
        print("File Error: Check the file name and path are correct")
except:
        print("Error: Something went wrong")
