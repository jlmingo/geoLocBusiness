
import pandas as pd
from functions import connectCollection, searchNear


def main():
    df_filtered = pd.read_csv("../input/clean_df_companies.csv")

    # Import airports and querying them

    db, airports = connectCollection('companies', 'airports')

    df_filtered["Closest_Airport"] = df_filtered.apply(lambda x: searchNear(
        x.longitude, x.latitude, airports, 30000), axis=1)
    df_filtered["Closest_Airport"] = df_filtered.Closest_Airport.apply(
        lambda x: list(x))
    df_filtered = df_filtered[df_filtered['Closest_Airport'].astype(bool)]

    # Import old companies around

    db, oldcos = connectCollection('companies', 'oldCos')

    df_filtered["Closest_oldCo"] = df_filtered.apply(lambda x: searchNear(
        x.longitude, x.latitude, oldcos, 2000), axis=1)
    df_filtered["Closest_oldCo"] = df_filtered.Closest_oldCo.apply(
        lambda x: list(x))
    df_filtered = df_filtered[df_filtered['Closest_oldCo'].astype(
        bool) == False]

    db, oldcos = connectCollection('companies', 'oldCos')

    df_filtered["Closest_oldCo"] = df_filtered.apply(lambda x: searchNear(
        x.longitude, x.latitude, oldcos, 2000), axis=1)
    df_filtered["Closest_oldCo"] = df_filtered.Closest_oldCo.apply(
        lambda x: list(x))
    df_filtered = df_filtered[df_filtered['Closest_oldCo'].astype(
        bool) == False]


if __name__ = "__main__":
    main()
