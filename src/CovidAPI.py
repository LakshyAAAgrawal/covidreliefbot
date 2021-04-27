import pandas as pd
import io
import requests
import json

from text_fns import TextResult

def get_url(sheet_id, gid):
    return "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&gid={}".format(sheet_id, gid)

def read_file(url):
    s=requests.get(url).content
    return pd.read_csv(io.StringIO(s.decode('utf-8')), skiprows=0).fillna('')

def get_oxygen_df():
    df = read_file(get_url("1uKtW_4Z5DxclK0jPSeJZ6MorfVB597tS3cruLRl7Hf8", "1735067831"))
    df = df[df.columns[1:8]]
    df = df[df["Verified "] == "Yes"]
    df["Last verified"] = pd.to_datetime(df["Last verified"], format="%d %B %H:%M %y", errors="coerce")
    df = df[df["Last verified"].notna()]
    df = df.sort_values(by="Last verified", ascending=False).reset_index(drop=True).loc[:10,:]
    return df

def fetch_data_from_API(resource, location):
    if resource == "Oxygen":
        df = get_oxygen_df()
        res = []
        for idx, row in df.iterrows():
            ret = ""
            ret += "===============\n"
            for col in row.index:
                if row[col] == "":
                    continue
                ret += "{}: *{}*\n".format(col, row[col])
            ret += "===============\n"
            res.append(ret)
        return res
    else:
        return "All the resources are available at https://t.me/covid_iiitd"

def join_entries(entries):
    entries_url = entries[0]

    for i in entries[1:]:
        entries_url += '%20OR%20{}'.format(str(i))
    return entries_url

def get_twitter_link(cities, resources):
    if resources == [] or cities == []:
        return ''

    location_text = join_entries(cities)
    resources_text = join_entries(resources)

    return 'https://twitter.com/search?q=({})%20({})%20-%22needed%22%20-%22need%22%20-%22needs%22%20-%22required%22%20-%22require%22%20-%22requires%22%20-%22requirement%22%20-%22requirements%22&f=live'.format(location_text, resources_text)

def get_best_resource_for(text_request):
    pass

def sync_resource(text_resource):
    pass
