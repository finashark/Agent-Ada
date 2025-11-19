"""
Test Gemini in Streamlit context
Run with: streamlit run test_gemini_streamlit.py
"""
import streamlit as st
import google.generativeai as genai

st.title("🧪 Gemini API Test")

st.markdown("### Step 1: Load API Key")

try:
    api_key = st.secrets['gemini']['api_key']
    st.success(f"✅ Loaded from secrets: {api_key[:20]}...")
except Exception as e:
    st.error(f"❌ Could not load from secrets: {e}")
    api_key = None

if api_key:
    st.markdown("### Step 2: Configure Gemini")
    try:
        genai.configure(api_key=api_key)
        st.success("✅ Gemini configured")
        
        st.markdown("### Step 3: Create Model")
        model = genai.GenerativeModel('gemini-2.5-flash')
        st.success("✅ Model created")
        
        st.markdown("### Step 4: Test Generation")
        if st.button("Generate Test Response"):
            with st.spinner("Generating..."):
                prompt = "Giới thiệu bản thân bạn là Ada, chuyên gia phân tích tài chính tại HFM. Viết 2-3 câu bằng tiếng Việt."
                response = model.generate_content(prompt)
                st.success("✅ Generation successful!")
                st.markdown("**Response:**")
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"❌ Error: {e}")
        import traceback
        st.code(traceback.format_exc())
else:
    st.warning("No API key available to test")
