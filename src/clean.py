import pandas as pd
import re
import geopandas as gpd
from src.functions import connectCollection, getLocation, df_to_gdf

#Import MongoDB collection and create DataFrame

db, coll = connectCollection('companies','companies')

pipeline = [
    { "$unwind": "$offices"},    
 ]

results = list(coll.aggregate(pipeline))
df = pd.DataFrame(results)
print("Collection imported succesfully, DataFrame Generated")
#Drop deadpooled companies

df = df[df.deadpooled_year.isnull()]
df.reset_index(inplace=True, drop= True)

#Unwind Office column
df = pd.concat([df.drop(['offices'], axis=1), df['offices'].apply(pd.Series)], axis=1)

#Re-classifying categories into Tech/Other
tech = ["web", "games_video", "mobile", "social", "photo_video", "network_hosting", "software", "ecommerce", "hardware", "semiconductor", "analytics", "biotech", "cleantech", "nanotech"]
df["Tech/Other"] = df["category_code"].apply(lambda x: "Tech" if x in tech else "Other")

#Clean money raised column

def moneyRaise(value):
    dicc_coin = {'CAD': 0.76,'RUB': 0.016, 'EUR': 1.11, 'GBP': 1.29}
    values_money = {'K':1000, 'M':1000000, 'B': 100000000000}
    value_number = float(re.search('[+-]?([0-9]*[.])?[0-9]+', value)[0])
    if value.endswith('B'):
        exchange = value_number*(values_money['B'])
    elif value.endswith('K[k]'):
        exchange = value_number*(values_money['K'])
    elif value.endswith('M'):
        exchange = value_number*(values_money['M'])
    elif value.startswith("C"):
        exchange =  value_number*(dicc_coin['CAD'])
    elif value.startswith("$"):
        exchange =  value_number
    elif value.startswith("€"):
        exchange = value_number*(dicc_coin['EUR'])
    elif value.startswith("£"):
        exchange = value_number*(dicc_coin['GBP'])
    elif value.startswith("r"):
        exchange = value_number*(dicc_coin['RUB'])
    else:
        exchange = value_number
    return int(exchange)

df.total_money_raised = df.total_money_raised.apply(moneyRaise)

drop_rows = df[((df.latitude.isnull() == True) | (df.longitude.isnull() == True))].index
df.drop(drop_rows, inplace=True)
df.to_csv("../Input/clean_df_companies.csv")
print("Cleaned DataFrame successfully exported to csv")

#Importing airports geoDataFrame

gdf_airports = gpd.read_file("../Input/ne_10m_airports/ne_10m_airports.shp")
print("Airports shp file imported.")

gdf_master = df_to_gdf(df)

gdf_airports["geoJSON"] = gdf_airports.geometry.apply(lambda x: getLocation(x))
gdf_airports = gdf_airports.loc[:,["name", "geometry", "geoJSON"]]

#Exporting to JSON
df_master = pd.DataFrame(gdf_master)
df_airports = pd.DataFrame(gdf_airports)
df_airports.drop(df_airports.columns[1], axis=1, inplace=True)
df_airports.to_json("airports.json", orient='records')
print("JSON file generated.")
