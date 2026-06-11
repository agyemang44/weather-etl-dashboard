# Weather ETL Dashboard

Flask app that fetches weather data from OpenWeather API, stores in SQLite, displays with Chart.js.

## Features
- ETL: Extract from API → Transform → Load to SQLite
- Real-time weather for Kumasi, Ghana
- 5-day forecast line chart
- Manual refresh endpoint = simulated scheduled job

## Tech Stack
Python, Flask, SQLite, Requests, Chart.js

## Setup
1. Get API key from openweathermap.org
2. Paste key in app.py line 6
3. pip install -r requirements.txt
4. sqlite3 weather.db < schema.sql
5. python app.py
6. Visit http://localhost:5000
7. Click "Refresh Data" to run ETL
