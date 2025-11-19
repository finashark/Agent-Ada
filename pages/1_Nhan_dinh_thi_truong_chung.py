"""
Trang 1: Nhận định thị trường chung
Hiển thị: Điểm nhấn, bảng chỉ số, lịch kinh tế, dòng tiền & tâm lý, quan điểm đầu ngày
"""
import streamlit as st
from datetime import datetime, timezone
import pandas as pd
import sys
import logging

sys.path.insert(0, '..')

from components.session_badge import render_session_bar, get_active_session_ttl

logger = logging.getLogger(__name__)
from components.timestamp import render_timestamp
from components.copy import copy_section, copy_page_content
from components.exporters import show_export_options
from data_providers.overview import build_overview, get_cross_asset_table
from data_providers.news_provider import NewsProvider
from data_providers.ai_analyst import get_ada_analyst

# Cấu hình trang
st.set_page_config(
    page_title="Nhận định thị trường chung",
    page_icon="📋",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .highlight-card {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 6px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📋 Nhận định thị trường chung")

# Timezone từ session state
tz_name = st.session_state.get("timezone", "Asia/Ho_Chi_Minh")

# Render session bar
now_utc = datetime.now(timezone.utc)
active_session = render_session_bar(now_utc)

# Load data
with st.spinner("Đang tải dữ liệu thị trường..."):
    overview = build_overview(tz_name)
    cross_asset_df = get_cross_asset_table()

# Timestamp
render_timestamp(
    datetime.fromisoformat(overview.last_updated),
    tz_name,
    overview.session
)

st.markdown("---")

# ============== SECTION 1: ĐIỂM NHẤN QUA ĐÊM ==============
st.markdown("## 🌟 Điểm nhấn qua đêm")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Highlights")
    for i, highlight in enumerate(overview.highlights, 1):
        st.markdown(f"{i}. {highlight}")
    
    # Copy button
    highlights_text = "\n".join([f"{i}. {h}" for i, h in enumerate(overview.highlights, 1)])
    copy_section(
        "Điểm nhấn qua đêm",
        highlights_text,
        show_preview=False,
        key_suffix="highlights"
    )

with col2:
    st.markdown("### Objectivity Notes")
    for note in overview.objectivity_notes:
        st.caption(note)

st.markdown("---")

# ============== SECTION 2: BẢNG CHỈ SỐ & TÀI SẢN CHÍNH ==============
st.markdown("## 📊 Bảng chỉ số & tài sản chính")

if not cross_asset_df.empty:
    st.dataframe(
        cross_asset_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Copy & Export
    col1, col2 = st.columns(2)
    with col1:
        copy_section(
            "Bảng chỉ số",
            cross_asset_df.to_string(index=False),
            show_preview=False,
            key_suffix="cross_asset"
        )
    
    with col2:
        show_export_options(
            data_csv=cross_asset_df.to_dict('records'),
            prefix="cross_asset_table"
        )
else:
    st.warning("⚠️ Không có dữ liệu bảng chỉ số")

st.caption("📌 Nguồn: yfinance | Lookback: D1=1 day, WTD=5 days, MTD=22 days | Z-score window=20 days")

st.markdown("---")

# ============== SECTION 3: LỊCH KINH TẾ HÔM NAY ==============
st.markdown("## 📅 Lịch kinh tế hôm nay")

if overview.economic_calendar:
    calendar_data = []
    for item in overview.economic_calendar:
        calendar_data.append({
            "Giờ": item.time_local,
            "Khu vực": item.region,
            "Sự kiện": item.event,
            "Ước tính": item.consensus if item.consensus else "N/A",
            "Trước đó": item.prior if item.prior else "N/A",
            "Ảnh hưởng": item.impact if item.impact else "N/A",
            "Link": item.source_url if item.source_url else ""
        })
    
    calendar_df = pd.DataFrame(calendar_data)
    st.dataframe(calendar_df, use_container_width=True, hide_index=True)
    
    # Export
    show_export_options(
        data_csv=calendar_data,
        data_json=calendar_data,
        prefix="economic_calendar"
    )
    
    # Copy
    copy_section(
        "Lịch kinh tế",
        calendar_df.to_string(index=False),
        show_preview=False,
        key_suffix="calendar"
    )
else:
    st.info("📌 Không có sự kiện kinh tế quan trọng hôm nay")

st.caption(f"⏰ Múi giờ: {tz_name} (có thể thay đổi trong Settings)")

st.markdown("---")

# ============== SECTION 4: DÒNG TIỀN & TÂM LÝ ==============
st.markdown("## 💹 Dòng tiền & Tâm lý rủi ro")

if overview.risk_sentiment:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        vix = overview.risk_sentiment.get("vix", 0)
        st.metric(
            "VIX (Volatility)",
            f"{vix:.2f}",
            delta=None,
            help="VIX trên 20 = lo ngại tăng, dưới 15 = thị trường ổn định"
        )
    
    with col2:
        dxy = overview.risk_sentiment.get("dxy", 0)
        st.metric(
            "DXY (USD Index)",
            f"{dxy:.2f}",
            delta=None,
            help="Sức mạnh đồng USD so với rổ tiền tệ"
        )
    
    with col3:
        us10y = overview.risk_sentiment.get("us10y", 0)
        st.metric(
            "US 10Y Yield",
            f"{us10y:.2f}%",
            delta=None,
            help="Lợi suất trái phiếu Mỹ 10 năm"
        )
    
    # Analysis - AI-Powered
    st.markdown("### Nhận định của Ada")
    
    # Get AI analysis for risk sentiment
    with st.spinner("Ada đang phân tích VIX và DXY..."):
        ada_analyst = get_ada_analyst()
        news_provider = NewsProvider()
        news_items = news_provider.get_news(hours_back=24, max_items=5)
        
        # Create focused prompt for risk sentiment
        # Safely get top 3 news (handle empty list)
        news_summary = ""
        if news_items and len(news_items) > 0:
            top_news = news_items[:3]
            news_summary = chr(10).join([f"- {item.get('title', 'N/A')}" for item in top_news])
        else:
            news_summary = "- Đang cập nhật tin tức..."
        
        risk_analysis_prompt = f"""Bạn là Ada, chuyên gia phân tích rủi ro thị trường.

DỮ LIỆU HIỆN TẠI:
- VIX: {vix:.2f}
- DXY: {dxy:.2f}
- US 10Y Yield: {us10y:.2f}%

TIN TỨC LIÊN QUAN:
{news_summary}

Viết 2 đoạn phân tích ngắn gọn (mỗi đoạn 3-4 câu):

**Đoạn 1: Phân tích VIX {vix:.2f}**
- Ý nghĩa của mức VIX hiện tại (so với ngưỡng 15-20)
- Tâm lý nhà đầu tư: Risk-on hay Risk-off?
- Tác động đến chiến lược giao dịch

**Đoạn 2: Phân tích DXY {dxy:.2f}**
- Xu hướng USD (so với ngưỡng 95-105)
- Tác động đến vàng, dầu, hàng hóa
- Ảnh hưởng đến emerging markets

Viết bằng tiếng Việt chuyên nghiệp, súc tích, có data cụ thể."""

        if ada_analyst.model:
            try:
                response = ada_analyst.model.generate_content(risk_analysis_prompt)
                st.markdown(response.text)
                risk_ai_text = response.text
            except Exception as e:
                logger.error(f"Gemini error: {e}")
                # Fallback
                st.markdown(f"VIX {vix:.2f} cho thấy thị trường {'biến động cao, tâm lý risk-off' if vix > 20 else 'ổn định, tâm lý risk-on' if vix < 15 else 'cân bằng'}.")
                st.markdown(f"DXY {dxy:.2f} đang {'mạnh, tạo áp lực lên vàng/dầu' if dxy > 105 else 'yếu, hỗ trợ hàng hóa' if dxy < 95 else 'ổn định trong vùng cân bằng'}.")
                risk_ai_text = f"VIX: {vix:.2f}, DXY: {dxy:.2f}"
        else:
            # Fallback when Gemini not available
            st.info("⚠️ Gemini AI chưa được cấu hình. Hiển thị phân tích cơ bản.")
            st.markdown(f"VIX {vix:.2f} cho thấy thị trường {'biến động cao, tâm lý risk-off' if vix > 20 else 'ổn định, tâm lý risk-on' if vix < 15 else 'cân bằng'}.")
            st.markdown(f"DXY {dxy:.2f} đang {'mạnh, tạo áp lực lên vàng/dầu' if dxy > 105 else 'yếu, hỗ trợ hàng hóa' if dxy < 95 else 'ổn định trong vùng cân bằng'}.")
            risk_ai_text = f"VIX: {vix:.2f}, DXY: {dxy:.2f}"
    
    # Copy
    risk_text = f"VIX: {vix:.2f}\nDXY: {dxy:.2f}\nUS10Y: {us10y:.2f}%"
    copy_section(
        "Dòng tiền & Tâm lý",
        risk_text,
        show_preview=False,
        key_suffix="risk"
    )
else:
    st.warning("⚠️ Không có dữ liệu tâm lý rủi ro")

st.markdown("---")

# ============== SECTION 5: QUAN ĐIỂM ĐẦU NGÀY ==============
st.markdown("## 🎯 Quan điểm đầu ngày")

st.markdown("### Nhận định của Ada")

# Get AI-powered analysis
with st.spinner("Ada đang tổng hợp thông tin và phân tích thị trường..."):
    # Fetch news
    news_provider = NewsProvider()
    news_items = news_provider.get_news(hours_back=24, max_items=10)
    
    # Get AI analyst
    ada_analyst = get_ada_analyst()
    
    # Get VIX, SPX, DXY from snapshot
    vix_level = overview.market_snapshot.get("^VIX", {}).get("last", 20)
    spx_change = overview.market_snapshot.get("^GSPC", {}).get("d1", 0)
    dxy_level = overview.risk_sentiment.get("dxy", 100)
    
    # Generate AI analysis
    ai_analysis = ada_analyst.generate_market_overview_analysis(
        snapshot=overview.market_snapshot,
        news=news_items,
        vix_level=vix_level,
        spx_change=spx_change,
        dxy_level=dxy_level
    )
    
    # Display analysis
    st.markdown(ai_analysis)

# Copy button
copy_section(
    "Quan điểm đầu ngày (AI-Generated)",
    ai_analysis,
    show_preview=False,
    key_suffix="ai_view"
)

st.markdown("---")

# ============== COPY TOÀN TRANG ==============
full_page_content = f"""
NHẬN ĐỊNH THỊ TRƯỜNG CHUNG
Cập nhật: {datetime.fromisoformat(overview.last_updated).strftime('%Y-%m-%d %H:%M:%S')} ({tz_name})
Phiên: {overview.session}

=== ĐIỂM NHẤN QUA ĐÊM ===
{highlights_text}

=== BẢNG CHỈ SỐ & TÀI SẢN CHÍNH ===
{cross_asset_df.to_string(index=False) if not cross_asset_df.empty else 'Không có dữ liệu'}

=== LỊCH KINH TẾ ===
{calendar_df.to_string(index=False) if overview.economic_calendar else 'Không có sự kiện'}

=== DÒNG TIỀN & TÂM LÝ ===
{risk_text if overview.risk_sentiment else 'Không có dữ liệu'}

=== QUAN ĐIỂM ĐẦU NGÀY ===
{ai_analysis}

---
Nguồn: yfinance + Gemini AI | Developed by Ken © 2025
"""

copy_page_content(full_page_content, label="📄 Copy toàn trang")

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ️ Thông tin trang")
    st.info(f"""
    **Cập nhật:** {datetime.fromisoformat(overview.last_updated).strftime('%H:%M:%S')}
    
    **Phiên:** {overview.session}
    
    **Số lượng highlights:** {len(overview.highlights)}
    
    **Sự kiện kinh tế:** {len(overview.economic_calendar)}
    """)
    
    if st.button("🔄 Làm mới dữ liệu"):
        st.cache_data.clear()
        st.rerun()
