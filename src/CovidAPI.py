import pandas as pd
import io
import requests
import json
import urllib.parse
import datetime

from text_fns import TextResult
from lists import resource_name_list

class Resources:
    def __init__(self):
        self.data = {
            "bed": pd.DataFrame(columns=["source", "LOCATION", "DATETIME", "Contact"]),
            "oxygen": pd.DataFrame(columns=["source", "LOCATION", "DATETIME", "Contact"]),
            "plasma": pd.DataFrame(columns=["source", "LOCATION", "DATETIME", "Contact"])
        }
        self.last_updated = None
        self.update_resources()

    def beds1(self):
        df = read_file(get_url("1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k", "411964277"))
        cols = ["Name", "Contact", "STATE", "LOCATION (CITY)", "Status", "DATETIME", "Special Notes", "Number of Beds with Ventilator", "Beds with oxygen"]
        df.columns = cols + [str(i) for i in range(len(df.columns)-len(cols))]
        df = df[cols]
        df = df[df["Status"] == "Beds Available"]
        df = df[df["DATETIME"] != ""]
        df["LOCATION"] = df["STATE"].str.lower().astype("str") + " " + df["LOCATION (CITY)"].str.lower().astype("str")
        df = df.drop(["STATE", "LOCATION (CITY)"], axis=1)
        #df = df[df["LOCATION"].str.contains("(" + ")|(".join(city_names) + ")", regex=True)]
        df["DATETIME"] = pd.to_datetime(df[df["DATETIME"] != ""]["DATETIME"].astype("str") + " 2021", format="%d/%m %I:%M %p %Y", errors="coerce")
        df = df[df["DATETIME"].notna()]
        #df = df.sort_values(by="DATETIME", ascending=False).reset_index(drop=True)
        df["Special Notes"] = df["Special Notes"].str.replace("\n", " ")
        self.data["bed"] = self.data["bed"][self.data["bed"]["source"] != 1]
        df["source"] = 1
        self.data["bed"] = self.data["bed"].append(df)

    def oxygen1(self):
        df = read_file(get_url("16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM", "99421346"))
        cols = ["NAME", "CONTACT", "STATE", "LOCATION (CITY)", "STATUS", "DATETIME", "PRICE", "CYLINDER", "CANS", "REFILL", "ADDITIONAL INFO"] 
        df.columns = cols + [str(i) for i in range(len(df.columns)-len(cols))]
        df = df[cols]
        df = df[df["STATUS"] == "Available"]
        df = df[df["DATETIME"] != ""]
        df["LOCATION"] = df["STATE"].str.lower().astype("str") + " " + df["LOCATION (CITY)"].str.lower().astype("str")
        df = df.drop(["STATE", "LOCATION (CITY)"], axis=1)
        #df = df[df["LOCATION"].str.contains("(" + ")|(".join(city_names) + ")", regex=True)]
        df["DATETIME"] = pd.to_datetime(df[df["DATETIME"] != ""]["DATETIME"].astype("str") + " 2021", format="%d/%m %I:%M %p %Y", errors="coerce")
        df = df[df["DATETIME"].notna()]
        #df = df.sort_values(by="DATETIME", ascending=False).reset_index(drop=True)
        df["ADDITIONAL INFO"] = df["ADDITIONAL INFO"].str.replace("\n", " ")
        self.data["oxygen"] = self.data["oxygen"][self.data["oxygen"]["source"] != 1]
        df["source"] = 1
        self.data["oxygen"] = self.data["oxygen"].append(df)

    def plasma1(self):
        df = read_file(get_url("1jouo3H8BY78AACdka00kJaVEq9ochQtL24-cf8biHoY", "981656284"))
        cols = ["DATE", "VERIFICATION STATUS", "RESOURCE/ORGANISATION NAME", "LOCATION", "RESOURCE SPECIFICS", "TIME OF VERIFICATION", "Contact", "RELEVANT INFORMATION"] 
        df.columns = cols + [str(i) for i in range(len(df.columns)-len(cols))]
        df = df[cols]
        df = df[df["DATE"] != ""]
        df["DATETIME"] = pd.to_datetime(df[df["DATE"] != ""]["DATE"], format="%d/%m/%Y", errors="coerce")
        df = df[df["DATETIME"].notna()]
        df = df.drop(["DATE", "RESOURCE SPECIFICS"], axis=1)
        df["source"] = 1
        df["LOCATION"] = df["LOCATION"].str.lower()
        self.data["plasma"] = self.data["plasma"][self.data["plasma"]["source"] != 1]
        self.data["plasma"] = self.data["plasma"].append(df)

    def update_beds(self):
        self.beds1()

    def update_oxygen(self):
        self.oxygen1()

    def update_plasma(self):
        self.plasma1()

    def update_resources(self):
        self.update_beds()
        self.update_oxygen()
        self.update_plasma()
        for res in self.data:
            self.data[res] = self.data[res].fillna("")
            self.data[res] = self.data[res].sort_values(by="DATETIME", ascending=False).reset_index(drop=True)
        self.last_updated = datetime.datetime.now()

    def find_leads(self, resources, locations):
        if self.last_updated == None or (datetime.datetime.now() - self.last_updated).seconds >= 180:
            self.update_resources()
        ret = ""
        for resource in resources:
            try:
                df = self.data[resource].drop(["source"], axis=1).reset_index(drop = True)
                df = df[df["LOCATION"].str.contains("(" + ")|(".join(locations) + ")", regex=True)].reset_index(drop = True)
                df = df.loc[:5].sample(n=1)
            except Exception as e:
                print(e)
                ret += "No leads available for " + resource + "\n"
                continue
            if ret != "":
                ret += "\n"
            ret += "*" + resource + "*\n"
            for idx, row in df.iterrows():
                #ret += "===============\n"
                for col in row.index:
                    if row[col] == "":
                        continue
                    ret += "*{}*: {}\n".format(col, row[col])
        return ret

def get_url(sheet_id, gid):
    return "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&gid={}".format(sheet_id, gid)

def read_file(url):
    s=requests.get(url).content
    return pd.read_csv(io.StringIO(s.decode('utf-8')), skiprows=0, dtype=str).fillna('')

def get_beds_df(city_names):
    df = read_file(get_url("1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k", "411964277"))
    cols = ["Hospital Name", "Phone Number", "STATE", "LOCATION (CITY)", "Status", "DATETIME", "Special Notes", "Number of Beds with Ventilator", "Beds with oxygen"]
    df.columns = cols + [str(i) for i in range(len(df.columns)-len(cols))]
    df = df[cols]
    df = df[df["Status"] == "Beds Available"]
    df = df[df["DATETIME"] != ""]
    df["LOCATION"] = df["STATE"].str.lower().astype("str") + " " + df["LOCATION (CITY)"].str.lower().astype("str")
    df = df.drop(["STATE", "LOCATION (CITY)"], axis=1)
    df = df[df["LOCATION"].str.contains("(" + ")|(".join(city_names) + ")", regex=True)]
    df["DATETIME"] = pd.to_datetime(df[df["DATETIME"] != ""]["DATETIME"].astype("str") + " 2021", format="%d/%m %I:%M %p %Y", errors="coerce")
    df = df[df["DATETIME"].notna()]
    df = df.sort_values(by="DATETIME", ascending=False).reset_index(drop=True)
    df["Special Notes"] = df["Special Notes"].str.replace("\n", " ")
    return df.loc[:5].sample(n=1)

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
