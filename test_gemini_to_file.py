"""
Test Gemini API and write results to file
"""
import google.generativeai as genai
import sys
from datetime import datetime

output_file = "gemini_test_result.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"=== GEMINI API TEST === {datetime.now()}\n\n")
    
    # API Key
    API_KEY = "AIzaSyBQUuZ8V5VycCBfg0XJ-U9bFszqxi_xmFY"
    f.write(f"API Key: {API_KEY[:20]}...\n\n")
    
    try:
        # Step 1: Configure
        genai.configure(api_key=API_KEY)
        f.write("✅ Step 1: API configured successfully\n")
        
        # Step 2: Create model
        model = genai.GenerativeModel('gemini-pro')
        f.write("✅ Step 2: Model created successfully\n")
        
        # Step 3: Test generation
        prompt = "Respond in Vietnamese: Giới thiệu bản thân bạn là Ada, chuyên gia phân tích tài chính."
        f.write(f"\nPrompt: {prompt}\n\n")
        
        response = model.generate_content(prompt)
        f.write(f"✅ Step 3: Generation successful\n\n")
        f.write(f"Response:\n{response.text}\n")
        
        f.write("\n=== ALL TESTS PASSED ===\n")
        
    except Exception as e:
        f.write(f"\n❌ ERROR: {e}\n")
        import traceback
        f.write(traceback.format_exc())

print(f"Test results written to: {output_file}")
