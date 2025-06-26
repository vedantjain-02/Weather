from datetime import datetime
from io import BytesIO
import threading
import time
from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, emit
import json
from data_store import get_past_data, save_data
from weather_api import get_weather_data

app = Flask(__name__)
socketio = SocketIO(app)

latest_weather = {} #sabhi users ko latest data bhejne ke liye 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download")
def download():
    hours = int(request.args.get("hours", 1)) #?hours=5
    data = get_past_data(hours)
    buf = BytesIO()
    buf.write(json.dumps(data, indent=2).encode('utf-8'))
    buf.seek(0)
    filename = f"weather_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    return send_file(buf, as_attachment=True, download_name=filename, mimetype='application/json')

@socketio.on("get_weather")
def handle_get_weather(data):
    global latest_weather

    city=data.get("city")
    coords = data.get("coords")

    # data fetch karo
    weather = get_weather_data(city=city, coords=coords)

    # Store karo past ke liye
    save_data(weather)

    # latest update sabko boardcast karo 
    latest_weather = weather
    emit("weather_update", weather, broadcast=True)

# har 10 min me auto broadcast 
def broadcast_weather_periodcally():
    while True:
        if latest_weather:
                socketio.emit("weather_update", latest_weather)
                time.sleep(600) #600 sec = 10 min

# thread start karo jab app chale
threading.Thread(target=broadcast_weather_periodcally, daemon=True).start()

if __name__ == "__main__":
    socketio.run(app, debug=True)