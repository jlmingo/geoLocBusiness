from pymongo import MongoClient
import geopandas as gpd
import pandas as pd
import re


def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

# Function for creating GeoJSON column, input must be GeoDataFrame (geopandas required)


def getLocation(gdf):
    long = gdf.x
    lat = gdf.y
    loc = {
        'type': 'Point',
        'coordinates': [long, lat]
    }
    return loc


def getLoc(long, lat):
    loc = {
        'type': 'Point',
        'coordinates': [long, lat]
    }
    return loc

# Convert df in geoDataFrame


def df_to_gdf(dataframe):
    gdf = gpd.GeoDataFrame(dataframe, geometry=gpd.points_from_xy(
        dataframe.longitude, dataframe.latitude))
    gdf.crs = {'init': 'epsg:4326'}
    gdf.reset_index(drop=True, inplace=True)
    return gdf


def moneyRaise(value):
    ''' Clean money raised column'''
    dicc_coin = {'CAD': 0.76, 'RUB': 0.016, 'EUR': 1.11, 'GBP': 1.29}
    values_money = {'K': 1000, 'M': 1000000, 'B': 100000000000}
    value_number = float(re.search('[+-]?([0-9]*[.])?[0-9]+', value)[0])
    if value.endswith('B'):
        exchange = value_number*(values_money['B'])
    elif value.endswith('K[k]'):
        exchange = value_number*(values_money['K'])
    elif value.endswith('M'):
        exchange = value_number*(values_money['M'])
    elif value.startswith("C"):
        exchange = value_number*(dicc_coin['CAD'])
    elif value.startswith("$"):
        exchange = value_number
    elif value.startswith("€"):
        exchange = value_number*(dicc_coin['EUR'])
    elif value.startswith("£"):
        exchange = value_number*(dicc_coin['GBP'])
    elif value.startswith("r"):
        exchange = value_number*(dicc_coin['RUB'])
    else:
        exchange = value_number
    return int(exchange)

# Look for nearbyplaces


def searchNear(latitude, longitude, collection, maxDistance):
    result = collection.find(
        {"geoJSON":
         {"$near":
          {"$geometry": {"type": "Point",  "coordinates": [latitude, longitude]},
           "$maxDistance": maxDistance,
           }
          }
         }
    ).limit(1)
    return result if len(list(result)) > 0 else [0]
