"""Weather data service with API integration and caching."""

import logging
import requests
from datetime import datetime
from typing import Optional, List, Dict

from config.api_config import (
    WEATHER_API_KEY, WEATHER_API_BASE_URL,
    WEATHER_ENDPOINTS, WEATHER_TIMEOUT
)
from config.settings import WEATHER_CACHE_HOURS
from services.cache_manager import get_cache_manager

logger = logging.getLogger(__name__)


class WeatherService:
    """Manages weather data from WeatherAPI.com."""

    def __init__(self):
        """Initialize weather service."""
        self.api_key = WEATHER_API_KEY
        self.base_url = WEATHER_API_BASE_URL
        self.cache = get_cache_manager()

    def get_current_weather(self, latitude: float, longitude: float,
                           force_refresh: bool = False) -> Optional[Dict]:
        """
        Get current weather for location.

        Args:
            latitude: Location latitude
            longitude: Location longitude
            force_refresh: Bypass cache and fetch fresh data

        Returns:
            Weather data dict or None
        """
        try:
            # Check cache first
            if not force_refresh:
                cached = self.cache.get_cached_weather(latitude, longitude,
                                                       forecast_date=str(datetime.now().date()))
                if cached:
                    logger.info(f'Using cached weather for ({latitude}, {longitude})')
                    return self._convert_cached_to_dict(cached[0])

            # Fetch from API
            weather_data = self._fetch_current_weather(latitude, longitude)

            if weather_data:
                # Cache the result
                self.cache.cache_weather_data(latitude, longitude, [weather_data])
                return weather_data
            else:
                # Try to use expired cache as fallback
                all_cached = self.cache.get_cached_weather(latitude, longitude)
                if all_cached:
                    logger.warning('Using expired cached weather')
                    return self._convert_cached_to_dict(all_cached[0])

            return None

        except Exception as e:
            logger.error(f'Error getting current weather: {str(e)}')
            return None

    def get_forecast(self, latitude: float, longitude: float, days: int = 7,
                    force_refresh: bool = False) -> Optional[List[Dict]]:
        """
        Get weather forecast for location.

        Args:
            latitude: Location latitude
            longitude: Location longitude
            days: Number of days to forecast (max 7)
            force_refresh: Bypass cache

        Returns:
            List of forecast dicts or None
        """
        try:
            days = min(days, 7)  # Max 7 days

            # Check cache
            if not force_refresh:
                cached = self.cache.get_cached_weather(latitude, longitude)
                if cached and len(cached) >= days:
                    logger.info(f'Using cached forecast for ({latitude}, {longitude})')
                    return [self._convert_cached_to_dict(c) for c in cached[:days]]

            # Fetch from API
            forecast_data = self._fetch_forecast(latitude, longitude, days)

            if forecast_data:
                # Cache results
                self.cache.cache_weather_data(latitude, longitude, forecast_data)
                return forecast_data

            return None

        except Exception as e:
            logger.error(f'Error getting forecast: {str(e)}')
            return None

    def _fetch_current_weather(self, latitude: float, longitude: float) -> Optional[Dict]:
        """Fetch current weather from API."""
        try:
            params = {
                'key': self.api_key,
                'q': f'{latitude},{longitude}',
                'aqi': 'no',
            }

            response = requests.get(
                f'{self.base_url}{WEATHER_ENDPOINTS["current"]}.json',
                params=params,
                timeout=WEATHER_TIMEOUT
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_current_weather(data)
            else:
                logger.error(f'Weather API error: {response.status_code}')
                return None

        except Exception as e:
            logger.error(f'Error fetching current weather: {str(e)}')
            return None

    def _fetch_forecast(self, latitude: float, longitude: float, days: int) -> Optional[List[Dict]]:
        """Fetch weather forecast from API."""
        try:
            params = {
                'key': self.api_key,
                'q': f'{latitude},{longitude}',
                'days': days,
                'aqi': 'no',
            }

            response = requests.get(
                f'{self.base_url}{WEATHER_ENDPOINTS["forecast"]}.json',
                params=params,
                timeout=WEATHER_TIMEOUT
            )

            if response.status_code == 200:
                data = response.json()
                return self._parse_forecast(data)
            else:
                logger.error(f'Forecast API error: {response.status_code}')
                return None

        except Exception as e:
            logger.error(f'Error fetching forecast: {str(e)}')
            return None

    @staticmethod
    def _parse_current_weather(api_response: Dict) -> Dict:
        """Parse current weather from API response."""
        try:
            current = api_response.get('current', {})
            location = api_response.get('location', {})

            return {
                'location_name': f"{location.get('name')}, {location.get('region')}",
                'forecast_date': str(datetime.now().date()),
                'temperature_c': current.get('temp_c'),
                'humidity_percent': current.get('humidity'),
                'wind_speed_kmh': current.get('wind_kph'),
                'precipitation_mm': current.get('precip_mm'),
                'rainfall_probability': 0,  # Not in current data
                'condition': current.get('condition', {}).get('text'),
                'uv_index': current.get('uv'),
            }
        except Exception as e:
            logger.error(f'Error parsing current weather: {str(e)}')
            return {}

    @staticmethod
    def _parse_forecast(api_response: Dict) -> List[Dict]:
        """Parse forecast from API response."""
        try:
            forecast_days = api_response.get('forecast', {}).get('forecastday', [])
            forecasts = []

            for day in forecast_days:
                day_data = day.get('day', {})
                forecast = {
                    'forecast_date': day.get('date'),
                    'temperature_c': (day_data.get('maxtemp_c') + day_data.get('mintemp_c')) / 2,
                    'temp_min_c': day_data.get('mintemp_c'),
                    'temp_max_c': day_data.get('maxtemp_c'),
                    'humidity_percent': day_data.get('avghumidity'),
                    'wind_speed_kmh': day_data.get('maxwind_kph'),
                    'precipitation_mm': day_data.get('totalprecip_mm'),
                    'rainfall_probability': day_data.get('daily_chance_of_rain'),
                    'condition': day_data.get('condition', {}).get('text'),
                    'uv_index': day_data.get('uv'),
                }
                forecasts.append(forecast)

            return forecasts
        except Exception as e:
            logger.error(f'Error parsing forecast: {str(e)}')
            return []

    @staticmethod
    def _convert_cached_to_dict(cached_obj) -> Dict:
        """Convert SQLAlchemy object to dict."""
        return {
            'forecast_date': str(cached_obj.forecast_date),
            'temperature_c': cached_obj.temperature_c,
            'temp_min_c': cached_obj.temp_min_c,
            'temp_max_c': cached_obj.temp_max_c,
            'humidity_percent': cached_obj.humidity_percent,
            'wind_speed_kmh': cached_obj.wind_speed_kmh,
            'precipitation_mm': cached_obj.precipitation_mm,
            'rainfall_probability': cached_obj.rainfall_probability,
            'condition': cached_obj.condition,
            'uv_index': cached_obj.uv_index,
        }


# Global weather service instance
_weather_service = None


def get_weather_service() -> WeatherService:
    """Get or create global weather service."""
    global _weather_service
    if _weather_service is None:
        _weather_service = WeatherService()
    return _weather_service
