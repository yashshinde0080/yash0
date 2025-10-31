"""API configuration and endpoints."""

import os

# Weather API
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
WEATHER_API_BASE_URL = 'http://api.weatherapi.com/v1'
WEATHER_ENDPOINTS = {
    'current': '/current.json',
    'forecast': '/forecast.json',
    'history': '/history.json',
}

# SoilGrids API (Satellite soil data)
SOILGRIDS_API_BASE_URL = 'https://rest.isric.org/soilgrids/v2.0'
SOILGRIDS_ENDPOINTS = {
    'properties': '/properties/query',
}

# Bhuvan API (ISRO - India-specific soil data)
BHUVAN_API_KEY = os.getenv('BHUVAN_API_KEY', '')
BHUVAN_API_BASE_URL = 'https://bhuvan-app1.nrsc.gov.in/api'
BHUVAN_ENDPOINTS = {
    'soil': '/soil',
    'landuse': '/landuse',
    'fertility': '/fertility',
}

# Agmarknet API (Market prices)
AGMARKNET_API_KEY = os.getenv('AGMARKNET_API_KEY', '')
AGMARKNET_API_BASE_URL = 'https://api.data.gov.in/resource'
AGMARKNET_RESOURCE_ID = '9ef84268-d588-465a-a5c0-3fab19590f2d'  # Mandi prices dataset

# Request headers
DEFAULT_HEADERS = {
    'User-Agent': 'FarmerAI/1.0',
    'Content-Type': 'application/json',
}

# API retry settings
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 0.5
RETRY_STATUS_CODES = [429, 500, 502, 503, 504]

# Request timeouts (seconds)
REQUEST_TIMEOUT = 30
WEATHER_TIMEOUT = 15
SOILGRIDS_TIMEOUT = 30
BHUVAN_TIMEOUT = 30
AGMARKNET_TIMEOUT = 20


class APIEndpoints:
    """Centralized API endpoint definitions."""

    @staticmethod
    def weather_current(latitude, longitude):
        """Get current weather endpoint."""
        return f"{WEATHER_API_BASE_URL}{WEATHER_ENDPOINTS['current']}"

    @staticmethod
    def weather_forecast(latitude, longitude, days=7):
        """Get weather forecast endpoint."""
        return f"{WEATHER_API_BASE_URL}{WEATHER_ENDPOINTS['forecast']}"

    @staticmethod
    def soilgrids_properties(latitude, longitude):
        """Get soil grid properties endpoint."""
        return f"{SOILGRIDS_API_BASE_URL}{SOILGRIDS_ENDPOINTS['properties']}"

    @staticmethod
    def bhuvan_soil(latitude, longitude):
        """Get Bhuvan soil data endpoint."""
        return f"{BHUVAN_API_BASE_URL}{BHUVAN_ENDPOINTS['soil']}"

    @staticmethod
    def agmarknet_prices(commodity=None, state=None):
        """Get Agmarknet market prices endpoint."""
        return f"{AGMARKNET_API_BASE_URL}/{AGMARKNET_RESOURCE_ID}"


# API request parameters
class APIParams:
    """Common API parameters."""

    # SoilGrids
    SOILGRIDS_DEPTH_LEVELS = ['0-5cm', '5-15cm', '15-30cm']
    SOILGRIDS_PROPERTIES = ['ph', 'organic_carbon', 'nitrogen', 'phosphorus', 'potassium']

    # Weather
    WEATHER_FORECAST_DAYS = 7
    WEATHER_INCLUDE_PARAMS = ['temp_c', 'humidity', 'wind_kph', 'precip_mm', 'condition']

    # Agmarknet
    AGMARKNET_COMMODITIES = [
        'Rice', 'Wheat', 'Cotton', 'Sugarcane', 'Pulses',
        'Corn', 'Vegetables', 'Fruits', 'Spices', 'Oilseeds'
    ]


# Error messages
API_ERROR_MESSAGES = {
    'TIMEOUT': 'API request timed out. Please check your connection.',
    'CONNECTION_ERROR': 'Failed to connect to API server.',
    'INVALID_RESPONSE': 'Received invalid response from API.',
    'RATE_LIMIT': 'API rate limit exceeded. Please try again later.',
    'UNAUTHORIZED': 'API key is missing or invalid.',
    'NOT_FOUND': 'Requested data not found.',
    'SERVER_ERROR': 'API server error. Please try again later.',
}
