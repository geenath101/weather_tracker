# Weather Tracker REST API

A containerized Python REST API for tracking weather data using Open-Meteo API.

## Quick Start with Docker 🐳

### Using Docker Compose (Recommended)
```bash
# Build and run the container
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop the container
docker-compose down
```

### Using Docker CLI
```bash
# Build the image
docker build -t weather-tracker-api .

# Run the container
docker run -p 5000:5000 weather-tracker-api

# Run in detached mode
docker run -d -p 5000:5000 --name weather-api weather-tracker-api

# Stop and remove
docker stop weather-api && docker rm weather-api
```

### Development Mode with Hot-Reload
```bash
# Build development image
docker build -f Dockerfile.dev -t weather-tracker-api:dev .

# Run with volume mount for code changes
docker run -p 5000:5000 -v $(pwd):/app weather-tracker-api:dev
```

## Local Development Setup (Without Docker)

1. Create and activate the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## API Endpoints

The API will be available at `http://127.0.0.1:5000`

### Health Check
```
GET /
```
Returns API status and version information.

### Get Weather Forecast
```
GET /api/weather?latitude=52.52&longitude=13.41
```
Returns hourly weather forecast for the specified coordinates.

**Query Parameters:**
- `latitude` (optional): Latitude coordinate (default: 52.52)
- `longitude` (optional): Longitude coordinate (default: 13.41)

**Response:**
```json
{
  "success": true,
  "data": {
    "coordinates": {
      "latitude": 52.52,
      "longitude": 13.41
    },
    "hourly": [
      {
        "date": "2024-01-01T00:00:00",
        "temperature_2m": 15.5
      }
    ]
  }
}
```

### Get Current Weather
```
GET /api/weather/current?latitude=52.52&longitude=13.41
```
Returns current weather data for the specified coordinates.

**Query Parameters:**
- `latitude` (optional): Latitude coordinate (default: 52.52)
- `longitude` (optional): Longitude coordinate (default: 13.41)

## Examples

Using curl:
```bash
# Health check
curl http://127.0.0.1:5000/

# Get weather for Berlin (default)
curl http://127.0.0.1:5000/api/weather

# Get weather for New York
curl "http://127.0.0.1:5000/api/weather?latitude=40.7128&longitude=-74.0060"

# Get current weather
curl "http://127.0.0.1:5000/api/weather/current?latitude=40.7128&longitude=-74.0060"
```

## Docker Details

- **Production Image**: Uses Gunicorn WSGI server with 4 workers
- **Security**: Runs as non-root user
- **Health Checks**: Built-in health monitoring
- **Cache**: Weather data is cached for 1 hour
- **Port**: 5000

## Project Structure

```
weather_tracker/
├── main.py                 # Flask API application
├── open_metro_client.py    # Weather API client
├── requirements.txt        # Python dependencies
├── Dockerfile             # Production container
├── Dockerfile.dev         # Development container
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker build exclusions
└── README.md             # This file
```


curl http://weatherapp-hwh2hegeb5epcnea.newzealandnorth-01.azurewebsites.net/api/weather?latitude=40.7128&longitude=-74.0060"
docker tag weather-tracker-api azurelearningdlg.azurecr.io/weather-tracker-api:latest




curl "http://127.0.0.1:5000/api/weather?latitude=40.7128&longitude=-74.0060"



docker run -d --name weather-test -p 5001:5000 weather-tracker-api:test && sleep 5 && curl -s "http://127.0.0.1:5001/api/weather/current?latitude=40.7128&longitude=-74.0060" | python3 -m json.tool | head -15

docker exec weather-test cat /app/open_metro_client.py | grep -A 2 -B 2 "strftime"