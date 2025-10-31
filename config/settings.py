"""Global app settings and constants."""

import os
from pathlib import Path

# Environment
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = BASE_DIR / 'models'
LOCALES_DIR = BASE_DIR / 'locales'
ASSETS_DIR = BASE_DIR / 'assets'

# Database
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATA_DIR}/app.db')

# Cache settings (in hours/days)
SOIL_CACHE_DAYS = int(os.getenv('SOIL_CACHE_DAYS', 30))
WEATHER_CACHE_HOURS = int(os.getenv('WEATHER_CACHE_HOURS', 6))
MARKET_CACHE_HOURS = int(os.getenv('MARKET_CACHE_HOURS', 24))
RECOMMENDATION_CACHE_DAYS = int(os.getenv('RECOMMENDATION_CACHE_DAYS', 7))

# ML Models
LLM_MODEL_PATH = os.getenv('LLM_MODEL_PATH', str(MODELS_DIR / 'llm' / 'mistral-7b-instruct-q4.gguf'))
LLM_CONTEXT_LENGTH = int(os.getenv('LLM_CONTEXT_LENGTH', 2048))
LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', 0.7))
LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', 512))

DISEASE_MODEL_PATH = os.getenv('DISEASE_MODEL_PATH', str(MODELS_DIR / 'disease_detection' / 'model.tflite'))
CROP_MODEL_PATH = os.getenv('CROP_MODEL_PATH', str(MODELS_DIR / 'crop_recommendation' / 'model.pkl'))
CROP_SCALER_PATH = os.getenv('CROP_SCALER_PATH', str(MODELS_DIR / 'crop_recommendation' / 'scaler.pkl'))

TRANSLATION_MODEL_PATH = os.getenv('TRANSLATION_MODEL_PATH', str(MODELS_DIR / 'translation'))

# Knowledge base
AGRICULTURE_KB_PATH = DATA_DIR / 'knowledge' / 'agriculture_kb.json'
DISEASE_INFO_PATH = DATA_DIR / 'knowledge' / 'disease_info.json'

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'हिन्दी',
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
    'mr': 'मराठी',
    'bn': 'বাংলা',
    'gu': 'ગુજરાતી',
    'kn': 'ಕನ್ನಡ',
    'ml': 'മലയാളം',
    'pa': 'ਪੰਜਾਬੀ',
    'or': 'ଓଡ଼ିଆ',
    'as': 'অসমীয়া',
}

# App UI Constants
APP_TITLE = 'Farmer AI'
APP_VERSION = '1.0.0'

# Colors (Material Design)
COLORS = {
    'primary': '#2E7D32',  # Green
    'primary_dark': '#1B5E20',
    'accent': '#FFA726',  # Orange
    'background': '#FAFAFA',
    'surface': '#FFFFFF',
    'error': '#D32F2F',
    'success': '#388E3C',
    'warning': '#F57C00',
    'info': '#1976D2',
}

# Font sizes
FONT_SIZES = {
    'title': 24,
    'headline': 20,
    'subheading': 16,
    'body': 14,
    'caption': 12,
}

# Timeouts (in seconds)
API_TIMEOUT = 30
LLM_TIMEOUT = 60
MODEL_INFERENCE_TIMEOUT = 30

# Batch sizes
SOIL_DATA_BATCH_SIZE = 10
WEATHER_DATA_BATCH_SIZE = 20
MARKET_DATA_BATCH_SIZE = 50

# Retention limits
MAX_CHAT_MESSAGES = 50
MAX_DETECTIONS = 20
MAX_SENSOR_READINGS = 1000

# GPS Constants
GPS_ACCURACY_THRESHOLD = 50  # meters
GPS_LOCATION_REFRESH_INTERVAL = 300  # seconds (5 minutes)

# IoT Constants
IoT_SYNC_INTERVAL = 60  # seconds
BACKGROUND_SYNC_INTERVAL = 300  # seconds (5 minutes)

# Connectivity
CONNECTIVITY_CHECK_INTERVAL = 300  # seconds
CONNECTIVITY_TIMEOUT = 5  # seconds

# Feature flags
ENABLE_IoT_SENSORS = True
ENABLE_VOICE_INPUT = True
ENABLE_OFFLINE_MODE = True
ENABLE_NOTIFICATIONS = True
