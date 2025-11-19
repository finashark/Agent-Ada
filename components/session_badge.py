"""
Component quản lý và hiển thị phiên giao dịch
"""
from datetime import datetime, time, timezone
import pytz
import streamlit as st


# Định nghĩa 5 phiên giao dịch chính
SESSIONS = [
    {
        "name": "Australia (Sydney)",
        "short_name": "Australia",
        "city": "Australia/Sydney",
        "open": time(8, 0),
        "close": time(16, 0),
        "color": "#FF6B6B"
    },
    {
        "name": "Japan (Tokyo)",
        "short_name": "Japan",
        "city": "Asia/Tokyo",
        "open": time(9, 0),
        "close": time(15, 0),
        "color": "#4ECDC4"
    },
    {
        "name": "Asia (Singapore/HK)",
        "short_name": "Asia",
        "city": "Asia/Singapore",
        "open": time(9, 0),
        "close": time(16, 30),
        "color": "#95E1D3"
    },
    {
        "name": "London",
        "short_name": "London",
        "city": "Europe/London",
        "open": time(8, 0),
        "close": time(16, 30),
        "color": "#F38181"
    },
    {
        "name": "New York (US)",
        "short_name": "New York",
        "city": "America/New_York",
        "open": time(9, 30),
        "close": time(16, 0),
        "color": "#AA96DA"
    },
]


def is_session_open(session: dict, now_utc: datetime) -> bool:
    """
    Kiểm tra phiên có đang mở không
    
    Args:
        session: Dict thông tin phiên
        now_utc: Thời gian hiện tại UTC
        
    Returns:
        True nếu phiên đang mở
    """
    try:
        tz = pytz.timezone(session["city"])
        local_now = now_utc.astimezone(tz)
        
        # Tạo datetime cho open và close trong ngày hiện tại
        open_dt = local_now.replace(
            hour=session["open"].hour,
            minute=session["open"].minute,
            second=0,
            microsecond=0
        )
        close_dt = local_now.replace(
            hour=session["close"].hour,
            minute=session["close"].minute,
            second=0,
            microsecond=0
        )
        
        # Kiểm tra nằm trong khoảng
        return open_dt <= local_now <= close_dt
    except Exception as e:
        st.error(f"Lỗi kiểm tra phiên {session['name']}: {e}")
        return False


def session_status(now_utc: datetime = None):
    """
    Kiểm tra trạng thái tất cả phiên
    
    Args:
        now_utc: Thời gian hiện tại UTC (None = lấy thời gian hiện tại)
        
    Returns:
        Tuple (badges: List[dict], active_session: str)
    """
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    
    badges = []
    active_session = None
    
    for session in SESSIONS:
        is_open = is_session_open(session, now_utc)
        status = "🟢 Open" if is_open else "🔴 Closed"
        
        badges.append({
            "name": session["short_name"],
            "full_name": session["name"],
            "status": status,
            "is_open": is_open,
            "color": session["color"]
        })
        
        # Ưu tiên phiên đang mở, không thì chọn Asia làm mặc định
        if is_open and active_session is None:
            active_session = session["short_name"]
    
    # Nếu không có phiên nào mở, chọn Asia làm mặc định
    if active_session is None:
        active_session = "Asia"
    
    return badges, active_session


def session_ttl(is_open: bool) -> int:
    """
    Xác định TTL cache theo trạng thái phiên
    
    Args:
        is_open: Phiên có đang mở không
        
    Returns:
        TTL tính bằng giây
    """
    return 300 if is_open else 1800  # 5 phút nếu mở, 30 phút nếu đóng


def render_session_bar(now_utc: datetime = None):
    """
    Render thanh trạng thái phiên
    
    Args:
        now_utc: Thời gian hiện tại UTC
        
    Returns:
        Tên phiên đang active
    """
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    
    badges, active_session = session_status(now_utc)
    
    # Hiển thị thanh phiên
    st.markdown("### 🌍 Trạng thái các phiên giao dịch")
    
    cols = st.columns(len(badges))
    
    for idx, badge in enumerate(badges):
        with cols[idx]:
            status_emoji = "🟢" if badge["is_open"] else "🔴"
            status_text = "OPEN" if badge["is_open"] else "CLOSED"
            
            # Tạo card cho mỗi phiên
            card_style = f"""
                background-color: {'#d4edda' if badge['is_open'] else '#f8d7da'};
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                border: 2px solid {'#28a745' if badge['is_open'] else '#dc3545'};
            """
            
            st.markdown(
                f"""
                <div style="{card_style}">
                    <div style="font-size: 24px;">{status_emoji}</div>
                    <div style="font-weight: bold; margin: 5px 0;">{badge['name']}</div>
                    <div style="font-size: 12px; color: #666;">{status_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    st.info(f"📊 **Phiên đang theo dõi:** {active_session}")
    
    return active_session


def get_active_session_ttl(now_utc: datetime = None) -> tuple:
    """
    Lấy phiên active và TTL tương ứng
    
    Args:
        now_utc: Thời gian UTC
        
    Returns:
        Tuple (active_session: str, ttl: int)
    """
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)
    
    badges, active_session = session_status(now_utc)
    
    # Tìm badge của active session
    active_badge = next((b for b in badges if b["name"] == active_session), None)
    
    if active_badge:
        ttl = session_ttl(active_badge["is_open"])
    else:
        ttl = 1800  # Default 30 phút
    
    return active_session, ttl
