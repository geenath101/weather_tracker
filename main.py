"""
Weather Tracker REST API
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from open_metro_client import invoke_openmeteo_client
#import debugpy
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Only start debugpy in the main process, not in the reloader process
# if os.environ.get("WERKZEUG_RUN_MAIN") is None:
#     try:
#    #     debugpy.listen(("0.0.0.0", 6678))
#         print("Debugger listening on port 6678...")
#         print("Waiting for debugger attach...")
#    #     debugpy.wait_for_client()
#         print("Debugger attached.")
#     except Exception as e:
#         print(f"Could not start debugger: {e}")

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "message": "Weather Tracker API",
        "version": "1.0.0"
    })

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Get weather data for specified coordinates"""
    try:
        # Get optional query parameters
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        
        # Fetch weather data
        hourly_dataframe = invoke_openmeteo_client(latitude, longitude)
        
        # Convert DataFrame to JSON-serializable format
       # weather_data = {
       #     "coordinates": {
       #         "latitude": latitude if latitude else 52.52,
       #         "longitude": longitude if longitude else 13.41
       #     },
       #     "hourly": hourly_dataframe.to_dict(orient='records')
        #}
        print(f"Returning weather data for lat: {latitude}, lon: {longitude}")
        return jsonify({
            "success": True,
            "data": hourly_dataframe.to_string()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    """Get current weather data"""
    try:
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        
        hourly_dataframe = invoke_openmeteo_client(latitude, longitude)
        
        # Get the first row (current weather)
        if not hourly_dataframe.empty:
            current = hourly_dataframe.iloc[0].to_dict()
            return jsonify({
                "success": True,
                "data": {
                    "coordinates": {
                        "latitude": latitude if latitude else 52.52,
                        "longitude": longitude if longitude else 13.41
                    },
                    "current": current
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "No weather data available"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    print("Starting Weather Tracker API...")
    print("API will be available at: http://127.0.0.1:5000")
    print("\nAvailable endpoints:")
    print("  GET /                    - Health check")
    print("  GET /api/weather         - Get hourly weather forecast")
    print("  GET /api/weather/current - Get current weather")
    print("\nQuery parameters: latitude, longitude (optional)")
    
    # Disable reloader to avoid debugpy port conflicts, or use use_reloader=False
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
