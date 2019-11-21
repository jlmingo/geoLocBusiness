import pandas as pd
from functions import getLoc


def main():
    df_oldcos = pd.read_csv("../input/clean_df_companies.csv")
    df_oldcos = df_oldcos[df_oldcos.founded_year < 2009]
    df_oldcos["geoJSON"] = df_oldcos.apply(
        lambda x: getLoc(x.longitude, x.latitude), axis=1)
    df_oldcos.drop(df_oldcos[(df_oldcos.longitude.isnull() == True) | (
        df_oldcos.latitude.isnull() == True)].index, inplace=True)
    df_oldcos.to_json("../input/oldCos.json", orient='records')
    print("oldCos.json exported successfully")


if __name__ == "__main__":
    main()
