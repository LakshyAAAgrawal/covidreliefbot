import pandas as pd
import io
import requests
import json
import urllib.parse

from text_fns import TextResult

def get_url(sheet_id, gid):
    return "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&gid={}".format(sheet_id, gid)

def read_file(url):
    s=requests.get(url).content
    return pd.read_csv(io.StringIO(s.decode('utf-8')), skiprows=0).fillna('')

def get_oxygen_df(city_names):
    df = read_file(get_url("16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM", "99421346"))
    cols = ["NAME", "CONTACT", "STATE", "LOCATION (CITY)", "STATUS", "DATETIME", "PRICE", "CYLINDER", "CANS", "REFILL", "ADDITIONAL INFO"] 
    df.columns = cols + [str(i) for i in range(len(df.columns)-len(cols))]
    df = df[cols]
    df = df[df["STATUS"] == "Available"]
    df = df[df["DATETIME"] != ""]
    df["LOCATION"] = df["STATE"].str.lower().astype("str") + " " + df["LOCATION (CITY)"].str.lower().astype("str")
    df = df.drop(["STATE", "LOCATION (CITY)"], axis=1)
    df = df[df["LOCATION"].str.contains("(" + ")|(".join(city_names) + ")", regex=True)]
    df["DATETIME"] = pd.to_datetime(df[df["DATETIME"] != ""]["DATETIME"].astype("str") + " 2021", format="%d/%m %I:%M %p %Y", errors="coerce")
    df = df[df["DATETIME"].notna()]
    df = df.sort_values(by="DATETIME", ascending=False).reset_index(drop=True)
    df["ADDITIONAL INFO"] = df["ADDITIONAL INFO"].str.replace("\n", " ")
    return df.loc[:5].sample(n=1)

def get_oxygen_df_IIITD():
    df = read_file(get_url("1uKtW_4Z5DxclK0jPSeJZ6MorfVB597tS3cruLRl7Hf8", "1735067831"))
    df = df[df.columns[1:8]]
    df = df[df["Verified "] == "Yes"]
    df["Last verified"] = pd.to_datetime(df["Last verified"], format="%d %B %H:%M %y", errors="coerce")
    df = df[df["Last verified"].notna()]
    df = df.sort_values(by="Last verified", ascending=False).reset_index(drop=True).loc[:10,:]
    return df

def fetch_data_from_API(resource, location):
    if resource == "oxygen":
        df = get_oxygen_df(location)
        res = []
        ret = ""
        for idx, row in df.iterrows():
            #ret += "===============\n"
            for col in row.index:
                if row[col] == "":
                    continue
                ret += "*{}*: {}\n".format(col, row[col])
            #ret += "===============\n"
            #res.append(ret)
        return ret
    else:
        return "All the resources are available at https://t.me/covid_iiitd"

def get_twitter_link(cities, resources):
    if resources == [] or cities == []:
        return ''
    return "https://twitter.com/search?q=" + urllib.parse.quote_plus(
        '({}) ({}) -"needed" -"need" -"needs" -"required" -"require" -"requires" -"requirement" -"requirements"'.format(" OR ".join(cities), " OR ".join(resources))
    ) + "&f=live"

def get_best_resource_for(text_request):
    pass

def sync_resource(text_resource):
    pass
