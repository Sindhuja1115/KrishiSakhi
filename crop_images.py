"""
Crop image samples for Krishi Sakhi
Provides sample data for crop diseases and treatments
"""

# Sample crop disease information
CROP_DISEASES = {
    "Rice": {
        "Blast Disease": {
            "symptoms": [
                "Diamond-shaped lesions on leaves",
                "Grayish-white centers with dark borders",
                "Neck rot causing panicle breakage"
            ],
            "treatment": [
                "Apply Tricyclazole fungicide",
                "Use resistant varieties",
                "Improve field drainage"
            ],
            "prevention": [
                "Avoid excessive nitrogen application",
                "Maintain proper water management",
                "Use disease-free seeds"
            ]
        },
        "Brown Spot": {
            "symptoms": [
                "Small brown spots on leaves",
                "Circular to oval lesions",
                "Seedling blight in severe cases"
            ],
            "treatment": [
                "Apply Mancozeb fungicide",
                "Remove infected plant debris",
                "Improve soil fertility"
            ],
            "prevention": [
                "Use certified seeds",
                "Maintain balanced nutrition",
                "Avoid water stress"
            ]
        }
    },
    "Coconut": {
        "Leaf Rot": {
            "symptoms": [
                "Yellow to brown leaf spots",
                "Wilting of affected leaves",
                "Premature leaf fall"
            ],
            "treatment": [
                "Apply Copper fungicide",
                "Remove affected leaves",
                "Improve air circulation"
            ],
            "prevention": [
                "Avoid overhead irrigation",
                "Maintain proper spacing",
                "Regular sanitation"
            ]
        }
    },
    "Pepper": {
        "Anthracnose": {
            "symptoms": [
                "Dark sunken lesions on fruits",
                "Leaf spots with yellow halos",
                "Stem cankers"
            ],
            "treatment": [
                "Apply Carbendazim fungicide",
                "Prune affected parts",
                "Improve ventilation"
            ],
            "prevention": [
                "Use resistant varieties",
                "Avoid water splash",
                "Regular field inspection"
            ]
        }
    }
}

def get_disease_info(crop, disease):
    """Get disease information for specific crop and disease"""
    return CROP_DISEASES.get(crop, {}).get(disease, {
        "symptoms": ["Consult agricultural expert"],
        "treatment": ["Seek professional advice"],
        "prevention": ["Regular monitoring"]
    })

def get_available_crops():
    """Get list of available crops"""
    return list(CROP_DISEASES.keys())

def get_crop_diseases(crop):
    """Get diseases for specific crop"""
    return list(CROP_DISEASES.get(crop, {}).keys())