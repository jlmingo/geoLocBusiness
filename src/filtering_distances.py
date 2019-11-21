
import pandas as pd
from functions import connectCollection, searchNear
from clean import df

#Import airports and querying them

db, coll = connectCollection('companies','airports')

df["Closest_Airport"] = df.apply(lambda x: searchNear(x.longitude, x.latitude, coll, 20000), axis=1)
df["Closest_Airport"] = df.Closest_Airport.apply(lambda x: list(x))
df = df[df['Closest_Airport'].astype(bool)]

#Import airports and querying them
