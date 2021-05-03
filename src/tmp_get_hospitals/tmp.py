from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
options.headless = True
path_to_geckodriver = "E:\covid_bot\geckodriver.exe"
sleep_time = 120


driver = webdriver.Firefox(executable_path=path_to_geckodriver, options=options)

def fetch_details():
    url = 'https://coronabeds.jantasamvad.org/all-covid-icu-beds.html'
    #url =  'https://coronabeds.jantasamvad.org/beds.html'
    driver.get(url)
    print("Got data")
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    info_list = soup.find('tbody',{ "id" : "hospitals_list" }).find_all('tr', {"class":"table-danger"})
    hospital_info = {}
    for row in info_list:
        hospital_name = row.find('th').text.strip()
        cols = row.find_all('td')
        hospital_info[hospital_name] = {}
        hospital_info[hospital_name]['update_time'] = cols[0].text.strip()
        hospital_info[hospital_name]['beds_available'] = int(cols[2].text.strip().split(" ")[0])
        #print("hospital_name", hospital_name, "update_time", update_time, "beds_available",beds_available)

    return hospital_info


def compare_details(old_data, new_data):
    for hospital_name, _ in old_data.items():
        if new_data[hospital_name]['beds_available'] > old_data[hospital_name]['beds_available']:
            print("GOT NEW ICU BED")
            print(hospital_name, new_data[hospital_name])


old_data = fetch_details()

while True:
    time.sleep(sleep_time)
    new_data = fetch_details()
    print(new_data)
    compare_details(old_data, new_data)
    old_data = new_data