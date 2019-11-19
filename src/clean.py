from pymongo import MongoClient
import pandas as pd
import re

#Import MongoDB collection and create DataFrame

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies','companies')

pipeline = [
    { "$unwind": "$offices"},    
 ]

results = list(coll.aggregate(pipeline))
df = pd.DataFrame(results)

#Drop deadpooled companies

df = df[df.deadpooled_year.isnull()]
df.reset_index(inplace=True, drop= True)

#Unwind Office column
df = pd.concat([df.drop(['offices'], axis=1), df['offices'].apply(pd.Series)], axis=1)

#Re-classifying categories into Tech/Other
tech = ["web", "games_video", "mobile", "social", "photo_video", "network_hosting", "software", "ecommerce", "hardware", "semiconductor", "analytics", "biotech", "cleantech", "nanotech"]
df["Tech/Other"] = df["category_code"].apply(lambda x: "Tech" if x in tech else "Other")

