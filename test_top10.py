#!/usr/bin/env python3
"""Test Top 10 US Equities"""

import logging
from data_providers.market_details import build_top10_equities

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

print("=" * 60)
print("Testing build_top10_equities()...")
print("=" * 60)

try:
    result = build_top10_equities()
    print(f"\n✅ Success! Got {len(result.items)} items")
    
    if result.items:
        print("\nTop 3:")
        for i, item in enumerate(result.items[:3], 1):
            print(f"  {i}. {item.ticker}: {item.pct_change_d:.2f}%")
    else:
        print("\n⚠️ WARNING: No items returned!")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
