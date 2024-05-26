import sqlite3
import requests
import json

# Access key  weatherstack APIs
access_key = "91950bcdba3256bdfa3df833bbaa1e11"
url = f"http://api.weatherstack.com/current?access_key={access_key}"

#user -- is inputi lokaciis gasagebad
location = input("chawere sasurveli lokacia:  ")

querystring = {"query": location}


response = requests.get(url, params=querystring)

if response.status_code == 200:
    data = response.json()

    if "current" in data:
        #json fileshi informaciis gadasatanad
        with open("weather_data.json","w") as json_file:
            json.dump(data, json_file, indent=4) 
        #sqlite connectis damyareba
        conn = sqlite3.connect('weather_data.db')
        c = conn.cursor()

        #table informaciis dasastorad
        c.execute('''CREATE TABLE IF NOT EXISTS weather (
                     location TEXT,          -- lokaciis saxeli
                     temperature REAL,       -- Temperature in Celsius
                     weather_description TEXT -- weatheris description
                     )''')
        c.execute("INSERT INTO weather (location, temperature, weather_description) VALUES (?, ?, ?)",
                  (location, data["current"].get("temperature"), data["current"].get("weather_descriptions", ["N/A"])[0]))

        conn.commit()
        conn.close()
        #terminalshi informaciis gamotana
        print("Weather information for", location)
        print("Temperature:", data["current"].get("temperature"), "°C")
        print("Weather Description:", data["current"].get("weather_descriptions", ["N/A"])[0])
    else:
        print("weatheris info araris xelmisawvdomi (albat)")
else:
    print("weather data ver aigo:", response.status_code)
