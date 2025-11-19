"""
Quick check if google-generativeai is installed
"""
try:
    import google.generativeai as genai
    print("✅ google-generativeai is installed")
    print(f"Version: {genai.__version__ if hasattr(genai, '__version__') else 'unknown'}")
except ImportError as e:
    print(f"❌ google-generativeai NOT installed: {e}")
    print("\nInstall with: pip install google-generativeai")
