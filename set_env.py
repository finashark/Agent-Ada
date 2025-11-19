"""
Set environment variables for news API keys
Run this before starting Streamlit if secrets.toml is not available
"""
import os

# Set API keys as environment variables
os.environ["NEWSAPI_KEY"] = "ab2c6f479852474a87498b70d7d2b38e"
os.environ["ALPHAVANTAGE_KEY"] = "YX8BR3SF06HM130H"
os.environ["FINNHUB_KEY"] = "ciujme9r01qi3i2j92q0ciujme9r01qi3i2j92qg"

print("✅ Environment variables set!")
print("Now run: streamlit run Home.py")
