
import requests
import os

API_KEY = os.getenv('API_KEY', '')

url_map = dict("onecall","https://api.openweathermap.org/data/3.0/onecall?lat={0}&lon={1}&appid={2}")

def invoke_one_call(latitude,longitude):
    response_as_dict = {}
    url = url_map.get("onecall")
    url.format(latitude,longitude,API_KEY)
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f" error response .. { response.status_code }")
        response_as_dict = response.json()
    except Exception as e:
        error = f"Error occurred while invoking endpoint ... { str(e) }"
        raise Exception(error)
    return response_as_dict
