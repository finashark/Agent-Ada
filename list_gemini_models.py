"""
List available Gemini models
"""
import google.generativeai as genai

API_KEY = "AIzaSyDCsVz0G7kbNG_4vXMdPkOXNkmEdYXDUnU"

try:
    genai.configure(api_key=API_KEY)
    print("Available Gemini models:\n")
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
            print(f"    Display name: {model.display_name}")
            print(f"    Methods: {model.supported_generation_methods}")
            print()
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
