"""
Data provider cho thông tin chi tiết theo thị trường (Trang 2)
Cung cấp snapshot, drivers, trade plans cho từng asset class
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import streamlit as st
import logging
from typing import Dict, List, Tuple
from schemas import MarketDetail, TradePlan, EquityTop10, EquityItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """
    Tính Average True Range (ATR)
    
    Args:
        high: Series giá cao nhất
        low: Series giá thấp nhất
        close: Series giá đóng cửa
        period: Chu kỳ ATR
        
    Returns:
        Series ATR
    """
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(period).mean()


@st.cache_data(ttl=600, show_spinner=False)
def fetch_ohlc(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch dữ liệu OHLC từ yfinance
    
    Args:
        ticker: Mã tài sản
        period: Khoảng thời gian
        interval: Khoảng cách dữ liệu
        
    Returns:
        DataFrame OHLC
    """
    try:
        logger.info(f"Fetching OHLC for {ticker}")
        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False
        )
        
        if df.empty:
            logger.warning(f"No data for {ticker}")
            return pd.DataFrame()
        
        logger.info(f"Fetched {len(df)} rows for {ticker}")
        return df
        
    except Exception as e:
        logger.error(f"Error fetching {ticker}: {e}")
        return pd.DataFrame()


def build_snapshot(df: pd.DataFrame) -> Dict:
    """
    Xây dựng snapshot từ OHLC data
    
    Args:
        df: DataFrame OHLC
        
    Returns:
        Dict snapshot
    """
    try:
        if df.empty or len(df) < 2:
            return {}
        
        last = float(df["Close"].iloc[-1])
        prev_close = float(df["Close"].iloc[-2])
        pct_d1 = ((last / prev_close) - 1) * 100
        
        day_low = float(df["Low"].iloc[-1])
        day_high = float(df["High"].iloc[-1])
        
        atr = calculate_atr(df["High"], df["Low"], df["Close"], period=14)
        atr_val = float(atr.iloc[-1]) if not atr.empty else np.nan
        
        ma20 = float(df["Close"].rolling(20).mean().iloc[-1]) if len(df) >= 20 else np.nan
        ma50 = float(df["Close"].rolling(50).mean().iloc[-1]) if len(df) >= 50 else np.nan
        
        snapshot = {
            "last": last,
            "pct_d1": pct_d1,
            "day_range": f"{day_low:.2f} - {day_high:.2f}",
            "atr14": atr_val,
            "ma20": ma20,
            "ma50": ma50,
            "above_ma20": last > ma20 if not np.isnan(ma20) else None,
            "above_ma50": last > ma50 if not np.isnan(ma50) else None
        }
        
        return snapshot
        
    except Exception as e:
        logger.error(f"Error building snapshot: {e}")
        return {}


def get_mock_news(asset: str) -> List[Dict]:
    """
    Mock tin tức cho asset (thay thế API tin tức)
    
    Args:
        asset: Mã tài sản
        
    Returns:
        List tin tức
    """
    news_templates = {
        "GC=F": [
            {"title": "(Fact) Fed giữ nguyên lãi suất", "url": "https://www.federalreserve.gov/"},
            {"title": "(Fact) USD index tăng 0.3%", "url": ""},
        ],
        "BTC-USD": [
            {"title": "(Fact) Bitcoin ETF inflows đạt $500M", "url": ""},
            {"title": "(Fact) SEC hoãn quyết định về Ethereum ETF", "url": ""},
        ],
        "^GSPC": [
            {"title": "(Fact) Earnings season Q3 vượt kỳ vọng 70%", "url": ""},
            {"title": "(Fact) Tech stocks dẫn dắt đà tăng", "url": ""},
        ]
    }
    
    return news_templates.get(asset, [
        {"title": "(Fact) Chưa có tin tức cập nhật", "url": ""}
    ])


def get_mock_drivers(asset: str) -> List[str]:
    """
    Mock yếu tố chi phối
    
    Args:
        asset: Mã tài sản
        
    Returns:
        List drivers với impact_sign
    """
    drivers_map = {
        "GC=F": [
            "(+) DXY yếu đi hỗ trợ giá vàng [High confidence]",
            "(0) Real yields ổn định [Medium confidence]",
            "(-) Risk appetite cải thiện làm giảm safe-haven demand [Medium confidence]"
        ],
        "BTC-USD": [
            "(+) ETF inflows mạnh [High confidence]",
            "(+) Macro bullish: kỳ vọng cắt giảm lãi suất [Medium confidence]",
            "(0) Regulatory uncertainty [Low confidence]"
        ],
        "^GSPC": [
            "(+) Earnings Q3 vượt kỳ vọng [High confidence]",
            "(0) Fed giữ stance hawkish [Medium confidence]",
            "(-) Valuations cao có thể hạn chế upside [Low confidence]"
        ]
    }
    
    return drivers_map.get(asset, [
        "(0) Chưa xác định rõ drivers [Low confidence]"
    ])


def build_trade_plan(asset: str, snapshot: Dict) -> TradePlan:
    """
    Xây dựng trade plan mẫu
    
    Args:
        asset: Mã tài sản
        snapshot: Snapshot data
        
    Returns:
        TradePlan object
    """
    last = snapshot.get("last", 0)
    atr = snapshot.get("atr14", 0)
    
    # Tính levels đơn giản (có thể cải thiện)
    r1 = last + atr if atr else None
    r2 = last + 2 * atr if atr else None
    s1 = last - atr if atr else None
    s2 = last - 2 * atr if atr else None
    
    plan = TradePlan(
        bias="Neutral",
        levels={
            "R1": r1,
            "R2": r2,
            "S1": s1,
            "S2": s2
        },
        trigger="Đóng nến H1 vượt R1 với volume tăng",
        invalidation="Thủng S2 với nến H4 đóng cửa bên dưới",
        timeframe="H1-H4",
        risk_events="CPI data, Fed minutes"
    )
    
    return plan


def build_detail(asset: str) -> MarketDetail:
    """
    Xây dựng MarketDetail cho một asset
    
    Args:
        asset: Mã tài sản
        
    Returns:
        MarketDetail object
    """
    logger.info(f"Building detail for {asset}")
    
    # Fetch OHLC
    df = fetch_ohlc(asset, period="6mo", interval="1d")
    
    # Build snapshot
    snapshot = build_snapshot(df)
    
    # Get news
    updates = get_mock_news(asset)
    
    # Get drivers
    drivers = get_mock_drivers(asset)
    
    # Build trade plan
    trade_plan = build_trade_plan(asset, snapshot)
    
    # Alternative scenarios
    alternative_scenarios = [
        "Nếu phá vỡ R2, target tiếp theo là R3 (Fibonacci extension)",
        "Nếu thủng S1, có thể test lại MA50 hoặc S2",
    ]
    
    detail = MarketDetail(
        asset=asset,
        snapshot=snapshot,
        updates=updates,
        drivers=drivers,
        trade_plan=trade_plan,
        alternative_scenarios=alternative_scenarios,
        notes="Cần theo dõi volume confirmation và divergence trên RSI",
        impact_sign="0",
        confidence="Medium",
        last_updated=datetime.now(timezone.utc).isoformat()
    )
    
    logger.info(f"Detail built for {asset}")
    return detail


# ============== US EQUITIES SPECIFIC ==============

@st.cache_data(ttl=86400, show_spinner=False)  # Cache 24h
def get_sp500_tickers() -> List[str]:
    """
    Lấy danh sách tickers S&P 500 từ Wikipedia
    
    Returns:
        List tickers
    """
    try:
        logger.info("Fetching S&P 500 tickers from Wikipedia")
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        tables = pd.read_html(url)
        df = tables[0]
        tickers = df["Symbol"].tolist()
        
        # Clean tickers (remove dots)
        tickers = [t.replace(".", "-") for t in tickers]
        
        logger.info(f"Fetched {len(tickers)} S&P 500 tickers")
        return tickers
        
    except Exception as e:
        logger.error(f"Error fetching S&P 500 tickers: {e}")
        # Fallback to a small list
        return ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK-B", "JPM", "V"]


def get_nasdaq_large_caps() -> List[str]:
    """
    Lấy danh sách cổ phiếu vốn hóa lớn và phổ biến trên NASDAQ
    
    Sử dụng các chỉ số thành phần của NASDAQ-100 và một số cổ phiếu blue-chip khác
    
    Returns:
        List tickers NASDAQ large-cap
    """
    # NASDAQ-100 major components + thêm một số cổ phiếu phổ biến
    nasdaq_tickers = [
        # Tech Giants
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA",
        # Semiconductors
        "AVGO", "AMD", "INTC", "QCOM", "MU", "AMAT", "LRCX", "KLAC", "MRVL", "NXPI",
        # Software & Cloud
        "ORCL", "ADBE", "CRM", "NOW", "INTU", "PANW", "SNPS", "CDNS", "ANSS", "WDAY",
        # E-commerce & Consumer
        "COST", "SBUX", "ABNB", "BKNG", "EBAY", "JD", "PDD", "MELI",
        # Biotech & Healthcare
        "GILD", "AMGN", "REGN", "VRTX", "BIIB", "MRNA", "ILMN", "SGEN",
        # Communications & Media
        "NFLX", "CMCSA", "CHTR", "EA", "ATVI", "TTWO",
        # Payment & Fintech
        "PYPL", "ADYEN", "SQ",
        # Other major NASDAQ
        "CSCO", "PEP", "TMUS", "TXN", "HON", "ADP", "ISRG", "LULU", "MDLZ", "ADI",
        "ASML", "PAYX", "CTAS", "MAR", "MCHP", "PCAR", "AEP", "KDP", "MNST", "DXCM",
        # Recent additions (AI wave)
        "ARM", "CRWD", "FTNT", "ZS", "DDOG", "NET", "SNOW", "MDB", "PLTR", "RBLX",
    ]
    
    logger.info(f"Using {len(nasdaq_tickers)} NASDAQ large-cap tickers")
    return nasdaq_tickers


def calculate_stock_score(ticker: str, pct_change: float, vol_ratio: float, has_news: bool = False) -> float:
    """
    Tính điểm xếp hạng cổ phiếu
    
    Args:
        ticker: Mã cổ phiếu
        pct_change: % thay đổi
        vol_ratio: Tỷ lệ volume vs trung bình
        has_news: Có tin tức không
        
    Returns:
        Điểm số
    """
    # Tính z-score cho % change và vol_ratio (đơn giản hoá)
    zscore_pct = pct_change / 5.0  # Giả định std = 5%
    zscore_vol = (vol_ratio - 1.0) / 0.5  # Giả định std = 0.5
    
    score = zscore_pct + zscore_vol
    
    if has_news:
        score += 1.0
    
    return score


@st.cache_data(ttl=600, show_spinner=False)
def build_top10_equities(universe: str = "NASDAQ Large-Cap") -> EquityTop10:
    """
    Xây dựng Top 10 cổ phiếu tăng mạnh nhất trong phiên gần nhất
    
    Universe: Các cổ phiếu vốn hóa lớn và phổ biến trên NASDAQ
    Xếp hạng: Top 10 cổ phiếu có % tăng cao nhất trong phiên gần nhất
    
    Args:
        universe: Universe name
        
    Returns:
        EquityTop10 object
    """
    logger.info("Building Top 10 strongest NASDAQ equities...")
    
    # Lấy danh sách NASDAQ large-caps
    tickers = get_nasdaq_large_caps()
    
    items = []
    
    # Fetch giá cho tất cả tickers (batch download nhanh hơn)
    logger.info(f"Fetching prices for {len(tickers)} NASDAQ tickers...")
    
    for ticker in tickers:
        try:
            df = fetch_ohlc(ticker, period="1mo", interval="1d")
            
            if df.empty or len(df) < 2:
                continue
            
            last = float(df["Close"].iloc[-1])
            prev = float(df["Close"].iloc[-2])
            pct_change = ((last / prev) - 1) * 100
            
            # Tính vol ratio
            if len(df) >= 20:
                vol_20d_avg = df["Volume"].tail(20).mean()
                last_vol = float(df["Volume"].iloc[-1])
                vol_ratio = last_vol / vol_20d_avg if vol_20d_avg > 0 else 1.0
            else:
                vol_ratio = 1.0
            
            # Simple score = pct_change (chỉ xếp hạng theo % tăng)
            score = pct_change
            
            # Tạo idea dựa trên % thay đổi
            if pct_change > 5:
                idea = "Tăng đột biến - cảnh báo profit-taking"
            elif pct_change > 3:
                idea = "Momentum mạnh - theo dõi pullback"
            elif pct_change > 1:
                idea = "Tăng nhẹ - xu hướng tích cực"
            elif pct_change > 0:
                idea = "Tăng yếu - consolidation"
            else:
                idea = "Điều chỉnh - chờ entry"
            
            item = EquityItem(
                ticker=ticker,
                last=last,
                pct_change=pct_change,
                vol_ratio=vol_ratio,
                catalyst="Market momentum",
                source_url=f"https://finance.yahoo.com/quote/{ticker}",
                idea=idea,
                score=score
            )
            
            items.append(item)
            
        except Exception as e:
            logger.warning(f"Error processing {ticker}: {e}")
            continue
    
    # Sắp xếp theo % tăng giảm (descending)
    items.sort(key=lambda x: x.pct_change, reverse=True)
    
    # Lấy top 10 tăng mạnh nhất
    top_items = items[:10]
    
    result = EquityTop10(
        universe=universe,
        method="Top 10 cổ phiếu tăng mạnh nhất trong phiên gần nhất (theo %d/d)",
        items=top_items,
        score_components={
            "ranking_criteria": "% Change D/D",
            "universe": "NASDAQ Large-Cap (~100 stocks)",
            "note": "Score = % Change, không weighted"
        },
        last_updated=datetime.now(timezone.utc).isoformat()
    )
    
    logger.info(f"Top 10 equities built with {len(top_items)} items (strongest gainers)")
    return result


# ============== FX MAJORS ==============

FX_MAJORS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X",
    "USDCAD=X",
    "USDCHF=X",
]


# ============== CRYPTO ==============

CRYPTO_MAJORS = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "BNB-USD",
    "XRP-USD",
    "ADA-USD",
]


# ============== COMMODITIES ==============

OIL_TICKERS = [
    "CL=F",  # WTI Crude
    "BZ=F",  # Brent Crude
]


# ============== INDICES ==============

GLOBAL_INDICES = [
    "^GSPC",      # S&P 500
    "^NDX",       # Nasdaq 100
    "^DJI",       # Dow Jones
    "^GDAXI",     # DAX
    "^FTSE",      # FTSE 100
    "^N225",      # Nikkei 225
    "^HSI",       # Hang Seng
    "^STOXX50E",  # Euro Stoxx 50
]
