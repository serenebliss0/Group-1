import requests
from datetime import datetime


def get_location_data():
    response = requests.get("http://ip-api.com/json/")
    data = response.json()

    print(data)

    city = data.get("city", "Unknown City")
    country = data.get("country", "Unknown Country")
    latitude = data.get("lat")
    longitude = data.get("lon")

    weather_data = None

    if latitude and longitude:
        weather = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        )

        weather_data = weather.json()

    return {
        "city": city,
        "country": country,
        "weather": weather_data
    }


def get_current_time():
    return datetime.now()


x = get_location_data()

print(x["city"])
print(x["country"])
print(x["weather"])