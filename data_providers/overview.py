"""
Data provider cho tổng quan thị trường (Trang 1)
Cung cấp dữ liệu điểm nhấn, vĩ mô, lịch kinh tế, tâm lý rủi ro
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
import streamlit as st
import logging
from typing import List, Dict, Tuple
from schemas import MarketOverview, CalendarItem
from components.session_badge import session_status, session_ttl
from components.session_cache import (
    get_market_data_cache_key,
    get_cached_data,
    set_cached_data,
    get_cache_timestamp,
    should_refresh_cache
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Danh sách tài sản theo dõi
CORE_ASSETS = [
    "^GSPC",     # S&P 500
    "^NDX",      # Nasdaq 100
    "^DJI",      # Dow Jones
    "DX-Y.NYB",  # US Dollar Index (DXY alternative - ^DXY often fails)
    "^VIX",      # Volatility Index
    "^TNX",      # 10-Year Treasury Yield
    "GC=F",      # Gold Futures
    "CL=F",      # Crude Oil WTI
    "BTC-USD",   # Bitcoin
]

# Ticker display name mapping
TICKER_DISPLAY_NAMES = {
    "DX-Y.NYB": "DXY",  # Display as DXY instead of DX-Y.NYB
}


def fetch_prices(tickers: List[str], period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch giá từ yfinance với session-based cache
    Chỉ fetch mới khi sang phiên giao dịch mới (4 lần/ngày tối đa)
    
    Args:
        tickers: Danh sách mã tài sản
        period: Khoảng thời gian (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        interval: Khoảng cách dữ liệu (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        
    Returns:
        DataFrame với giá Close
    """
    # Tạo cache key cho phiên hiện tại
    cache_key = get_market_data_cache_key()
    cache_timestamp = get_cache_timestamp(cache_key)
    
    # Kiểm tra xem có cần refresh không
    if not should_refresh_cache(cache_timestamp):
        # Lấy từ cache
        cached_data = get_cached_data(cache_key)
        if cached_data is not None:
            logger.info(f"📦 Using cached market data from {cache_timestamp}")
            return cached_data
    
    # Fetch data mới
    logger.info(f"🔄 Fetching fresh market data (new session)")
    try:
        logger.info(f"Fetching prices for {len(tickers)} tickers: period={period}, interval={interval}")
        
        data = yf.download(
            tickers=tickers,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
            threads=True
        )
        
        # Xử lý MultiIndex columns nếu có nhiều tickers
        if isinstance(data.columns, pd.MultiIndex):
            data = data["Close"]
        
        logger.info(f"Successfully fetched {len(data)} rows of data")
        
        # Lưu vào cache
        set_cached_data(cache_key, data)
        logger.info(f"💾 Cached market data for session")
        
        return data
        
    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        st.warning(f"⚠️ Không thể tải dữ liệu giá: {e}")
        return pd.DataFrame()


def calculate_period_return(prices: pd.Series, days: int) -> float:
    """
    Tính % thay đổi trong một khoảng thời gian
    
    Args:
        prices: Series giá
        days: Số ngày lookback
        
    Returns:
        % thay đổi
    """
    try:
        if len(prices) <= days + 1:
            return (prices.iloc[-1] / prices.iloc[0] - 1.0) * 100.0
        return (prices.iloc[-1] / prices.iloc[-(days + 1)] - 1.0) * 100.0
    except:
        return np.nan


def calculate_zscore(series: pd.Series, window: int = 20) -> float:
    """
    Tính z-score của giá trị cuối cùng
    
    Args:
        series: Series dữ liệu
        window: Cửa sổ tính toán
        
    Returns:
        z-score
    """
    try:
        if len(series) < window:
            return np.nan
        
        mean = series.tail(window).mean()
        std = series.tail(window).std()
        
        if std == 0:
            return 0.0
        
        return (series.iloc[-1] - mean) / std
    except:
        return np.nan


@st.cache_data(ttl=600, show_spinner=False)
def get_market_snapshot() -> Dict:
    """
    Lấy snapshot thị trường hiện tại
    
    Returns:
        Dict chứa giá hiện tại, % thay đổi D1, WTD, MTD, z-scores
    """
    try:
        prices = fetch_prices(CORE_ASSETS, period="3mo", interval="1d")
        
        if prices.empty:
            return {}
        
        snapshot = {}
        
        for ticker in CORE_ASSETS:
            try:
                if ticker not in prices.columns:
                    continue
                
                ticker_prices = prices[ticker].dropna()
                
                if len(ticker_prices) < 2:
                    continue
                
                last_price = float(ticker_prices.iloc[-1])
                d1_return = calculate_period_return(ticker_prices, 1)
                wtd_return = calculate_period_return(ticker_prices, 5)
                mtd_return = calculate_period_return(ticker_prices, 22)
                zscore = calculate_zscore(ticker_prices, window=20)
                
                # Use display name if available
                display_ticker = TICKER_DISPLAY_NAMES.get(ticker, ticker)
                
                snapshot[display_ticker] = {
                    "last": last_price,
                    "d1": d1_return,
                    "wtd": wtd_return,
                    "mtd": mtd_return,
                    "zscore": zscore
                }
                
            except Exception as e:
                logger.warning(f"Error processing {ticker}: {e}")
                continue
        
        logger.info(f"Market snapshot created with {len(snapshot)} assets")
        return snapshot
        
    except Exception as e:
        logger.error(f"Error in get_market_snapshot: {e}")
        return {}


@st.cache_data(ttl=1800, show_spinner=False)
def get_mock_calendar() -> List[CalendarItem]:
    """
    Mock lịch kinh tế (sử dụng khi không có API key)
    
    Returns:
        List CalendarItem
    """
    today = datetime.now(timezone.utc)
    
    mock_events = [
        CalendarItem(
            time_local="20:30",
            region="US",
            event="CPI (YoY)",
            consensus=3.2,
            prior=3.4,
            impact="High",
            source_url="https://www.bls.gov/"
        ),
        CalendarItem(
            time_local="14:00",
            region="US",
            event="FOMC Minutes",
            consensus=None,
            prior=None,
            impact="High",
            source_url="https://www.federalreserve.gov/"
        ),
        CalendarItem(
            time_local="15:30",
            region="EU",
            event="ECB Speech",
            consensus=None,
            prior=None,
            impact="Medium",
            source_url="https://www.ecb.europa.eu/"
        ),
    ]
    
    return mock_events


def generate_highlights(snapshot: Dict) -> List[str]:
    """
    Tạo điểm nhấn từ dữ liệu thị trường
    
    Args:
        snapshot: Market snapshot data
        
    Returns:
        List highlights (Fact + Interpretation tách rõ)
    """
    highlights = []
    
    try:
        # S&P 500
        if "^GSPC" in snapshot:
            spx = snapshot["^GSPC"]
            highlights.append(
                f"(Fact) S&P 500: {spx['last']:.2f} ({spx['d1']:+.2f}%, z-score: {spx['zscore']:.2f})"
            )
            
            if abs(spx['d1']) > 1.0:
                direction = "tăng mạnh" if spx['d1'] > 0 else "giảm mạnh"
                highlights.append(
                    f"(Interpretation) SPX {direction}, phản ánh tâm lý thị trường biến động"
                )
        
        # VIX
        if "^VIX" in snapshot:
            vix = snapshot["^VIX"]
            highlights.append(
                f"(Fact) VIX: {vix['last']:.2f} ({vix['d1']:+.2f}%)"
            )
            
            if vix['last'] > 20:
                highlights.append(
                    f"(Interpretation) VIX trên 20 cho thấy lo ngại gia tăng trên thị trường"
                )
        
        # DXY
        if "DXY" in snapshot:
            dxy = snapshot["DXY"]
            highlights.append(
                f"(Fact) DXY: {dxy['last']:.2f} ({dxy['d1']:+.2f}%)"
            )
        
        # Gold
        if "GC=F" in snapshot:
            gold = snapshot["GC=F"]
            highlights.append(
                f"(Fact) Vàng: ${gold['last']:.2f} ({gold['d1']:+.2f}%)"
            )
        
    except Exception as e:
        logger.error(f"Error generating highlights: {e}")
    
    return highlights if highlights else ["Chưa có dữ liệu điểm nhấn"]


def generate_macro_briefs() -> List[str]:
    """
    Tạo tóm tắt vĩ mô
    
    Returns:
        List macro briefs
    """
    briefs = [
        "(Fact) Fed duy trì lãi suất 5.25-5.50%, chờ thêm dữ liệu lạm phát",
        "(Fact) PMI sản xuất Mỹ tháng trước: 48.7 (dưới 50 = suy giảm)",
        "(Interpretation) Thị trường kỳ vọng Fed có thể cắt giảm lãi suất trong Q4",
    ]
    return briefs


def build_overview(tz_name: str = "Asia/Ho_Chi_Minh") -> MarketOverview:
    """
    Xây dựng MarketOverview cho Trang 1
    
    Args:
        tz_name: Timezone name
        
    Returns:
        MarketOverview object
    """
    logger.info("Building market overview...")
    
    now_utc = datetime.now(timezone.utc)
    badges, active_session = session_status(now_utc)
    
    # Lấy snapshot thị trường
    snapshot = get_market_snapshot()
    
    # Tạo highlights
    highlights = generate_highlights(snapshot)
    
    # Tạo macro briefs
    macro_briefs = generate_macro_briefs()
    
    # Risk sentiment
    risk_sentiment = {}
    if "^VIX" in snapshot:
        risk_sentiment["vix"] = snapshot["^VIX"]["last"]
    if "DXY" in snapshot:
        risk_sentiment["dxy"] = snapshot["DXY"]["last"]
    if "^TNX" in snapshot:
        risk_sentiment["us10y"] = snapshot["^TNX"]["last"]
    
    # Lịch kinh tế
    calendar = get_mock_calendar()
    
    # Objectivity notes
    objectivity_notes = [
        "✓ Tách rõ Fact (sự kiện/số liệu) và Interpretation (diễn giải)",
        "✓ Hiển thị nguồn dữ liệu: yfinance + lịch kinh tế mock",
        "✓ Z-score tính trên cửa sổ 20 ngày",
        "✓ Tránh khẳng định tuyệt đối, thừa nhận giới hạn dự báo"
    ]
    
    overview = MarketOverview(
        date=now_utc.date().isoformat(),
        highlights=highlights,
        macro_briefs=macro_briefs,
        risk_sentiment=risk_sentiment,
        market_snapshot=snapshot,  # Add snapshot for AI analysis
        economic_calendar=calendar,
        session=active_session,
        last_updated=now_utc.isoformat(),
        objectivity_notes=objectivity_notes
    )
    
    logger.info("Market overview built successfully")
    return overview


@st.cache_data(ttl=600, show_spinner=False)
def get_cross_asset_table() -> pd.DataFrame:
    """
    Tạo bảng cross-asset với D1/WTD/MTD
    
    Returns:
        DataFrame
    """
    snapshot = get_market_snapshot()
    
    if not snapshot:
        return pd.DataFrame()
    
    data = []
    for ticker, vals in snapshot.items():
        data.append({
            "Asset": ticker,
            "Last": f"{vals['last']:.2f}",
            "D1 (%)": f"{vals['d1']:.2f}",
            "WTD (%)": f"{vals['wtd']:.2f}",
            "MTD (%)": f"{vals['mtd']:.2f}",
            "Z-Score": f"{vals['zscore']:.2f}"
        })
    
    return pd.DataFrame(data)
