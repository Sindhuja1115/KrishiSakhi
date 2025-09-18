"""
Translation utilities for Krishi Sakhi
Provides bilingual support for English and Malayalam
"""

# Translation dictionary for key terms
TRANSLATIONS = {
    "en": {
        # Navigation
        "dashboard": "Dashboard",
        "profile": "Profile",
        "farms": "My Farms",
        "activities": "Activities",
        "disease_detection": "Disease Detection",
        "weather": "Weather",
        "chat": "AI Assistant",
        "knowledge": "Knowledge Base",
        "community": "Community",
        "reports": "Reports",
        "reminders": "Reminders",
        "settings": "Settings",
        
        # Common terms
        "farmer": "Farmer",
        "farm": "Farm",
        "crop": "Crop",
        "disease": "Disease",
        "pest": "Pest",
        "weather": "Weather",
        "soil": "Soil",
        "irrigation": "Irrigation",
        "fertilizer": "Fertilizer",
        "pesticide": "Pesticide",
        "harvest": "Harvest",
        "planting": "Planting",
        "sowing": "Sowing",
        
        # Crop names
        "rice": "Rice",
        "coconut": "Coconut",
        "pepper": "Black Pepper",
        "cardamom": "Cardamom",
        "rubber": "Rubber",
        "tea": "Tea",
        "coffee": "Coffee",
        "banana": "Banana",
        "mango": "Mango",
        "jackfruit": "Jackfruit"
    },
    
    "ml": {
        # Navigation
        "dashboard": "ഡാഷ്ബോർഡ്",
        "profile": "പ്രൊഫൈൽ",
        "farms": "എന്റെ കൃഷിയിടങ്ങൾ",
        "activities": "പ്രവർത്തനങ്ങൾ",
        "disease_detection": "രോഗ നിർണയം",
        "weather": "കാലാവസ്ഥ",
        "chat": "AI സഹായി",
        "knowledge": "അറിവ് ശേഖരം",
        "community": "കമ്മ്യൂണിറ്റി",
        "reports": "റിപ്പോർട്ടുകൾ",
        "reminders": "ഓർമ്മപ്പെടുത്തലുകൾ",
        "settings": "ക്രമീകരണങ്ങൾ",
        
        # Common terms
        "farmer": "കർഷകൻ",
        "farm": "കൃഷിയിടം",
        "crop": "വിള",
        "disease": "രോഗം",
        "pest": "കീടം",
        "weather": "കാലാവസ്ഥ",
        "soil": "മണ്ണ്",
        "irrigation": "ജലസേചനം",
        "fertilizer": "വളം",
        "pesticide": "കീടനാശിനി",
        "harvest": "വിളവെടുപ്പ്",
        "planting": "നടീൽ",
        "sowing": "വിതയ്ക്കൽ",
        
        # Crop names
        "rice": "നെല്ല്",
        "coconut": "തെങ്ങ്",
        "pepper": "കുരുമുളക്",
        "cardamom": "ഏലം",
        "rubber": "റബ്ബർ",
        "tea": "ചായ",
        "coffee": "കാപ്പി",
        "banana": "വാഴ",
        "mango": "മാവ്",
        "jackfruit": "ചക്ക"
    }
}

def get_translation(key: str, language: str = "en") -> str:
    """Get translation for a key in specified language"""
    return TRANSLATIONS.get(language, {}).get(key, TRANSLATIONS["en"].get(key, key))

def get_all_translations(language: str = "en") -> dict:
    """Get all translations for a language"""
    return TRANSLATIONS.get(language, TRANSLATIONS["en"])

# Government schemes data
GOVERNMENT_SCHEMES = {
    "en": {
        "kisan_credit_card": {
            "name": "Kisan Credit Card",
            "description": "Credit facility for farmers to meet their cultivation needs",
            "eligibility": "All farmers owning cultivable land",
            "benefits": ["Low interest rates", "Flexible repayment", "Insurance coverage"],
            "how_to_apply": "Visit nearest bank branch with land documents"
        },
        "pradhan_mantri_kisan_samman": {
            "name": "PM-KISAN Scheme",
            "description": "Income support to all landholding farmer families",
            "eligibility": "Small and marginal farmers with landholding up to 2 hectares",
            "benefits": ["₹6,000 per year in three installments"],
            "how_to_apply": "Apply online through PM-KISAN portal"
        }
    },
    
    "ml": {
        "kisan_credit_card": {
            "name": "കിസാൻ ക്രെഡിറ്റ് കാർഡ്",
            "description": "കർഷകരുടെ കൃഷി ആവശ്യങ്ങൾക്കായി വായ്പാ സൗകര്യം",
            "eligibility": "കൃഷിയോഗ്യമായ ഭൂമിയുള്ള എല്ലാ കർഷകരും",
            "benefits": ["കുറഞ്ഞ പലിശ നിരക്ക്", "വഴക്കമുള്ള തിരിച്ചടവ്", "ഇൻഷുറൻസ് കവറേജ്"],
            "how_to_apply": "ഭൂമി രേഖകളുമായി അടുത്തുള്ള ബാങ്ക് ബ്രാഞ്ച് സന്ദർശിക്കുക"
        },
        "pradhan_mantri_kisan_samman": {
            "name": "പിഎം-കിസാൻ പദ്ധതി",
            "description": "ഭൂമിയുള്ള എല്ലാ കർഷക കുടുംബങ്ങൾക്കും വരുമാന പിന്തുണ",
            "eligibility": "2 ഹെക്ടർ വരെ ഭൂമിയുള്ള ചെറുകിട, നാമമാത്ര കർഷകർ",
            "benefits": ["മൂന്ന് ഇൻസ്റ്റാൾമെന്റുകളിലായി വർഷത്തിൽ ₹6,000"],
            "how_to_apply": "പിഎം-കിസാൻ പോർട്ടലിലൂടെ ഓൺലൈൻ അപേക്ഷിക്കുക"
        }
    }
}

def get_government_schemes(language: str = "en") -> dict:
    """Get government schemes in specified language"""
    return GOVERNMENT_SCHEMES.get(language, GOVERNMENT_SCHEMES["en"])