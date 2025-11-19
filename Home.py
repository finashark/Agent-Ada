"""
Home.py - Trang chủ của ứng dụng báo cáo thị trường
"""
import streamlit as st
from datetime import datetime, timezone, timedelta
import pytz
import pandas as pd
from data_providers.overview import get_market_snapshot, build_overview
from data_providers.market_details import build_top10_equities
from data_providers.news_provider import get_market_news

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
    .summary-box {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin: 15px 0;
    }
    .news-box {
        background-color: #f3e5f5;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #9c27b0;
        margin: 10px 0;
    }
    .metric-positive {
        color: #4caf50;
        font-weight: bold;
    }
    .metric-negative {
        color: #f44336;
        font-weight: bold;
    }
    .metric-neutral {
        color: #ff9800;
        font-weight: bold;
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

# ============== BÁO CÁO TỔNG HỢP ==============
st.markdown("## 📊 Báo cáo tổng hợp nhanh")

with st.spinner("Đang tổng hợp dữ liệu từ các trang..."):
    try:
        # Lấy dữ liệu thị trường
        snapshot = get_market_snapshot()
        overview = build_overview()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌟 Điểm nổi bật")
            
            # VIX & Risk Sentiment
            if "^VIX" in snapshot:
                vix = snapshot["^VIX"]["last"]
                vix_color = "metric-negative" if vix > 20 else "metric-positive" if vix < 15 else "metric-neutral"
                risk_mode = "Risk-Off (Lo ngại cao)" if vix > 20 else "Risk-On (Thị trường ổn định)" if vix < 15 else "Neutral"
                st.markdown(f"""
                <div class="summary-box">
                    <strong>🎯 Tâm lý thị trường:</strong> <span class="{vix_color}">{risk_mode}</span><br>
                    VIX hiện tại: <strong>{vix:.2f}</strong> ({snapshot["^VIX"]["d1"]:+.2f}%)
                </div>
                """, unsafe_allow_html=True)
            
            # S&P 500
            if "^GSPC" in snapshot:
                spx = snapshot["^GSPC"]
                spx_color = "metric-positive" if spx["d1"] > 0 else "metric-negative"
                st.markdown(f"""
                <div class="summary-box">
                    <strong>📈 S&P 500:</strong> <span class="{spx_color}">{spx['last']:.2f} ({spx['d1']:+.2f}%)</span><br>
                    WTD: {spx['wtd']:+.2f}% | MTD: {spx['mtd']:+.2f}%
                </div>
                """, unsafe_allow_html=True)
            
            # DXY
            if "DXY" in snapshot:
                dxy = snapshot["DXY"]
                dxy_trend = "Mạnh (>105)" if dxy["last"] > 105 else "Yếu (<95)" if dxy["last"] < 95 else "Neutral"
                st.markdown(f"""
                <div class="summary-box">
                    <strong>💵 USD Index (DXY):</strong> {dxy['last']:.2f} - {dxy_trend}<br>
                    Hôm nay: {dxy['d1']:+.2f}%
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🏆 Top Performers")
            
            try:
                # Lấy Top 3 từ NASDAQ
                top10 = build_top10_equities(universe="NASDAQ Large-Cap")
                if top10.items and len(top10.items) >= 3:
                    st.markdown("**Top 3 cổ phiếu tăng mạnh nhất (NASDAQ):**")
                    for i, item in enumerate(top10.items[:3], 1):
                        color = "metric-positive" if item.pct_change > 0 else "metric-negative"
                        st.markdown(f"""
                        <div class="summary-box">
                            <strong>{i}. {item.ticker}</strong>: <span class="{color}">${item.last:.2f} ({item.pct_change:+.2f}%)</span><br>
                            <small>{item.idea}</small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("📊 Đang cập nhật Top performers...")
            except Exception as e:
                st.info("📊 Đang cập nhật Top performers...")
            
            # Commodities nổi bật
            if "GC=F" in snapshot and "CL=F" in snapshot:
                gold = snapshot["GC=F"]
                oil = snapshot["CL=F"]
                st.markdown("**Hàng hóa:**")
                st.markdown(f"""
                <div class="summary-box">
                    <strong>🥇 Vàng:</strong> ${gold['last']:.2f} ({gold['d1']:+.2f}%)<br>
                    <strong>🛢️ Dầu WTI:</strong> ${oil['last']:.2f} ({oil['d1']:+.2f}%)
                </div>
                """, unsafe_allow_html=True)
        
        # Quan điểm tổng hợp
        st.markdown("### 💡 Quan điểm tổng hợp của Ada")
        
        # Xây dựng nhận định tự động dựa trên dữ liệu
        market_bias = "Neutral"
        if "^VIX" in snapshot and "^GSPC" in snapshot:
            vix = snapshot["^VIX"]["last"]
            spx_d1 = snapshot["^GSPC"]["d1"]
            
            if vix < 15 and spx_d1 > 0.5:
                market_bias = "Bullish (Risk-On)"
                bias_color = "metric-positive"
            elif vix > 20 or spx_d1 < -1.0:
                market_bias = "Bearish (Risk-Off)"
                bias_color = "metric-negative"
            else:
                market_bias = "Neutral (Quan sát)"
                bias_color = "metric-neutral"
        else:
            bias_color = "metric-neutral"
        
        st.markdown(f"""
        <div class="summary-box">
            <strong>🎯 Bias thị trường:</strong> <span class="{bias_color}">{market_bias}</span><br><br>
            
            <strong>Điểm cần chú ý:</strong><br>
            • Theo dõi VIX và DXY để đánh giá tâm lý rủi ro<br>
            • Kiểm tra lịch kinh tế (CPI, FOMC) có thể gây biến động<br>
            • Top stocks NASDAQ đang dẫn dắt thị trường<br>
            • Vàng và Dầu phản ánh dòng tiền an toàn vs rủi ro<br><br>
            
            <strong>⏰ Phiên giao dịch hiện tại:</strong> {overview.session}<br>
            <strong>🕐 Cập nhật lần cuối:</strong> {datetime.fromisoformat(overview.last_updated).strftime('%Y-%m-%d %H:%M:%S UTC')}
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"⚠️ Đang tải dữ liệu tổng hợp... (Có thể mất vài giây)")

st.markdown("---")

# ============== TIN TỨC QUAN TRỌNG ==============
st.markdown("## 📰 Tin tức & Sự kiện quan trọng")

# Debug: Show secrets status
with st.expander("🔍 Debug: API Status", expanded=False):
    try:
        has_secrets = hasattr(st, 'secrets') and "news" in st.secrets
        st.write(f"Secrets available: {has_secrets}")
        if has_secrets:
            st.write(f"NewsAPI key: {'✓ Present' if st.secrets['news'].get('newsapi_key') else '✗ Missing'}")
            st.write(f"Alpha Vantage key: {'✓ Present' if st.secrets['news'].get('alphavantage_key') else '✗ Missing'}")
            st.write(f"Finnhub key: {'✓ Present' if st.secrets['news'].get('finnhub_key') else '✗ Missing'}")
    except Exception as e:
        st.error(f"Error checking secrets: {e}")

with st.spinner("Đang tải tin tức từ NewsAPI, Alpha Vantage, Finnhub..."):
    try:
        # Lấy tin tức thực từ API
        news_items = get_market_news(hours_back=48, max_items=10)
        
        st.write(f"DEBUG: Received {len(news_items) if news_items else 0} items")  # Debug line
        
        if news_items and len(news_items) > 0:
            st.success(f"✅ Đã tải {len(news_items)} tin tức mới nhất từ các nguồn uy tín")
            st.success(f"✅ Đã tải {len(news_items)} tin tức mới nhất từ các nguồn uy tín")
            
            # Hiển thị tin tức
            for news in news_items:
                impact_color = "#ff5252" if news["impact"] == "High" else "#ff9800" if news["impact"] == "Medium" else "#4caf50"
                sentiment_emoji = "🟢" if news["sentiment"] == "Positive" else "🔴" if news["sentiment"] == "Negative" else "🟡"
                
                # Parse time
                try:
                    if "T" in news["time"]:
                        news_time = datetime.fromisoformat(news["time"].replace("Z", "+00:00"))
                    else:
                        news_time = datetime.strptime(news["time"], "%Y%m%dT%H%M%S")
                    time_str = news_time.strftime("%Y-%m-%d %H:%M")
                except:
                    time_str = news["time"]
                
                # Tạo link nếu có URL
                title_display = f"[{news['title']}]({news['url']})" if news.get("url") else news['title']
                
                st.markdown(f"""
                <div class="news-box">
                    <strong>{sentiment_emoji} {news['asset']}</strong> | 
                    <span style="color: {impact_color}; font-weight: bold;">{news['impact']} Impact</span> | 
                    <small>{time_str}</small><br>
                    <strong>{news['title']}</strong><br>
                    <small>📰 Nguồn: {news['source']}</small>
                </div>
                """, unsafe_allow_html=True)
            
            st.caption("🔄 Tin tức được cập nhật mỗi 30 phút | Cache TTL: 1800s")
            
        else:
            st.warning("⚠️ Không thể tải tin tức từ các API. Hiển thị dữ liệu mẫu...")
            
            # Fallback to mock data
            now = datetime.now(timezone.utc)
            mock_news = [
                {
                    "time": (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                    "asset": "S&P 500",
                    "title": "Fed giữ nguyên lãi suất 5.25-5.50%, tín hiệu dovish",
                    "impact": "High",
                    "sentiment": "Positive",
                    "source": "Reuters"
                },
                {
                    "time": (now - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
                    "asset": "NVDA",
                    "title": "NVIDIA báo cáo thu nhập Q4 vượt kỳ vọng, doanh thu AI tăng 78%",
                    "impact": "High",
                    "sentiment": "Positive",
                    "source": "Bloomberg"
                },
                {
                    "time": (now - timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"),
                    "asset": "BTC",
                    "title": "Bitcoin ETF có dòng vào ròng $500M trong tuần qua",
                    "impact": "Medium",
                    "sentiment": "Positive",
                    "source": "CoinDesk"
                }
            ]
            
            for news in mock_news:
                impact_color = "#ff5252" if news["impact"] == "High" else "#ff9800"
                sentiment_emoji = "🟢" if news["sentiment"] == "Positive" else "🔴"
                
                st.markdown(f"""
                <div class="news-box">
                    <strong>{sentiment_emoji} {news['asset']}</strong> | 
                    <span style="color: {impact_color}; font-weight: bold;">{news['impact']} Impact</span> | 
                    <small>{news['time']}</small><br>
                    <strong>{news['title']}</strong><br>
                    <small>📰 Nguồn: {news['source']} (Mock data)</small>
                </div>
                """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Lỗi khi tải tin tức: {e}")
        st.info("""
        💡 **Khắc phục:**
        - Kiểm tra API keys trong `.streamlit/secrets.toml`
        - Kiểm tra kết nối internet
        - Xem logs để biết provider nào bị lỗi
        """)

st.markdown("---")

# Status
st.markdown("## ℹ️ Thông tin hệ thống")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Phiên bản", "v1.1.0")

with col2:
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now_time = datetime.now(tz)
    st.metric("Thời gian hiện tại (VN)", now_time.strftime("%H:%M:%S"))

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
    
    # Clear cache button
    if st.button("🔄 Xóa cache & tải lại tin tức"):
        st.cache_data.clear()
        st.success("✅ Đã xóa cache!")
        st.rerun()
    
    st.markdown("---")
    
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
