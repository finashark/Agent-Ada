#!/usr/bin/env python3
"""Simple yfinance test"""

import yfinance as yf

print("Testing yfinance...")
print("=" * 60)

# Test 1 ticker
ticker = "AAPL"
print(f"\nFetching {ticker}...")

try:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d")
    
    if hist.empty:
        print(f"⚠️ No data for {ticker}")
    else:
        print(f"✅ Got {len(hist)} days of data")
        print(hist.tail())
        
        last = hist["Close"].iloc[-1]
        prev = hist["Close"].iloc[-2]
        pct = ((last / prev) - 1) * 100
        
        print(f"\nLast: ${last:.2f}")
        print(f"% Change: {pct:+.2f}%")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
