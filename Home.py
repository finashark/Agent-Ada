"""
Home.py - Trang chủ của ứng dụng báo cáo thị trường
"""
import streamlit as st
from datetime import datetime
import pytz

# Cấu hình trang
st.set_page_config(
    page_title="Agent Ada - Báo Cáo Thị Trường",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .feature-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📊 Agent Ada - Báo Cáo Thị Trường Hằng Ngày</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Hệ thống báo cáo thị trường chuyên nghiệp cho môi giới CFDs</div>', unsafe_allow_html=True)

st.markdown("---")

# Thông tin Agent Ada
st.markdown("### 👋 Xin chào! Tôi là Agent Ada")
st.markdown("""
Tôi là chuyên gia tài chính chứng khoán với nhiều năm kinh nghiệm, chuyên biên tập nội dung 
tài chính hỗ trợ cho các nhân viên môi giới tại sàn HFM.

**Nhiệm vụ của tôi:**
- 📈 Phân tích và tổng hợp thông tin thị trường hằng ngày
- 📊 Cung cấp dữ liệu khoa học, khách quan với nguồn rõ ràng
- 💼 Hỗ trợ môi giới cập nhật thông tin cho khách hàng
- 🎯 Đưa ra khung phân tích có hệ thống và dễ sử dụng
""")

st.markdown("---")

# Giới thiệu tính năng
st.markdown("## 🎯 Các tính năng chính")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📋 Trang 1: Nhận định chung</div>
        <ul>
            <li>Điểm nhấn qua đêm</li>
            <li>Bảng chỉ số cross-asset</li>
            <li>Lịch kinh tế</li>
            <li>Dòng tiền & tâm lý</li>
            <li>Quan điểm đầu ngày</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📊 Trang 2: Chi tiết thị trường</div>
        <ul>
            <li>US Equities (Top 10)</li>
            <li>Vàng (XAUUSD)</li>
            <li>FX Majors</li>
            <li>Crypto</li>
            <li>Dầu (WTI/Brent)</li>
            <li>Chỉ số toàn cầu</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📈 Trang 3: Phụ lục dữ liệu</div>
        <ul>
            <li>Lịch kinh tế chi tiết</li>
            <li>Heatmap biến động</li>
            <li>Bảng kỹ thuật nhanh</li>
            <li>Xuất dữ liệu (CSV/JSON)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Nguyên tắc hoạt động
st.markdown("## 🔍 Nguyên tắc hoạt động")

st.markdown("""
<div class="info-box">
    <strong>✓ Khoa học & Khách quan:</strong><br>
    • Tách rõ <strong>Fact</strong> (sự kiện/số liệu) và <strong>Interpretation</strong> (diễn giải)<br>
    • Hiển thị nguồn dữ liệu ngay cạnh số liệu<br>
    • Sử dụng z-score, percentile khi phù hợp<br>
    • Tránh khẳng định tuyệt đối
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>⏰ Cập nhật theo phiên:</strong><br>
    • Tự động theo dõi 5 phiên: Australia, Japan, Asia, London, New York<br>
    • Cache thông minh: TTL 5 phút (phiên mở) / 30 phút (phiên đóng)<br>
    • Timestamp rõ ràng với múi giờ
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>📋 Tiện ích Copy & Export:</strong><br>
    • Nút Copy cho mọi mục lớn<br>
    • Export CSV, JSON, Markdown<br>
    • Dễ dàng gửi cho khách hàng
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Hướng dẫn sử dụng
st.markdown("## 📖 Hướng dẫn sử dụng")

with st.expander("🚀 Bắt đầu nhanh", expanded=True):
    st.markdown("""
    1. **Chọn trang** từ sidebar bên trái:
       - Trang 1: Nhận định thị trường chung
       - Trang 2: Chi tiết theo thị trường
       - Trang 3: Phụ lục dữ liệu
    
    2. **Xem thông tin** được cập nhật theo phiên giao dịch
    
    3. **Sử dụng nút Copy** để sao chép nội dung cần thiết
    
    4. **Export dữ liệu** sang CSV/JSON nếu cần phân tích thêm
    """)

with st.expander("📊 Hiểu về phiên giao dịch"):
    st.markdown("""
    Ứng dụng theo dõi 5 phiên giao dịch chính:
    
    - 🇦🇺 **Australia (Sydney):** 08:00 - 16:00 (giờ địa phương)
    - 🇯🇵 **Japan (Tokyo):** 09:00 - 15:00 (giờ địa phương)
    - 🌏 **Asia (Singapore/HK):** 09:00 - 16:30 (giờ địa phương)
    - 🇬🇧 **London:** 08:00 - 16:30 (giờ địa phương)
    - 🇺🇸 **New York:** 09:30 - 16:00 ET
    
    Dữ liệu được cập nhật thường xuyên hơn khi phiên đang mở.
    """)

with st.expander("🎓 Hiểu về chỉ số và thuật ngữ"):
    st.markdown("""
    **Các chỉ số chính:**
    - **VIX:** Volatility Index - đo lường độ biến động kỳ vọng của S&P 500
    - **DXY:** US Dollar Index - sức mạnh của USD so với rổ tiền tệ
    - **US10Y (^TNX):** Lợi suất trái phiếu Mỹ kỳ hạn 10 năm
    - **ATR(14):** Average True Range 14 ngày - đo biến động giá
    - **MA20/MA50:** Moving Average 20/50 ngày
    - **Z-score:** Số độ lệch chuẩn so với trung bình
    
    **Khung phân tích Trade Plan:**
    - **Bias:** Xu hướng (Bullish/Bearish/Neutral)
    - **Trigger:** Điều kiện vào lệnh
    - **Invalidation:** Điều kiện huỷ kịch bản
    - **Timeframe:** Khung thời gian theo dõi
    """)

st.markdown("---")

# Status
st.markdown("## ℹ️ Thông tin hệ thống")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Phiên bản", "v1.0.0")

with col2:
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(tz)
    st.metric("Thời gian hiện tại (VN)", now.strftime("%H:%M:%S"))

with col3:
    st.metric("Nguồn dữ liệu", "yfinance + mock")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px 0;">
    <p>© 2025 Developed by Ken | Được phát triển cho sàn HFM</p>
    <p style="font-size: 0.9rem;">
        <strong>Lưu ý:</strong> Thông tin được cung cấp chỉ mang tính chất tham khảo. 
        Không phải lời khuyên đầu tư. Vui lòng tự nghiên cứu và đánh giá rủi ro.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Cài đặt")
    
    # Timezone selector
    tz_options = ["Asia/Ho_Chi_Minh", "Asia/Singapore", "UTC", "America/New_York", "Europe/London"]
    selected_tz = st.selectbox("Múi giờ hiển thị", tz_options, index=0)
    st.session_state["timezone"] = selected_tz
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("Tự động làm mới", value=True)
    st.session_state["auto_refresh"] = auto_refresh
    
    if auto_refresh:
        refresh_interval = st.slider("Tần suất làm mới (giây)", 60, 600, 300)
        st.session_state["refresh_interval"] = refresh_interval
