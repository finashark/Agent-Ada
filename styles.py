"""
Styles và utility functions cho formatting
"""

def fmt_percent(x: float, decimals: int = 2) -> str:
    """
    Format số thành phần trăm
    
    Args:
        x: Số cần format
        decimals: Số chữ số thập phân
        
    Returns:
        Chuỗi đã format
    """
    return f"{x:.{decimals}f}%"


def fmt_price(x: float, decimals: int = 2) -> str:
    """
    Format giá với dấu phẩy phân cách
    
    Args:
        x: Giá cần format
        decimals: Số chữ số thập phân
        
    Returns:
        Chuỗi đã format
    """
    return f"{x:,.{decimals}f}"


def fmt_currency(x: float, symbol: str = "$", decimals: int = 2) -> str:
    """
    Format tiền tệ
    
    Args:
        x: Số tiền
        symbol: Ký hiệu tiền tệ
        decimals: Số chữ số thập phân
        
    Returns:
        Chuỗi đã format
    """
    return f"{symbol}{x:,.{decimals}f}"


def fmt_volume(x: float) -> str:
    """
    Format volume (K, M, B, T)
    
    Args:
        x: Volume
        
    Returns:
        Chuỗi đã format
    """
    if x >= 1e12:
        return f"{x/1e12:.2f}T"
    elif x >= 1e9:
        return f"{x/1e9:.2f}B"
    elif x >= 1e6:
        return f"{x/1e6:.2f}M"
    elif x >= 1e3:
        return f"{x/1e3:.2f}K"
    else:
        return f"{x:.2f}"


def color_positive_negative(value: float) -> str:
    """
    Trả về màu dựa trên giá trị dương/âm
    
    Args:
        value: Giá trị
        
    Returns:
        Tên màu
    """
    if value > 0:
        return "green"
    elif value < 0:
        return "red"
    else:
        return "gray"


def trend_emoji(value: float, threshold: float = 0) -> str:
    """
    Trả về emoji xu hướng
    
    Args:
        value: Giá trị
        threshold: Ngưỡng
        
    Returns:
        Emoji
    """
    if value > threshold:
        return "🟢 ↑"
    elif value < -threshold:
        return "🔴 ↓"
    else:
        return "🟡 →"
