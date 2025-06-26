import requests


API_KEY = "dcf15ab069ad87dba78fe05dadf78e6c"

def get_weather_data(city=None, coords=None):
    if coords:
        lat = coords['lat']
        lon = coords['lon']
        url = url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"

    response = requests.get(url)
    data = response.json()

    # agar kuch galat city ya coords diya ho toh handle karo
    if response.status_code !=200 or "main" not in data:
        return {
            "city": city or "unknown",
            "temp": "N/A",
            "humidity": "N/A",
            "wind": "N/A",
            "description": "Could not fetch weather",
            "timestamp": 0
        }
    
    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "timestamp": data["dt"]
    }