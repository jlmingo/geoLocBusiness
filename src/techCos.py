import pandas as pd
from functions import getLoc


def main():

    df_techCos = pd.read_csv("../input/clean_df_companies.csv")
    df_techCos[(df_techCos["Tech/Other"] == "Tech") &
               (df_techCos["total_money_raised"] >= 1000000)]
    df_techCos["geoJSON"] = df_techCos.apply(
        lambda x: getLoc(x.longitude, x.latitude), axis=1)
    df_techCos.drop(df_techCos[(df_techCos.longitude.isnull() == True) | (
        df_techCos.latitude.isnull() == True)].index, inplace=True)
    df_techCos.to_json("../input/techCos.json", orient='records')
    print("df_techCos.json exported successfully")


if __name__ == "__main__":
    main()
