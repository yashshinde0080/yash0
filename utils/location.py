"""Location and GPS utilities."""

import logging
from typing import Tuple, Optional
from math import radians, cos, sin, asin, sqrt

logger = logging.getLogger(__name__)


class LocationUtils:
    """Utilities for location handling."""

    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> bool:
        """
        Validate GPS coordinates.

        Args:
            latitude: Latitude value
            longitude: Longitude value

        Returns:
            True if valid, False otherwise
        """
        try:
            lat = float(latitude)
            lon = float(longitude)
            return -90 <= lat <= 90 and -180 <= lon <= 180
        except (TypeError, ValueError):
            return False

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate great circle distance between two points on earth (in km).

        Args:
            lat1, lon1: First coordinate
            lat2, lon2: Second coordinate

        Returns:
            Distance in kilometers
        """
        try:
            # Convert to radians
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

            # Haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a))
            km = 6371 * c

            return km
        except Exception as e:
            logger.error(f'Error calculating distance: {str(e)}')
            return 0.0

    @staticmethod
    def is_in_india(latitude: float, longitude: float) -> bool:
        """
        Check if coordinates are within India.

        Returns:
            True if within India, False otherwise
        """
        # India's approximate bounding box
        india_north = 35.5  # Ladakh
        india_south = 8.1   # Kerala
        india_west = 68.1   # Gujarat
        india_east = 97.2   # Arunachal Pradesh

        try:
            lat = float(latitude)
            lon = float(longitude)
            return (india_south <= lat <= india_north and
                    india_west <= lon <= india_east)
        except (TypeError, ValueError):
            return False

    @staticmethod
    def get_region_name(latitude: float, longitude: float) -> str:
        """
        Get approximate Indian region/state name from coordinates.

        Args:
            latitude: GPS latitude
            longitude: GPS longitude

        Returns:
            Region/State name
        """
        # Simplified mapping - would need more detailed data in production
        regions = {
            'North': (28, 32, 75, 80),  # (lat_min, lat_max, lon_min, lon_max)
            'Northeast': (24, 29, 88, 97),
            'East': (22, 26, 84, 88),
            'Central': (20, 24, 76, 84),
            'West': (18, 23, 68, 76),
            'South': (8, 18, 76, 84),
            'South_East': (12, 20, 78, 85),
        }

        try:
            lat = float(latitude)
            lon = float(longitude)

            for region, (lat_min, lat_max, lon_min, lon_max) in regions.items():
                if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                    return region.replace('_', ' ')

            return 'Unknown'
        except (TypeError, ValueError):
            return 'Unknown'

    @staticmethod
    def format_coordinates(latitude: float, longitude: float) -> str:
        """Format coordinates for display."""
        try:
            lat = float(latitude)
            lon = float(longitude)
            return f'{lat:.4f}°N, {lon:.4f}°E'
        except (TypeError, ValueError):
            return 'Invalid coordinates'


# Commonly used crops by region (for recommendations)
REGION_CROPS = {
    'North': ['Wheat', 'Rice', 'Mustard', 'Cotton', 'Corn'],
    'Northeast': ['Rice', 'Tea', 'Citrus', 'Vegetables', 'Betel leaf'],
    'East': ['Rice', 'Pulses', 'Sugarcane', 'Oilseeds', 'Potatoes'],
    'Central': ['Cotton', 'Soybeans', 'Pulses', 'Groundnut', 'Rice'],
    'West': ['Cotton', 'Groundnut', 'Millets', 'Sugarcane', 'Fruits'],
    'South': ['Rice', 'Coffee', 'Tea', 'Spices', 'Coconut'],
    'South_East': ['Rice', 'Pulses', 'Oilseeds', 'Sugarcane', 'Vegetables'],
}


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate GPS coordinates."""
    return LocationUtils.validate_coordinates(latitude, longitude)


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in km."""
    return LocationUtils.haversine_distance(lat1, lon1, lat2, lon2)


def get_region(latitude: float, longitude: float) -> str:
    """Get region name from coordinates."""
    return LocationUtils.get_region_name(latitude, longitude)
