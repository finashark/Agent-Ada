"""
Trang 1: Nhận định thị trường chung
Hiển thị: Điểm nhấn, bảng chỉ số, lịch kinh tế, dòng tiền & tâm lý, quan điểm đầu ngày
"""
import streamlit as st
from datetime import datetime, timezone
import pandas as pd
import sys
sys.path.insert(0, '..')

from components.session_badge import render_session_bar, get_active_session_ttl
from components.timestamp import render_timestamp
from components.copy import copy_section, copy_page_content
from components.exporters import show_export_options
from data_providers.overview import build_overview, get_cross_asset_table

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
    
    # Analysis
    st.markdown("### Phân tích")
    
    # VIX analysis
    if vix > 20:
        st.markdown("- **VIX > 20:** 🔴 Lo ngại gia tăng trên thị trường, tâm lý risk-off")
    elif vix < 15:
        st.markdown("- **VIX < 15:** 🟢 Thị trường ổn định, tâm lý risk-on")
    else:
        st.markdown("- **VIX 15-20:** 🟡 Mức biến động trung bình")
    
    # DXY analysis
    if dxy > 105:
        st.markdown("- **DXY > 105:** USD mạnh, áp lực lên vàng và tài sản rủi ro")
    elif dxy < 95:
        st.markdown("- **DXY < 95:** USD yếu, hỗ trợ vàng và commodities")
    else:
        st.markdown("- **DXY 95-105:** USD ổn định trong range")
    
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

st.markdown("""
### Bias chung: **Neutral với xu hướng Risk-On nhẹ**

**Trigger:**
- Đóng nến H4 S&P 500 vượt 4,600 với volume cao
- VIX giảm dưới 15
- DXY không vượt 105

**Invalidation:**
- CPI data vượt kỳ vọng >3.5%
- VIX tăng trên 22
- Địa chính trị bùng phát

**Timeframe:** H4 - D1

**Rủi ro sự kiện:**
- CPI data 20:30 (UTC+7)
- FOMC Minutes
- Earnings season Q4
""")

market_view_text = """
Bias chung: Neutral với xu hướng Risk-On nhẹ

Trigger:
- Đóng nến H4 S&P 500 vượt 4,600 với volume cao
- VIX giảm dưới 15
- DXY không vượt 105

Invalidation:
- CPI data vượt kỳ vọng >3.5%
- VIX tăng trên 22
- Địa chính trị bùng phát

Timeframe: H4 - D1

Rủi ro sự kiện:
- CPI data 20:30 (UTC+7)
- FOMC Minutes
- Earnings season Q4
"""

copy_section(
    "Quan điểm đầu ngày",
    market_view_text,
    show_preview=False,
    key_suffix="view"
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
{market_view_text}

---
Nguồn: yfinance | Agent Ada © 2025
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
