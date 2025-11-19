"""
Session-based caching system
Chỉ refresh data khi phiên giao dịch mới bắt đầu (4 lần/ngày)
Cache được share giữa tất cả users để tiết kiệm API calls
"""
from datetime import datetime, time, timezone
import pytz
import streamlit as st
from typing import Optional, Tuple, Any
import hashlib


# 4 phiên giao dịch chính trong ngày
TRADING_SESSIONS = [
    {
        "name": "Asia",
        "timezone": "Asia/Singapore",
        "start": time(9, 0),   # 9:00 AM Singapore
        "end": time(16, 30)    # 4:30 PM Singapore
    },
    {
        "name": "Europe",
        "timezone": "Europe/London",
        "start": time(8, 0),   # 8:00 AM London
        "end": time(16, 30)    # 4:30 PM London
    },
    {
        "name": "US",
        "timezone": "America/New_York",
        "start": time(9, 30),  # 9:30 AM New York
        "end": time(16, 0)     # 4:00 PM New York
    },
    {
        "name": "After-Hours",
        "timezone": "America/New_York",
        "start": time(16, 0),  # 4:00 PM New York
        "end": time(20, 0)     # 8:00 PM New York
    }
]


def get_current_session(now_utc: Optional[datetime] = None) -> Tuple[str, datetime]:
    """
    Xác định phiên giao dịch hiện tại
    
    Args:
        now_utc: Thời gian UTC (None = lấy thời gian hiện tại)
        
    Returns:
        Tuple (session_name, session_start_utc)
    """
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    
    # Kiểm tra từng phiên
    for session in TRADING_SESSIONS:
        tz = pytz.timezone(session["timezone"])
        local_now = now_utc.astimezone(tz)
        
        # Tạo datetime cho start và end trong ngày hiện tại
        start_dt = local_now.replace(
            hour=session["start"].hour,
            minute=session["start"].minute,
            second=0,
            microsecond=0
        )
        end_dt = local_now.replace(
            hour=session["end"].hour,
            minute=session["end"].minute,
            second=0,
            microsecond=0
        )
        
        # Kiểm tra nằm trong phiên
        if start_dt <= local_now <= end_dt:
            # Convert start_dt sang UTC
            session_start_utc = start_dt.astimezone(timezone.utc)
            return session["name"], session_start_utc
    
    # Nếu không phiên nào active, trả về "Off-Market"
    # Session start = đầu ngày UTC
    session_start_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    return "Off-Market", session_start_utc


def get_session_cache_key(cache_type: str = "market_data") -> str:
    """
    Tạo cache key dựa trên phiên hiện tại
    Cache key thay đổi khi sang phiên mới → force refresh
    
    Args:
        cache_type: Loại cache (market_data, news, ai_analysis)
        
    Returns:
        Cache key string (VD: "market_data_2025-11-19_Asia")
    """
    session_name, session_start = get_current_session()
    date_str = session_start.strftime("%Y-%m-%d")
    
    return f"{cache_type}_{date_str}_{session_name}"


# Wrapper functions để cache data với session-based key
# Cache này được SHARE giữa tất cả users
@st.cache_data(ttl=None, show_spinner=False)
def _cached_fetch(_cache_key: str, _fetch_func, *args, **kwargs) -> Any:
    """
    Internal cache wrapper - SHARED giữa tất cả users
    
    Args:
        _cache_key: Cache key (unused, chỉ để force invalidate)
        _fetch_func: Function để fetch data
        *args, **kwargs: Arguments cho fetch_func
        
    Returns:
        Cached data
    """
    # Khi cache_key thay đổi (sang phiên mới), Streamlit sẽ tự động
    # invalidate cache và gọi lại function này
    return _fetch_func(*args, **kwargs)


def should_refresh_cache(last_update: Optional[datetime] = None) -> bool:
    """
    Kiểm tra có nên refresh cache không
    
    Args:
        last_update: Thời điểm update cuối cùng (UTC)
        
    Returns:
        True nếu cần refresh (phiên mới hoặc chưa có data)
    """
    if last_update is None:
        return True
    
    # Lấy session hiện tại và session của lần update cuối
    current_session, current_start = get_current_session()
    
    # Nếu last_update trước session_start hiện tại → cần refresh
    return last_update < current_start


def get_cached_data(_fetch_func, *args, **kwargs) -> Any:
    """
    Lấy data từ shared cache hoặc fetch mới nếu cần
    
    Cơ chế:
    - Cache key dựa trên phiên hiện tại
    - Khi sang phiên mới → cache key thay đổi → auto refresh
    - Cache được SHARE giữa tất cả users → chỉ user đầu tiên fetch
    
    Args:
        _fetch_func: Function để fetch data (VD: lambda: fetch_prices(...))
        *args, **kwargs: Arguments cho fetch_func
        
    Returns:
        Cached hoặc fresh data
    """
    # Tạo cache key dựa trên function name
    func_name = _fetch_func.__name__ if hasattr(_fetch_func, '__name__') else 'data'
    cache_key = get_session_cache_key(func_name)
    
    # Gọi cached function - Streamlit sẽ tự động:
    # 1. Check cache dựa trên cache_key
    # 2. Nếu cache_key khác (phiên mới) → invalidate và fetch mới
    # 3. Nếu cache_key giống → return cached data (SHARED cho tất cả users)
    return _cached_fetch(cache_key, _fetch_func, *args, **kwargs)


def set_cached_data(cache_key: str, data: any):
    """
    Legacy function - không cần dùng nữa
    Cache được handle tự động bởi get_cached_data()
    """
    pass


def get_cache_timestamp(cache_key: str) -> Optional[datetime]:
    """
    Legacy function - không cần dùng nữa
    """
    return None


def render_session_info():
    """
    Hiển thị thông tin phiên hiện tại và cache status
    """
    session_name, session_start = get_current_session()
    now_utc = datetime.now(timezone.utc)
    
    # Tính thời gian còn lại trong phiên
    session_tz = None
    for sess in TRADING_SESSIONS:
        if sess["name"] == session_name:
            session_tz = pytz.timezone(sess["timezone"])
            break
    
    if session_tz:
        local_now = now_utc.astimezone(session_tz)
        local_start = session_start.astimezone(session_tz)
        
        st.info(f"""
📊 **Phiên hiện tại:** {session_name}  
🕐 **Bắt đầu phiên:** {local_start.strftime('%H:%M %Z')}  
💾 **Cache strategy:** Data được giữ nguyên trong suốt phiên, chỉ refresh khi sang phiên mới  
♻️ **Tần suất update:** Tối đa 4 lần/ngày (1 lần/phiên)
        """)
    else:
        st.info(f"📊 **Trạng thái:** {session_name} - Ngoài giờ giao dịch")


# Helper functions cho việc sử dụng
def get_market_data_cache_key() -> str:
    """Shortcut cho market data cache key"""
    return get_session_cache_key("market_data")


def get_news_cache_key() -> str:
    """Shortcut cho news cache key"""
    return get_session_cache_key("news")


def get_ai_analysis_cache_key() -> str:
    """Shortcut cho AI analysis cache key"""
    return get_session_cache_key("ai_analysis")
