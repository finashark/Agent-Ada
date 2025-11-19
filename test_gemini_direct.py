"""
Direct test of Gemini API without Streamlit
"""
import google.generativeai as genai
import sys

API_KEY = "AIzaSyDCsVz0G7kbNG_4vXMdPkOXNkmEdYXDUnU"

print("=" * 60)
print("GEMINI API DIRECT TEST")
print("=" * 60)

try:
    print("\n1. Configuring API...")
    genai.configure(api_key=API_KEY)
    print("   [OK] API configured")
    
    print("\n2. Creating model...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("   [OK] Model created")
    
    print("\n3. Testing generation...")
    prompt = "Viết 2 câu giới thiệu bản thân bạn là Ada, chuyên gia phân tích tài chính."
    print(f"   Prompt: {prompt}")
    
    response = model.generate_content(prompt)
    print("\n   [OK] Generation successful!")
    print("\n" + "=" * 60)
    print("RESPONSE:")
    print("=" * 60)
    print(response.text)
    print("=" * 60)
    
    print("\n[SUCCESS] ALL TESTS PASSED\n")
    sys.exit(0)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    print("\nFull traceback:")
    import traceback
    traceback.print_exc()
    sys.exit(1)
