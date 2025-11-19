#!/usr/bin/env python3
"""Test Gemini API configuration"""

import sys
import os

# Test 1: Check secrets.toml file
print("=" * 60)
print("TEST 1: Check secrets.toml")
print("=" * 60)

secrets_path = ".streamlit/secrets.toml"
if os.path.exists(secrets_path):
    print(f"✅ Found {secrets_path}")
    with open(secrets_path, 'r') as f:
        content = f.read()
        if '[gemini]' in content:
            print("✅ [gemini] section exists")
            if 'api_key' in content:
                # Extract key (first 20 chars)
                lines = content.split('\n')
                for line in lines:
                    if 'api_key' in line and '=' in line:
                        key_part = line.split('=')[1].strip().strip('"')[:20]
                        print(f"✅ API key found: {key_part}...")
        else:
            print("❌ [gemini] section NOT found")
else:
    print(f"❌ {secrets_path} NOT found")

print()

# Test 2: Try to import and initialize
print("=" * 60)
print("TEST 2: Initialize Gemini")
print("=" * 60)

try:
    import streamlit as st
    
    # Mock st.secrets for testing
    if not hasattr(st, 'secrets'):
        print("⚠️ Not running in Streamlit, will use file parsing")
        import toml
        if os.path.exists(secrets_path):
            config = toml.load(secrets_path)
            if 'gemini' in config and 'api_key' in config['gemini']:
                api_key = config['gemini']['api_key']
                print(f"✅ Loaded API key from TOML: {api_key[:20]}...")
            else:
                print("❌ gemini.api_key not found in TOML")
                api_key = None
        else:
            api_key = None
    else:
        api_key = st.secrets.get('gemini', {}).get('api_key')
        print(f"✅ Loaded from st.secrets: {api_key[:20] if api_key else 'None'}...")
    
    if api_key:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        print("✅ Gemini model initialized successfully!")
        
        # Test a simple generation
        print("\nTesting generation...")
        response = model.generate_content("Say 'Hello, Ada!' in Vietnamese")
        print(f"✅ Response: {response.text}")
        
    else:
        print("❌ API key is None")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test completed!")
