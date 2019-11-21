import pandas as pd
from functions import connectCollection, searchNear, searchNearWithoutLimit, embed_map
import folium
import folium
from folium.plugins import HeatMap


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

    # Checking which cities have more techCos around
    df_filtered["Number_of_TechCo_around"] = df_filtered.Closest_techCo.apply(
        lambda x: len(x))
    df_check_techCos = df_filtered[["city", "Number_of_TechCo_around"]]
    df_check_techCos = df_check_techCos.groupby("city").sum().sort_values(
        by="Number_of_TechCo_around", ascending=False)

    # Checking apartment rent prices
    df_apartment = pd.read_csv("../input/apartment-rent-summary.csv")
    df_apartment[df_apartment["Location"].str.contains(
        "Atlanta|Chicago|Denver|Austin|San Mateo") == True].sort_values(by=["Price_3br"], ascending=False)
    '''
    Austin will be chosen, as it has many tech companies around, good rental prices and outranked Silicon Valley as the top city for startups
    http://austin.culturemap.com/news/innovation/07-03-19-austin-ranking-best-cities-startups-commercialcafe/
    '''
    df_austin = df_filtered[df_filtered.city == "Austin"]
    df_austin.reset_index(inplace=True, drop=True)
    df_austin.to_csv("../input/df_austin.csv")

    df_austin_final = df_austin.copy()

    df_austin_final["Airport_Latitude"] = df_austin_final["Closest_Airport"].apply(
        lambda x: x[0]["geoJSON"]["coordinates"][1])
    df_austin_final["Airport_Longitude"] = df_austin_final["Closest_Airport"].apply(
        lambda x: x[0]["geoJSON"]["coordinates"][0])
    df_austin_final["Starbucks_Latitude"] = df_austin_final["Closest_Starbucks"].apply(
        lambda x: x[0]["geoJSON"]["coordinates"][1])
    df_austin_final["Starbucks_Longitude"] = df_austin_final["Closest_Starbucks"].apply(
        lambda x: x[0]["geoJSON"]["coordinates"][0])
    df_austin_final["TechCo_Latitude"] = df_austin_final["Closest_techCo"].apply(
        lambda x: x[0]["geoJSON"]["coordinates"][1])
    df_austin_final["TechCo_Longitude"] = df_austin_final["Closest_techCo"].apply(
        lambda x: x[0]["geoJSON"]["coordinates"][0])

    # Create map with release incidents and monitoring stations
    m = folium.Map(location=[30.288653, -97.822884], zoom_start=11)
    HeatMap(data=df_austin_final[['latitude',
                                  'longitude']], radius=50).add_to(m)
    for idx, row in df_austin_final.iterrows():
        folium.Marker([row['latitude'], row['longitude']],
                      icon=folium.Icon(icon='home', color='blue')).add_to(m)
        folium.Marker([row['Starbucks_Latitude'], row['Starbucks_Longitude']],
                      icon=folium.Icon(icon='cutlery', color='darkgreen')).add_to(m)
        folium.Marker([row['Airport_Latitude'], row['Airport_Longitude']],
                      icon=folium.Icon(icon='plane', color='red')).add_to(m)

    # Show the map
    embed_map(m, 'm1.html')


if __name__ == "__main__":
    main()
