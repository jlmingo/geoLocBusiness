
import pandas as pd
from functions import connectCollection, searchNear, searchNearWithoutLimit


def main():
    df_filtered = pd.read_csv("../input/clean_df_companies.csv")
    print("clean_df_companies.csv successfully imported")
    # Import airports around
    db, airports = connectCollection('companies', 'airports')
    print("airports collection successfully loaded")

    df_filtered["Closest_Airport"] = df_filtered.apply(lambda x: searchNear(
        x.longitude, x.latitude, airports, 40000), axis=1)
    df_filtered = df_filtered[df_filtered['Closest_Airport'].astype(bool)]

    # Import old companies around
    db, oldcos = connectCollection('companies', 'oldCos')
    print("oldCos collection successfully loaded")

    df_filtered["Closest_oldCo"] = df_filtered.apply(lambda x: searchNear(
        x.longitude, x.latitude, oldcos, 300), axis=1)
    df_filtered = df_filtered[df_filtered['Closest_oldCo'].astype(
        bool) == False]

    # Import Starbucks around
    db, starbucks = connectCollection('companies', 'starbucks')
    print("starbucks collection successfully loaded")

    df_filtered["Closest_Starbucks"] = df_filtered.apply(lambda x: searchNear(
        x.longitude, x.latitude, starbucks, 1000), axis=1)
    df_filtered = df_filtered[df_filtered['Closest_Starbucks'].astype(
        bool)]

    # Import Tech Companies with >$1m raised around
    db, techCos = connectCollection('companies', 'techCos')
    print("techCos collection successfully loaded")

    df_filtered["Closest_techCo"] = df_filtered.apply(lambda x: searchNearWithoutLimit(
        x.longitude, x.latitude, techCos, 400), axis=1)
    df_filtered = df_filtered[df_filtered['Closest_techCo'].astype(
        bool)]
    df_filtered.reset_index(inplace=True, drop=True)
    df_filtered.to_csv("../input/df_filtered")
    print("df_filtered.csv successfully exported")

    # Selecting and filtering podium of cities
    '''
    Top3 of cities is London, Los Angeles and Austin. So we filter these three.
    '''
    df_podium = df_filtered[(df_filtered.city == "London") | (
        df_filtered.city == "Los Angeles") | (df_filtered.city == "Austin")]
    df_podium.reset_index(inplace=True, drop=True)
    dropcol = df_podium.iloc[:, 0]
    df_podium

    # Filter to see distances to airports, Starbucks and number of successfull technology companies around.
    df_podium["Coord_Closest_Airport"] = df_podium.Closest_Airport.apply(
        lambda x: x[0]["geoJSON"]["coordinates"])
    df_podium["Coord_Closest_Starbucks"] = df_podium.Closest_Starbucks.apply(
        lambda x: x[0]["geoJSON"]["coordinates"])
    df_podium["N_techCos_Around"] = df_podium.Closest_techCo.apply(
        lambda x: len(x))
    df_austin = df_podium[df_podium.city == "Austin"]
    df_austin.to_csv("../input/df_austin.csv")
    # We see that Austin has 8 technology companies around, therefore we will choose this city.
    print("df_austin.csv successfully exported")


if __name__ == "__main__":
    main()
