from flask import Flask, render_template
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = "80ea880b615821a9c4f371dccfe4986c" # Replace this
CITY = "Kumasi"
DB = "weather.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    conn = get_db()
    for item in data['list'][:10]: # Store next 10 time slots
        dt = datetime.fromtimestamp(item['dt'])
        temp = item['main']['temp']
        desc = item['weather'][0]['description']
        conn.execute('INSERT INTO weather (timestamp, temp, description) VALUES (?,?,?)',
                     (dt, temp, desc))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    records = conn.execute('SELECT * FROM weather ORDER BY timestamp DESC LIMIT 10').fetchall()
    conn.close()

    timestamps = [r['timestamp'] for r in records][::-1] # reverse for chart
    temps = [r['temp'] for r in records][::-1]
    current = records[0] if records else None

    return render_template('index.html', records=records, current=current,
                           timestamps=timestamps, temps=temps)

@app.route('/refresh')
def refresh():
    conn = get_db()
    conn.execute('DELETE FROM weather') # Clear old data
    conn.commit()
    conn.close()
    fetch_weather()
    return "Data refreshed! <a href='/'>View Dashboard</a>"

if __name__ == '__main__':
    app.run(debug=True)
