import pandas as pd
import io
import requests
import json

def get_url(sheet_id, gid):
    return "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&gid={}".format(sheet_id, gid)

def read_file(url):
    s=requests.get(url).content
    return pd.read_csv(io.StringIO(s.decode('utf-8')), header=None).fillna('')

def get_master_schema(resource_name):
    file_name = "master_schema/master_schema_{}.csv".format(resource_name)
    return pd.read_csv(file_name)

def process_column_id(val, raw_df):
    operation_raw = val.split("+")
    column_val = ""
    for i in operation_raw:
        try:
            idx = int(i)
            column_val += raw_df.iloc[:,idx]
        except ValueError:
            column_val += i
    return column_val


def populate_dataframe(df, raw_df, mapping):
    for key, val in mapping.items():
         df[key]  = process_column_id(val, raw_df)
    return df


def read_setting(file_name):
    f = open(file_name)
    setting = json.load(f)
    df  = get_master_schema(setting['resource'])
    print(get_url(setting['sheet_id'], setting['gid']))
    raw_df = read_file(get_url(setting['sheet_id'], setting['gid']))
    return populate_dataframe(df, raw_df, setting['mapping'])


def main():
    pass

print(read_setting('sheet_settings/sheet_setting.json'))
