import geopandas as gpd
import pandas as pd
from functions import getLocation


def main():
    # Importing airports geoDataFrame
    gdf_airports = gpd.read_file(
        "../input/ne_10m_airports/ne_10m_airports.shp")
    print("Airports shp file imported.")

    gdf_airports["geoJSON"] = gdf_airports.geometry.apply(
        lambda x: getLocation(x))
    gdf_airports = gdf_airports.loc[:, ["name", "geometry", "geoJSON"]]

    # Exporting airports to JSON
    df_airports = pd.DataFrame(gdf_airports)
    df_airports.drop(df_airports.columns[1], axis=1, inplace=True)
    df_airports.to_json("../input/airports.json", orient='records')
    print("Airports JSON file generated.")


if __name__ == "__main__":
    main()
