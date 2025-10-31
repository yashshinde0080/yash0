"""Database connection and initialization manager."""

import logging
from pathlib import Path
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from config.settings import DATABASE_URL, DATA_DIR, DEBUG_MODE
from database.models import Base, UserSettings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and initialization."""

    def __init__(self):
        """Initialize database manager."""
        self.engine = None
        self.SessionLocal = None
        self._initialize_database()

    def _initialize_database(self):
        """Initialize database engine and create tables."""
        try:
            # Create data directory if it doesn't exist
            DATA_DIR.mkdir(parents=True, exist_ok=True)

            # Create SQLite engine
            if DEBUG_MODE:
                # In-memory SQLite for testing
                self.engine = create_engine(
                    'sqlite:///:memory:',
                    connect_args={'check_same_thread': False},
                    poolclass=StaticPool,
                    echo=False
                )
            else:
                # File-based SQLite
                self.engine = create_engine(
                    DATABASE_URL,
                    connect_args={'check_same_thread': False},
                    echo=DEBUG_MODE
                )

            # Enable foreign keys
            @event.listens_for(self.engine, 'connect')
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute('PRAGMA foreign_keys=ON')
                cursor.close()

            # Create all tables
            Base.metadata.create_all(self.engine)

            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )

            # Initialize default user settings
            self._initialize_default_data()

            # Create indexes
            self._create_indexes()

            logger.info('Database initialized successfully')

        except Exception as e:
            logger.error(f'Failed to initialize database: {str(e)}')
            raise

    def _initialize_default_data(self):
        """Initialize default data (user settings)."""
        try:
            session = self.SessionLocal()

            # Check if default user exists
            user = session.query(UserSettings).filter_by(id=1).first()

            if not user:
                # Create default user settings
                default_user = UserSettings(
                    id=1,
                    farmer_name='Farmer',
                    app_language='en',
                    voice_language='en',
                    auto_detect_location=True,
                    notifications_enabled=True
                )
                session.add(default_user)
                session.commit()
                logger.info('Default user settings created')

            session.close()
        except Exception as e:
            logger.error(f'Failed to initialize default data: {str(e)}')
            raise

    def _create_indexes(self):
        """Create database indexes for performance."""
        try:
            session = self.SessionLocal()

            indexes = [
                'CREATE INDEX IF NOT EXISTS idx_fields_location ON fields(latitude, longitude)',
                'CREATE INDEX IF NOT EXISTS idx_soil_data_location ON soil_data(latitude, longitude)',
                'CREATE INDEX IF NOT EXISTS idx_soil_data_expires ON soil_data(expires_at)',
                'CREATE INDEX IF NOT EXISTS idx_weather_data_location_date ON weather_data(latitude, longitude, forecast_date)',
                'CREATE INDEX IF NOT EXISTS idx_weather_data_expires ON weather_data(expires_at)',
                'CREATE INDEX IF NOT EXISTS idx_market_data_commodity ON market_data(commodity_name, price_date)',
                'CREATE INDEX IF NOT EXISTS idx_market_data_expires ON market_data(expires_at)',
                'CREATE INDEX IF NOT EXISTS idx_recommendations_field ON recommendations(field_id)',
                'CREATE INDEX IF NOT EXISTS idx_recommendations_expires ON recommendations(expires_at)',
                'CREATE INDEX IF NOT EXISTS idx_chat_history_timestamp ON chat_history(timestamp)',
                'CREATE INDEX IF NOT EXISTS idx_disease_detections_field ON disease_detections(field_id)',
                'CREATE INDEX IF NOT EXISTS idx_iot_readings_device ON iot_sensor_readings(device_id, reading_timestamp)',
                'CREATE INDEX IF NOT EXISTS idx_sync_queue_status ON sync_queue(status)',
            ]

            for index_sql in indexes:
                session.execute(text(index_sql))

            session.commit()
            logger.info('Database indexes created')
            session.close()
        except Exception as e:
            logger.error(f'Failed to create indexes: {str(e)}')
            # Don't raise - indexes are optional for functionality

    def get_session(self) -> Session:
        """Get a new database session."""
        if not self.SessionLocal:
            raise RuntimeError('Database not initialized')
        return self.SessionLocal()

    def close(self):
        """Close database connections."""
        if self.engine:
            self.engine.dispose()
            logger.info('Database connection closed')

    def health_check(self) -> bool:
        """Check if database is healthy."""
        try:
            session = self.SessionLocal()
            session.execute(text('SELECT 1'))
            session.close()
            return True
        except Exception as e:
            logger.error(f'Database health check failed: {str(e)}')
            return False


# Global database manager instance
db_manager = None


def init_db():
    """Initialize global database manager."""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager


def get_db():
    """Get global database manager."""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager
