import json
import requests

def get_weather(lat, lon):
    """Use Open-Meteo to fetch current weather for given coordinates."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    current = data["current_weather"]
    return {
        "temperature_2m": current["temperature"],
    }


def lambda_handler(event, context):

        headers = event.get("headers", {})

        try:
            lat = float(headers.get("cloudfront-viewer-latitude",0))
            lon = float(headers.get("cloudfront-viewer-longitude",0))
        except ValueError:
            lat, lon = 0, 0

        city = headers.get("cloudfront-viewer-city","Unknown")
        country = headers.get("cloudfront-viewer-country","Unknown")
        weather = get_weather(lat, lon)


        return {
            "statusCode": 200,
            "body": json.dumps({
                "city": city,
                "country": country,
                "weather": weather
            })
        }


