"""
News Provider - Tích hợp tin tức thực từ NewsAPI, Alpha Vantage, Finnhub
"""
import requests
import streamlit as st
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
import logging
from components.session_cache import (
    get_cached_data
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsProvider:
    """Provider tổng hợp tin tức từ nhiều nguồn với fallback"""
    
    def __init__(self):
        # Load API keys từ secrets
        try:
            if hasattr(st, 'secrets') and "news" in st.secrets:
                self.newsapi_key = st.secrets["news"].get("newsapi_key")
                self.alphavantage_key = st.secrets["news"].get("alphavantage_key")
                self.finnhub_key = st.secrets["news"].get("finnhub_key")
                logger.info("Loaded API keys from Streamlit secrets")
            else:
                logger.warning("Streamlit secrets not available, trying environment variables")
                import os
                self.newsapi_key = os.getenv("NEWSAPI_KEY")
                self.alphavantage_key = os.getenv("ALPHAVANTAGE_KEY")
                self.finnhub_key = os.getenv("FINNHUB_KEY")
        except Exception as e:
            logger.error(f"Failed to load API keys: {e}")
            self.newsapi_key = None
            self.alphavantage_key = None
            self.finnhub_key = None
        
        logger.info(f"API Keys loaded: NewsAPI={'✓' if self.newsapi_key else '✗'}, AlphaVantage={'✓' if self.alphavantage_key else '✗'}, Finnhub={'✓' if self.finnhub_key else '✗'}")
    
    def get_news(self, hours_back: int = 48, max_items: int = 10) -> List[Dict]:
        """
        Lấy tin tức từ các provider với session-based SHARED cache
        Cache được share giữa tất cả users - chỉ user đầu tiên fetch
        
        Args:
            hours_back: Số giờ lấy tin ngược lại
            max_items: Số lượng tin tối đa
            
        Returns:
            List tin tức đã chuẩn hóa
        """
        # Định nghĩa fetch function
        def _fetch():
            logger.info(f"🔄 Fetching fresh news (new session or first user)")
            errors = []
            
            # Try NewsAPI first
            if self.newsapi_key:
                try:
                    logger.info("Attempting to fetch from NewsAPI...")
                    news = self._fetch_newsapi(hours_back, max_items)
                    if news and len(news) > 0:
                        logger.info(f"Fetched {len(news)} items from NewsAPI - will be cached for entire session")
                        return news
                    else:
                        logger.warning("NewsAPI returned empty results")
                except Exception as e:
                    error_msg = f"NewsAPI failed: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
            else:
                logger.warning("NewsAPI key not available")
            
            # Fallback to Alpha Vantage
            if self.alphavantage_key:
                try:
                    logger.info("Attempting to fetch from Alpha Vantage...")
                    news = self._fetch_alphavantage(max_items)
                    if news and len(news) > 0:
                        logger.info(f"Fetched {len(news)} items from Alpha Vantage - will be cached for entire session")
                        return news
                    else:
                        logger.warning("Alpha Vantage returned empty results")
                except Exception as e:
                    error_msg = f"Alpha Vantage failed: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
            else:
                logger.warning("Alpha Vantage key not available")
            
            # Fallback to Finnhub
            if self.finnhub_key:
                try:
                    logger.info("Attempting to fetch from Finnhub...")
                    news = self._fetch_finnhub(hours_back, max_items)
                    if news and len(news) > 0:
                        logger.info(f"Fetched {len(news)} items from Finnhub - will be cached for entire session")
                        return news
                    else:
                        logger.warning("Finnhub returned empty results")
                except Exception as e:
                    error_msg = f"Finnhub failed: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
            else:
                logger.warning("Finnhub key not available")
            
            # All failed
            logger.error(f"All news providers failed. Errors: {errors}")
            return []
        
        # Dùng shared cache - tự động handle session-based invalidation
        return get_cached_data(_fetch)
    
    def _fetch_newsapi(self, hours_back: int, max_items: int) -> List[Dict]:
        """Fetch từ NewsAPI.org"""
        from_date = (datetime.now(timezone.utc) - timedelta(hours=hours_back)).strftime("%Y-%m-%d")
        
        # Keywords tập trung vào US markets và major assets
        keywords = '("S&P 500" OR "Nasdaq" OR "Dow Jones" OR "Federal Reserve" OR "Fed rate" OR FOMC OR Bitcoin OR Ethereum OR "gold price" OR "oil price" OR "USD index")'
        
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": keywords,
            "from": from_date,
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": max_items * 2,  # Lấy nhiều hơn để filter
            "apiKey": self.newsapi_key,
            "domains": "bloomberg.com,reuters.com,cnbc.com,wsj.com,ft.com,marketwatch.com,investing.com"  # Chỉ nguồn uy tín
        }
        
        logger.info(f"Calling NewsAPI with params: q={params['q'][:50]}...")
        response = requests.get(url, params=params, timeout=15)
        logger.info(f"NewsAPI response status: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"NewsAPI data: status={data.get('status')}, totalResults={data.get('totalResults', 0)}")
        
        if data["status"] != "ok":
            raise Exception(f"NewsAPI error: {data.get('message', 'Unknown')} - Code: {data.get('code', 'N/A')}")
        
        # Chuẩn hóa format và filter quality
        news_items = []
        for article in data.get("articles", []):
            # Skip removed articles
            if article.get("title") == "[Removed]":
                continue
            
            news_items.append({
                "time": article["publishedAt"],
                "title": article["title"],
                "source": article["source"]["name"],
                "url": article.get("url", ""),
                "asset": self._extract_asset(article["title"] + " " + article.get("description", "")),
                "impact": self._estimate_impact(article["title"]),
                "sentiment": self._analyze_sentiment(article["title"])
            })
            
            if len(news_items) >= max_items:
                break
        
        logger.info(f"Processed {len(news_items)} articles from NewsAPI")
        return news_items
    
    def _fetch_alphavantage(self, max_items: int) -> List[Dict]:
        """Fetch từ Alpha Vantage News & Sentiment"""
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "NEWS_SENTIMENT",
            "topics": "technology,finance,economy",
            "limit": max_items,
            "apikey": self.alphavantage_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_items = []
        for item in data.get("feed", []):
            # Parse sentiment score
            sentiment_score = float(item.get("overall_sentiment_score", 0))
            sentiment = "Positive" if sentiment_score > 0.15 else "Negative" if sentiment_score < -0.15 else "Neutral"
            
            news_items.append({
                "time": item["time_published"],
                "title": item["title"],
                "source": item["source"],
                "url": item.get("url", ""),
                "asset": self._extract_asset_from_tickers(item.get("ticker_sentiment", [])),
                "impact": "Medium",  # Alpha Vantage không có impact score
                "sentiment": sentiment
            })
        
        return news_items[:max_items]
    
    def _fetch_finnhub(self, hours_back: int, max_items: int) -> List[Dict]:
        """Fetch từ Finnhub.io"""
        from_date = datetime.now(timezone.utc) - timedelta(hours=hours_back)
        from_timestamp = int(from_date.timestamp())
        to_timestamp = int(datetime.now(timezone.utc).timestamp())
        
        url = "https://finnhub.io/api/v1/news"
        params = {
            "category": "general",
            "minId": 0,
            "token": self.finnhub_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_items = []
        for item in data:
            # Filter by time
            if item["datetime"] < from_timestamp:
                continue
            
            news_items.append({
                "time": datetime.fromtimestamp(item["datetime"], tz=timezone.utc).isoformat(),
                "title": item["headline"],
                "source": item["source"],
                "url": item.get("url", ""),
                "asset": self._extract_asset(item["headline"]),
                "impact": "Medium",
                "sentiment": self._analyze_sentiment(item["headline"])
            })
            
            if len(news_items) >= max_items:
                break
        
        return news_items
    
    def _extract_asset(self, text: str) -> str:
        """Trích xuất asset từ tiêu đề"""
        text_lower = text.lower()
        
        # Check keywords
        if "s&p 500" in text_lower or "s&p500" in text_lower or "spx" in text_lower:
            return "S&P 500"
        elif "nasdaq" in text_lower or "qqq" in text_lower:
            return "NASDAQ"
        elif "bitcoin" in text_lower or "btc" in text_lower:
            return "BTC"
        elif "ethereum" in text_lower or "eth" in text_lower:
            return "ETH"
        elif "gold" in text_lower:
            return "Gold"
        elif "oil" in text_lower or "crude" in text_lower or "wti" in text_lower:
            return "Oil"
        elif "dollar" in text_lower or "dxy" in text_lower or "usd" in text_lower:
            return "USD"
        elif "fed" in text_lower or "federal reserve" in text_lower or "fomc" in text_lower:
            return "Fed/Rates"
        elif "euro" in text_lower or "eur" in text_lower:
            return "EUR/USD"
        
        # Check tickers
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"]
        for ticker in tickers:
            if ticker.lower() in text_lower or ticker in text:
                return ticker
        
        return "Market"
    
    def _extract_asset_from_tickers(self, ticker_sentiment: List[Dict]) -> str:
        """Trích xuất asset từ ticker sentiment (Alpha Vantage)"""
        if not ticker_sentiment:
            return "Market"
        
        # Lấy ticker có relevance cao nhất
        best_ticker = max(ticker_sentiment, key=lambda x: float(x.get("relevance_score", 0)))
        return best_ticker.get("ticker", "Market")
    
    def _estimate_impact(self, text: str) -> str:
        """Ước lượng impact dựa trên keywords"""
        text_lower = text.lower()
        
        high_impact_keywords = [
            "fed", "fomc", "interest rate", "inflation", "cpi", "unemployment",
            "gdp", "earnings", "crash", "surge", "plunge", "soar", "record"
        ]
        
        medium_impact_keywords = [
            "gain", "loss", "rise", "fall", "increase", "decrease",
            "analyst", "forecast", "outlook", "report"
        ]
        
        for keyword in high_impact_keywords:
            if keyword in text_lower:
                return "High"
        
        for keyword in medium_impact_keywords:
            if keyword in text_lower:
                return "Medium"
        
        return "Low"
    
    def _analyze_sentiment(self, text: str) -> str:
        """Phân tích sentiment đơn giản dựa trên keywords"""
        text_lower = text.lower()
        
        positive_keywords = [
            "gain", "surge", "rally", "rise", "jump", "soar", "climb",
            "beat", "exceed", "outperform", "bullish", "optimistic",
            "strong", "robust", "growth", "recovery"
        ]
        
        negative_keywords = [
            "loss", "fall", "drop", "plunge", "crash", "decline", "sink",
            "miss", "disappoint", "underperform", "bearish", "pessimistic",
            "weak", "concern", "risk", "recession", "inflation"
        ]
        
        pos_count = sum(1 for kw in positive_keywords if kw in text_lower)
        neg_count = sum(1 for kw in negative_keywords if kw in text_lower)
        
        if pos_count > neg_count:
            return "Positive"
        elif neg_count > pos_count:
            return "Negative"
        else:
            return "Neutral"


@st.cache_data(ttl=1800, show_spinner=False)  # Cache 30 phút
def get_market_news(hours_back: int = 48, max_items: int = 10) -> List[Dict]:
    """
    Cached function để lấy tin tức
    
    Args:
        hours_back: Số giờ lấy tin ngược lại
        max_items: Số lượng tin tối đa
        
    Returns:
        List tin tức
    """
    provider = NewsProvider()
    return provider.get_news(hours_back, max_items)
