import sqlite3
import logging
from collections import namedtuple

create_table_query = '''
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
insert_table_query = '''
INSERT INTO stations
(sid, time, aqi, main, pm10, pm2p5, no2, so2, co, o3) VALUES
(?, datetime(?), ?, ?, ?, ?, ?, ?, ?, ?)
'''
check_query = '''
SELECT COUNT(*) FROM stations where sid = ? AND time = datetime(?)
'''

def aqi_insert_stations(data):
    station_list = [namedtuple('Station', station.keys())(*station.values()) for station in data["station"]]
    insert_data = [(s.id, s.pubTime, int(s.aqi), s.primary, int(s.pm10), int(s.pm2p5), int(s.no2), int(s.so2), float(s.co), int(s.o3)) for s in station_list]
    with sqlite3.connect("output/aqi.db") as conn:
        cur = conn.cursor()
        cur.execute(create_table_query)
        for d in insert_data:
            cur.execute(check_query, (d[0], d[1]))
            count = cur.fetchone()[0]
            if count == 0:
                cur.execute(insert_table_query, d)
        conn.commit()
