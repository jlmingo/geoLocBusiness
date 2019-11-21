import pandas as pd
from functions import getLoc

df = pd.read_csv("../Input/store-locations/directory.csv")
df.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}, inplace=True)
df["geoJSON"] = df.apply(lambda x: getLoc(x.longitude, x.latitude), axis=1)
df.drop(df[(df.longitude.isnull() == True) | (df.latitude.isnull() == True)].index, inplace=True)
df.to_json("../Input/starbucks.json", orient='records')")
print("starbucks.json exported successfully
