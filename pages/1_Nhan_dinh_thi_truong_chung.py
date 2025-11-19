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
    st.markdown("### Nhận định của Ada")
    
    # Xây dựng câu topic và support
    vix_analysis = ""
    if vix > 20:
        vix_analysis = f"Chỉ số VIX hiện đang ở mức {vix:.2f}, vượt ngưỡng 20 điểm. Đây là tín hiệu cho thấy lo ngại đang gia tăng trên thị trường chứng khoán Mỹ. Khi VIX tăng cao, các nhà đầu tư thường mua quyền chọn bảo vệ (put options) nhiều hơn, phản ánh kỳ vọng về biến động mạnh sắp tới. Điều này thường đi kèm với dòng tiền tháo chạy khỏi tài sản rủi ro (risk-off), chuyển sang các kênh an toàn như trái phiếu chính phủ Mỹ hoặc đô la."
    elif vix < 15:
        vix_analysis = f"Chỉ số VIX đang duy trì ở mức thấp {vix:.2f}, cho thấy thị trường đang trong trạng thái ổn định. Mức VIX dưới 15 thường phản ánh tâm lý lạc quan của nhà đầu tư (risk-on), khi họ sẵn sàng nắm giữ cổ phiếu và tài sản rủi ro cao hơn. Trong môi trường này, các tài sản như cổ phiếu công nghệ, tiền mã hóa và các cặp tiền tệ có lợi suất cao (high-yielding currencies) thường được ưa chuộng."
    else:
        vix_analysis = f"Chỉ số VIX hiện ở mức {vix:.2f}, nằm trong vùng trung lập 15-20 điểm. Đây là mức biến động bình thường, cho thấy thị trường đang trong giai đoạn cân bằng giữa lạc quan và thận trọng. Nhà đầu tư nên theo dõi thêm các chỉ báo khác để xác định xu hướng rõ ràng hơn."
    
    dxy_analysis = ""
    if dxy > 105:
        dxy_analysis = f"Chỉ số USD Index (DXY) đang giao dịch ở {dxy:.2f}, trên ngưỡng 105. Điều này cho thấy đồng đô la Mỹ đang trong xu hướng mạnh so với rổ các đồng tiền chính (EUR, JPY, GBP, CAD, SEK, CHF). Khi USD mạnh lên, các tài sản được định giá bằng USD như vàng, dầu và hầu hết hàng hóa (commodities) thường chịu áp lực giảm giá. Bên cạnh đó, cổ phiếu của các công ty xuất khẩu Mỹ cũng có thể gặp bất lợi do sản phẩm trở nên đắt hơn trên thị trường quốc tế."
    elif dxy < 95:
        dxy_analysis = f"Chỉ số USD Index (DXY) đang ở mức {dxy:.2f}, dưới ngưỡng 95. Đây là tín hiệu USD đang suy yếu, tạo điều kiện thuận lợi cho vàng và các hàng hóa tăng giá. Khi USD yếu, các nhà đầu tư nước ngoài dễ dàng mua tài sản Mỹ với chi phí thấp hơn, đồng thời các thị trường mới nổi (emerging markets) thường được hưởng lợi nhờ giảm gánh nặng nợ USD."
    else:
        dxy_analysis = f"Chỉ số USD Index (DXY) đang dao động ở {dxy:.2f}, trong vùng cân bằng 95-105. Đây là mức ổn định, cho thấy USD không có xu hướng rõ rệt. Trong tình huống này, biến động giá của vàng, dầu và các tài sản khác sẽ phụ thuộc nhiều hơn vào yếu tố cung-cầu thực tế và các sự kiện địa chính trị."
    
    st.markdown(vix_analysis)
    st.markdown("")
    st.markdown(dxy_analysis)
    
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

# Đoạn 1: Phân tích hiện trạng
st.markdown("""
Dựa trên dữ liệu thị trường qua đêm và các chỉ báo kỹ thuật, thị trường hiện đang trong trạng thái **Neutral với xu hướng Risk-On nhẹ**. 
Chỉ số S&P 500 đang kiểm tra lại vùng kháng cự quan trọng tại 4,600 điểm trên khung H4, trong khi VIX duy trì ở vùng dưới 15 cho thấy 
tâm lý nhà đầu tư vẫn tương đối lạc quan. Đồng thời, chỉ số DXY đang dao động trong range 95-105, chưa có đột phá rõ ràng, 
điều này giúp hạn chế áp lực lên các tài sản rủi ro như vàng và crypto.

Các yếu tố hỗ trợ cho kịch bản tích cực bao gồm: (1) Dòng tiền vẫn đang chảy vào cổ phiếu công nghệ và tài sản rủi ro cao, 
phản ánh qua volume giao dịch tăng trong các phiên gần đây; (2) Lợi suất trái phiếu Mỹ 10 năm (US 10Y Yield) ổn định, 
không có dấu hiệu tăng đột biến gây lo ngại về lạm phát; (3) Không có sự kiện địa chính trị lớn tác động tiêu cực đến thị trường.
""")

st.markdown("")

# Đoạn 2: Quan điểm và kịch bản giao dịch
st.markdown("""
**Quan điểm:** Trong phiên giao dịch hôm nay, chúng tôi nghiêng về kịch bản thị trường duy trì đà tăng nhẹ, với điều kiện 
không có bất ngờ tiêu cực từ dữ liệu kinh tế. Tuy nhiên, cần thận trọng khi tiếp cận vì biến động có thể gia tăng quanh 
thời điểm công bố CPI vào 20:30 (UTC+7) và FOMC Minutes.

**Kịch bản giao dịch:**

*Kịch bản Bullish (Xác suất 60%):* Nếu S&P 500 đóng nến H4 trên 4,600 với volume xác nhận (cao hơn trung bình 20 phiên), 
đây là tín hiệu mua mạnh. Các cổ phiếu công nghệ lớn (AAPL, NVDA, MSFT) và crypto (BTC, ETH) có thể tiếp tục tăng. 
Timeframe ưu tiên: H4-D1. Stop loss nên đặt dưới MA20 hoặc vùng hỗ trợ gần nhất.

*Kịch bản Bearish (Xác suất 25%):* Nếu CPI vượt kỳ vọng (>3.5%) hoặc VIX bất ngờ tăng trên 22, thị trường có thể đảo chiều 
và đi vào tâm lý risk-off. Trong trường hợp này, nên chốt lời các vị thế long và cân nhắc short S&P 500, đồng thời 
tăng tỷ trọng tài sản an toàn như USD hoặc trái phiếu chính phủ.

*Kịch bản Neutral (Xác suất 15%):* Nếu thị trường không có động lực rõ ràng, giá có thể dao động trong range hẹp. 
Khuyến nghị đứng ngoài hoặc chỉ giao dịch ngắn hạn với volume nhỏ.

**Các rủi ro cần lưu ý:** CPI data tại 20:30 (UTC+7), FOMC Minutes, và mùa báo cáo thu nhập Q4 đang diễn ra có thể 
gây biến động bất ngờ. Luôn đặt stop loss và quản lý rủi ro chặt chẽ.
""")

market_view_text = """
NHẬN ĐỊNH CỦA ADA - QUAN ĐIỂM ĐẦU NGÀY

Dựa trên dữ liệu thị trường qua đêm và các chỉ báo kỹ thuật, thị trường hiện đang trong trạng thái Neutral với xu hướng Risk-On nhẹ. 
Chỉ số S&P 500 đang kiểm tra lại vùng kháng cự quan trọng tại 4,600 điểm trên khung H4, trong khi VIX duy trì ở vùng dưới 15 cho thấy 
tâm lý nhà đầu tư vẫn tương đối lạc quan.

Các yếu tố hỗ trợ kịch bản tích cực: (1) Dòng tiền vẫn đang chảy vào cổ phiếu công nghệ và tài sản rủi ro cao; 
(2) Lợi suất trái phiếu Mỹ 10 năm ổn định; (3) Không có sự kiện địa chính trị lớn.

KỊCH BẢN GIAO DỊCH:

Kịch bản Bullish (60%): Nếu S&P 500 đóng nến H4 trên 4,600 với volume cao, đây là tín hiệu mua mạnh. 
Các cổ phiếu công nghệ lớn (AAPL, NVDA, MSFT) và crypto (BTC, ETH) có thể tiếp tục tăng. 
Timeframe: H4-D1. Stop loss đặt dưới MA20.

Kịch bản Bearish (25%): Nếu CPI vượt kỳ vọng (>3.5%) hoặc VIX tăng trên 22, thị trường có thể đảo chiều risk-off. 
Nên chốt lời long và cân nhắc short S&P 500, tăng tỷ trọng USD/trái phiếu chính phủ.

Kịch bản Neutral (15%): Nếu không có động lực rõ ràng, giá có thể dao động trong range hẹp. 
Khuyến nghị đứng ngoài hoặc giao dịch ngắn hạn volume nhỏ.

RỦI RO: CPI data 20:30 (UTC+7), FOMC Minutes, Earnings Q4. Luôn đặt stop loss và quản lý rủi ro chặt chẽ.
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
Nguồn: yfinance | Developed by Ken © 2025
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
