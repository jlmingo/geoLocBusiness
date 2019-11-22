import pandas as pd
import re
import geopandas as gpd
from functions import connectCollection, getLocation, df_to_gdf, moneyRaise

# Import MongoDB collection and create base cleaned DataFrame


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
    df.to_csv("../input/clean_df_companies.csv")
    print("Cleaned DataFrame successfully exported to csv")


if __name__ == "__main__":
    main()
