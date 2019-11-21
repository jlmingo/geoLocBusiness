
import pandas as pd
from functions import connectCollection, searchNear


def main():
    df_filtered = pd.read_csv("../input/clean_df_companies.csv")

    # Import airports around
    db, airports = connectCollection('companies', 'airports')

    df_filtered["Closest_Airport"] = df_filtered.apply(lambda x: searchNear(
        x.longitude, x.latitude, airports, 40000), axis=1)
    df_filtered = df_filtered[df_filtered['Closest_Airport'].astype(bool)]

    # Import old companies around
    db, oldcos = connectCollection('companies', 'oldCos')

    df_filtered["Closest_oldCo"] = df_filtered.apply(lambda x: searchNear(
        x.longitude, x.latitude, oldcos, 300), axis=1)
    df_filtered = df_filtered[df_filtered['Closest_oldCo'].astype(
        bool) == False]

    # Import Starbucks around
    db, starbucks = connectCollection('companies', 'starbucks')

    df_filtered["Closest_Starbucks"] = df_filtered.apply(lambda x: searchNear(
        x.longitude, x.latitude, starbucks, 1000), axis=1)
    df_filtered = df_filtered[df_filtered['Closest_Starbucks'].astype(
        bool)]

    # Import Tech Companies with >$1m raised around
    db, techCos = connectCollection('companies', 'techCos')

    df_filtered["Closest_techCo"] = df_filtered.apply(lambda x: searchNearWithoutLimit(
        x.longitude, x.latitude, techCos, 400), axis=1)
    df_filtered = df_filtered[df_filtered['Closest_techCo'].astype(
        bool)]
    df_filtered.reset_index(inplace=True, drop=True)
    df_filtered.to_csv("../input/df_fileter")


if __name__ == "__main__":
    main()
