from bs4 import BeautifulSoup
import json
import time
import requests
import pandas as pd
from datetime import datetime
sleep_time = 60*5

resources = ['beds', 'oxygen_beds', 'covid_icu_beds', 'ventilators', 'icu_beds_without_ventilator', 'noncovid_icu_beds']

def fetch_details():
    url = 'https://coronabeds.jantasamvad.org/covid-info.js'
    a = requests.get(url)
    print("get data")
    data = json.loads(a.content[23:-1])
    for resource in resources:
        del data[resource]["All"]
    return data

def make_data_format(data):
    formated_data = { 'DATETIME': {} }
    for resource in resources:
        formated_data[resource] = {}
        for hospital in list(data[resource].keys()):
            formated_data[resource][hospital] = data[resource][hospital]['vacant']
            formated_data['DATETIME'][hospital] = datetime.strptime(data[resource][hospital]['last_updated_at'] + " 2021",'%I:%M %p, %b %d %Y' ) # EG '07:35 AM, May 08'
    df = pd.DataFrame(formated_data)
    df["source"] = 1
    df["LOCATION"] = "Delhi"
    df["Contact"] = "https://coronabeds.jantasamvad.org/"
    df.index.name = "Hospital Name"
    return df.reset_index()

if name__=='__main__':
    data = fetch_details()
    print(make_data_format(data))



'''
def find_resources(old_data, new_data):
    """compare old and new data
    """
    for resource in resources:
        for hospital in list(old_data[resource].keys()):
            if new_data[resource][hospital]['vacant'] > old_data[resource][hospital]['vacant']:
                print(hospital,"Got new",resource,  new_data[resource][hospital]['vacant'], "new", new_data[resource][hospital]['vacant'] - old_data[resource][hospital]['vacant'] )

            
old_data = fetch_details()
find_resources(old_data, old_data)
while True:
    time.sleep(sleep_time)
    new_data = fetch_details()
    find_resources(old_data, new_data)
    old_data = new_data

'''

