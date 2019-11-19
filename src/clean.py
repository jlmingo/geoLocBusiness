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

#Dropping rows with null coordinates

drop_rows = df[((df.latitude.isnull() == True) | (df.longitude.isnull() == True))].index
df.drop(drop_rows, inplace=True)

df.to_csv("../output/master_dafaFrame.csv")

#Creating DataFrame with Tech companies, >$1m raised
df_tech = df[(df["Tech/Other"] == "Tech") & (df["total_money_raised"] >= 1000000)]
df_tech.to_csv("./output/tech_dafaFrame.csv")

#Creating DataFrame with old companies < 2009
df_old = df[df["founded_year"]<=2009]
df_old.to_csv("./output/old_dafaFrame.csv")