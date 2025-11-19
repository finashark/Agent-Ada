"""
Component hiển thị timestamp với timezone
"""
from datetime import datetime
import pytz
import streamlit as st


def render_timestamp(
    last_updated: datetime, 
    tz_name: str = "Asia/Ho_Chi_Minh", 
    session_name: str = None,
    show_icon: bool = True
):
    """
    Hiển thị timestamp với múi giờ và phiên
    
    Args:
        last_updated: DateTime UTC cần hiển thị
        tz_name: Tên timezone (pytz)
        session_name: Tên phiên giao dịch
        show_icon: Có hiển thị icon không
    """
    try:
        tz = pytz.timezone(tz_name)
        local_dt = last_updated.astimezone(tz)
        
        icon = "🕐 " if show_icon else ""
        timestamp_str = local_dt.strftime('%Y-%m-%d %H:%M:%S')
        
        if session_name:
            caption = f"{icon}Cập nhật: **{timestamp_str}** ({tz_name}) | Phiên: **{session_name}**"
        else:
            caption = f"{icon}Cập nhật: **{timestamp_str}** ({tz_name})"
        
        st.caption(caption)
    except Exception as e:
        st.caption(f"⚠️ Lỗi hiển thị timestamp: {e}")


def get_current_time(tz_name: str = "Asia/Ho_Chi_Minh") -> datetime:
    """
    Lấy thời gian hiện tại theo timezone
    
    Args:
        tz_name: Tên timezone
        
    Returns:
        datetime object với timezone
    """
    utc_now = datetime.now(pytz.UTC)
    tz = pytz.timezone(tz_name)
    return utc_now.astimezone(tz)


def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format datetime theo chuỗi format
    
    Args:
        dt: datetime object
        format_str: Chuỗi format
        
    Returns:
        Chuỗi datetime đã format
    """
    return dt.strftime(format_str)
