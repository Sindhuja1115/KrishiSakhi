"""
Krishi Sakhi Frontend - Streamlit Application
AI-Powered Farming Assistant for Kerala Farmers
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import io
import base64
import json
import random
from voice_assistant import VoiceAssistant
try:
    import speech_recognition as sr  # STT
    STT_AVAILABLE = True
except Exception:
    STT_AVAILABLE = False
try:
    from streamlit_mic_recorder import mic_recorder
    MIC_AVAILABLE = True
except Exception:
    MIC_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Krishi Sakhi - AI Farming Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Kerala theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E7D32, #FFC107);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
    }
    
    .weather-card {
        background: linear-gradient(135deg, #81C784, #AED581);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .disease-alert {
        background: #FFF3E0;
        border: 1px solid #FF9800;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #E8F5E8, #FFF8E1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"
if 'language' not in st.session_state:
    st.session_state.language = "en"
if 'farmer_data' not in st.session_state:
    st.session_state.farmer_data = None
if 'voice_assistant' not in st.session_state:
    st.session_state.voice_assistant = VoiceAssistant()

# API base URL
API_BASE = "http://localhost:8000/api"

# Helper functions
def make_api_request(endpoint, method="GET", data=None, headers=None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE}{endpoint}"
        if headers is None:
            headers = {}
        
        if st.session_state.access_token:
            headers["Authorization"] = f"Bearer {st.session_state.access_token}"
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None

def get_translation(key, language="en"):
    """Get translation for UI text"""
    translations = {
        "en": {
            "dashboard": "Dashboard",
            "my_farms": "My Farms",
            "activities": "Activities",
            "disease_detection": "Disease Detection",
            "weather": "Weather",
            "ai_chat": "AI Assistant",
            "knowledge_base": "Knowledge Base",
            "community": "Community",
            "reports": "Reports",
            "welcome": "Welcome to Krishi Sakhi",
            "login": "Login",
            "register": "Register",
            "logout": "Logout",
            "create_account": "Create New Account",
            "full_name": "Full Name",
            "phone_number": "Phone Number",
            "email_address": "Email Address",
            "location": "Location",
            "preferred_language": "Preferred Language",
            "password": "Password",
            "confirm_password": "Confirm Password",
            "registration_successful": "Registration successful! Welcome to Krishi Sakhi!",
            "registration_failed": "Registration failed. Phone number or email may already be registered.",
            "fill_all_fields": "Please fill in all fields",
            "passwords_dont_match": "Passwords do not match",
            "password_too_short": "Password must be at least 6 characters long",
            "invalid_phone": "Please enter a valid Indian phone number (+91XXXXXXXXXX)",
            "invalid_email": "Please enter a valid email address",
            "choose_language": "Choose your preferred language:",
            "language_selected": "Language Selected",
            "weather_advisory": "Weather Advisory",
            "select_location": "Select Location",
            "five_day_forecast": "5-Day Forecast",
            "farming_advisory": "Farming Advisory",
            "good_for_planting": "Good for planting",
            "avoid_activities": "Avoid outdoor activities",
            "harvest_time": "Harvest time",
            "fertilizer_time": "Apply fertilizer",
            "irrigation_needed": "Irrigation needed",
            "detection_results": "Detection Results",
            "disease_label": "Disease",
            "confidence_label": "Confidence",
            "severity_label": "Severity",
            "symptoms_label": "Symptoms",
            "treatment_label": "Treatment",
            "prevention_label": "Prevention",
            "analyzing_image": "Analyzing image with AI...",
            "speak_replies": "Speak replies",
            "voice_chat": "Voice Chat",
            "add_new_farm": "Add New Farm",
            "farm_name": "Farm Name",
            "land_size_hectares": "Land Size (hectares)",
            "soil_type": "Soil Type",
            "irrigation_type": "Irrigation Type",
            "crop_types": "Crop Types",
            "add_farm": "Add Farm",
            "farm_added_success": "Farm added successfully!",
            "filter_by_activity": "Filter by Activity",
            "filter_by_crop": "Filter by Crop",
            "filter_by_farm": "Filter by Farm",
            "no_activities_found": "No activities found for the selected filters.",
            "record_new_activity": "Record New Activity",
            "select_farm": "Select Farm",
            "activity_type": "Activity Type",
            "date_label": "Date",
            "crop_name_opt": "Crop Name (optional)",
            "quantity_opt": "Quantity (optional)",
            "cost_opt": "Cost (₹, optional)",
            "description": "Description",
            "notes_opt": "Notes (optional)",
            "record_activity": "Record Activity",
            "activity_recorded_success": "Activity recorded successfully!",
            "label_farm": "Farm",
            "label_crop": "Crop",
            "label_qty": "Qty",
            "label_cost": "Cost",
            "community_dashboard": "Community Dashboard",
            "community_alerts": "Community Alerts",
            "affected_farms": "Affected Farms",
            "regional_stats": "Regional Statistics",
            "disease_reports_title": "Disease Reports (Last 30 Days)",
            "farmers_by_crop": "Farmers by Crop Type",
            "discussion_forum": "Discussion Forum",
            "forum_placeholder": "Community discussion forum coming soon! Connect with fellow farmers, share experiences, and get expert advice.",
            "date": "Date",
            "read_full_guide": "Read Full Guide"
        },
        "ml": {
            "dashboard": "ഡാഷ്ബോർഡ്",
            "my_farms": "എന്റെ കൃഷിയിടങ്ങൾ",
            "activities": "പ്രവർത്തനങ്ങൾ",
            "disease_detection": "രോഗ നിർണയം",
            "weather": "കാലാവസ്ഥ",
            "ai_chat": "AI സഹായി",
            "knowledge_base": "അറിവ് ശേഖരം",
            "community": "കമ്മ്യൂണിറ്റി",
            "reports": "റിപ്പോർട്ടുകൾ",
            "welcome": "കൃഷി സഖിയിലേക്ക് സ്വാഗതം",
            "login": "ലോഗിൻ",
            "register": "രജിസ്റ്റർ",
            "logout": "ലോഗ് ഔട്ട്",
            "create_account": "പുതിയ അക്കൗണ്ട് സൃഷ്ടിക്കുക",
            "full_name": "പൂർണ്ണ നാമം",
            "phone_number": "ഫോൺ നമ്പർ",
            "email_address": "ഇമെയിൽ വിലാസം",
            "location": "സ്ഥലം",
            "preferred_language": "ഇഷ്ടപ്പെട്ട ഭാഷ",
            "password": "പാസ്‌വേഡ്",
            "confirm_password": "പാസ്‌വേഡ് സ്ഥിരീകരിക്കുക",
            "registration_successful": "രജിസ്ട്രേഷൻ വിജയകരമാണ്! കൃഷി സഖിയിലേക്ക് സ്വാഗതം!",
            "registration_failed": "രജിസ്ട്രേഷൻ പരാജയപ്പെട്ടു. ഫോൺ നമ്പർ അല്ലെങ്കിൽ ഇമെയിൽ ഇതിനകം രജിസ്റ്റർ ചെയ്തിരിക്കാം.",
            "fill_all_fields": "ദയവായി എല്ലാ ഫീൽഡുകളും പൂരിപ്പിക്കുക",
            "passwords_dont_match": "പാസ്‌വേഡുകൾ പൊരുത്തപ്പെടുന്നില്ല",
            "password_too_short": "പാസ്‌വേഡ് കുറഞ്ഞത് 6 അക്ഷരങ്ങൾ ഉണ്ടായിരിക്കണം",
            "invalid_phone": "ദയവായി സാധുവായ ഇന്ത്യൻ ഫോൺ നമ്പർ നൽകുക (+91XXXXXXXXXX)",
            "invalid_email": "ദയവായി സാധുവായ ഇമെയിൽ വിലാസം നൽകുക",
            "choose_language": "നിങ്ങളുടെ ഇഷ്ടപ്പെട്ട ഭാഷ തിരഞ്ഞെടുക്കുക:",
            "language_selected": "ഭാഷ തിരഞ്ഞെടുത്തു",
            "weather_advisory": "കാലാവസ്ഥ ഉപദേശം",
            "select_location": "സ്ഥലം തിരഞ്ഞെടുക്കുക",
            "five_day_forecast": "5 ദിവസത്തെ കാലാവസ്ഥ പ്രവചനം",
            "farming_advisory": "കൃഷി ഉപദേശം",
            "good_for_planting": "നടീലിന് നല്ലത്",
            "avoid_activities": "പുറത്തെ പ്രവർത്തനങ്ങൾ ഒഴിവാക്കുക",
            "harvest_time": "വിളവെടുപ്പ് സമയം",
            "fertilizer_time": "വളം ചേർക്കുക",
            "irrigation_needed": "ജലസേചനം ആവശ്യം",
            "detection_results": "നിർണയ ഫലം",
            "disease_label": "രോഗം",
            "confidence_label": "വിശ്വാസ്യത",
            "severity_label": "തീവ്രത",
            "symptoms_label": "ലക്ഷണങ്ങൾ",
            "treatment_label": "ചികിത്സ",
            "prevention_label": "പ്രതിരോധം",
            "analyzing_image": "AI ഉപയോഗിച്ച് ചിത്രം വിശകലനം ചെയ്യുന്നു...",
            "speak_replies": "മറുപടികൾ ശബ്ദമായി സംസാരിക്കുക",
            "voice_chat": "വോയ്സ് ചാറ്റ്",
            "add_new_farm": "പുതിയ കൃഷിയിടം ചേർക്കുക",
            "farm_name": "ഫാം പേര്",
            "land_size_hectares": "ഭൂമിയുടെ വലിപ്പം (ഹെക്ടർ)",
            "soil_type": "മണ്ണിന്റെ തരം",
            "irrigation_type": "ജലസേചന രീതി",
            "crop_types": "വിളകളുടെ തരം",
            "add_farm": "ഫാം ചേർക്കുക",
            "farm_added_success": "ഫാം വിജയകരമായി ചേർത്തു!",
            "filter_by_activity": "പ്രവർത്തനം അനുസരിച്ച് ഫിൽറ്റർ",
            "filter_by_crop": "വിള അനുസരിച്ച് ഫിൽറ്റർ",
            "filter_by_farm": "ഫാം അനുസരിച്ച് ഫിൽറ്റർ",
            "no_activities_found": "തിരഞ്ഞെടുത്ത ഫിൽറ്ററുകൾക്ക് പ്രവർത്തനങ്ങൾ കണ്ടെത്തിയില്ല.",
            "record_new_activity": "പുതിയ പ്രവർത്തനം രേഖപ്പെടുത്തുക",
            "select_farm": "ഫാം തിരഞ്ഞെടുക്കുക",
            "activity_type": "പ്രവർത്തനത്തിന്റെ തരം",
            "date_label": "തീയതി",
            "crop_name_opt": "വിളയുടെ പേര് (ഐച്ഛികം)",
            "quantity_opt": "അളവ് (ഐച്ഛികം)",
            "cost_opt": "ചെലവ് (₹, ഐച്ഛികം)",
            "description": "വിവരണം",
            "notes_opt": "കുറിപ്പുകൾ (ഐച്ഛികം)",
            "record_activity": "പ്രവർത്തനം രേഖപ്പെടുത്തുക",
            "activity_recorded_success": "പ്രവർത്തനം വിജയകരമായി രേഖപ്പെടുത്തി!",
            "label_farm": "ഫാം",
            "label_crop": "വിള",
            "label_qty": "അളവ്",
            "label_cost": "ചെലവ്",
            "community_dashboard": "കമ്മ്യൂണിറ്റി ഡാഷ്ബോർഡ്",
            "community_alerts": "കമ്മ്യൂണിറ്റി അലർട്ടുകൾ",
            "affected_farms": "ബാധിത ഫാമുകൾ",
            "regional_stats": "പ്രാദേശിക സ്ഥിതിവിവരക്കണക്കുകൾ",
            "disease_reports_title": "രോഗ റിപ്പോർട്ടുകൾ (കഴിഞ്ഞ 30 ദിവസം)",
            "farmers_by_crop": "വിളപ്രകാരം കർഷകരുടെ എണ്ണം",
            "discussion_forum": "ചർച്ചാ ഫോറം",
            "forum_placeholder": "കമ്മ്യൂണിറ്റി ചർച്ചാ ഫോറം വരുന്നു! സഹകർഷകരുമായി ബന്ധപ്പെടുക, അനുഭവങ്ങൾ പങ്കിടുക, വിദഗ്ധ സഹായം നേടുക.",
            "date": "തീയതി",
            "read_full_guide": "പൂർണ്ണ ഗൈഡ് വായിക്കുക"
        }
    }
    return translations.get(language, {}).get(key, translations["en"].get(key, key))

# Authentication functions
def login_user(phone, password):
    """Login user"""
    data = {"phone": phone, "password": password}
    response = make_api_request("/auth/login", "POST", data)
    
    if response:
        st.session_state.authenticated = True
        st.session_state.access_token = response["access_token"]
        st.session_state.farmer_id = response["farmer_id"]
        return True
    return False

def register_user(name, phone, email, password, location, language="en"):
    """Register new user"""
    data = {
        "name": name,
        "phone": phone,
        "email": email,
        "password": password,
        "location": location,
        "language": language
    }
    response = make_api_request("/auth/register", "POST", data)
    
    if response:
        st.session_state.authenticated = True
        st.session_state.access_token = response["access_token"]
        st.session_state.farmer_id = response["farmer_id"]
        return True
    return False

def demo_login():
    """Demo login"""
    response = make_api_request("/auth/demo-login", "POST")
    
    if response:
        st.session_state.authenticated = True
        st.session_state.access_token = response["access_token"]
        st.session_state.farmer_id = response["farmer_id"]
        return True
    return False

def get_farmer_profile():
    """Get farmer profile"""
    if not st.session_state.farmer_data:
        response = make_api_request("/farmers/profile")
        if response:
            st.session_state.farmer_data = response
    return st.session_state.farmer_data

# Page components
def show_login_page():
    """Show login page"""
    st.markdown('<div class="main-header"><h1>🌾 കൃഷി സഖി - Krishi Sakhi</h1><p>AI-Powered Farming Assistant for Kerala Farmers</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Login / ലോഗിൻ")
        
        tab1, tab2, tab3 = st.tabs(["Login", "Register", "Demo"])
        
        with tab1:
            phone = st.text_input("Phone Number", placeholder="+91XXXXXXXXXX")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            if st.button("Login", use_container_width=True):
                if phone and password:
                    if login_user(phone, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.error("Please fill in all fields")
        
        with tab2:
            st.info("📝 Create New Account")
            
            # Language selection at the top
            st.subheader("🌐 Select Your Preferred Language")
            col_lang1, col_lang2, col_lang3 = st.columns([1, 2, 1])
            
            with col_lang2:
                selected_language = st.radio(
                    get_translation("choose_language", "en"),  # Always show in English for clarity
                    ["English", "മലയാളം"],
                    horizontal=True,
                    key="reg_language"
                )
            
            st.markdown("---")
            
            # Set current language based on selection
            current_lang = "ml" if selected_language == "മലയാളം" else "en"
            
            with st.form("registration_form"):
                st.subheader(f"📋 {get_translation('create_account', current_lang)}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input(get_translation("full_name", current_lang), placeholder="Enter your full name")
                    phone = st.text_input(get_translation("phone_number", current_lang), placeholder="+91XXXXXXXXXX")
                    email = st.text_input(get_translation("email_address", current_lang), placeholder="your.email@example.com")
                
                with col2:
                    location = st.selectbox(get_translation("location", current_lang), [
                        "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha",
                        "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad",
                        "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"
                    ])
                    password = st.text_input(get_translation("password", current_lang), type="password", placeholder="Create a strong password")
                    confirm_password = st.text_input(get_translation("confirm_password", current_lang), type="password", placeholder="Confirm your password")
                
                # Language confirmation
                st.info(f"✅ **{get_translation('preferred_language', current_lang)}:** {selected_language}")
                
                if st.form_submit_button("Register", use_container_width=True):
                    # Validation
                    if not all([name, phone, email, location, password, confirm_password]):
                        st.error(get_translation("fill_all_fields", current_lang))
                    elif password != confirm_password:
                        st.error(get_translation("passwords_dont_match", current_lang))
                    elif len(password) < 6:
                        st.error(get_translation("password_too_short", current_lang))
                    elif not phone.startswith("+91") or len(phone) != 13:
                        st.error(get_translation("invalid_phone", current_lang))
                    elif "@" not in email or "." not in email:
                        st.error(get_translation("invalid_email", current_lang))
                    else:
                        lang_code = "ml" if selected_language == "മലയാളം" else "en"
                        if register_user(name, phone, email, password, location, lang_code):
                            # Set the selected language in session state
                            st.session_state.language = lang_code
                            st.success(get_translation("registration_successful", current_lang))
                            st.rerun()
                        else:
                            st.error(get_translation("registration_failed", current_lang))
        
        with tab3:
            st.info("🚀 Quick Demo Access")
            st.write("Experience Krishi Sakhi without registration")
            
            if st.button("🎯 Start Demo", use_container_width=True):
                if demo_login():
                    st.success("Welcome to Krishi Sakhi Demo!")
                    st.rerun()

def show_dashboard():
    """Show dashboard"""
    if st.session_state.language == "ml":
        dashboard_title = "🌾 കൃഷി സഖി ഡാഷ്ബോർഡ്"
        welcome_text = "വീണ്ടും സ്വാഗതം"
    else:
        dashboard_title = "🌾 Krishi Sakhi Dashboard"
        welcome_text = "Welcome back"
    
    st.markdown(f'<div class="main-header"><h1>{dashboard_title}</h1></div>', unsafe_allow_html=True)
    
    # Get farmer profile
    farmer = get_farmer_profile()
    if farmer:
        st.write(f"{welcome_text}, {farmer['name']}! 🙏")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.language == "ml":
            st.metric("🏡 എന്റെ കൃഷിയിടങ്ങൾ", "2", "+1")
        else:
            st.metric("🏡 My Farms", "2", "+1")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.language == "ml":
            st.metric("📅 പ്രവർത്തനങ്ങൾ (30d)", "15", "+5")
        else:
            st.metric("📅 Activities (30d)", "15", "+5")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.language == "ml":
            st.metric("💰 മാസിക ചെലവ്", "₹8,500", "+12%")
        else:
            st.metric("💰 Monthly Cost", "₹8,500", "+12%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.language == "ml":
            st.metric("⚠️ അലേർട്ടുകൾ", "3", "+2")
        else:
            st.metric("⚠️ Alerts", "3", "+2")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.language == "ml":
            st.subheader("📊 മാസിക പ്രവർത്തനങ്ങൾ")
            activities_data = {
                "Activity": ["നടീൽ", "ജലസേചനം", "വളം", "കീടനിയന്ത്രണം", "വിളവെടുപ്പ്"],
                "Count": [4, 8, 3, 2, 3]
            }
        else:
            st.subheader("📊 Monthly Activities")
            activities_data = {
                "Activity": ["Sowing", "Watering", "Fertilizing", "Pest Control", "Harvesting"],
                "Count": [4, 8, 3, 2, 3]
            }
        fig = px.bar(activities_data, x="Activity", y="Count", 
                    color="Count", color_continuous_scale="Greens")
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        if st.session_state.language == "ml":
            st.subheader("💸 ചെലവ് പ്രവണതകൾ")
        else:
            st.subheader("💸 Cost Trends")
        # Mock data for cost trends
        dates = [datetime.now() - timedelta(days=30-i) for i in range(0, 30, 5)]
        costs = [1200, 1500, 800, 2000, 1800, 2200]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=costs, mode='lines+markers',
                               line=dict(color='#4CAF50', width=3),
                               marker=dict(size=8)))
        fig.update_layout(title="Daily Costs (₹)", xaxis_title="Date", yaxis_title="Amount")
        st.plotly_chart(fig, width='stretch')
    
    # Weather and alerts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="weather-card"><h3>🌤️ Today\'s Weather</h3><p>Partly Cloudy</p><p>28°C | 75% Humidity</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="disease-alert"><h4>⚠️ Community Alert</h4><p>Blast disease reported in Rice crops near Kottayam area. Monitor your crops closely.</p></div>', unsafe_allow_html=True)

def show_farms_page():
    """Show farms management page"""
    if st.session_state.language == "ml":
        st.header("🏡 എന്റെ കൃഷിയിടങ്ങൾ")
    else:
        st.header("🏡 My Farms")
    
    # Get farms data
    farms_data = make_api_request("/farms")
    
    if farms_data:
        for farm in farms_data:
            with st.expander(f"📍 {farm['name']} - {farm['location']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Land Size:** {farm['land_size']} hectares")
                    st.write(f"**Soil Type:** {farm['soil_type']}")
                with col2:
                    st.write(f"**Irrigation:** {farm['irrigation_type']}")
                    st.write(f"**Crops:** {', '.join(farm['crop_types'])}")
                with col3:
                    st.write(f"**Created:** {farm['created_at'][:10]}")
    
    st.markdown("---")
    
    # Add new farm
    with st.expander(f"➕ {get_translation('add_new_farm', st.session_state.language)}"):
        with st.form("add_farm"):
            col1, col2 = st.columns(2)
            
            with col1:
                farm_name = st.text_input(get_translation('farm_name', st.session_state.language))
                location = st.text_input(get_translation('location', st.session_state.language))
                land_size = st.number_input(get_translation('land_size_hectares', st.session_state.language), min_value=0.1, value=1.0)
            
            with col2:
                soil_type = st.selectbox(get_translation('soil_type', st.session_state.language), ["Loamy", "Clay", "Sandy", "Red Soil", "Alluvial"])
                irrigation_type = st.selectbox(get_translation('irrigation_type', st.session_state.language), ["Drip", "Sprinkler", "Flood", "Rain-fed"])
                crop_types = st.multiselect(get_translation('crop_types', st.session_state.language), 
                    ["Rice", "Coconut", "Pepper", "Cardamom", "Rubber", "Tea", "Coffee", "Banana"])
            
            if st.form_submit_button(get_translation('add_farm', st.session_state.language)):
                data = {
                    "name": farm_name,
                    "location": location,
                    "land_size": land_size,
                    "soil_type": soil_type,
                    "irrigation_type": irrigation_type,
                    "crop_types": crop_types
                }
                
                response = make_api_request("/farms", "POST", data)
                if response:
                    st.success(get_translation('farm_added_success', st.session_state.language))
                    st.rerun()

def show_activities_page():
    """Show activities page"""
    if st.session_state.language == "ml":
        st.header("📅 കൃഷി പ്രവർത്തനങ്ങൾ")
    else:
        st.header("📅 Farm Activities")
    
    # Get activities data
    activities_data = make_api_request("/activities")
    
    if activities_data:
        # Create DataFrame for better display
        df = pd.DataFrame(activities_data)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            activity_filter = st.selectbox(get_translation('filter_by_activity', st.session_state.language), 
                ["All"] + list(df['activity_type'].unique()) if len(df) > 0 else ["All"])
        with col2:
            crop_filter = st.selectbox(get_translation('filter_by_crop', st.session_state.language), 
                ["All"] + list(df['crop_name'].dropna().unique()) if len(df) > 0 else ["All"])
        with col3:
            date_range = st.date_input(get_translation('date_label', st.session_state.language), [datetime.now() - timedelta(days=30), datetime.now()])
        
        # Apply filters
        filtered_df = df.copy()
        if activity_filter != "All":
            filtered_df = filtered_df[filtered_df['activity_type'] == activity_filter]
        if crop_filter != "All":
            filtered_df = filtered_df[filtered_df['crop_name'] == crop_filter]
        
        # Display activities
        if len(filtered_df) > 0:
            for _, activity in filtered_df.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                    with col1:
                        st.write(f"**{activity['activity_type']}** - {activity['description']}")
                        st.write(f"{get_translation('label_farm', st.session_state.language)}: {activity['farm_name']}")
                    with col2:
                        st.write(f"{get_translation('date_label', st.session_state.language)}: {activity['date']}")
                        if activity['crop_name']:
                            st.write(f"{get_translation('label_crop', st.session_state.language)}: {activity['crop_name']}")
                    with col3:
                        if activity['quantity']:
                            st.write(f"{get_translation('label_qty', st.session_state.language)}: {activity['quantity']}")
                    with col4:
                        if activity['cost']:
                            st.write(f"{get_translation('label_cost', st.session_state.language)}: ₹{activity['cost']}")
                    st.markdown("---")
        else:
            st.info(get_translation('no_activities_found', st.session_state.language))
    
    # Add new activity
    with st.expander(f"➕ {get_translation('record_new_activity', st.session_state.language)}"):
        farms_data = make_api_request("/farms")
        
        if farms_data:
            with st.form("add_activity"):
                col1, col2 = st.columns(2)
                
                with col1:
                    farm_id = st.selectbox(get_translation('select_farm', st.session_state.language), 
                        [(farm['id'], farm['name']) for farm in farms_data], 
                        format_func=lambda x: x[1])
                    activity_type = st.selectbox(get_translation('activity_type', st.session_state.language), 
                        ["Sowing", "Transplanting", "Watering", "Fertilizing", 
                         "Weeding", "Pest Control", "Harvesting", "Pruning"])
                    date = st.date_input(get_translation('date_label', st.session_state.language), datetime.now())
                
                with col2:
                    crop_name = st.text_input(get_translation('crop_name_opt', st.session_state.language))
                    quantity = st.number_input(get_translation('quantity_opt', st.session_state.language), min_value=0.0)
                    cost = st.number_input(get_translation('cost_opt', st.session_state.language), min_value=0.0)
                
                description = st.text_area(get_translation('description', st.session_state.language))
                notes = st.text_area(get_translation('notes_opt', st.session_state.language))
                
                if st.form_submit_button(get_translation('record_activity', st.session_state.language)):
                    data = {
                        "farm_id": farm_id[0],
                        "activity_type": activity_type,
                        "description": description,
                        "date": date.isoformat(),
                        "crop_name": crop_name if crop_name else None,
                        "quantity": quantity if quantity > 0 else None,
                        "cost": cost if cost > 0 else None,
                        "notes": notes if notes else None
                    }
                    
                    response = make_api_request("/activities", "POST", data)
                    if response:
                        st.success(get_translation('activity_recorded_success', st.session_state.language))
                        st.rerun()

def show_disease_detection():
    """Show disease detection page"""
    if st.session_state.language == "ml":
        st.header("🔬 AI രോഗ നിർണയം")
        st.write("AI ഉപയോഗിച്ച് രോഗങ്ങൾ കണ്ടെത്താൻ നിങ്ങളുടെ വിളയുടെ ഒരു ചിത്രം അപ്‌ലോഡ് ചെയ്യുക")
    else:
        st.header("🔬 AI Disease Detection")
        st.write("Upload an image of your crop to detect diseases using AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.language == "ml":
            uploader_text = "വിളയുടെ ചിത്രം തിരഞ്ഞെടുക്കുക"
            caption_text = "അപ്‌ലോഡ് ചെയ്ത ചിത്രം"
            crop_select_text = "വിളയുടെ തരം തിരഞ്ഞെടുക്കുക"
            crop_options = ["നെല്ല്", "തെങ്ങ്", "കുരുമുളക്", "ഏലം", "റബ്ബർ", "വാഴ"]
            analyze_text = "🔍 ചിത്രം വിശകലനം ചെയ്യുക"
        else:
            uploader_text = "Choose crop image"
            caption_text = "Uploaded Image"
            crop_select_text = "Select Crop Type"
            crop_options = ["Rice", "Coconut", "Pepper", "Cardamom", "Rubber", "Banana"]
            analyze_text = "🔍 Analyze Image"
        
        uploaded_file = st.file_uploader(uploader_text, type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption=caption_text, use_column_width=True)
            
            crop_name = st.selectbox(crop_select_text, crop_options)
            
            if st.button(analyze_text, use_container_width=True):
                with st.spinner(get_translation("analyzing_image", st.session_state.language)):
                    # Mock disease detection result
                    import random
                    diseases = {
                        "Rice": ["Blast Disease", "Brown Spot", "Bacterial Blight"],
                        "Coconut": ["Leaf Rot", "Crown Rot", "Bud Rot"],
                        "Pepper": ["Anthracnose", "Bacterial Wilt", "Root Rot"]
                    }
                    
                    disease = random.choice(diseases.get(crop_name, diseases["Rice"]))
                    confidence = random.uniform(0.7, 0.95)
                    
                    result = {
                        "disease": disease,
                        "confidence": confidence * 100,
                        "severity": "High" if confidence > 0.8 else "Medium",
                        "symptoms": ["Leaf spots", "Discoloration", "Wilting"],
                        "treatment": ["Apply fungicide", "Remove affected parts", "Improve drainage"],
                        "prevention": ["Use resistant varieties", "Maintain hygiene", "Monitor regularly"]
                    }
                    
                    st.session_state.detection_result = result
    
    with col2:
        if 'detection_result' in st.session_state:
            result = st.session_state.detection_result
            
            st.subheader(f"🎯 {get_translation('detection_results', st.session_state.language)}")
            
            # Disease info
            disease_label = get_translation('disease_label', st.session_state.language)
            confidence_label = get_translation('confidence_label', st.session_state.language)
            severity_label = get_translation('severity_label', st.session_state.language)
            st.markdown(f"**{disease_label}:** {result['disease']}")
            st.markdown(f"**{confidence_label}:** {result['confidence']:.1f}%")
            st.markdown(f"**{severity_label}:** {result['severity']}")
            
            # Progress bar for confidence
            st.progress(result['confidence'] / 100)
            
            # Symptoms
            st.subheader(f"🔍 {get_translation('symptoms_label', st.session_state.language)}")
            for symptom in result['symptoms']:
                st.write(f"• {symptom}")
            
            # Treatment
            st.subheader(f"💊 {get_translation('treatment_label', st.session_state.language)}")
            for treatment in result['treatment']:
                st.write(f"• {treatment}")
            
            # Prevention
            st.subheader(f"🛡️ {get_translation('prevention_label', st.session_state.language)}")
            for prevention in result['prevention']:
                st.write(f"• {prevention}")

def show_weather_page():
    """Show weather page"""
    st.header(f"🌤️ {get_translation('weather_advisory', st.session_state.language)}")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        location = st.selectbox(get_translation("select_location", st.session_state.language), [
            "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha",
            "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad",
            "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"
        ])
    
    # Mock weather data
    current_weather = {
        "temperature": 28,
        "humidity": 75,
        "rainfall": 2.5,
        "wind_speed": 12,
        "description": "Partly cloudy",
        "icon": "⛅"
    }
    
    with col1:
        st.markdown(f"""
        <div class="weather-card">
            <h2>{current_weather['icon']} {location}</h2>
            <h1>{current_weather['temperature']}°C</h1>
            <p>{current_weather['description']}</p>
            <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
                <div>💧 {current_weather['humidity']}%</div>
                <div>🌧️ {current_weather['rainfall']}mm</div>
                <div>💨 {current_weather['wind_speed']} km/h</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 5-day forecast
    st.subheader(f"📅 {get_translation('five_day_forecast', st.session_state.language)}")
    
    forecast_data = []
    for i in range(5):
        date = datetime.now() + timedelta(days=i)
        forecast_data.append({
            "Date": date.strftime("%m/%d"),
            "Day": date.strftime("%A"),
            "High": random.randint(26, 32),
            "Low": random.randint(20, 25),
            "Rain": random.randint(0, 10),
            "Icon": random.choice(["☀️", "⛅", "🌦️", "🌧️"])
        })
    
    df_forecast = pd.DataFrame(forecast_data)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, (_, day) in enumerate(df_forecast.iterrows()):
        with [col1, col2, col3, col4, col5][i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border: 1px solid #ddd; border-radius: 8px;">
                <h4>{day['Day'][:3]}</h4>
                <div style="font-size: 2rem;">{day['Icon']}</div>
                <p>{day['High']}° / {day['Low']}°</p>
                <p>🌧️ {day['Rain']}mm</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Farming advisory
    st.subheader(f"🌾 {get_translation('farming_advisory', st.session_state.language)}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.language == "ml":
            st.markdown("**✅ ശുപാർശ ചെയ്യുന്ന പ്രവർത്തനങ്ങൾ:**")
            st.write("• ഭൂമി തയ്യാറാക്കൽ")
            st.write("• വളം പ്രയോഗം")
            st.write("• കീട നിരീക്ഷണം")
            st.write("• നേഴ്സറി മാനേജ്മെന്റ്")
        else:
            st.markdown("**✅ Recommended Activities:**")
            st.write("• Land preparation")
            st.write("• Fertilizer application")
            st.write("• Pest monitoring")
            st.write("• Nursery management")
    
    with col2:
        if st.session_state.language == "ml":
            st.markdown("**❌ ഈ പ്രവർത്തനങ്ങൾ ഒഴിവാക്കുക:**")
            st.write("• കനത്ത യന്ത്ര പ്രവർത്തനങ്ങൾ")
            st.write("• കീടനാശിനി തളിക്കൽ")
            st.write("• വിളവെടുപ്പ് പ്രവർത്തനങ്ങൾ")
        else:
            st.markdown("**❌ Avoid These Activities:**")
            st.write("• Heavy machinery operations")
            st.write("• Pesticide spraying")
            st.write("• Harvesting operations")

def show_ai_chat():
    """Show AI chat assistant"""
    if st.session_state.language == "ml":
        st.header("🤖 AI കൃഷി സഹായി")
    else:
        st.header("🤖 AI Farming Assistant")
    
    # Initialize chat history early
    if 'chat_history' not in st.session_state:
        if st.session_state.language == "ml":
            welcome_msg = "ഹലോ! ഞാൻ നിങ്ങളുടെ AI കൃഷി അസിസ്റ്റന്റ്. ഇന്ന് എങ്ങനെ സഹായിക്കാം?"
        else:
            welcome_msg = "Hello! I'm your AI farming assistant. How can I help you today?"
        st.session_state.chat_history = [
            {"role": "assistant", "content": welcome_msg}
        ]

    # Use session language
    chat_language = "മലയാളം" if st.session_state.language == "ml" else "English"
    
    # Voice controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        voice_label = get_translation('voice_chat', st.session_state.language)
        if MIC_AVAILABLE:
            audio = mic_recorder(start_prompt=f"🎤 {voice_label}", stop_prompt="⏹️ Stop", key="mic")
            if audio and 'bytes' in audio:
                transcript = None
                if STT_AVAILABLE:
                    try:
                        recognizer = sr.Recognizer()
                        with sr.AudioFile(io.BytesIO(audio['bytes'])) as source:
                            audio_data = recognizer.record(source)
                        # Prefer Malayalam if UI is Malayalam; fallback to English
                        language = 'ml-IN' if st.session_state.language == 'ml' else 'en-IN'
                        transcript = recognizer.recognize_google(audio_data, language=language)
                    except Exception:
                        transcript = None
                if not transcript:
                    transcript = "[voice message]"

                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": transcript})
                st.caption(f"🎙️ Voice captured: {transcript}")

                # Generate AI response immediately for voice input
                lang_code = 'ml' if st.session_state.language == 'ml' else 'en'
                user_lower = transcript.lower()
                if any(word in user_lower for word in ['rice', 'paddy', 'നെല്ല്', 'വിത്ത്']):
                    response = "നെല്ല് കൃഷിക്ക് ജൂൺ-ജൂലൈ മാസങ്ങളാണ് ഏറ്റവും നല്ല സമയം. നല്ല വിത്ത് ഉപയോഗിച്ച് 20x15 സെ.മീ അകലത്തിൽ നടുക. വളം ആവശ്യത്തിന് ചേർക്കുക. ജലനിർമാണം ശ്രദ്ധിക്കുക." if lang_code == 'ml' else "For rice cultivation in Kerala, the best planting time is June-July. Use quality seeds with 20x15 cm spacing. Apply balanced fertilizer as per soil test recommendations. Maintain proper water management."
                elif any(word in user_lower for word in ['coconut', 'തെങ്ങ്', 'നാളികേരം']):
                    response = "തെങ്ങ് കൃഷിക്ക് മഴക്കാലമാണ് നല്ല സമയം. ഏഴ് മീറ്റർ അകലത്തിൽ നടുക. വാർഷികം 50 കിലോ ജൈവവളം ചേർക്കുക. ശരിയായ വാരിനീക്കൽ ഉറപ്പാക്കുക." if lang_code == 'ml' else "For coconut farming, monsoon season is ideal. Plant with 7-meter spacing. Apply 50kg organic manure annually. Ensure proper drainage and regular weeding."
                elif any(word in user_lower for word in ['pepper', 'കുരുമുളക്']):
                    response = "കുരുമുളക് കൃഷിക്ക് മേയ്-ജൂൺ മാസങ്ങളാണ് നല്ല സമയം. ജീവിത സ്റ്റാൻഡേർഡ് ഉപയോഗിക്കുക. വാർഷികം 10 കിലോ ജൈവവളം ചേർക്കുക. നല്ല വാരിനീക്കലും നിഴൽ മാനേജ്മെന്റും ഉറപ്പാക്കുക." if lang_code == 'ml' else "For pepper cultivation, May-June is the best season. Use live standards like silver oak. Apply 10kg organic manure per vine annually. Ensure good drainage and shade management (50-60%)."
                elif any(word in user_lower for word in ['disease', 'pest', 'രോഗം', 'കീടം']):
                    response = "രോഗങ്ങൾ തടയാൻ വയലിൽ വൃത്തിയും ശുചിത്വവും പാലിക്കുക. രോഗബാധിത ചെടികൾ നീക്കം ചെയ്യുക. സംയോജിത കീടനിയന്ത്രണം പാലിക്കുക. ആവശ്യമെങ്കിൽ കാർഷിക വിദഗ്ധനെ സമീപിക്കുക." if lang_code == 'ml' else "To prevent diseases, maintain field hygiene and remove infected plants. Use integrated pest management practices. Regular monitoring is essential. Consult agricultural experts when needed."
                elif any(word in user_lower for word in ['weather', 'rain', 'monsoon', 'കാലാവസ്ഥ', 'മഴ']):
                    response = "കേരള കർഷകർക്കുള്ള കാലാവസ്ഥ ഉപദേശം: ദൈനംദിന കാലാവസ്ഥ പ്രവചനം നിരീക്ഷിക്കുക. മഴ പ്രവചനത്തെ അടിസ്ഥാനമാക്കി പ്രവർത്തനങ്ങൾ ആസൂത്രണം ചെയ്യുക. മഴക്കാലത്ത് ഇൻപുട്ടുകൾക്ക് മൂടിയ സംഭരണം ഉപയോഗിക്കുക." if lang_code == 'ml' else "Weather advisory for Kerala farmers: Monitor daily weather forecasts. Plan activities based on rainfall predictions. Use covered storage for inputs during monsoon. Ensure proper field drainage during heavy rains."
                # Government schemes responses
                elif any(word in user_lower for word in ['scheme', 'schemes', 'subsidy', 'government', 'pm-kisan', 'pm kisan', 'pmkisan', 'pm-fasal', 'pm fasal', 'kisan credit', 'കേന്ദ്ര', 'സർക്കാർ', 'സബ്സിഡി', 'സ്കീം']):
                    if lang_code == 'ml':
                        response = (
                            "സർക്കാർ സ്കീമുകളുടെ ചുരുക്കം:\n"
                            "• PM-KISAN: വർഷത്തിൽ ₹6,000 നേരിട്ട് കർഷകരുടെ അക്കൗണ്ടിൽ.\n"
                            "• PM Fasal Bima Yojana: വിള ഇൻഷുറൻസ് കുറഞ്ഞ പ്രീമിയത്തിൽ.\n"
                            "• Kisan Credit Card (KCC): കുറഞ്ഞ പലിശയിൽ പ്രവർത്തി വായ്പ.\n"
                            "• Kerala State Farming Subsidies: ജലസേചനം, ഡ്രിപ്പ്, പോളിഹൗസ്, യന്ത്രങ്ങൾ എന്നിവയ്ക്ക് സബ്സിഡികൾ.\n"
                            "അപേക്ഷിക്കാനുള്ള മാർഗ്ഗം: Krishi Officer/അക്കർക്കൾ ഓഫീസിലോ https://pmkisan.gov.in/ / https://keralaagriculture.gov.in/ വഴി."
                        )
                    else:
                        response = (
                            "Summary of key government schemes:\n"
                            "• PM-KISAN: ₹6,000 per year to eligible farmers (DBT).\n"
                            "• PM Fasal Bima Yojana: Crop insurance with low premium.\n"
                            "• Kisan Credit Card (KCC): Working capital at subsidized interest.\n"
                            "• Kerala State Subsidies: Support for drip irrigation, polyhouse, farm machinery, etc.\n"
                            "How to apply: Visit local Krishi office or portals https://pmkisan.gov.in/ and https://keralaagriculture.gov.in/."
                        )
                else:
                    response = "നിങ്ങളുടെ ചോദ്യം മനസ്സിലായി. കൃഷിയുമായി ബന്ധപ്പെട്ട കൂടുതൽ വിവരങ്ങൾക്ക് പ്രാദേശിക കാർഷിക ഓഫീസറെ സമീപിക്കുക. കൃഷി സഖി എപ്പോഴും നിങ്ങളുടെ സഹായത്തിന് ഉണ്ട്!" if lang_code == 'ml' else "I understand your question. For specific farming advice in your area, consult local agricultural extension officers. Krishi Sakhi is always here to help!"

                st.session_state.chat_history.append({"role": "assistant", "content": response})

                # Speak reply if enabled
                try:
                    if 'voice_assistant' in st.session_state and st.session_state.get('speak_replies'):
                        ok, audio_bytes, mime = st.session_state.voice_assistant.speak_text(response, language=lang_code)
                        if ok and audio_bytes:
                            st.session_state['pending_audio'] = {'bytes': audio_bytes, 'mime': mime}
                except Exception:
                    pass

                st.rerun()
        else:
            if st.button(f"🎤 {voice_label}"):
                try:
                    recognized = st.session_state.voice_assistant.listen_for_speech()
                    if recognized:
                        st.session_state.chat_history.append({"role": "user", "content": recognized})
                        st.success(recognized)
                        st.rerun()
                except Exception:
                    st.warning("Voice feature temporarily unavailable.")
    
    # Chat interface
    
    # Speak replies toggle
    with col2:
        speak_label = get_translation('speak_replies', st.session_state.language)
        speak_replies = st.toggle(speak_label, key="speak_replies")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div style="background: #E3F2FD; padding: 1rem; margin: 0.5rem 0; border-radius: 10px;">👤 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background: #E8F5E8; padding: 1rem; margin: 0.5rem 0; border-radius: 10px;">🤖 {message["content"]}</div>', unsafe_allow_html=True)

    # If there is pending audio to play, render it once
    if st.session_state.get('pending_audio'):
        audio_payload = st.session_state.pop('pending_audio')
        try:
            st.audio(audio_payload.get('bytes'), format=audio_payload.get('mime'))
        except Exception:
            pass
    
    # Chat input
    if st.session_state.language == "ml":
        placeholder = "നിങ്ങളുടെ കൃഷി ചോദ്യം ഇവിടെ ടൈപ്പ് ചെയ്യുക..."
    else:
        placeholder = "Type your farming question here..."
    user_input = st.chat_input(placeholder)
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        lang_code = "ml" if chat_language == "മലയാളം" else "en"
        
        # Enhanced AI responses based on keywords
        user_lower = user_input.lower()
        
        # Rice farming responses
        if any(word in user_lower for word in ['rice', 'paddy', 'നെല്ല്', 'വിത്ത്']):
            if lang_code == "ml":
                response = "നെല്ല് കൃഷിക്ക് ജൂൺ-ജൂലൈ മാസങ്ങളാണ് ഏറ്റവും നല്ല സമയം. നല്ല വിത്ത് ഉപയോഗിച്ച് 20x15 സെ.മീ അകലത്തിൽ നടുക. വളം ആവശ്യത്തിന് ചേർക്കുക. ജലനിർമാണം ശ്രദ്ധിക്കുക."
            else:
                response = "For rice cultivation in Kerala, the best planting time is June-July. Use quality seeds with 20x15 cm spacing. Apply balanced fertilizer as per soil test recommendations. Maintain proper water management."
        
        # Coconut farming responses
        elif any(word in user_lower for word in ['coconut', 'തെങ്ങ്', 'നാളികേരം']):
            if lang_code == "ml":
                response = "തെങ്ങ് കൃഷിക്ക് മഴക്കാലമാണ് നല്ല സമയം. ഏഴ് മീറ്റർ അകലത്തിൽ നടുക. വാർഷികം 50 കിലോ ജൈവവളം ചേർക്കുക. ശരിയായ വാരിനീക്കൽ ഉറപ്പാക്കുക."
            else:
                response = "For coconut farming, monsoon season is ideal. Plant with 7-meter spacing. Apply 50kg organic manure annually. Ensure proper drainage and regular weeding."
        
        # Pepper farming responses
        elif any(word in user_lower for word in ['pepper', 'കുരുമുളക്', 'മരിച്ച']):
            if lang_code == "ml":
                response = "കുരുമുളക് കൃഷിക്ക് മേയ്-ജൂൺ മാസങ്ങളാണ് നല്ല സമയം. ജീവിത സ്റ്റാൻഡേർഡ് ഉപയോഗിക്കുക. വാർഷികം 10 കിലോ ജൈവവളം ചേർക്കുക. നല്ല വാരിനീക്കലും നിഴൽ മാനേജ്മെന്റും ഉറപ്പാക്കുക."
            else:
                response = "For pepper cultivation, May-June is the best season. Use live standards like silver oak. Apply 10kg organic manure per vine annually. Ensure good drainage and shade management (50-60%)."
        
        # Disease management responses
        elif any(word in user_lower for word in ['disease', 'pest', 'രോഗം', 'കീടം']):
            if lang_code == "ml":
                response = "രോഗങ്ങൾ തടയാൻ വയലിൽ വൃത്തിയും ശുചിത്വവും പാലിക്കുക. രോഗബാധിത ചെടികൾ നീക്കം ചെയ്യുക. സംയോജിത കീടനിയന്ത്രണം പാലിക്കുക. ആവശ്യമെങ്കിൽ കാർഷിക വിദഗ്ധനെ സമീപിക്കുക."
            else:
                response = "To prevent diseases, maintain field hygiene and remove infected plants. Use integrated pest management practices. Regular monitoring is essential. Consult agricultural experts when needed."
        
        # Weather-related responses
        elif any(word in user_lower for word in ['weather', 'rain', 'monsoon', 'കാലാവസ്ഥ', 'മഴ']):
            if lang_code == "ml":
                response = "കേരള കർഷകർക്കുള്ള കാലാവസ്ഥ ഉപദേശം: ദൈനംദിന കാലാവസ്ഥ പ്രവചനം നിരീക്ഷിക്കുക. മഴ പ്രവചനത്തെ അടിസ്ഥാനമാക്കി പ്രവർത്തനങ്ങൾ ആസൂത്രണം ചെയ്യുക. മഴക്കാലത്ത് ഇൻപുട്ടുകൾക്ക് മൂടിയ സംഭരണം ഉപയോഗിക്കുക."
            else:
                response = "Weather advisory for Kerala farmers: Monitor daily weather forecasts. Plan activities based on rainfall predictions. Use covered storage for inputs during monsoon. Ensure proper field drainage during heavy rains."
        
        # Government schemes responses
        elif any(word in user_lower for word in ['scheme', 'schemes', 'subsidy', 'government', 'pm-kisan', 'pm kisan', 'pmkisan', 'pm-fasal', 'pm fasal', 'kisan credit', 'കേന്ദ്ര', 'സർക്കാർ', 'സബ്സിഡി', 'സ്കീം']):
            if lang_code == 'ml':
                response = (
                    "സർക്കാർ സ്കീമുകളുടെ ചുരുക്കം:\n"
                    "• PM-KISAN: വർഷത്തിൽ ₹6,000 നേരിട്ട് കർഷകരുടെ അക്കൗണ്ടിൽ.\n"
                    "• PM Fasal Bima Yojana: വിള ഇൻഷുറൻസ് കുറഞ്ഞ പ്രീമിയത്തിൽ.\n"
                    "• Kisan Credit Card (KCC): കുറഞ്ഞ പലിശയിൽ പ്രവർത്തി വായ്പ.\n"
                    "• കേരള സർക്കാരിന്റെ സബ്സിഡികൾ: ഡ്രിപ്പ്, പോളിഹൗസ്, യന്ത്രങ്ങൾ മുതലായവ.\n"
                    "അപേക്ഷ: Krishi Office / https://pmkisan.gov.in/ / https://keralaagriculture.gov.in/"
                )
            else:
                response = (
                    "Key government schemes:\n"
                    "• PM-KISAN: ₹6,000 per year (DBT).\n"
                    "• PM Fasal Bima Yojana: Low premium crop insurance.\n"
                    "• Kisan Credit Card (KCC): Subsidized working capital.\n"
                    "• Kerala subsidies: Drip irrigation, polyhouse, machinery support.\n"
                    "Apply: Local Krishi office / https://pmkisan.gov.in/ / https://keralaagriculture.gov.in/"
                )

        # General farming advice
        else:
            if lang_code == "ml":
                response = "നിങ്ങളുടെ ചോദ്യം മനസ്സിലായി. കൃഷിയുമായി ബന്ധപ്പെട്ട കൂടുതൽ വിവരങ്ങൾക്ക് പ്രാദേശിക കാർഷിക ഓഫീസറെ സമീപിക്കുക. കൃഷി സഖി എപ്പോഴും നിങ്ങളുടെ സഹായത്തിന് ഉണ്ട്!"
            else:
                response = "I understand your question. For specific farming advice in your area, I recommend consulting with local agricultural extension officers or experts. Krishi Sakhi is always here to help you!"
        
        # Add AI response
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Speak the reply if enabled and render audio
        try:
            if 'voice_assistant' in st.session_state and st.session_state.get('speak_replies'):
                lang_code = 'ml' if st.session_state.language == 'ml' else 'en'
                ok, audio_bytes, mime = st.session_state.voice_assistant.speak_text(response, language=lang_code)
                if ok and audio_bytes:
                    st.audio(audio_bytes, format=mime)
        except Exception:
            pass
        st.rerun()
    
    # Quick questions
    st.subheader("💡 Quick Questions")
    quick_questions = [
        "What is the best time to plant rice?",
        "How to control pests in coconut?",
        "Fertilizer schedule for pepper?",
        "Weather suitable for harvesting?",
        "How to prevent diseases in crops?",
        "Best irrigation methods for Kerala?"
    ]
    
    if chat_language == "മലയാളം":
        quick_questions = [
            "നെല്ല് നടുന്നതിന് ഏറ്റവും നല്ല സമയം?",
            "തെങ്ങിലെ കീടങ്ങളെ എങ്ങനെ നിയന്ത്രിക്കാം?",
            "കുരുമുളകിന് വളം എപ്പോൾ ചേർക്കാം?",
            "വിളവെടുപ്പിന് അനുകൂലമായ കാലാവസ്ഥ?",
            "വിളകളിലെ രോഗങ്ങൾ എങ്ങനെ തടയാം?",
            "കേരളത്തിന് ഏറ്റവും നല്ല ജലസേചന മാർഗ്ഗങ്ങൾ?"
        ]
    
    cols = st.columns(2)
    for i, question in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(question, key=f"q_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": question})
                # Add mock response
                response = "Great question! Let me help you with detailed information about this topic."
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

def show_knowledge_base():
    """Show knowledge base"""
    if st.session_state.language == "ml":
        st.header("📚 അറിവ് ശേഖരം")
        search_placeholder = "വിളകൾ, രോഗങ്ങൾ, സ്കീമുകൾ തിരയുക..."
    else:
        st.header("📚 Knowledge Base")
        search_placeholder = "Search for crops, diseases, schemes..."
    
    # Search
    search_query = st.text_input("🔍 Search articles", placeholder=search_placeholder)
    
    # Categories
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.language == "ml":
            button_text = "🌾 വിളകൾ"
        else:
            button_text = "🌾 Crops"
        if st.button(button_text, use_container_width=True):
            st.session_state.kb_category = "crops"
    
    with col2:
        if st.session_state.language == "ml":
            button_text = "🐛 രോഗങ്ങൾ & കീടങ്ങൾ"
        else:
            button_text = "🐛 Diseases & Pests"
        if st.button(button_text, use_container_width=True):
            st.session_state.kb_category = "diseases"
    
    with col3:
        if st.session_state.language == "ml":
            button_text = "🏛️ സർക്കാർ സ്കീമുകൾ"
        else:
            button_text = "🏛️ Government Schemes"
        if st.button(button_text, use_container_width=True):
            st.session_state.kb_category = "schemes"
    
    st.markdown("---")
    
    # Display articles based on category
    if 'kb_category' not in st.session_state:
        st.session_state.kb_category = "crops"
    
    if st.session_state.kb_category == "crops":
        show_crop_articles()
    elif st.session_state.kb_category == "diseases":
        show_disease_articles()
    elif st.session_state.kb_category == "schemes":
        show_scheme_articles()

def show_crop_articles():
    """Show crop-related articles"""
    st.subheader("🌾 Crop Cultivation Guides")
    
    crops = [
        {
            "name": "Rice (നെല്ല്)",
            "description": "Complete guide to rice cultivation in Kerala",
            "seasons": "Kharif, Rabi, Summer",
            "yield": "4-6 tons/hectare"
        },
        {
            "name": "Coconut (തെങ്ങ്)",
            "description": "Coconut farming practices and management",
            "seasons": "Year-round",
            "yield": "80-150 nuts/palm/year"
        },
        {
            "name": "Black Pepper (കുരുമുളക്)",
            "description": "Spice cultivation in Kerala conditions",
            "seasons": "May-June planting",
            "yield": "2-5 kg/vine"
        }
    ]
    
    for crop in crops:
        with st.expander(f"📖 {crop['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**{get_translation('description', st.session_state.language)}:** {crop['description']}")
                st.write(f"**{get_translation('farming_advisory', st.session_state.language)}:** {crop['seasons']}")
            with col2:
                st.write(f"**{get_translation('harvest_time', st.session_state.language)}:** {crop['yield']}")
                if st.button(f"📖 {get_translation('read_full_guide', st.session_state.language)}", key=f"crop_{crop['name']}"):
                    # Speak the crop guide in selected language
                    if 'voice_assistant' in st.session_state:
                        lang_code = 'ml' if st.session_state.language == 'ml' else 'en'
                        text = f"{crop['name']}. {crop['description']}. {crop['seasons']}. {crop['yield']}"
                        ok, audio_bytes, mime = st.session_state.voice_assistant.speak_text(text, language=lang_code)
                        if ok and audio_bytes:
                            st.audio(audio_bytes, format=mime)

def show_disease_articles():
    """Show disease-related articles"""
    st.subheader("🐛 Disease & Pest Management")
    
    diseases = [
        {
            "name": "Rice Blast Disease",
            "crops": "Rice",
            "symptoms": "Diamond-shaped lesions on leaves",
            "treatment": "Fungicide application"
        },
        {
            "name": "Coconut Leaf Rot",
            "crops": "Coconut",
            "symptoms": "Yellow to brown leaf spots",
            "treatment": "Copper fungicide spray"
        }
    ]
    
    for disease in diseases:
        with st.expander(f"🔬 {disease['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**{get_translation('label_crop', st.session_state.language)}:** {disease['crops']}")
                st.write(f"**{get_translation('symptoms_label', st.session_state.language)}:** {disease['symptoms']}")
            with col2:
                st.write(f"**{get_translation('treatment_label', st.session_state.language)}:** {disease['treatment']}")
                if st.button(f"📖 {get_translation('read_full_guide', st.session_state.language)}", key=f"disease_{disease['name']}"):
                    if 'voice_assistant' in st.session_state:
                        lang_code = 'ml' if st.session_state.language == 'ml' else 'en'
                        text = f"{disease['name']}. {disease['symptoms']}. {disease['treatment']}"
                        ok, audio_bytes, mime = st.session_state.voice_assistant.speak_text(text, language=lang_code)
                        if ok and audio_bytes:
                            st.audio(audio_bytes, format=mime)

def show_scheme_articles():
    """Show government scheme articles"""
    st.subheader("🏛️ Government Schemes for Farmers")
    
    schemes = [
        {
            "name": "Kisan Credit Card",
            "description": "Credit facility for farmers",
            "eligibility": "All farmers with cultivable land",
            "benefits": "Low interest loans"
        },
        {
            "name": "PM-KISAN Scheme",
            "description": "Income support scheme",
            "eligibility": "Small and marginal farmers",
            "benefits": "₹6,000 per year"
        }
    ]
    
    for scheme in schemes:
        with st.expander(f"💰 {scheme['name']}"):
            st.write(f"**{get_translation('description', st.session_state.language)}:** {scheme['description']}")
            st.write(f"**Eligibility:** {scheme['eligibility']}")
            st.write(f"**Benefits:** {scheme['benefits']}")
            st.button(f"Apply Now", key=f"scheme_{scheme['name']}")

def show_community_page():
    """Show community page"""
    st.header(f"👥 {get_translation('community_dashboard', st.session_state.language)}")
    
    # Community alerts
    st.subheader(f"⚠️ {get_translation('community_alerts', st.session_state.language)}")
    
    alerts = [
        {
            "type": "disease",
            "title": "Blast Disease Alert - Kottayam",
            "description": "Multiple reports of blast disease in rice crops",
            "affected_farms": 12,
            "date": "2024-01-15"
        },
        {
            "type": "pest",
            "title": "Brown Planthopper - Alappuzha",
            "description": "Increased hopper activity reported",
            "affected_farms": 8,
            "date": "2024-01-14"
        }
    ]
    
    for alert in alerts:
        alert_color = "#FF5722" if alert['type'] == "disease" else "#FF9800"
        st.markdown(f"""
        <div style=\"border-left: 4px solid {alert_color}; padding: 1rem; margin: 1rem 0; background: #FFF3E0;\">
            <h4>🚨 {alert['title']}</h4>
            <p>{alert['description']}</p>
            <p><strong>{get_translation('affected_farms', st.session_state.language)}:</strong> {alert['affected_farms']} | <strong>{get_translation('date', st.session_state.language)}:</strong> {alert['date']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Regional statistics
    st.subheader(f"📊 {get_translation('regional_stats', st.session_state.language)}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Disease distribution
        disease_data = {
            "Disease": ["Blast Disease", "Brown Spot", "Leaf Rot", "Anthracnose"],
            "Reports": [15, 8, 12, 5]
        }
        title = get_translation('disease_reports_title', st.session_state.language)
        fig = px.pie(disease_data, values="Reports", names="Disease", title=title)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Crop distribution
        crop_data = {
            "Crop": ["Rice", "Coconut", "Pepper", "Cardamom", "Others"],
            "Farmers": [150, 120, 80, 45, 60]
        }
        title = get_translation('farmers_by_crop', st.session_state.language)
        fig = px.bar(crop_data, x="Crop", y="Farmers", title=title,
                    color="Farmers", color_continuous_scale="Greens")
        st.plotly_chart(fig, width='stretch')
    
    # Discussion forum (placeholder)
    st.subheader(f"💬 {get_translation('discussion_forum', st.session_state.language)}")
    st.info(f"🚧 {get_translation('forum_placeholder', st.session_state.language)}")

def show_reports_page():
    """Show reports and analytics page"""
    st.header("📈 Reports & Analytics")
    
    # Time period selection
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        date_range = st.date_input("Select Period", 
            [datetime.now() - timedelta(days=90), datetime.now()])
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Activities", "45", "+12")
    with col2:
        st.metric("Total Cost", "₹25,600", "+18%")
    with col3:
        st.metric("Avg Cost/Day", "₹285", "+5%")
    with col4:
        st.metric("Farms Active", "2", "0")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Activity trends
        st.subheader("📅 Activity Trends")
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30)
        activity_counts = [random.randint(0, 5) for _ in range(30)]
        
        fig = px.line(x=dates, y=activity_counts, title="Daily Activities")
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Number of Activities")
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Cost analysis
        st.subheader("💰 Cost Analysis")
        categories = ["Seeds", "Fertilizer", "Pesticides", "Labor", "Equipment"]
        costs = [4500, 8900, 3200, 6800, 2200]
        
        fig = px.pie(values=costs, names=categories, title="Cost Distribution")
        st.plotly_chart(fig, width='stretch')
    
    # Detailed table
    st.subheader("📋 Detailed Activity Report")
    
    # Mock data for table
    report_data = {
        "Date": [datetime.now() - timedelta(days=i) for i in range(10)],
        "Farm": ["Green Valley"] * 10,
        "Activity": ["Sowing", "Watering", "Fertilizing"] * 3 + ["Weeding"],
        "Crop": ["Rice", "Coconut", "Pepper"] * 3 + ["Rice"],
        "Cost": [500, 200, 800, 450, 300, 600, 750, 400, 350, 250]
    }
    
    df = pd.DataFrame(report_data)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(df, width='stretch')
    
    # Export functionality
    if st.button("📥 Export Report (CSV)"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="farming_report.csv",
            mime="text/csv"
        )

# Sidebar navigation
def show_sidebar():
    """Show sidebar navigation"""
    st.sidebar.markdown("## 🌾 Krishi Sakhi")
    
    if st.session_state.authenticated:
        farmer = get_farmer_profile()
        if farmer:
            st.sidebar.write(f"Welcome, {farmer['name']}")
        
        # Language selection
        selected_language = st.sidebar.selectbox(
            "🌐 Language", 
            ["English", "മലയാളം"],
            index=0 if st.session_state.language == "en" else 1
        )
        
        if selected_language == "മലയാളം":
            st.session_state.language = "ml"
        else:
            st.session_state.language = "en"
        
        st.sidebar.markdown("---")
        
        # Navigation menu
        menu_items = [
            ("dashboard", "🏠 Dashboard", "ഡാഷ്ബോർഡ്"),
            ("farms", "🏡 My Farms", "എന്റെ കൃഷിയിടങ്ങൾ"),
            ("activities", "📅 Activities", "പ്രവർത്തനങ്ങൾ"),
            ("disease_detection", "🔬 Disease Detection", "രോഗ നിർണയം"),
            ("weather", "🌤️ Weather", "കാലാവസ്ഥ"),
            ("ai_chat", "🤖 AI Assistant", "AI സഹായി"),
            ("knowledge", "📚 Knowledge Base", "അറിവ് ശേഖരം"),
            ("community", "👥 Community", "കമ്മ്യൂണിറ്റി"),
            ("reports", "📈 Reports", "റിപ്പോർട്ടുകൾ")
        ]
        
        for page_id, en_label, ml_label in menu_items:
            label = ml_label if st.session_state.language == "ml" else en_label
            if st.sidebar.button(label, key=page_id, use_container_width=True):
                st.session_state.current_page = page_id
                st.rerun()
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🔓 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.access_token = None
            st.session_state.farmer_data = None
            st.rerun()

# Main application
def main():
    """Main application function"""
    show_sidebar()
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        # Route to appropriate page
        if st.session_state.current_page == "dashboard":
            show_dashboard()
        elif st.session_state.current_page == "farms":
            show_farms_page()
        elif st.session_state.current_page == "activities":
            show_activities_page()
        elif st.session_state.current_page == "disease_detection":
            show_disease_detection()
        elif st.session_state.current_page == "weather":
            show_weather_page()
        elif st.session_state.current_page == "ai_chat":
            show_ai_chat()
        elif st.session_state.current_page == "knowledge":
            show_knowledge_base()
        elif st.session_state.current_page == "community":
            show_community_page()
        elif st.session_state.current_page == "reports":
            show_reports_page()
        else:
            show_dashboard()

if __name__ == "__main__":
    main()
