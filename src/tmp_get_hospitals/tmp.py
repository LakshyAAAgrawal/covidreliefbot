from bs4 import BeautifulSoup
import json
import time
import requests
sleep_time = 60*5

resources = ['beds', 'oxygen_beds', 'covid_icu_beds', 'ventilators', 'icu_beds_without_ventilator', 'noncovid_icu_beds']

def fetch_details():
    url = 'https://coronabeds.jantasamvad.org/covid-info.js'
    #url =  'https://coronabeds.jantasamvad.org/beds.html'
    a = requests.get(url)
    print("get data")
    data = json.loads(a.content[23:-1])
    for resource in resources:
        del data[resource]["All"]
    return data


def find_resources(old_data, new_data):
    for resource in resources:
        for hospital in list(old_data[resource].keys()):
            if new_data[resource][hospital]['vacant'] > old_data[resource][hospital]['vacant']:
                print(hospital,"Got new",resource,  new_data[resource][hospital]['vacant'])

            
old_data = fetch_details()
find_resources(old_data, old_data)
while True:
    time.sleep(sleep_time)
    new_data = fetch_details()
    find_resources(old_data, new_data)
    old_data = new_data