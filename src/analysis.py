import pandas as pd
import requests


def get_filename_list(url):
    """Extracting the 2.nd table from the URL, and from there, the 1st col: filename."""
    html = requests.get(url).content
    df_list = pd.read_html(html)
    return df_list[1][0]


def create_conditions_df(file):
    """set up df."""
    try:
        df = pd.read_csv(file, sep='|')
        if "downcase_name" in df.columns:
            return df.drop(columns=["id", "name"])
        else:
            df["name"] = df["name"].str.lower()
            return df.drop(columns=["id"])
    except Exception as e:
        print(e)
        return pd.DataFrame([])


def create_countries_df(file):
    """set up df."""
    try:
        df = pd.read_csv(file, sep='|')
        df_final = df.drop(columns=["id", "removed"])
        return df_final
    except Exception as e:
        print(e)
        return pd.DataFrame([])

