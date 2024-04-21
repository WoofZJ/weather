import requests
import json
import schedule
import time
import logging
from db import aqi_insert_stations

region_code = 101070107
city_code = 101070101
location = "123.41,41.765"
with open("config/key.txt", "r", encoding="utf8") as key_input:
    key = key_input.read()

def update_aqi():
    url = f"https://devapi.qweather.com/v7/air/now?key={key}&location={city_code}"
    response = requests.get(url)
    if response.status_code == 200:
        aqi_insert_stations(json.loads(str(response.content, encoding="utf8")))
    else:
        print(f"error! status code: {response.status_code}")

if __name__ == "__main__":
    update_aqi()
    schedule.every(30).minutes.do(update_aqi)
    while True:
        schedule.run_pending()
        time.sleep(60)