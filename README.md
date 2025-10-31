# Farmer AI - Agricultural Decision Support System

An AI-powered mobile application providing personalized agricultural guidance to farmers using machine learning, satellite data, and multilingual support.

## 🌾 Overview

Farmer AI is a comprehensive agricultural decision support system that helps farmers make informed decisions about crop selection, disease management, and resource optimization. The app works seamlessly in offline environments with local AI models and caching.

**Key Features:**
- 🤖 AI-powered crop recommendations based on soil, weather, and market data
- 📸 Disease detection from crop images
- 🗣️ Multilingual voice and chat interface (12 Indian languages)
- 🌐 Offline-first architecture with automatic sync
- 🌍 Real-time weather, market prices, and soil data
- 🚜 Multi-field management with crop rotation tracking
- 📊 Profit and sustainability analysis
- 🔌 IoT sensor integration for precision farming

## 🚀 Quick Start

### Installation

```bash
# Clone and navigate
cd yash0

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python -c "from database.db_manager import init_db; init_db()"

# Run the app
python main.py
```

## 📱 Application Features

### 1. Home Dashboard
- Current weather and 7-day forecast
- Top crop recommendations with profit estimates
- Current soil status (pH, NPK, moisture)
- Market prices for major crops

### 2. AI Chat Assistant
- Ask agricultural questions in 12 Indian languages
- Voice input/output support
- Context-aware responses using local knowledge base
- Works completely offline

### 3. Disease Detection
- Capture or upload leaf/crop images
- AI-powered disease identification
- Treatment recommendations
- Save to history

### 4. Field Management
- Add and track multiple fields
- Field-specific recommendations
- Crop rotation tracking
- Historical yield records

### 5. Settings
- Language selection (12 Indian languages)
- Location management
- IoT sensor pairing
- Offline mode
- Cache management

## 🌐 Supported Languages

Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese, English

## 📊 Technology Stack

- **Framework:** Flet (Python)
- **Database:** SQLite
- **ML:** scikit-learn, TensorFlow Lite, Mistral-7B LLM
- **Translation:** IndicTrans2
- **APIs:** WeatherAPI.com, SoilGrids, Bhuvan, Agmarknet

## 🔌 Data Sources

- **Satellite:** SoilGrids (soil), Bhuvan (ISRO)
- **Weather:** WeatherAPI.com
- **Markets:** Agmarknet API
- **IoT:** Bluetooth/WiFi sensors (optional)

## 🤖 AI Models

- **Crop Recommendation:** Random Forest/Gradient Boosting
- **Disease Detection:** CNN with TensorFlow Lite
- **Chat:** Local Mistral-7B LLM (offline)
- **Translation:** IndicTrans2 (offline)

## ✅ Development Status

### Completed ✓
- Project structure and configuration
- Database layer (SQLAlchemy ORM, 12 tables)
- Core services framework
- Cache management
- Offline coordination
- Utility functions (connectivity, location, formatters, validators)
- Weather service integration
- Requirements and environment setup

### In Progress 🔄
- ML components (crop recommendation, disease detection)
- AI components (LLM engine, RAG, translation)
- UI screens (Flet components)
- Main app entry point

### Planned 📋
- Integration testing
- Performance optimization
- Deployment preparation

## 📞 Support

See PLANNING.md for detailed technical specifications.