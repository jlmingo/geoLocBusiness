
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import math
from functions import embed_map


def main():
    df_filtered = pd.read_csv("../input/df_filtered.csv")
    df_austin_final = pd.read_csv("../input/df_austin_final.csv")

    # Austin map
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
    embed_map(m, '../output/m_1.html')
    print("Austin successfully exported to output folder with name m1_html")

    # Cluster and heat map
    m_2 = folium.Map(location=[40.4893538, -3.6827461], zoom_start=2)

    mc = MarkerCluster()
    for idx, row in df_filtered.iterrows():
        if not math.isnan(row['longitude']) and not math.isnan(row['latitude']):
            mc.add_child(folium.Marker([row['latitude'], row['longitude']]))
    m_2.add_child(mc)
    HeatMap(data=df_filtered[['TechCo_Latitude',
                              'TechCo_Longitude']], radius=50).add_to(mc)

    embed_map(m_2, '../output/m_2.html')
    print("Cluster and heatmap successfully exported to output folder with name m2_html")


if __name__ == "__main__":
    main()
