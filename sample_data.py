"""
Sample data for Krishi Sakhi demo
Contains mock data for farmers, farms, activities, and other entities
"""

from datetime import datetime, timedelta
import random

# Sample farmer data
SAMPLE_FARMERS = [
    {
        "id": 1,
        "name": "Ravi Kumar",
        "phone": "+919876543210",
        "email": "ravi.kumar@email.com",
        "location": "Kottayam",
        "language": "en"
    },
    {
        "id": 2,
        "name": "മീര ദേവി",
        "phone": "+919876543211",
        "email": "meera.devi@email.com",
        "location": "Thrissur",
        "language": "ml"
    }
]

# Sample farm data
SAMPLE_FARMS = [
    {
        "id": 1,
        "farmer_id": 1,
        "name": "Green Valley Farm",
        "location": "Kottayam",
        "land_size": 2.5,
        "soil_type": "Loamy",
        "irrigation_type": "Drip",
        "crop_types": ["Rice", "Coconut", "Pepper"]
    },
    {
        "id": 2,
        "farmer_id": 2,
        "name": "സുജാത കൃഷിയിടം",
        "location": "Thrissur",
        "land_size": 1.8,
        "soil_type": "Clay",
        "irrigation_type": "Flood",
        "crop_types": ["Rice", "Banana", "Turmeric"]
    }
]

# Knowledge base articles
KNOWLEDGE_BASE = {
    "en": {
        "crops": {
            "rice": {
                "title": "Rice Cultivation in Kerala",
                "content": """
                Rice is the staple food crop of Kerala. The state has three rice growing seasons:
                
                **Seasons:**
                - Kharif (June-November)
                - Rabi (December-March) 
                - Summer (April-May)
                
                **Varieties:**
                - High yielding varieties: IR64, Jyothi, Uma
                - Traditional varieties: Pokkali, Kaipad, Chennellu
                
                **Cultivation Practices:**
                - Seedbed preparation: 20-25 days before transplanting
                - Transplanting: 3-4 weeks old seedlings
                - Spacing: 20x15 cm or 20x20 cm
                - Water management: Maintain 2-3 cm water level
                """,
                "tags": ["staple", "kharif", "rabi", "transplanting"]
            },
            "coconut": {
                "title": "Coconut Farming Guide",
                "content": """
                Coconut is one of the most important plantation crops of Kerala.
                
                **Planting:**
                - Season: Best during monsoon (June-September)
                - Spacing: 7.5m x 7.5m (175 palms/hectare)
                - Pit size: 1m x 1m x 1m
                
                **Varieties:**
                - Tall varieties: West Coast Tall, East Coast Tall
                - Dwarf varieties: Chowghat Orange Dwarf, Malayan Dwarf
                - Hybrid varieties: Kerasree, Kera Ganga
                """,
                "tags": ["plantation", "monsoon", "intercropping"]
            }
        }
    },
    
    "ml": {
        "crops": {
            "rice": {
                "title": "കേരളത്തിലെ നെല്ല് കൃഷി",
                "content": """
                നെല്ല് കേരളത്തിന്റെ പ്രധാന ഭക്ഷ്യവിളയാണ്. സംസ്ഥാനത്ത് മൂന്ന് നെല്ല് കൃഷി സീസണുകളുണ്ട്:
                
                **സീസണുകൾ:**
                - ഖരീഫ് (ജൂൺ-നവംബർ)
                - റാബി (ഡിസംബർ-മാർച്ച്)
                - വേനൽ (ഏപ്രിൽ-മേയ്)
                
                **ഇനങ്ങൾ:**
                - ഉയർന്ന വിളവ് ഇനങ്ങൾ: IR64, ജ്യോതി, ഉമ
                - പരമ്പരാഗത ഇനങ്ങൾ: പൊക്കാലി, കായ്പാട്, ചെന്നെല്ല്
                """,
                "tags": ["പ്രധാന", "ഖരീഫ്", "റാബി"]
            }
        }
    }
}

def get_sample_activities():
    """Generate sample activities for demo"""
    activities = []
    activity_types = [
        "Sowing", "Transplanting", "Watering", "Fertilizing", 
        "Weeding", "Pest Control", "Harvesting", "Pruning"
    ]
    
    crops = ["Rice", "Coconut", "Pepper", "Cardamom", "Banana"]
    
    for i in range(20):
        date = datetime.now() - timedelta(days=random.randint(0, 30))
        activities.append({
            "id": i + 1,
            "farm_id": random.randint(1, 2),
            "activity_type": random.choice(activity_types),
            "description": f"Regular {random.choice(activity_types).lower()} activity",
            "date": date.strftime("%Y-%m-%d"),
            "crop_name": random.choice(crops),
            "quantity": round(random.uniform(1, 10), 1),
            "cost": round(random.uniform(100, 2000), 2),
            "notes": "Activity completed successfully"
        })
    
    return activities

def get_sample_data():
    """Get all sample data"""
    return {
        "farmers": SAMPLE_FARMERS,
        "farms": SAMPLE_FARMS,
        "activities": get_sample_activities(),
        "knowledge_base": KNOWLEDGE_BASE
    }