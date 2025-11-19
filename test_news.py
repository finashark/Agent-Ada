"""
Test script để kiểm tra news API
"""
import sys
sys.path.insert(0, '.')

from data_providers.news_provider import NewsProvider
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

print("=" * 60)
print("Testing News Provider APIs")
print("=" * 60)

provider = NewsProvider()

print(f"\nAPI Keys status:")
print(f"  NewsAPI: {'✓' if provider.newsapi_key else '✗'}")
print(f"  Alpha Vantage: {'✓' if provider.alphavantage_key else '✗'}")
print(f"  Finnhub: {'✓' if provider.finnhub_key else '✗'}")

print("\n" + "=" * 60)
print("Fetching news...")
print("=" * 60)

news = provider.get_news(hours_back=48, max_items=5)

print(f"\nResults: {len(news)} items")
print("=" * 60)

if news:
    for i, item in enumerate(news, 1):
        print(f"\n{i}. [{item['asset']}] {item['title']}")
        print(f"   Source: {item['source']} | Impact: {item['impact']} | Sentiment: {item['sentiment']}")
        print(f"   Time: {item['time']}")
else:
    print("\n❌ No news fetched. Check logs above for errors.")

print("\n" + "=" * 60)
