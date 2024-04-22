import sqlite3
import logging
from collections import namedtuple

create_aqi_table_query = '''
CREATE TABLE IF NOT EXISTS stations (
    sid TEXT,
    time DATETIME,
    aqi INTEGER,
    main TEXT,
    pm10 INTEGER,
    pm2p5 INTEGER,
    no2 INTEGER,
    so2 INTEGER,
    co REAL,
    o3 INTEGER
)
'''
insert_aqi_table_query = '''
INSERT INTO stations
(sid, time, aqi, main, pm10, pm2p5, no2, so2, co, o3) VALUES
(?, datetime(?), ?, ?, ?, ?, ?, ?, ?, ?)
'''
check_aqi_query = '''
SELECT COUNT(*) FROM stations where sid = ? AND time = datetime(?)
'''
create_weather_table_query = '''
CREATE TABLE IF NOT EXISTS weather (
    region INTEGER,
    time DATETIME,
    temp INTEGER,
    humidity INTEGER,
    type INTEGER,
    wind360 INTEGER,
    windDir TEXT,
    windScale INTEGER,
    windSpeed INTEGER,
    pressure INTEGER,
    cloud INTEGER,
    vis   INTEGER,
    precip REAL,
    feelsLike INTEGER
)
'''
insert_weather_table_query = '''
INSERT INTO weather
(region, time, temp, humidity, type, wind360, windDir, windScale, windSpeed, pressure, cloud, vis, precip, feelsLike) VALUES
(?, datetime(?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''
check_weather_query = '''
SELECT COUNT(*) FROM weather where region = ? AND time = datetime(?)
'''

def aqi_insert_stations(data):
    station_list = [namedtuple('Station', station.keys())(*station.values()) for station in data["station"]]
    insert_data = [(s.id, s.pubTime, int(s.aqi), s.primary, int(s.pm10), int(s.pm2p5), int(s.no2), int(s.so2), float(s.co), int(s.o3)) for s in station_list]
    with sqlite3.connect("output/aqi.db") as conn:
        cur = conn.cursor()
        cur.execute(create_aqi_table_query)
        for d in insert_data:
            cur.execute(check_aqi_query, (d[0], d[1]))
            count = cur.fetchone()[0]
            if count == 0:
                cur.execute(insert_aqi_table_query, d)
        conn.commit()

def weather_insert(data, region):
    now = namedtuple("Now", data["now"].keys())(*data["now"].values())
    insert_data = (region, now.obsTime, int(now.temp), int(now.humidity), now.text, int(now.wind360), now.windDir, int(now.windScale), int(now.windSpeed), int(now.pressure), int(now.cloud), int(now.vis), float(now.precip), int(now.feelsLike))
    with sqlite3.connect("output/weather.db") as conn:
        cur = conn.cursor()
        cur.execute(create_weather_table_query)
        cur.execute(check_weather_query, (insert_data[0], insert_data[1]))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute(insert_weather_table_query, insert_data)
        conn.commit()