"""
AI Service for Krishi Sakhi
Handles disease detection and chat functionality using Hugging Face models
"""

import os
import json
import torch
from PIL import Image
import numpy as np
import requests
from typing import Dict, List, Optional
import asyncio
import random

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    from transformers import ViTImageProcessor, ViTForImageClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: Transformers not available. Using mock AI responses.")

class AIService:
    def __init__(self):
        """Initialize AI models and services"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.chat_model = None
        self.disease_classifier = None
        self.image_processor = None
        
        if TRANSFORMERS_AVAILABLE:
            self.initialize_models()
        
    def initialize_models(self):
        """Initialize Hugging Face models"""
        try:
            print("Initializing AI models...")
            
            # Initialize text generation model for chat
            self.chat_model = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                device=0 if torch.cuda.is_available() else -1,
                max_length=200,
                do_sample=True,
                temperature=0.7
            )
            
            # Initialize image classification for disease detection
            self.image_processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
            self.disease_classifier = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')
            
            print("AI models initialized successfully!")
        except Exception as e:
            print(f"Error initializing AI models: {str(e)}")
            # Fallback to mock responses
            self.chat_model = None
            self.disease_classifier = None
    
    async def detect_disease(self, image_path: str, crop_name: str) -> Dict:
        """
        Detect plant disease from uploaded image
        """
        try:
            if not os.path.exists(image_path):
                # For demo, generate mock detection
                return self._get_mock_disease_detection(crop_name)
            
            # Load and process image
            image = Image.open(image_path).convert("RGB")
            
            if self.disease_classifier and self.image_processor:
                # Use actual Hugging Face model
                inputs = self.image_processor(image, return_tensors="pt")
                
                with torch.no_grad():
                    outputs = self.disease_classifier(**inputs)
                    logits = outputs.logits
                    predicted_class_idx = logits.argmax(-1).item()
                    confidence = torch.nn.functional.softmax(logits, dim=-1).max().item()
                
                # Map to plant diseases
                disease_name = self._map_to_plant_disease(predicted_class_idx, crop_name)
            else:
                # Mock response for demo
                disease_name, confidence = self._get_mock_disease_detection(crop_name)
            
            # Get disease information
            disease_info = self._get_disease_info(disease_name, crop_name)
            
            return {
                "disease": disease_name,
                "confidence": round(confidence * 100, 2),
                "severity": "High" if confidence > 0.8 else "Medium" if confidence > 0.5 else "Low",
                "symptoms": disease_info["symptoms"],
                "treatment": disease_info["treatment"],
                "prevention": disease_info["prevention"]
            }
            
        except Exception as e:
            return {
                "error": f"Disease detection failed: {str(e)}",
                "disease": "Unknown",
                "confidence": 0,
                "severity": "Unknown",
                "symptoms": ["Could not analyze image"],
                "treatment": ["Please consult agricultural expert"],
                "prevention": ["Regular monitoring recommended"]
            }
    
    def _get_mock_disease_detection(self, crop_name: str) -> tuple:
        """Generate mock disease detection for demo"""
        mock_diseases = {
            "Rice": [("Blast Disease", 0.85), ("Brown Spot", 0.75), ("Bacterial Blight", 0.65)],
            "Coconut": [("Leaf Rot", 0.80), ("Crown Rot", 0.70), ("Bud Rot", 0.60)],
            "Pepper": [("Anthracnose", 0.90), ("Bacterial Wilt", 0.75), ("Root Rot", 0.55)],
            "Cardamom": [("Capsule Rot", 0.85), ("Leaf Spot", 0.70), ("Rhizome Rot", 0.60)],
            "Rubber": [("Leaf Fall Disease", 0.80), ("Pink Disease", 0.70), ("Root Disease", 0.55)]
        }
        
        diseases = mock_diseases.get(crop_name, mock_diseases["Rice"])
        return random.choice(diseases)
    
    def _map_to_plant_disease(self, class_idx: int, crop_name: str) -> str:
        """Map generic classification to plant-specific diseases"""
        disease_maps = {
            "Rice": ["Blast Disease", "Brown Spot", "Bacterial Blight", "Sheath Blight"],
            "Coconut": ["Leaf Rot", "Crown Rot", "Bud Rot", "Stem Bleeding"],
            "Pepper": ["Anthracnose", "Bacterial Wilt", "Root Rot", "Leaf Spot"],
            "Cardamom": ["Capsule Rot", "Leaf Spot", "Rhizome Rot", "Viral Disease"]
        }
        
        crop_diseases = disease_maps.get(crop_name, disease_maps["Rice"])
        return crop_diseases[class_idx % len(crop_diseases)]
    
    def _get_disease_info(self, disease_name: str, crop_name: str) -> Dict:
        """Get detailed information about detected disease"""
        disease_database = {
            "Blast Disease": {
                "symptoms": [
                    "Diamond-shaped lesions on leaves",
                    "White to gray centers with brown borders",
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
            },
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
            },
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
        
        return disease_database.get(disease_name, {
            "symptoms": ["Symptoms vary based on disease type"],
            "treatment": ["Consult agricultural extension officer"],
            "prevention": ["Regular monitoring and good practices"]
        })
    
    async def chat_response(self, message: str, language: str = "en") -> str:
        """
        Generate AI chat response for farming queries
        """
        try:
            # Preprocess message for farming context
            farming_context = self._add_farming_context(message)
            
            if self.chat_model and len(message) < 200:
                # Use actual Hugging Face model for short queries
                response = self.chat_model(
                    farming_context,
                    max_length=150,
                    num_return_sequences=1,
                    temperature=0.7,
                    pad_token_id=50256
                )
                
                # Extract the generated response
                full_response = response[0]['generated_text']
                ai_response = full_response[len(farming_context):].strip()
                
                if not ai_response:
                    ai_response = self._get_farming_response(message, language)
            else:
                # Use rule-based responses
                ai_response = self._get_farming_response(message, language)
            
            # Translate if needed
            if language == "ml":
                ai_response = self._translate_to_malayalam(ai_response)
            
            return ai_response
            
        except Exception as e:
            error_response = "I apologize, but I'm having trouble processing your question right now. Please try again or consult with a local agricultural expert."
            
            if language == "ml":
                error_response = "ക്ഷമിക്കണം, ഇപ്പോൾ നിങ്ങളുടെ ചോദ്യം പ്രോസസ്സ് ചെയ്യുന്നതിൽ പ്രശ്നമുണ്ട്. ദയവായി വീണ്ടും ശ്രമിക്കുക അല്ലെങ്കിൽ പ്രാദേശിക കാർഷിക വിദഗ്ധനെ സമീപിക്കുക."
            
            return error_response
    
    def _add_farming_context(self, message: str) -> str:
        """Add farming context to user message"""
        context = "As an AI farming assistant for Kerala farmers, please provide helpful advice about: "
        return context + message
    
    def _get_farming_response(self, message: str, language: str = "en") -> str:
        """Generate rule-based farming responses"""
        message_lower = message.lower()
        
        # Rice farming responses
        if any(word in message_lower for word in ['rice', 'paddy', 'നെല്ല്']):
            if any(word in message_lower for word in ['planting', 'sowing', 'വിതയ്ക്കൽ']):
                return "For rice cultivation in Kerala: 1) Best planting time is June-July for Kharif season. 2) Use 25-30 kg seeds per hectare. 3) Maintain 2-3 cm water level initially. 4) Plant with 20x15 cm spacing for better yield."
            elif any(word in message_lower for word in ['fertilizer', 'nutrition', 'വളം']):
                return "Rice fertilizer schedule: 1) Apply 60 kg N, 30 kg P2O5, 30 kg K2O per hectare. 2) Split nitrogen application: 50% at transplanting, 25% at tillering, 25% at panicle initiation. 3) Use organic compost for better soil health."
            elif any(word in message_lower for word in ['disease', 'blast', 'രോഗം']):
                return "Common rice diseases in Kerala: 1) Blast disease - Apply Tricyclazole fungicide. 2) Brown spot - Use Mancozeb spray. 3) Bacterial blight - Use copper-based fungicides. 4) Maintain proper field hygiene and drainage."
        
        # Coconut farming responses
        elif any(word in message_lower for word in ['coconut', 'തെങ്ങ്']):
            if any(word in message_lower for word in ['planting', 'growing']):
                return "Coconut farming tips: 1) Plant during monsoon season (June-September). 2) Maintain 7-8 meter spacing between trees. 3) Apply 50 kg organic manure annually. 4) Ensure proper drainage and regular weeding."
            elif any(word in message_lower for word in ['fertilizer', 'nutrition']):
                return "Coconut nutrition: 1) Apply 500g Urea, 320g Super phosphate, 1200g MOP per palm annually. 2) Add 50 kg organic manure. 3) Apply lime if soil is acidic. 4) Use micronutrient sprays during monsoon."
        
        # Pepper farming responses
        elif any(word in message_lower for word in ['pepper', 'കുരുമുളക്']):
            return "Black pepper cultivation: 1) Best season for planting is May-June. 2) Use live standards like silver oak or erythrina. 3) Apply 10 kg organic manure per vine annually. 4) Ensure good drainage and shade management (50-60%)."
        
        # Weather-related responses
        elif any(word in message_lower for word in ['weather', 'rain', 'monsoon', 'കാലാവസ്ഥ']):
            return "Weather advisory for Kerala farmers: 1) Monitor daily weather forecasts. 2) Plan activities based on rainfall predictions. 3) Use covered storage for inputs during monsoon. 4) Ensure proper field drainage during heavy rains."
        
        # Disease-related responses
        elif any(word in message_lower for word in ['disease', 'pest', 'രോഗം']):
            return "Common disease management: 1) Regular field monitoring is essential. 2) Use IPM (Integrated Pest Management) approaches. 3) Apply organic pesticides when possible. 4) Maintain field hygiene and remove infected plants."
        
        # Soil-related responses
        elif any(word in message_lower for word in ['soil', 'മണ്ണ്']):
            return "Soil management tips: 1) Test soil pH regularly (ideal 6.0-7.5). 2) Add organic matter to improve soil structure. 3) Practice crop rotation to maintain fertility. 4) Use green manures like cowpea or daincha."
        
        # General farming response
        else:
            return "I'm here to help with your farming questions! You can ask me about crop cultivation, disease management, weather advisory, soil health, or any other agricultural topics specific to Kerala farming conditions."
    
    def _translate_to_malayalam(self, text: str) -> str:
        """Basic English to Malayalam translation for key terms"""
        translations = {
            "rice": "നെല്ല്",
            "coconut": "തെങ്ങ്",
            "pepper": "കുരുമുളക്",
            "farming": "കൃഷി",
            "disease": "രോഗം",
            "fertilizer": "വളം",
            "soil": "മണ്ണ്",
            "weather": "കാലാവസ്ഥ",
            "crop": "വിള",
            "planting": "നടീൽ",
            "harvest": "വിളവെടുപ്പ്",
            "water": "വെള്ളം",
            "season": "സീസൺ",
            "monsoon": "മഴക്കാലം"
        }
        
        # Simple word replacement
        translated = text
        for english, malayalam in translations.items():
            translated = translated.replace(english, malayalam)
        
        # Add Malayalam context
        if any(word in text.lower() for word in ["hello", "hi", "help"]):
            return "നമസ്കാരം! ഞാൻ കൃഷി സഖി ആണ്. കൃഷിയുമായി ബന്ധപ്പെട്ട നിങ്ങളുടെ ചോദ്യങ്ങൾക്ക് ഉത്തരം നൽകാൻ ഞാൻ ഇവിടെയുണ്ട്."
        
        return translated