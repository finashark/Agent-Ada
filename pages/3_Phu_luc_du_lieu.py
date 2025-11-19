"""
Trang 3: Phụ lục dữ liệu & bảng biểu (Quốc tế)
Không bao gồm nội dung riêng Việt Nam
"""
import streamlit as st
from datetime import datetime, timezone
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '..')

from components.timestamp import render_timestamp
from components.copy import copy_section, copy_page_content
from components.exporters import show_export_options
from data_providers.overview import get_cross_asset_table, CORE_ASSETS, fetch_prices
from data_providers.market_details import fetch_ohlc, build_snapshot
from data_providers.derivatives_wrappers import DerivsClient

# Cấu hình trang
st.set_page_config(
    page_title="Phụ lục dữ liệu",
    page_icon="📈",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .data-section {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    .heatmap-cell-positive {
        background-color: #d4edda;
        color: #155724;
    }
    .heatmap-cell-negative {
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📈 Phụ lục dữ liệu & bảng biểu (Quốc tế)")

tz_name = st.session_state.get("timezone", "Asia/Ho_Chi_Minh")
now_utc = datetime.now(timezone.utc)

render_timestamp(now_utc, tz_name, "Asia")

st.markdown("---")

# ============== MODULE 1: LỊCH KINH TẾ ==============
st.markdown("## 📅 Lịch kinh tế (Chuẩn hóa)")

# Timezone selector
selected_tz = st.selectbox(
    "Chọn múi giờ hiển thị:",
    ["UTC", "Asia/Ho_Chi_Minh", "Asia/Singapore", "America/New_York", "Europe/London"],
    index=1
)

# Mock calendar data (thực tế nên load từ API)
calendar_data = [
    {
        "Giờ (UTC)": "13:30",
        "Giờ (Local)": "20:30" if selected_tz == "Asia/Ho_Chi_Minh" else "13:30",
        "Khu vực": "US",
        "Sự kiện": "CPI (YoY)",
        "Forecast": "3.2%",
        "Previous": "3.4%",
        "Actual": None,
        "Impact": "High",
        "Link": "https://www.bls.gov/"
    },
    {
        "Giờ (UTC)": "07:00",
        "Giờ (Local)": "14:00" if selected_tz == "Asia/Ho_Chi_Minh" else "07:00",
        "Khu vực": "US",
        "Sự kiện": "FOMC Minutes",
        "Forecast": None,
        "Previous": None,
        "Actual": None,
        "Impact": "High",
        "Link": "https://www.federalreserve.gov/"
    },
    {
        "Giờ (UTC)": "08:30",
        "Giờ (Local)": "15:30" if selected_tz == "Asia/Ho_Chi_Minh" else "08:30",
        "Khu vực": "EU",
        "Sự kiện": "ECB Press Conference",
        "Forecast": None,
        "Previous": None,
        "Actual": None,
        "Impact": "Medium",
        "Link": "https://www.ecb.europa.eu/"
    },
]

calendar_df = pd.DataFrame(calendar_data)
st.dataframe(calendar_df, use_container_width=True, hide_index=True)

st.caption(f"⏰ Múi giờ hiển thị: {selected_tz}")

# Export & Copy
col1, col2 = st.columns(2)

with col1:
    show_export_options(
        data_csv=calendar_data,
        data_json=calendar_data,
        prefix="economic_calendar"
    )

with col2:
    calendar_text = calendar_df.to_string(index=False)
    copy_section("Lịch kinh tế", calendar_text, show_preview=False, key_suffix="cal")

st.markdown("---")

# ============== MODULE 2: HEATMAP BIẾN ĐỘNG ==============
st.markdown("## 🔥 Heatmap biến động cross-asset")

st.info("📊 Hiển thị % thay đổi theo các khung thời gian: D1, WTD, MTD")

with st.spinner("Đang tạo heatmap..."):
    # Load data
    prices = fetch_prices(CORE_ASSETS, period="3mo", interval="1d")
    
    if not prices.empty:
        heatmap_data = []
        
        for asset in CORE_ASSETS:
            if asset not in prices.columns:
                continue
            
            asset_prices = prices[asset].dropna()
            
            if len(asset_prices) < 2:
                continue
            
            # D1
            d1 = ((asset_prices.iloc[-1] / asset_prices.iloc[-2]) - 1) * 100
            
            # WTD (5 days)
            wtd = ((asset_prices.iloc[-1] / asset_prices.iloc[-6]) - 1) * 100 if len(asset_prices) >= 6 else np.nan
            
            # MTD (22 days)
            mtd = ((asset_prices.iloc[-1] / asset_prices.iloc[-23]) - 1) * 100 if len(asset_prices) >= 23 else np.nan
            
            heatmap_data.append({
                "Asset": asset,
                "D1 (%)": d1,
                "WTD (%)": wtd,
                "MTD (%)": mtd
            })
        
        heatmap_df = pd.DataFrame(heatmap_data)
        
        # Format và style
        def color_negative_red(val):
            try:
                val = float(val)
                color = '#d4edda' if val > 0 else '#f8d7da' if val < 0 else 'white'
                return f'background-color: {color}'
            except:
                return ''
        
        styled_df = heatmap_df.style.applymap(
            color_negative_red, 
            subset=['D1 (%)', 'WTD (%)', 'MTD (%)']
        ).format({
            'D1 (%)': '{:.2f}',
            'WTD (%)': '{:.2f}',
            'MTD (%)': '{:.2f}'
        })
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        st.caption("📌 Nguồn: yfinance | Lookback: D1=1 day, WTD=5 days, MTD=22 days")
        
        # Export & Copy
        col1, col2 = st.columns(2)
        
        with col1:
            show_export_options(
                data_csv=heatmap_data,
                data_json=heatmap_data,
                prefix="heatmap"
            )
        
        with col2:
            heatmap_text = heatmap_df.to_string(index=False)
            copy_section("Heatmap", heatmap_text, show_preview=False, key_suffix="heat")
    else:
        st.warning("⚠️ Không thể tải dữ liệu heatmap")

st.markdown("---")

# ============== MODULE 3: BẢNG KỸ THUẬT NHANH ==============
st.markdown("## 📊 Bảng kỹ thuật nhanh")

st.info("Hiển thị: Last, %D1, Range, ATR(14), MA20, MA50")

with st.spinner("Đang tính toán chỉ báo kỹ thuật..."):
    technical_data = []
    
    for asset in CORE_ASSETS:
        try:
            df = fetch_ohlc(asset, period="6mo", interval="1d")
            
            if df.empty or len(df) < 2:
                continue
            
            snapshot = build_snapshot(df)
            
            if not snapshot:
                continue
            
            technical_data.append({
                "Asset": asset,
                "Last": f"{snapshot.get('last', 0):.2f}",
                "%D1": f"{snapshot.get('pct_d1', 0):+.2f}%",
                "Range": snapshot.get('day_range', 'N/A'),
                "ATR(14)": f"{snapshot.get('atr14', 0):.2f}",
                "MA20": f"{snapshot.get('ma20', 0):.2f}",
                "MA50": f"{snapshot.get('ma50', 0):.2f}",
                "MA Status": "🟢" if snapshot.get('above_ma20') and snapshot.get('above_ma50') 
                           else "🔴" if not snapshot.get('above_ma20') and not snapshot.get('above_ma50')
                           else "🟡"
            })
            
        except Exception as e:
            st.warning(f"Lỗi khi xử lý {asset}: {e}")
            continue
    
    if technical_data:
        technical_df = pd.DataFrame(technical_data)
        st.dataframe(technical_df, use_container_width=True, hide_index=True)
        
        st.caption("📌 🟢 = Above MA20 & MA50 | 🔴 = Below MA20 & MA50 | 🟡 = Mixed")
        
        # Export & Copy
        col1, col2 = st.columns(2)
        
        with col1:
            show_export_options(
                data_csv=technical_data,
                data_json=technical_data,
                prefix="technical_table"
            )
        
        with col2:
            technical_text = technical_df.to_string(index=False)
            copy_section("Bảng kỹ thuật", technical_text, show_preview=False, key_suffix="tech")
    else:
        st.warning("⚠️ Không có dữ liệu kỹ thuật")

st.markdown("---")

# ============== MODULE 4: CRYPTO FUNDING/OI ==============
st.markdown("## ₿ Crypto Funding Rate & Open Interest")

st.info("📊 Dữ liệu Funding Rate và Open Interest từ các sàn chính (Binance, Bybit, OKX, Deribit)")

# Initialize derivatives client
try:
    derivs_client = DerivsClient()
    
    # Crypto symbols to track
    crypto_symbols = ["BTCUSDT", "ETHUSDT"]
    exchanges = ["binance", "bybit", "okx"]
    
    # Tab cho Funding Rate và OI
    funding_tab, oi_tab = st.tabs(["📈 Funding Rate", "📊 Open Interest"])
    
    with funding_tab:
        st.markdown("### Funding Rate hiện tại")
        st.caption("Funding rate dương → Long trả Short | Funding rate âm → Short trả Long")
        
        funding_data = []
        
        for symbol in crypto_symbols:
            for exchange in exchanges:
                try:
                    fp = derivs_client.funding_latest(exchange, symbol)
                    if fp:
                        funding_data.append({
                            "Exchange": fp.exchange,
                            "Symbol": fp.symbol,
                            "Funding Rate": f"{fp.rate * 100:.4f}%",
                            "Annual Rate": f"{fp.rate * 100 * 365 * 3:.2f}%",  # 3 times per day
                            "Timestamp": pd.to_datetime(fp.ts, unit='ms').strftime('%Y-%m-%d %H:%M:%S'),
                            "Status": "🟢 Longs trả" if fp.rate > 0 else "🔴 Shorts trả" if fp.rate < 0 else "⚪ Neutral"
                        })
                except Exception as e:
                    st.warning(f"⚠️ Không thể lấy funding rate từ {exchange} cho {symbol}: {str(e)[:100]}")
                    continue
        
        if funding_data:
            funding_df = pd.DataFrame(funding_data)
            st.dataframe(funding_df, use_container_width=True, hide_index=True)
            
            # Analysis
            st.markdown("#### Phân tích")
            avg_btc = funding_df[funding_df['Symbol'].str.contains('BTC')]['Funding Rate'].str.rstrip('%').astype(float).mean()
            if abs(avg_btc) > 0.05:
                sentiment = "🟢 Bullish mạnh" if avg_btc > 0 else "🔴 Bearish mạnh"
                st.warning(f"**BTC:** {sentiment} - Funding rate trung bình: {avg_btc:.4f}%")
            else:
                st.success(f"**BTC:** ⚪ Neutral - Funding rate trung bình: {avg_btc:.4f}%")
            
            # Export & Copy
            col1, col2 = st.columns(2)
            with col1:
                show_export_options(
                    data_csv=funding_data,
                    data_json=funding_data,
                    prefix="crypto_funding"
                )
            
            with col2:
                funding_text = funding_df.to_string(index=False)
                copy_section("Crypto Funding Rate", funding_text, show_preview=False, key_suffix="funding")
        else:
            st.warning("⚠️ Không có dữ liệu funding rate")
    
    with oi_tab:
        st.markdown("### Open Interest hiện tại")
        st.caption("Open Interest = Tổng số hợp đồng futures đang mở")
        
        oi_data = []
        
        for symbol in crypto_symbols:
            for exchange in exchanges:
                try:
                    oi = derivs_client.oi_snapshot(exchange, symbol)
                    if oi:
                        oi_data.append({
                            "Exchange": oi.exchange,
                            "Symbol": oi.symbol,
                            "Open Interest": f"{oi.open_interest:,.2f}",
                            "Timestamp": pd.to_datetime(oi.ts, unit='ms').strftime('%Y-%m-%d %H:%M:%S'),
                            "Value (USD)": f"${oi.meta.get('sumOpenInterestValue', 0):,.0f}" if 'sumOpenInterestValue' in oi.meta else "N/A"
                        })
                except Exception as e:
                    st.warning(f"⚠️ Không thể lấy OI từ {exchange} cho {symbol}: {str(e)[:100]}")
                    continue
        
        if oi_data:
            oi_df = pd.DataFrame(oi_data)
            st.dataframe(oi_df, use_container_width=True, hide_index=True)
            
            st.markdown("#### Giải thích")
            st.info("""
            - **OI tăng + giá tăng:** Bullish (tiền mới vào thị trường)
            - **OI tăng + giá giảm:** Bearish (short mới mở)
            - **OI giảm + giá tăng:** Short covering (đóng short)
            - **OI giảm + giá giảm:** Long liquidation (đóng long)
            """)
            
            # Export & Copy
            col1, col2 = st.columns(2)
            with col1:
                show_export_options(
                    data_csv=oi_data,
                    data_json=oi_data,
                    prefix="crypto_oi"
                )
            
            with col2:
                oi_text = oi_df.to_string(index=False)
                copy_section("Crypto Open Interest", oi_text, show_preview=False, key_suffix="oi")
        else:
            st.warning("⚠️ Không có dữ liệu Open Interest")

except Exception as e:
    st.error(f"❌ Lỗi khi tải dữ liệu derivatives: {e}")
    st.info("""
    💡 **Gợi ý:**
    - Kiểm tra kết nối internet
    - Một số sàn có thể bị giới hạn rate limit
    - Thử lại sau vài phút
    """)

st.markdown("---")

# ============== MODULE 5: NGUỒN & VERSIONING ==============
st.markdown("## ℹ️ Nguồn dữ liệu & Versioning")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Nguồn dữ liệu")
    st.markdown("""
    - **Giá & Chỉ số:** yfinance
    - **Lịch kinh tế:** Mock data (cần API key)
    - **Crypto funding:** Chưa tích hợp
    """)

with col2:
    st.markdown("### Thời gian cập nhật")
    st.markdown(f"""
    - **Lần cuối:** {now_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC
    - **Múi giờ:** {tz_name}
    - **Phiên:** Asia (mặc định)
    """)

with col3:
    st.markdown("### Versioning")
    st.markdown("""
    - **App version:** v1.0.0
    - **Ngày phát hành:** 2025-11-19
    - **Framework:** Streamlit
    """)

st.markdown("---")

# ============== COPY TOÀN TRANG ==============
full_content = f"""
PHỤ LỤC DỮ LIỆU & BẢNG BIỂU (QUỐC TẾ)
Cập nhật: {now_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC
Múi giờ: {tz_name}

=== LỊCH KINH TẾ ===
{calendar_df.to_string(index=False)}

=== HEATMAP BIẾN ĐỘNG ===
{heatmap_df.to_string(index=False) if 'heatmap_df' in locals() else 'Không có dữ liệu'}

=== BẢNG KỸ THUẬT NHANH ===
{technical_df.to_string(index=False) if 'technical_df' in locals() else 'Không có dữ liệu'}

---
Nguồn: yfinance, mock data
Agent Ada © 2025
"""

copy_page_content(full_content, label="📄 Copy toàn trang")

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ Thông tin trang")
    st.info("""
    **Modules:**
    
    1️⃣ Lịch kinh tế chuẩn hóa
    
    2️⃣ Heatmap biến động
    
    3️⃣ Bảng kỹ thuật nhanh
    
    4️⃣ Crypto funding (chưa có)
    
    5️⃣ Nguồn & versioning
    """)
    
    st.markdown("### 📤 Export tổng hợp")
    
    if st.button("📥 Tải tất cả dữ liệu (JSON)"):
        all_data = {
            "calendar": calendar_data,
            "heatmap": heatmap_data if 'heatmap_data' in locals() else [],
            "technical": technical_data if 'technical_data' in locals() else [],
            "timestamp": now_utc.isoformat(),
            "timezone": tz_name
        }
        
        import json
        json_str = json.dumps(all_data, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="📥 Tải JSON",
            data=json_str,
            file_name=f"market_data_{now_utc.strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    if st.button("🔄 Làm mới dữ liệu"):
        st.cache_data.clear()
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px 0;">
    <p><strong>Lưu ý:</strong> Dữ liệu được cung cấp chỉ mang tính chất tham khảo.</p>
    <p>Không bao gồm nội dung riêng về thị trường Việt Nam.</p>
</div>
""", unsafe_allow_html=True)
