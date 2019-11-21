import pandas as pd
import re
import geopandas as gpd
from functions import connectCollection, getLocation, df_to_gdf, moneyRaise

# Import MongoDB collection and create DataFrame


def main():
    db, coll = connectCollection('companies', 'companies')

    pipeline = [
        {"$unwind": "$offices"},
    ]

    results = list(coll.aggregate(pipeline))
    df = pd.DataFrame(results)
    print("Collection imported succesfully, DataFrame Generated")

    # Drop deadpooled companies

    df = df[df.deadpooled_year.isnull()]
    df.reset_index(inplace=True, drop=True)

    # Unwind Office column
    df = pd.concat([df.drop(['offices'], axis=1),
                    df['offices'].apply(pd.Series)], axis=1)

    # Re-classifying categories into Tech/Other
    tech = ["web", "games_video", "mobile", "social", "photo_video", "network_hosting", "software",
            "ecommerce", "hardware", "semiconductor", "analytics", "biotech", "cleantech", "nanotech"]
    df["Tech/Other"] = df["category_code"].apply(
        lambda x: "Tech" if x in tech else "Other")

    # Cleaning and fixing column of money raised
    df.total_money_raised = df.total_money_raised.apply(moneyRaise)

    # Dropping columns with null longitude or latitude
    drop_rows = df[((df.latitude.isnull() == True) |
                    (df.longitude.isnull() == True))].index
    df.drop(drop_rows, inplace=True)

    # Exporting DataFrame
    df.to_csv("../Input/clean_df_companies.csv")
    print("Cleaned DataFrame successfully exported to csv")

    # Importing airports geoDataFrame
    gdf_airports = gpd.read_file(
        "../Input/ne_10m_airports/ne_10m_airports.shp")
    print("Airports shp file imported.")

    gdf_airports["geoJSON"] = gdf_airports.geometry.apply(
        lambda x: getLocation(x))
    gdf_airports = gdf_airports.loc[:, ["name", "geometry", "geoJSON"]]

    # Exporting airports to JSON
    df_airports = pd.DataFrame(gdf_airports)
    df_airports.drop(df_airports.columns[1], axis=1, inplace=True)
    df_airports.to_json("airports.json", orient='records')
    print("Airports JSON file generated.")


if __name__ == "__main__":
    main()
