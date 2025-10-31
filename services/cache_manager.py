"""Cache management for API responses and ML predictions."""

import logging
from datetime import datetime, timedelta
from typing import Optional, Any

from database.db_manager import get_db
from database.models import SoilData, WeatherData, MarketData, Recommendation
from config.settings import (
    SOIL_CACHE_DAYS, WEATHER_CACHE_HOURS,
    MARKET_CACHE_HOURS, RECOMMENDATION_CACHE_DAYS
)

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages data caching with expiry."""

    def __init__(self):
        """Initialize cache manager."""
        self.db = get_db()

    # ==================== Soil Data Cache ====================

    def get_cached_soil_data(self, latitude: float, longitude: float) -> Optional[SoilData]:
        """Get cached soil data if valid."""
        try:
            session = self.db.get_session()
            soil_data = session.query(SoilData).filter(
                SoilData.latitude == latitude,
                SoilData.longitude == longitude,
                SoilData.expires_at > datetime.utcnow()
            ).first()
            session.close()
            return soil_data
        except Exception as e:
            logger.error(f'Error retrieving cached soil data: {str(e)}')
            return None

    def cache_soil_data(self, latitude: float, longitude: float, soil_data_dict: dict,
                       source: str = 'soilgrids', field_id: Optional[int] = None):
        """Cache soil data."""
        try:
            session = self.db.get_session()

            expires_at = datetime.utcnow() + timedelta(days=SOIL_CACHE_DAYS)

            cache_entry = SoilData(
                field_id=field_id,
                latitude=latitude,
                longitude=longitude,
                source=source,
                fetched_at=datetime.utcnow(),
                expires_at=expires_at,
                **soil_data_dict
            )

            session.add(cache_entry)
            session.commit()
            session.close()

            logger.info(f'Cached soil data for ({latitude}, {longitude})')
        except Exception as e:
            logger.error(f'Error caching soil data: {str(e)}')

    def cleanup_expired_soil_data(self):
        """Delete expired soil data."""
        try:
            session = self.db.get_session()
            deleted = session.query(SoilData).filter(
                SoilData.expires_at <= datetime.utcnow()
            ).delete()
            session.commit()
            session.close()
            logger.info(f'Deleted {deleted} expired soil data entries')
        except Exception as e:
            logger.error(f'Error cleaning up soil data: {str(e)}')

    # ==================== Weather Data Cache ====================

    def get_cached_weather(self, latitude: float, longitude: float,
                          forecast_date: Optional[str] = None) -> Optional[list]:
        """Get cached weather data."""
        try:
            session = self.db.get_session()
            query = session.query(WeatherData).filter(
                WeatherData.latitude == latitude,
                WeatherData.longitude == longitude,
                WeatherData.expires_at > datetime.utcnow()
            )

            if forecast_date:
                query = query.filter(WeatherData.forecast_date == forecast_date)

            results = query.all()
            session.close()
            return results if results else None
        except Exception as e:
            logger.error(f'Error retrieving cached weather: {str(e)}')
            return None

    def cache_weather_data(self, latitude: float, longitude: float, weather_list: list):
        """Cache weather forecast data."""
        try:
            session = self.db.get_session()
            expires_at = datetime.utcnow() + timedelta(hours=WEATHER_CACHE_HOURS)

            for weather_dict in weather_list:
                cache_entry = WeatherData(
                    latitude=latitude,
                    longitude=longitude,
                    fetched_at=datetime.utcnow(),
                    expires_at=expires_at,
                    **weather_dict
                )
                session.add(cache_entry)

            session.commit()
            session.close()
            logger.info(f'Cached weather for ({latitude}, {longitude})')
        except Exception as e:
            logger.error(f'Error caching weather data: {str(e)}')

    def cleanup_expired_weather_data(self):
        """Delete expired weather data."""
        try:
            session = self.db.get_session()
            deleted = session.query(WeatherData).filter(
                WeatherData.expires_at <= datetime.utcnow()
            ).delete()
            session.commit()
            session.close()
            logger.info(f'Deleted {deleted} expired weather entries')
        except Exception as e:
            logger.error(f'Error cleaning up weather data: {str(e)}')

    # ==================== Market Data Cache ====================

    def get_cached_market_prices(self, commodity: str, state: Optional[str] = None) -> Optional[list]:
        """Get cached market prices."""
        try:
            session = self.db.get_session()
            query = session.query(MarketData).filter(
                MarketData.commodity_name == commodity,
                MarketData.expires_at > datetime.utcnow()
            )

            if state:
                query = query.filter(MarketData.state == state)

            results = query.order_by(MarketData.price_date.desc()).all()
            session.close()
            return results if results else None
        except Exception as e:
            logger.error(f'Error retrieving cached market data: {str(e)}')
            return None

    def cache_market_data(self, market_data_list: list):
        """Cache market price data."""
        try:
            session = self.db.get_session()
            expires_at = datetime.utcnow() + timedelta(hours=MARKET_CACHE_HOURS)

            for market_dict in market_data_list:
                cache_entry = MarketData(
                    fetched_at=datetime.utcnow(),
                    expires_at=expires_at,
                    **market_dict
                )
                session.add(cache_entry)

            session.commit()
            session.close()
            logger.info(f'Cached {len(market_data_list)} market price entries')
        except Exception as e:
            logger.error(f'Error caching market data: {str(e)}')

    def cleanup_expired_market_data(self):
        """Delete expired market data."""
        try:
            session = self.db.get_session()
            deleted = session.query(MarketData).filter(
                MarketData.expires_at <= datetime.utcnow()
            ).delete()
            session.commit()
            session.close()
            logger.info(f'Deleted {deleted} expired market data entries')
        except Exception as e:
            logger.error(f'Error cleaning up market data: {str(e)}')

    # ==================== Recommendations Cache ====================

    def get_cached_recommendations(self, field_id: Optional[int] = None) -> Optional[list]:
        """Get cached crop recommendations."""
        try:
            session = self.db.get_session()
            query = session.query(Recommendation).filter(
                Recommendation.expires_at > datetime.utcnow()
            )

            if field_id:
                query = query.filter(Recommendation.field_id == field_id)

            results = query.order_by(Recommendation.rank).all()
            session.close()
            return results if results else None
        except Exception as e:
            logger.error(f'Error retrieving cached recommendations: {str(e)}')
            return None

    def cache_recommendations(self, recommendations_list: list, field_id: Optional[int] = None):
        """Cache crop recommendations."""
        try:
            session = self.db.get_session()
            expires_at = datetime.utcnow() + timedelta(days=RECOMMENDATION_CACHE_DAYS)

            for rec_dict in recommendations_list:
                cache_entry = Recommendation(
                    field_id=field_id,
                    generated_at=datetime.utcnow(),
                    expires_at=expires_at,
                    **rec_dict
                )
                session.add(cache_entry)

            session.commit()
            session.close()
            logger.info(f'Cached {len(recommendations_list)} recommendations')
        except Exception as e:
            logger.error(f'Error caching recommendations: {str(e)}')

    def cleanup_expired_recommendations(self):
        """Delete expired recommendations."""
        try:
            session = self.db.get_session()
            deleted = session.query(Recommendation).filter(
                Recommendation.expires_at <= datetime.utcnow()
            ).delete()
            session.commit()
            session.close()
            logger.info(f'Deleted {deleted} expired recommendation entries')
        except Exception as e:
            logger.error(f'Error cleaning up recommendations: {str(e)}')

    # ==================== General Cache Management ====================

    def cleanup_all_expired_cache(self):
        """Cleanup all expired cache entries."""
        logger.info('Starting cache cleanup...')
        self.cleanup_expired_soil_data()
        self.cleanup_expired_weather_data()
        self.cleanup_expired_market_data()
        self.cleanup_expired_recommendations()
        logger.info('Cache cleanup completed')

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        try:
            session = self.db.get_session()

            stats = {
                'soil_entries': session.query(SoilData).count(),
                'weather_entries': session.query(WeatherData).count(),
                'market_entries': session.query(MarketData).count(),
                'recommendation_entries': session.query(Recommendation).count(),
                'total_entries': (
                    session.query(SoilData).count() +
                    session.query(WeatherData).count() +
                    session.query(MarketData).count() +
                    session.query(Recommendation).count()
                ),
            }

            session.close()
            return stats
        except Exception as e:
            logger.error(f'Error getting cache stats: {str(e)}')
            return {}


# Global cache manager instance
cache_manager = None


def get_cache_manager():
    """Get or create global cache manager."""
    global cache_manager
    if cache_manager is None:
        cache_manager = CacheManager()
    return cache_manager
