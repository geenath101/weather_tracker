"""
Weather Tracker REST API
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from open_weather_api  import invoke_one_call
#import debugpy
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

ENABLED_MOCK = os.getenv('ENABLED_MOCK', 'true').lower() == 'true'

"""Get weather data for specified coordinates"""
@app.route('/api/weather', methods=['GET'])
def get_weather():
    try:
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        weather_data = ""
        if ENABLED_MOCK:
            try:
                with open('src/mock_response.json','r') as f:
                    weather_data = json.load(f)
            except Exception as e:
               error_message = f"error reading mock response:{str(e)}"
               raise Exception(error_message)
        else:
            respone_dict = invoke_one_call(latitude,longitude)
            print(f" printing response .... {respone_dict}")
      
        print(f"Returning weather data for lat: {latitude}, lon: {longitude}")
        return jsonify({
            "success": True,
            "data": weather_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500



if __name__ == "__main__":
    # Disable reloader to avoid debugpy port conflicts, or use use_reloader=False
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
