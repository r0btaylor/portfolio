# This script accepts a large .csv as input ("bristol-air-quality-data.csv")
# The script then crops all entries >= 2010-01-01 00:00
# Monitoring site locations are checked against a dictionary of accurate site ID numbers
# Entries with inaccurate Site and Site IDs are removed
# Final data is output to 'clean.csv'

import pandas as pd

try:   
    #read the csv, store as df
    df = pd.read_csv("bristol-air-quality-data.csv", sep=";",low_memory=False)

    #filter for date target and send to new csv
    df = df.loc[(df["Date Time"] >= '2010-01-01 00:00')]

    #Create dictionary of siteIDs+locations
    dflocs = ({188:"AURN Bristol Centre",
                   203:"Brislington Depot",
                   206:"Rupert Street",
                   209:"IKEA M32",
                   213:"Old Market", 
                   215:"Parson Street School",
                   228:"Temple Meads Station",
                   270:"Wells Road",
                   271:"Trailer Portway P&R",
                   375:"Newfoundland Road Police Station",
                   395:"Shiner's Garage",
                   452:"AURN St Pauls",
                   447:"Bath Road",
                   459:"Cheltenham Road \ Station Road",
                   463:"Fishponds Road",
                   481:"CREATE Centre Roof",
                   500:"Temple Way",
                   501:"Colston Avenue"
                  })

    #Create filter to check matching SiteID&Locations
    IDfilt = df["Location"]==df.SiteID.map(dflocs)

    #Perform filter. Print line, siteID, location for filtered entries
    print(df.loc[(~IDfilt),("SiteID","Location")])
    df = df.loc[(IDfilt)]

    #rename columns to remove spaces from names
    df = df.rename(columns={"Date Time":"DateTime", "Air Pressure":"AirPressure", "Instrument Type":"InstrumentType"})

    #Send final clean entries to csv
    df.to_csv("clean.csv",index=False)

except FileNotFoundError:
    print("File Error: Check the file name and path are correct")
except:
    print("Error: Something went wrong")