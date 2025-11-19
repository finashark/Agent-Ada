#!/usr/bin/env python3
"""Test Ada AI Analyst with Gemini"""

import logging
from data_providers.ai_analyst import get_ada_analyst

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

print("=" * 60)
print("Testing Ada AI Analyst (Gemini)")
print("=" * 60)

# Initialize
analyst = get_ada_analyst()

if analyst.model is None:
    print("\n❌ Gemini not initialized. Check API key in secrets.toml")
else:
    print("\n✅ Gemini initialized successfully!")
    
    # Mock data
    snapshot = {
        "^VIX": {"last": 18.5, "d1": 2.3},
        "^GSPC": {"last": 5950.0, "d1": -0.5},
        "DXY": {"last": 103.5, "d1": 0.3}
    }
    
    news = [
        {
            "title": "Fed signals rate cut possible in December",
            "description": "Federal Reserve officials indicate they may consider cutting rates if inflation continues to moderate",
            "sentiment": "Positive",
            "impact": "High",
            "assets": ["S&P 500", "USD"]
        },
        {
            "title": "Tech stocks rally on strong AI earnings",
            "description": "NVDA and MSFT beat expectations, boosting tech sector",
            "sentiment": "Positive",
            "impact": "Medium",
            "assets": ["NVDA", "MSFT", "NASDAQ"]
        }
    ]
    
    print("\nGenerating market overview analysis...")
    print("-" * 60)
    
    analysis = analyst.generate_market_overview_analysis(
        snapshot=snapshot,
        news=news,
        vix_level=18.5,
        spx_change=-0.5,
        dxy_level=103.5
    )
    
    print(analysis)
    print("\n" + "=" * 60)
    print("✅ Test completed!")
