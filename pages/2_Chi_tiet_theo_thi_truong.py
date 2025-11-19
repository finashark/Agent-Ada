"""
Trang 2: Thông tin chi tiết theo thị trường
Tabs: US Equities, Vàng, FX Majors, Crypto, Dầu, Chỉ số
"""
import streamlit as st
from datetime import datetime, timezone
import pandas as pd
import sys
sys.path.insert(0, '..')

from components.timestamp import render_timestamp
from components.copy import copy_section, copy_page_content
from components.exporters import show_export_options
from data_providers.market_details import (
    build_detail, build_top10_equities,
    FX_MAJORS, CRYPTO_MAJORS, OIL_TICKERS, GLOBAL_INDICES
)

# Cấu hình trang
st.set_page_config(
    page_title="Chi tiết theo thị trường",
    page_icon="📊",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .asset-card {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin: 15px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Thông tin chi tiết theo thị trường")

tz_name = st.session_state.get("timezone", "Asia/Ho_Chi_Minh")

st.markdown("---")

# Tabs
tabs = st.tabs([
    "🇺🇸 US Equities",
    "🥇 Vàng (XAUUSD)",
    "💱 FX Majors",
    "₿ Crypto",
    "🛢️ Dầu",
    "📈 Chỉ số"
])


# ============== HELPER FUNCTION ==============
def render_asset_detail(asset: str, detail, key_prefix: str):
    """Render chi tiết một asset theo chuẩn A-B-C-D-E"""
    
    # Timestamp
    render_timestamp(
        datetime.fromisoformat(detail.last_updated),
        tz_name,
        "Asia"
    )
    
    # (A) SNAPSHOT
    st.markdown('<div class="section-header">📊 (A) Snapshot</div>', unsafe_allow_html=True)
    
    snapshot = detail.snapshot
    if snapshot:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Last", f"{snapshot.get('last', 0):.2f}")
        
        with col2:
            pct_d1 = snapshot.get('pct_d1', 0)
            st.metric("%D1", f"{pct_d1:+.2f}%", delta=f"{pct_d1:.2f}%")
        
        with col3:
            st.metric("Range", snapshot.get('day_range', 'N/A'))
        
        with col4:
            st.metric("ATR(14)", f"{snapshot.get('atr14', 0):.2f}")
        
        col5, col6 = st.columns(2)
        
        with col5:
            ma20 = snapshot.get('ma20', 0)
            above_ma20 = snapshot.get('above_ma20', None)
            status = "🟢 Above" if above_ma20 else "🔴 Below" if above_ma20 is not None else "N/A"
            st.metric("MA20", f"{ma20:.2f}", help=status)
        
        with col6:
            ma50 = snapshot.get('ma50', 0)
            above_ma50 = snapshot.get('above_ma50', None)
            status = "🟢 Above" if above_ma50 else "🔴 Below" if above_ma50 is not None else "N/A"
            st.metric("MA50", f"{ma50:.2f}", help=status)
        
        snapshot_text = f"""
Asset: {asset}
Last: {snapshot.get('last', 0):.2f}
%D1: {snapshot.get('pct_d1', 0):+.2f}%
Range: {snapshot.get('day_range', 'N/A')}
ATR(14): {snapshot.get('atr14', 0):.2f}
MA20: {snapshot.get('ma20', 0):.2f} ({status})
MA50: {snapshot.get('ma50', 0):.2f}
"""
        copy_section(f"{asset} - Snapshot", snapshot_text, show_preview=False, key_suffix=f"{key_prefix}_snap")
    
    # (B) CẬP NHẬT & LINK
    st.markdown('<div class="section-header">📰 (B) Cập nhật & Link</div>', unsafe_allow_html=True)
    
    if detail.updates:
        for update in detail.updates:
            title = update.get('title', '')
            url = update.get('url', '')
            if url:
                st.markdown(f"- [{title}]({url})")
            else:
                st.markdown(f"- {title}")
        
        updates_text = "\n".join([f"- {u.get('title', '')}" for u in detail.updates])
        copy_section(f"{asset} - Updates", updates_text, show_preview=False, key_suffix=f"{key_prefix}_upd")
    else:
        st.info("Chưa có cập nhật mới")
    
    # (C) YẾU TỐ CHI PHỐI
    st.markdown('<div class="section-header">🎯 (C) Yếu tố chi phối</div>', unsafe_allow_html=True)
    
    if detail.drivers:
        for driver in detail.drivers:
            st.markdown(f"- {driver}")
        
        drivers_text = "\n".join([f"- {d}" for d in detail.drivers])
        copy_section(f"{asset} - Drivers", drivers_text, show_preview=False, key_suffix=f"{key_prefix}_drv")
    else:
        st.info("Chưa xác định drivers")
    
    # (D) KẾ HOẠCH GIAO DỊCH
    st.markdown('<div class="section-header">💼 (D) Kế hoạch giao dịch (Khách quan)</div>', unsafe_allow_html=True)
    
    plan = detail.trade_plan
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Bias:** {plan.bias}")
        st.markdown(f"**Trigger:** {plan.trigger}")
        st.markdown(f"**Timeframe:** {plan.timeframe}")
    
    with col2:
        st.markdown(f"**Invalidation:** {plan.invalidation}")
        st.markdown(f"**Rủi ro sự kiện:** {plan.risk_events if plan.risk_events else 'N/A'}")
    
    # Levels
    if plan.levels:
        levels_df = pd.DataFrame([plan.levels])
        st.dataframe(levels_df, use_container_width=True, hide_index=True)
    
    plan_text = f"""
Bias: {plan.bias}
Trigger: {plan.trigger}
Invalidation: {plan.invalidation}
Timeframe: {plan.timeframe}
Rủi ro sự kiện: {plan.risk_events if plan.risk_events else 'N/A'}
Levels: R1={plan.levels.get('R1')}, R2={plan.levels.get('R2')}, S1={plan.levels.get('S1')}, S2={plan.levels.get('S2')}
"""
    copy_section(f"{asset} - Trade Plan", plan_text, show_preview=False, key_suffix=f"{key_prefix}_plan")
    
    # (E) RỦI RO & KỊCH BẢN THAY THẾ
    st.markdown('<div class="section-header">⚠️ (E) Rủi ro & Kịch bản thay thế</div>', unsafe_allow_html=True)
    
    if detail.alternative_scenarios:
        for scenario in detail.alternative_scenarios:
            st.markdown(f"- {scenario}")
        
        scenarios_text = "\n".join([f"- {s}" for s in detail.alternative_scenarios])
        copy_section(f"{asset} - Scenarios", scenarios_text, show_preview=False, key_suffix=f"{key_prefix}_scen")
    
    if detail.notes:
        st.info(f"📝 **Notes:** {detail.notes}")
    
    st.markdown("---")


# ============== TAB 1: US EQUITIES ==============
with tabs[0]:
    st.markdown("## 🇺🇸 US Equities - Top 10 cổ phiếu đáng chú ý")
    
    with st.spinner("Đang phân tích S&P 500..."):
        top10 = build_top10_equities(universe="S&P 500")
    
    st.markdown(f"**Universe:** {top10.universe}")
    st.markdown(f"**Phương pháp:** {top10.method}")
    render_timestamp(
        datetime.fromisoformat(top10.last_updated),
        tz_name,
        "Asia"
    )
    
    # Bảng Top 10
    if top10.items:
        data = []
        for item in top10.items:
            data.append({
                "Ticker": item.ticker,
                "Last": f"{item.last:.2f}",
                "%D/D": f"{item.pct_change:+.2f}%",
                "Vol/20D": f"{item.vol_ratio:.2f}x",
                "Catalyst": item.catalyst if item.catalyst else "N/A",
                "Idea": item.idea if item.idea else "N/A",
                "Score": f"{item.score:.2f}"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export & Copy
        col1, col2 = st.columns(2)
        
        with col1:
            show_export_options(
                data_csv=data,
                data_json=data,
                prefix="top10_equities"
            )
        
        with col2:
            top10_text = "\n".join([f"{i+1}. {item.ticker} - {item.pct_change:+.2f}% - {item.idea}" 
                                    for i, item in enumerate(top10.items)])
            copy_section("Top 10 Equities", top10_text, show_preview=False, key_suffix="top10")
    else:
        st.warning("⚠️ Không có dữ liệu Top 10")
    
    # Score components
    st.markdown("### Score Components")
    st.json(top10.score_components)


# ============== TAB 2: VÀNG ==============
with tabs[1]:
    st.markdown("## 🥇 Vàng (XAUUSD)")
    
    with st.spinner("Đang tải dữ liệu vàng..."):
        gold_detail = build_detail("GC=F")
    
    render_asset_detail("GC=F (Gold Futures)", gold_detail, "gold")
    
    # Thêm chỉ báo phụ
    st.markdown("### Chỉ báo liên quan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.spinner("Loading DXY..."):
            dxy_detail = build_detail("^DXY")
            dxy_snap = dxy_detail.snapshot
            if dxy_snap:
                st.metric("DXY", f"{dxy_snap.get('last', 0):.2f}", 
                         delta=f"{dxy_snap.get('pct_d1', 0):+.2f}%")
    
    with col2:
        with st.spinner("Loading US10Y..."):
            us10y_detail = build_detail("^TNX")
            us10y_snap = us10y_detail.snapshot
            if us10y_snap:
                st.metric("US 10Y Yield", f"{us10y_snap.get('last', 0):.2f}%", 
                         delta=f"{us10y_snap.get('pct_d1', 0):+.2f}%")


# ============== TAB 3: FX MAJORS ==============
with tabs[2]:
    st.markdown("## 💱 FX Majors")
    
    selected_fx = st.selectbox("Chọn cặp FX:", FX_MAJORS, index=0)
    
    with st.spinner(f"Đang tải {selected_fx}..."):
        fx_detail = build_detail(selected_fx)
    
    render_asset_detail(selected_fx, fx_detail, f"fx_{selected_fx}")
    
    # Overview tất cả FX Majors
    with st.expander("📊 Overview tất cả FX Majors"):
        fx_overview = []
        for fx in FX_MAJORS:
            try:
                detail = build_detail(fx)
                snap = detail.snapshot
                if snap:
                    fx_overview.append({
                        "Pair": fx,
                        "Last": f"{snap.get('last', 0):.4f}",
                        "%D1": f"{snap.get('pct_d1', 0):+.2f}%",
                        "ATR(14)": f"{snap.get('atr14', 0):.4f}"
                    })
            except:
                continue
        
        if fx_overview:
            fx_df = pd.DataFrame(fx_overview)
            st.dataframe(fx_df, use_container_width=True, hide_index=True)


# ============== TAB 4: CRYPTO ==============
with tabs[3]:
    st.markdown("## ₿ Crypto Large Caps")
    
    selected_crypto = st.selectbox("Chọn crypto:", CRYPTO_MAJORS, index=0)
    
    with st.spinner(f"Đang tải {selected_crypto}..."):
        crypto_detail = build_detail(selected_crypto)
    
    render_asset_detail(selected_crypto, crypto_detail, f"crypto_{selected_crypto}")
    
    # Overview tất cả Crypto
    with st.expander("📊 Overview tất cả Crypto"):
        crypto_overview = []
        for crypto in CRYPTO_MAJORS:
            try:
                detail = build_detail(crypto)
                snap = detail.snapshot
                if snap:
                    crypto_overview.append({
                        "Crypto": crypto,
                        "Last": f"${snap.get('last', 0):,.2f}",
                        "%D1": f"{snap.get('pct_d1', 0):+.2f}%",
                        "ATR(14)": f"{snap.get('atr14', 0):.2f}"
                    })
            except:
                continue
        
        if crypto_overview:
            crypto_df = pd.DataFrame(crypto_overview)
            st.dataframe(crypto_df, use_container_width=True, hide_index=True)


# ============== TAB 5: DẦU ==============
with tabs[4]:
    st.markdown("## 🛢️ Dầu (WTI / Brent)")
    
    selected_oil = st.selectbox("Chọn loại dầu:", OIL_TICKERS, 
                                format_func=lambda x: "WTI Crude" if x == "CL=F" else "Brent Crude")
    
    with st.spinner(f"Đang tải {selected_oil}..."):
        oil_detail = build_detail(selected_oil)
    
    render_asset_detail(selected_oil, oil_detail, f"oil_{selected_oil}")
    
    # So sánh WTI vs Brent
    st.markdown("### So sánh WTI vs Brent")
    
    col1, col2 = st.columns(2)
    
    with col1:
        wti = build_detail("CL=F")
        wti_snap = wti.snapshot
        if wti_snap:
            st.metric("WTI", f"${wti_snap.get('last', 0):.2f}", 
                     delta=f"{wti_snap.get('pct_d1', 0):+.2f}%")
    
    with col2:
        brent = build_detail("BZ=F")
        brent_snap = brent.snapshot
        if brent_snap:
            st.metric("Brent", f"${brent_snap.get('last', 0):.2f}", 
                     delta=f"{brent_snap.get('pct_d1', 0):+.2f}%")


# ============== TAB 6: CHỈ SỐ ==============
with tabs[5]:
    st.markdown("## 📈 Chỉ số toàn cầu")
    
    selected_index = st.selectbox("Chọn chỉ số:", GLOBAL_INDICES, index=0)
    
    with st.spinner(f"Đang tải {selected_index}..."):
        index_detail = build_detail(selected_index)
    
    render_asset_detail(selected_index, index_detail, f"index_{selected_index}")
    
    # Overview tất cả chỉ số
    with st.expander("📊 Overview tất cả chỉ số"):
        indices_overview = []
        for idx in GLOBAL_INDICES:
            try:
                detail = build_detail(idx)
                snap = detail.snapshot
                if snap:
                    above_ma20 = snap.get('above_ma20', None)
                    above_ma50 = snap.get('above_ma50', None)
                    
                    status = ""
                    if above_ma20 and above_ma50:
                        status = "🟢 Bullish"
                    elif not above_ma20 and not above_ma50:
                        status = "🔴 Bearish"
                    else:
                        status = "🟡 Mixed"
                    
                    indices_overview.append({
                        "Index": idx,
                        "Last": f"{snap.get('last', 0):,.2f}",
                        "%D1": f"{snap.get('pct_d1', 0):+.2f}%",
                        "Status": status
                    })
            except:
                continue
        
        if indices_overview:
            indices_df = pd.DataFrame(indices_overview)
            st.dataframe(indices_df, use_container_width=True, hide_index=True)


# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ Thông tin trang")
    st.info("""
    **Cấu trúc phân tích:**
    
    (A) Snapshot - Dữ liệu hiện tại
    
    (B) Updates & Links - Tin tức
    
    (C) Drivers - Yếu tố chi phối
    
    (D) Trade Plan - Kế hoạch giao dịch
    
    (E) Risks - Rủi ro & kịch bản thay thế
    """)
    
    if st.button("🔄 Làm mới dữ liệu"):
        st.cache_data.clear()
        st.rerun()
