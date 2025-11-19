"""
Simple test to verify Gemini API works
"""
import google.generativeai as genai

# Directly use API key
API_KEY = "AIzaSyBQUuZ8V5VycCBfg0XJ-U9bFszqxi_xmFY"

print("Testing Gemini API...")
print(f"API Key: {API_KEY[:20]}...")

try:
    # Configure
    genai.configure(api_key=API_KEY)
    print("✅ API configured")
    
    # Create model
    model = genai.GenerativeModel('gemini-pro')
    print("✅ Model created")
    
    # Test generation
    response = model.generate_content("Say 'Xin chào! Tôi là Ada, chuyên gia phân tích tài chính.' in Vietnamese")
    print(f"✅ Generation successful:\n{response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
