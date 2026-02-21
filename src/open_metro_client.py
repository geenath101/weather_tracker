import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error

def invoke_openmeteo_client(latitude=None, longitude=None):
	hourly_dataframe = None
	try:
		print(f"invoking Open-Meteo client for lat: {latitude}, lon: {longitude}")
		cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
		retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
		openmeteo = openmeteo_requests.Client(session = retry_session)

		# Make sure all required weather variables are listed here
		# The order of variables in hourly or daily is important to assign them correctly below
		url = "https://api.open-meteo.com/v1/forecast"
		params = {
			"latitude": latitude if latitude is not None else 52.52,
			"longitude": longitude if longitude is not None else 13.41,
			"hourly": "temperature_2m",
		}
		print(f"invoking openmeteo for lat: {latitude}, lon: {longitude}")
		responses = openmeteo.weather_api(url, params=params)
		print(f"recieved response: {latitude}, lon: {longitude}")

		# Process first location. Add a for-loop for multiple locations or weather models
		response = responses[0]
		#print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
		#print(f"Elevation: {response.Elevation()} m asl")
		#print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

		# Process hourly data. The order of variables needs to be the same as requested.
		hourly = response.Hourly()
		hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

		# Create timestamps - use timestamp arithmetic to avoid timezone comparison issues
		start_timestamp = hourly.Time()
		interval_seconds = hourly.Interval()
		num_intervals = len(hourly_temperature_2m)
		
		# Generate timestamps as UTC datetime strings directly
		timestamps = []
		for i in range(num_intervals):
			ts = start_timestamp + (i * interval_seconds)
			dt = pd.to_datetime(ts, unit="s", utc=True)
			timestamps.append(dt.strftime('%Y-%m-%dT%H:%M:%S+00:00'))
		
		hourly_data = {
			"date": timestamps,
			"temperature_2m": hourly_temperature_2m
		}

		hourly_dataframe = pd.DataFrame(data = hourly_data)

		# Dates are already strings, no conversion needed
		#print("\nHourly data\n", hourly_dataframe)
	except Exception as e:
		print(f"Error fetching weather data: {e}")
		raise  # Re-raise the exception so the API can return a proper error response
	return hourly_dataframe
	
