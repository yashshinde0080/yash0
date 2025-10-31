"""SQLAlchemy ORM models for the agricultural app database."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Date, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserSettings(Base):
    """User preferences and profile."""
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True, default=1)
    farmer_name = Column(String(100))
    phone_number = Column(String(20))
    profile_photo_path = Column(String(500))
    app_language = Column(String(5), default='en', nullable=False)
    voice_language = Column(String(5), default='en', nullable=False)
    default_latitude = Column(Float)
    default_longitude = Column(Float)
    default_location_name = Column(String(200))
    auto_detect_location = Column(Boolean, default=True)
    offline_mode = Column(Boolean, default=False)
    notifications_enabled = Column(Boolean, default=True)
    weather_alerts = Column(Boolean, default=True)
    price_alerts = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Field(Base):
    """User's agricultural fields."""
    __tablename__ = 'fields'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    size_value = Column(Float, nullable=False)
    size_unit = Column(String(20), nullable=False)  # 'acres' or 'hectares'
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String(200))
    current_crop = Column(String(100))
    planting_date = Column(Date)
    expected_harvest_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    crop_history = relationship('CropHistory', back_populates='field', cascade='all, delete-orphan')
    soil_data = relationship('SoilData', back_populates='field', cascade='all, delete-orphan')
    recommendations = relationship('Recommendation', back_populates='field', cascade='all, delete-orphan')
    disease_detections = relationship('DiseaseDetection', back_populates='field', cascade='all, delete-orphan')
    iot_devices = relationship('IoTDevice', back_populates='field', cascade='all, delete-orphan')


class CropHistory(Base):
    """Crop rotation history for each field."""
    __tablename__ = 'crop_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    field_id = Column(Integer, ForeignKey('fields.id'), nullable=False)
    crop_name = Column(String(100), nullable=False)
    crop_family = Column(String(50))
    planting_date = Column(Date, nullable=False)
    harvest_date = Column(Date)
    yield_amount = Column(Float)
    yield_unit = Column(String(20))  # 'kg', 'tons', 'quintals'
    profit = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    field = relationship('Field', back_populates='crop_history')


class SoilData(Base):
    """Cached soil property data."""
    __tablename__ = 'soil_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    field_id = Column(Integer, ForeignKey('fields.id'))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    source = Column(String(50), nullable=False)  # 'soilgrids', 'bhuvan', 'iot', 'manual'
    ph_level = Column(Float)
    organic_carbon = Column(Float)
    nitrogen_ppm = Column(Float)
    phosphorus_ppm = Column(Float)
    potassium_ppm = Column(Float)
    moisture_percent = Column(Float)
    bulk_density = Column(Float)
    clay_percent = Column(Float)
    sand_percent = Column(Float)
    silt_percent = Column(Float)
    soil_classification = Column(String(100))
    fertility_index = Column(Float)
    fetched_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    field = relationship('Field', back_populates='soil_data')


class WeatherData(Base):
    """Cached weather data and forecasts."""
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_name = Column(String(200))
    forecast_date = Column(Date, nullable=False)
    temperature_c = Column(Float)
    temp_min_c = Column(Float)
    temp_max_c = Column(Float)
    humidity_percent = Column(Float)
    wind_speed_kmh = Column(Float)
    precipitation_mm = Column(Float)
    rainfall_probability = Column(Float)
    condition = Column(String(100))
    uv_index = Column(Float)
    fetched_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)


class MarketData(Base):
    """Cached crop prices and market trends."""
    __tablename__ = 'market_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    commodity_name = Column(String(100), nullable=False)
    state = Column(String(100))
    district = Column(String(100))
    market_name = Column(String(100))
    price_per_quintal = Column(Float, nullable=False)
    price_date = Column(Date, nullable=False)
    price_change_percent = Column(Float)
    volume_traded = Column(Float)
    min_price = Column(Float)
    max_price = Column(Float)
    trend_30day_avg = Column(Float)
    trend_90day_avg = Column(Float)
    fetched_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)


class Recommendation(Base):
    """Cached crop recommendations."""
    __tablename__ = 'recommendations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    field_id = Column(Integer, ForeignKey('fields.id'))
    crop_name = Column(String(100), nullable=False)
    crop_family = Column(String(50))
    rank = Column(Integer, nullable=False)
    confidence_score = Column(Float)
    expected_yield_kg = Column(Float)
    profit_margin_percent = Column(Float)
    estimated_profit_inr = Column(Float)
    sustainability_score = Column(Float)
    reasoning = Column(Text)
    planting_season = Column(String(50))  # Kharif, Rabi, Zaid
    planting_start_month = Column(String(20))
    planting_end_month = Column(String(20))
    input_soil_ph = Column(Float)
    input_nitrogen = Column(Float)
    input_phosphorus = Column(Float)
    input_potassium = Column(Float)
    input_temperature = Column(Float)
    input_rainfall = Column(Float)
    input_humidity = Column(Float)
    generated_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    field = relationship('Field', back_populates='recommendations')


class ChatHistory(Base):
    """Store chat conversations."""
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    original_language = Column(String(5))
    translated_content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DiseaseDetection(Base):
    """Store disease detection history."""
    __tablename__ = 'disease_detections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    field_id = Column(Integer, ForeignKey('fields.id'))
    image_path = Column(String(500), nullable=False)
    disease_name = Column(String(200), nullable=False)
    disease_name_local = Column(String(200))
    confidence_score = Column(Float, nullable=False)
    severity_level = Column(String(20))  # 'low', 'medium', 'high'
    crop_type = Column(String(100))
    description = Column(Text)
    symptoms = Column(Text)  # JSON array
    treatments = Column(Text)  # JSON array
    prevention_tips = Column(Text)  # JSON array
    detected_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    field = relationship('Field', back_populates='disease_detections')


class IoTDevice(Base):
    """Connected IoT sensor configurations."""
    __tablename__ = 'iot_devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_name = Column(String(100), nullable=False)
    device_type = Column(String(50), nullable=False)  # 'bluetooth', 'wifi', 'mqtt'
    connection_string = Column(String(200))
    sensor_types = Column(Text)  # JSON array
    field_id = Column(Integer, ForeignKey('fields.id'))
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    field = relationship('Field', back_populates='iot_devices')
    sensor_readings = relationship('IoTSensorReading', back_populates='device', cascade='all, delete-orphan')


class IoTSensorReading(Base):
    """Real-time IoT sensor data."""
    __tablename__ = 'iot_sensor_readings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('iot_devices.id'), nullable=False)
    ph_level = Column(Float)
    nitrogen_ppm = Column(Float)
    phosphorus_ppm = Column(Float)
    potassium_ppm = Column(Float)
    moisture_percent = Column(Float)
    temperature_c = Column(Float)
    reading_timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    device = relationship('IoTDevice', back_populates='sensor_readings')


class SyncQueue(Base):
    """Queue for offline data sync."""
    __tablename__ = 'sync_queue'

    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_type = Column(String(50), nullable=False)  # 'field', 'crop_history', 'soil_data', 'detection'
    entity_id = Column(Integer)
    action = Column(String(20), nullable=False)  # 'create', 'update', 'delete'
    payload = Column(Text, nullable=False)  # JSON data
    status = Column(String(20), default='pending')  # 'pending', 'syncing', 'completed', 'failed'
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    synced_at = Column(DateTime)
