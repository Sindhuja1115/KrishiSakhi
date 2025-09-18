"""
Weather Service for Krishi Sakhi
Provides weather forecasts and farming advisories for Kerala
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

class WeatherService:
    def __init__(self):
        """Initialize weather service"""
        # Using OpenWeatherMap API (demo mode)
        self.api_key = "demo-api-key"
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Kerala districts for location mapping
        self.kerala_districts = {
            "thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366},
            "kollam": {"lat": 8.8932, "lon": 76.6141},
            "pathanamthitta": {"lat": 9.2648, "lon": 76.7870},
            "alappuzha": {"lat": 9.4981, "lon": 76.3388},
            "kottayam": {"lat": 9.5916, "lon": 76.5222},
            "idukki": {"lat": 9.8501, "lon": 76.9969},
            "ernakulam": {"lat": 9.9312, "lon": 76.2673},
            "thrissur": {"lat": 10.5276, "lon": 76.2144},
            "palakkad": {"lat": 10.7867, "lon": 76.6548},
            "malappuram": {"lat": 11.0410, "lon": 76.0788},
            "kozhikode": {"lat": 11.2588, "lon": 75.7804},
            "wayanad": {"lat": 11.6054, "lon": 76.0867},
            "kannur": {"lat": 11.8745, "lon": 75.3704},
            "kasaragod": {"lat": 12.4996, "lon": 74.9869}
        }
        
    async def get_weather_forecast(self, location: str) -> Dict:
        """Get 5-day weather forecast for location"""
        try:
            # For demo, return mock data
            return self._get_mock_weather_data(location)
            
        except Exception as e:
            print(f"Weather API error: {str(e)}")
            return self._get_mock_weather_data(location)
    
    def _get_coordinates(self, location: str) -> Dict:
        """Get coordinates for location"""
        location_lower = location.lower()
        
        # Check if it's a Kerala district
        for district, coords in self.kerala_districts.items():
            if district in location_lower:
                return coords
        
        # Default to Kochi if location not found
        return self.kerala_districts["ernakulam"]
    
    def _get_mock_weather_data(self, location: str) -> Dict:
        """Generate mock weather data for demo"""
        # Kerala typical weather patterns
        base_temp = 28
        base_humidity = 75
        
        forecasts = []
        for i in range(5):
            date = datetime.now() + timedelta(days=i)
            
            # Simulate weather variation
            temp_variation = random.uniform(-3, 5)
            humidity_variation = random.uniform(-10, 15)
            rain_chance = random.uniform(0, 100)
            
            forecasts.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": date.strftime("%A"),
                "temperature": {
                    "max": round(base_temp + temp_variation + 2),
                    "min": round(base_temp + temp_variation - 2),
                    "avg": round(base_temp + temp_variation)
                },
                "humidity": round(max(50, min(95, base_humidity + humidity_variation))),
                "rainfall": round(rain_chance / 10, 1) if rain_chance > 60 else 0,
                "wind_speed": round(random.uniform(5, 15), 1),
                "description": self._get_weather_description(rain_chance, temp_variation),
                "icon": self._get_weather_icon(rain_chance, temp_variation)
            })
        
        return {
            "location": location,
            "current": forecasts[0],
            "forecast": forecasts,
            "alerts": self._get_weather_alerts(forecasts)
        }
    
    def _get_weather_description(self, rain_chance: float, temp_variation: float) -> str:
        """Get weather description based on conditions"""
        if rain_chance > 80:
            return "Heavy rain expected"
        elif rain_chance > 60:
            return "Light to moderate rain"
        elif rain_chance > 30:
            return "Partly cloudy with possible showers"
        elif temp_variation > 2:
            return "Hot and sunny"
        else:
            return "Partly cloudy"
    
    def _get_weather_icon(self, rain_chance: float, temp_variation: float) -> str:
        """Get weather icon based on conditions"""
        if rain_chance > 80:
            return "🌧️"
        elif rain_chance > 60:
            return "🌦️"
        elif rain_chance > 30:
            return "⛅"
        elif temp_variation > 2:
            return "☀️"
        else:
            return "🌤️"
    
    def _get_weather_alerts(self, forecasts: List[Dict]) -> List[str]:
        """Generate weather alerts"""
        alerts = []
        
        for forecast in forecasts[:3]:  # Check next 3 days
            if forecast["rainfall"] > 5:
                alerts.append(f"Heavy rainfall expected on {forecast['day']} ({forecast['rainfall']}mm)")
            
            if forecast["temperature"]["max"] > 35:
                alerts.append(f"High temperature alert for {forecast['day']} ({forecast['temperature']['max']}°C)")
            
            if forecast["wind_speed"] > 20:
                alerts.append(f"Strong winds expected on {forecast['day']} ({forecast['wind_speed']} km/h)")
        
        return alerts
    
    async def get_farming_advisory(self, weather_data: Dict, location: str) -> Dict:
        """Generate farming advisory based on weather"""
        current_weather = weather_data["current"]
        forecast = weather_data["forecast"]
        
        advisories = []
        
        # Rainfall advisory
        total_rain = sum([f["rainfall"] for f in forecast[:3]])
        if total_rain > 15:
            advisories.append({
                "type": "rainfall",
                "priority": "high",
                "message": "Heavy rainfall expected. Ensure proper drainage and postpone spray applications.",
                "malayalam": "കനത്ത മഴ പ്രതീക്ഷിക്കുന്നു. നല്ല നീർവാർച്ച ഉറപ്പാക്കുകയും സ്പ്രേ പ്രയോഗം മാറ്റിവയ്ക്കുകയും ചെയ്യുക."
            })
        elif total_rain < 2:
            advisories.append({
                "type": "drought",
                "priority": "medium",
                "message": "Low rainfall expected. Plan for irrigation and water conservation.",
                "malayalam": "കുറഞ്ഞ മഴ പ്രതീക്ഷിക്കുന്നു. ജലസേചനവും ജലസംരക്ഷണവും ആസൂത്രണം ചെയ്യുക."
            })
        
        # Temperature advisory
        max_temp = max([f["temperature"]["max"] for f in forecast[:3]])
        if max_temp > 35:
            advisories.append({
                "type": "heat",
                "priority": "high",
                "message": "High temperatures expected. Increase irrigation frequency and provide shade for sensitive crops.",
                "malayalam": "ഉയർന്ന താപനില പ്രതീക്ഷിക്കുന്നു. ജലസേചന ആവൃത്തി വർധിപ്പിച്ച് സെൻസിറ്റീവ് വിളകൾക്ക് തണൽ നൽകുക."
            })
        
        # Humidity advisory
        avg_humidity = sum([f["humidity"] for f in forecast[:3]]) / 3
        if avg_humidity > 85:
            advisories.append({
                "type": "humidity",
                "priority": "medium",
                "message": "High humidity may increase disease risk. Monitor crops closely and ensure good air circulation.",
                "malayalam": "ഉയർന്ന ആർദ്രത രോഗസാധ്യത വർധിപ്പിക്കും. വിളകൾ സൂക്ഷ്മമായി നിരീക്ഷിച്ച് നല്ല വായു സഞ്ചാരം ഉറപ്പാക്കുക."
            })
        
        # Crop-specific advisories
        crop_advisories = self._get_crop_specific_advisory(weather_data)
        advisories.extend(crop_advisories)
        
        return {
            "advisories": advisories,
            "best_activities": self._get_recommended_activities(weather_data),
            "avoid_activities": self._get_activities_to_avoid(weather_data)
        }
    
    def _get_crop_specific_advisory(self, weather_data: Dict) -> List[Dict]:
        """Get crop-specific weather advisories"""
        advisories = []
        current = weather_data["current"]
        
        # Rice advisory
        if current["rainfall"] > 10:
            advisories.append({
                "type": "rice",
                "priority": "medium",
                "message": "Good conditions for rice transplanting. Ensure fields are properly leveled.",
                "malayalam": "നെല്ല് നടീലിന് അനുകൂല സാഹചര്യം. വയലുകൾ ശരിയായി നിരപ്പാക്കിയിട്ടുണ്ടെന്ന് ഉറപ്പാക്കുക."
            })
        
        # Coconut advisory
        if current["wind_speed"] > 20:
            advisories.append({
                "type": "coconut",
                "priority": "high",
                "message": "Strong winds may damage coconut palms. Secure loose fronds and harvest mature nuts.",
                "malayalam": "ശക്തമായ കാറ്റ് തെങ്ങുകൾക്ക് കേടുപാടുകൾ വരുത്തിയേക്കാം. അയഞ്ഞ ഇലകൾ ബന്ധിച്ച് പഴുത്ത കായ്കൾ പറിക്കുക."
            })
        
        return advisories
    
    def _get_recommended_activities(self, weather_data: Dict) -> List[str]:
        """Get recommended farming activities based on weather"""
        activities = []
        current = weather_data["current"]
        
        if current["rainfall"] < 2 and current["temperature"]["max"] < 32:
            activities.extend([
                "Land preparation",
                "Fertilizer application",
                "Pesticide spraying",
                "Harvesting"
            ])
        
        if current["rainfall"] > 5:
            activities.extend([
                "Transplanting rice",
                "Planting rain-fed crops",
                "Nursery management"
            ])
        
        return activities
    
    def _get_activities_to_avoid(self, weather_data: Dict) -> List[str]:
        """Get activities to avoid based on weather"""
        avoid = []
        current = weather_data["current"]
        
        if current["rainfall"] > 10:
            avoid.extend([
                "Pesticide/fertilizer spraying",
                "Harvesting",
                "Field operations with heavy machinery"
            ])
        
        if current["wind_speed"] > 20:
            avoid.extend([
                "Spraying operations",
                "Tree climbing",
                "Drone operations"
            ])
        
        return avoid