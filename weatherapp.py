import sqlite3
import requests
import json

access_key = "91950bcdba3256bdfa3df833bbaa1e11"
url = f"http://api.weatherstack.com/current?access_key={access_key}"

location = input("Enter your desired location: ")

querystring = {"query": location}

response = requests.get(url, params=querystring)

if response.status_code == 200:
    data = response.json()

    if "current" in data:
        # Connect to the SQLite database
        conn = sqlite3.connect('weather_data.db')
        c = conn.cursor()

        # Create a table to store weather information if not exists
        c.execute('''CREATE TABLE IF NOT EXISTS weather (
                     id INTEGER PRIMARY KEY,
                     location TEXT,
                     temperature REAL,
                     weather_description TEXT
                     )''')

        # Insert data into the database
        c.execute("INSERT INTO weather (location, temperature, weather_description) VALUES (?, ?, ?)",
                  (location, data["current"].get("temperature"), data["current"].get("weather_descriptions", ["N/A"])[0]))

        # Commit changes and close connection
        conn.commit()
        conn.close()

        print("Weather information for", location)
        print("Temperature:", data["current"].get("temperature"), "°C")
        print("Weather Description:", data["current"].get("weather_descriptions", ["N/A"])[0])
    else:
        print("No current weather information available.")
else:
    print("Failed to fetch weather data. Status code:", response.status_code)
