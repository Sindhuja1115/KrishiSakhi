# Krishi Sakhi - AI-Powered Farming Assistant

🌾 **AI-powered farming assistant for Kerala farmers with bilingual support (English/Malayalam)**

## Overview

Krishi Sakhi is a comprehensive farming assistant that leverages AI technology to help Kerala farmers with crop management, disease detection, weather advisory, and community insights. Built with Python using FastAPI backend and Streamlit frontend.

## 🎯 Core Features

### 🌱 Farm Management
- **Farmer Profiles**: Complete registration and profile management
- **Multi-Farm Support**: Manage multiple plots with different crops
- **Activity Tracking**: Record daily farming activities with cost tracking
- **Crop Management**: Track different crop types, varieties, and growth stages

### 🤖 AI-Powered Features
- **Disease Detection**: Upload crop images for AI-powered disease identification using Hugging Face models
- **Smart Chat Assistant**: Conversational interface with farming expertise in English & Malayalam
- **Voice Interaction**: Voice-enabled chat with speech recognition and text-to-speech
- **Predictive Analytics**: Weather-based farming recommendations

### 🌤️ Weather Intelligence
- **Kerala-Specific Forecasts**: Detailed weather data for all Kerala districts
- **Farming Advisories**: Actionable guidance based on weather conditions
- **Activity Recommendations**: What to do and what to avoid based on weather
- **Crop-Specific Alerts**: Weather alerts tailored to different crops

### 📚 Knowledge Base
- **Crop Guides**: Comprehensive cultivation guides for Kerala crops
- **Disease Encyclopedia**: Detailed information about plant diseases and treatments
- **Government Schemes**: Information about farming schemes and subsidies
- **Best Practices**: Expert-curated farming techniques and tips

### 👥 Community Features
- **Disease Alerts**: Community-wide disease and pest alerts
- **Regional Statistics**: Farming trends and statistics by region
- **Peer Learning**: Connect with other farmers in your area
- **Expert Network**: Access to agricultural experts and advisors

### 📊 Analytics & Reports
- **Activity Analytics**: Track farming activities and patterns
- **Cost Analysis**: Monitor expenses and profitability
- **Yield Tracking**: Record and analyze crop yields
- **Performance Metrics**: Dashboard with key farming indicators

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLite, Python
- **Frontend**: Streamlit, Plotly (charts), PIL (image processing)
- **AI/ML**: Hugging Face Transformers, PyTorch, Computer Vision models
- **Voice**: SpeechRecognition, gTTS, pyttsx3 (optional)
- **Database**: SQLite with comprehensive schema
- **Deployment**: Local development, easily deployable to cloud

## 📁 Project Structure

```
krishi-sakhi/
├── backend/
│   ├── main.py                 # FastAPI application with all endpoints
│   ├── models/
│   │   └── database.py         # Database models and initialization
│   ├── services/
│   │   ├── ai_service.py       # AI/ML services (Hugging Face integration)
│   │   └── weather_service.py  # Weather API and advisories
│   └── utils/
│       └── translations.py     # Bilingual support utilities
├── frontend/
│   ├── app.py                 # Streamlit application with all pages
│   └── voice_assistant.py      # Voice recognition and TTS
├── assets/
│   ├── sample_data.py          # Demo data and mock datasets
│   └── crop_images.py          # Sample crop images and disease info
└── README.md                   # This file
```

## 🚀 Quick Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Install required packages**
   ```bash
   pip install fastapi uvicorn streamlit plotly pillow pandas requests
   pip install transformers torch torchvision pydantic python-jose
   ```

   **For voice features (optional):**
   ```bash
   pip install speechrecognition gtts pygame pyttsx3
   ```

2. **Initialize the database**
   ```bash
   cd backend
   python models/database.py
   ```

### Running the Application

1. **Start the FastAPI Backend**
   ```bash
   # Terminal 1
   cd backend
   python main.py
   ```
   The API will be available at: http://localhost:8000

2. **Start the Streamlit Frontend**
   ```bash
   # Terminal 2 (new terminal)
   cd frontend
   streamlit run app.py
   ```
   The web app will open at: http://localhost:8501

## 🎮 Demo Usage

### Quick Demo Login
1. Open the Streamlit app
2. Click "🎯 Start Demo" on the login page
3. Explore all features with pre-populated demo data

### Manual Login (Demo Credentials)
- **Phone**: +919876543210
- **Password**: any password (demo mode accepts any password)

## 💡 Key Features Demo

### 1. 🔬 AI Disease Detection
- Navigate to "Disease Detection"
- Upload any plant image
- Select crop type (Rice, Coconut, Pepper, etc.)
- Get AI-powered disease identification with treatment suggestions

### 2. 🤖 AI Chat Assistant
- Go to "AI Assistant"
- Ask farming questions in English or Malayalam
- Try voice chat (click microphone icon)
- Get expert advice on crops, diseases, weather

### 3. 🌤️ Weather Advisory
- Check "Weather" section
- Select your Kerala district
- View 5-day forecasts with farming recommendations
- Get activity suggestions based on weather

### 4. 📊 Farm Analytics
- Visit "Reports" section
- Track your farming activities and costs
- View interactive charts and trends
- Export detailed reports

### 5. 👥 Community Dashboard
- Check "Community" section
- View regional disease alerts
- See farming statistics for your area
- Connect with fellow farmers

## 🎯 Sample Voice Commands

**English:**
- "What is the best time to plant rice?"
- "Show me the weather forecast"
- "How to control pests in coconut?"
- "Go to dashboard"

**Malayalam:**
- "നെല്ല് എങ്ങനെ നടാം?" (How to plant rice?)
- "കാലാവസ്ഥ കാണിക്കുക" (Show weather)
- "ഡാഷ്ബോർഡ് കാണിക്കുക" (Show dashboard)

## 🔗 API Documentation

When backend is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **API Schema**: http://localhost:8000/redoc

### Key API Endpoints

```python
# Authentication
POST /api/auth/login
POST /api/auth/register
POST /api/auth/demo-login

# Farm Management
GET /api/farms
POST /api/farms
GET /api/activities
POST /api/activities

# AI Features
POST /api/ai/detect-disease
POST /api/ai/chat

# Weather & Advisory
GET /api/weather?location={district}

# Knowledge & Community
GET /api/knowledge/crops
GET /api/knowledge/diseases
GET /api/community/alerts
```

## 🛠️ Development

### Adding New Features

1. **Backend (FastAPI)**
   - Add new endpoints in `backend/main.py`
   - Extend database schema in `backend/models/database.py`
   - Add AI services in `backend/services/`

2. **Frontend (Streamlit)**
   - Add new pages in `frontend/main.py`
   - Create components and forms
   - Integrate with backend APIs

3. **AI Features**
   - Extend `backend/services/ai_service.py`
   - Add new Hugging Face models
   - Implement custom AI logic

### Database Schema

The SQLite database includes:
- **farmers**: User accounts and profiles
- **farms**: Farm details and properties
- **activities**: Daily farming activities
- **disease_detections**: AI analysis results
- **reminders**: Notifications and alerts
- **chat_history**: AI conversation logs

### Customization Options

- **Languages**: Add new languages in `utils/translations.py`
- **Crops**: Extend crop data in `assets/sample_data.py`
- **AI Models**: Swap models in `services/ai_service.py`
- **UI Themes**: Modify CSS in `frontend/main.py`

## 🌐 Production Deployment

For production use:

1. **Environment Setup**
   - Set secure database credentials
   - Configure API keys (weather, AI services)
   - Set production domain URLs

2. **Database Migration**
   - Migrate from SQLite to PostgreSQL
   - Set up backup strategies
   - Configure connection pooling

3. **Security**
   - Enable HTTPS
   - Configure CORS policies
   - Implement rate limiting
   - Use secure JWT secrets

4. **Performance**
   - Implement Redis caching
   - Optimize AI model loading
   - Set up load balancing
   - Use CDN for static assets

## 🤝 Contributing

This is a hackathon prototype. For production use:

1. **Security**: Implement proper authentication and authorization
2. **Performance**: Optimize database queries and AI model loading
3. **Testing**: Add unit tests and integration tests
4. **Documentation**: Expand API and user documentation
5. **Monitoring**: Add logging and monitoring systems

## 📱 Mobile Responsiveness

The Streamlit interface is optimized for:
- 📱 Mobile phones (iOS/Android)
- 📱 Tablets (iPad/Android tablets)
- 💻 Desktop computers
- 🌐 All modern web browsers

## 🌍 Multilingual Support

Currently supports:
- 🇺🇸 English
- 🇮🇳 മലയാളം (Malayalam)

Easy to extend to other Indian languages by updating `utils/translations.py`

## 🔧 Troubleshooting

### Common Issues

1. **Backend not starting**
   ```bash
   # Check if port 8000 is free
   lsof -i :8000
   # Kill existing process if needed
   kill -9 <PID>
   ```

2. **Frontend connection errors**
   - Ensure backend is running on localhost:8000
   - Check firewall settings
   - Verify API endpoints in frontend code

3. **Voice features not working**
   - Voice features are optional
   - Install additional packages if needed
   - Check browser microphone permissions

4. **AI models loading slowly**
   - First-time model downloads take time
   - Ensure stable internet connection
   - Models are cached after first use

### Performance Optimization

- **Database**: Regular cleanup of old records
- **AI Models**: Use GPU if available (CUDA)
- **Caching**: Implement Redis for frequently accessed data
- **Images**: Optimize image sizes for disease detection

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review API documentation at http://localhost:8000/docs
3. Examine log files for error details


**Built with ❤️ for Kerala Farmers by the Krishi Sakhi Team**
