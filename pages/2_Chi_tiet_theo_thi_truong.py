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
    build_detail,
    FX_MAJORS, CRYPTO_MAJORS, OIL_TICKERS, GLOBAL_INDICES
)
from data_providers.ai_analyst import get_ada_analyst
from data_providers.news_provider import NewsProvider

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
    "🥇 Vàng (XAUUSD)",
    "💱 FX Majors",
    "₿ Crypto",
    "🛢️ Dầu",
    "📈 Chỉ số"
])


# ============== HELPER FUNCTION ==============
def format_drivers_narrative(drivers: list, asset: str) -> str:
    """Chuyển drivers list thành văn bản tường thuật"""
    if not drivers:
        return "Chưa xác định rõ các yếu tố chi phối chính cho tài sản này trong phiên hiện tại."
    
    # Phân loại drivers theo impact
    positive = [d for d in drivers if d.startswith("(+)")]
    neutral = [d for d in drivers if d.startswith("(0)")]
    negative = [d for d in drivers if d.startswith("(-)")]
    
    # Đoạn topic
    narrative = f"**Phân tích các yếu tố chi phối giá {asset}:**\n\n"
    
    # Yếu tố tích cực
    if positive:
        narrative += "Các yếu tố hỗ trợ giá tăng bao gồm "
        factors = []
        for p in positive:
            clean = p.replace("(+)", "").split("[")[0].strip()
            factors.append(clean.lower())
        narrative += ", ".join(factors) + ". "
        
        # Giải thích logic
        if "DXY" in positive[0] or "USD" in positive[0]:
            narrative += "Khi USD suy yếu, các tài sản được định giá bằng USD như vàng và commodities thường tăng giá do trở nên rẻ hơn đối với người mua nắm giữ các đồng tiền khác. "
        elif "ETF" in positive[0] or "inflow" in positive[0]:
            narrative += "Dòng tiền lớn vào các quỹ ETF phản ánh nhu cầu mua mạnh từ nhà đầu tư tổ chức, tạo áp lực tăng giá bền vững. "
        elif "Earnings" in positive[0]:
            narrative += "Kết quả kinh doanh vượt kỳ vọng cho thấy sức khỏe tài chính tốt của doanh nghiệp, thúc đẩy tâm lý lạc quan và nhu cầu mua cổ phiếu. "
    
    # Yếu tố trung tính
    if neutral:
        narrative += "\n\nCác yếu tố trung tính (chưa rõ hướng tác động) "
        factors = []
        for n in neutral:
            clean = n.replace("(0)", "").split("[")[0].strip()
            factors.append(clean.lower())
        narrative += "bao gồm " + ", ".join(factors) + ". "
        narrative += "Những yếu tố này cần được theo dõi thêm vì có thể chuyển hướng tích cực hoặc tiêu cực tùy vào diễn biến thực tế. "
    
    # Yếu tố tiêu cực
    if negative:
        narrative += "\n\nNgược lại, áp lực giảm giá đến từ "
        factors = []
        for ng in negative:
            clean = ng.replace("(-)", "").split("[")[0].strip()
            factors.append(clean.lower())
        narrative += ", ".join(factors) + ". "
        
        # Giải thích
        if "risk appetite" in negative[0] or "risk-on" in negative[0]:
            narrative += "Khi thị trường chuyển sang tâm lý risk-on, nhà đầu tư ưu tiên các tài sản rủi ro cao như cổ phiếu thay vì tài sản an toàn như vàng, gây áp lực bán. "
        elif "Valuations" in negative[0] or "định giá" in negative[0]:
            narrative += "Định giá cao (P/E ratio lớn) có thể khiến nhà đầu tư thận trọng, lo ngại về khả năng tăng trưởng tiếp theo, dẫn đến chốt lời. "
    
    return narrative


def format_scenarios_narrative(scenarios: list, asset: str) -> str:
    """Chuyển alternative scenarios thành văn bản tường thuật"""
    if not scenarios:
        return "Hiện chưa có kịch bản rủi ro nào được xác định rõ ràng."
    
    narrative = f"**Đánh giá rủi ro và kịch bản thay thế cho {asset}:**\n\n"
    
    narrative += "Trong môi trường thị trường hiện tại, các kịch bản rủi ro cần lưu ý bao gồm: "
    
    for i, scenario in enumerate(scenarios, 1):
        clean_scenario = scenario.lstrip("- ").strip()
        if i == 1:
            narrative += f"({i}) {clean_scenario}; "
        elif i == len(scenarios):
            narrative += f"({i}) {clean_scenario}. "
        else:
            narrative += f"({i}) {clean_scenario}; "
    
    narrative += "\n\n"
    narrative += """Nhà đầu tư nên chuẩn bị các kịch bản phòng thủ bằng cách: đặt stop-loss chặt chẽ ở các mức kỹ thuật quan trọng, 
đa dạng hóa danh mục để giảm rủi ro tập trung, và theo dõi sát sao các tin tức kinh tế vĩ mô cũng như sự kiện địa chính trị. 
Trong trường hợp kịch bản xấu xảy ra, việc chốt lời sớm hoặc giảm tỷ trọng vị thế có thể giúp bảo vệ vốn hiệu quả."""
    
    return narrative


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
    
    # (C) YẾỤ TỐ CHI PHỐI
    st.markdown('<div class="section-header">🎯 (C) Yếu tố chi phối</div>', unsafe_allow_html=True)
    
    if detail.drivers:
        st.markdown("### Nhận định của Ada")
        
        # AI-powered analysis
        with st.spinner("Ada đang phân tích các yếu tố chi phối..."):
            ada_analyst = get_ada_analyst()
            news_provider = NewsProvider()
            
            # Get relevant news (last 12 hours, more focused)
            news_items = news_provider.get_news(hours_back=12, max_items=5)
            
            if ada_analyst.model:
                try:
                    # Build prompt for drivers analysis
                    drivers_list = "\n".join([f"- {d}" for d in detail.drivers])
                    
                    # Safely get top 3 news (handle empty list)
                    news_summary = ""
                    if news_items and len(news_items) > 0:
                        top_news = news_items[:3]
                        news_summary = chr(10).join([f"- {item.get('title', 'N/A')}" for item in top_news])
                    else:
                        news_summary = "- Đang cập nhật tin tức..."
                    
                    prompt = f"""Bạn là Ada, chuyên gia phân tích tài sản {asset}.

CÁC YẾU TỐ CHI PHỐI GIÁ HIỆN TẠI:
{drivers_list}

GIÁ HIỆN TẠI: ${detail.snapshot.get('last', 0):.2f} ({detail.snapshot.get('pct_d1', 0):+.2f}% trong ngày)

TIN TỨC LIÊN QUAN:
{news_summary}

Viết 2 đoạn văn ngắn gọn (mỗi đoạn 3-4 câu) bằng tiếng Việt:

**Đoạn 1**: Phân tích các yếu tố tích cực (+) và tiêu cực (-) đang tác động lên giá {asset}. Giải thích cơ chế tác động (ví dụ: DXY yếu → vàng tăng vì trở nên rẻ hơn cho buyer ngoài USD).

**Đoạn 2**: Đánh giá yếu tố nào đang chiếm ưu thế (bullish hay bearish) và dự báo xu hướng ngắn hạn dựa trên balance của các drivers này.

Viết chuyên nghiệp, súc tích, có số liệu cụ thể."""
                    
                    response = ada_analyst.model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    # Fallback to static
                    drivers_narrative = format_drivers_narrative(detail.drivers, asset)
                    st.markdown(drivers_narrative)
            else:
                # Fallback when AI unavailable
                drivers_narrative = format_drivers_narrative(detail.drivers, asset)
                st.markdown(drivers_narrative)
        
        # Hiển thị danh sách gốc trong expander
        with st.expander("📊 Xem drivers chi tiết (dạng danh sách)"):
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
    
    # (E) RỦI RO & KỊC H BẢN THAY THẾ
    st.markdown('<div class="section-header">⚠️ (E) Rủi ro & Kịch bản thay thế</div>', unsafe_allow_html=True)
    
    if detail.alternative_scenarios:
        st.markdown("### Nhận định của Ada")
        
        # AI-powered risk analysis
        with st.spinner("Ada đang phân tích rủi ro và kịch bản thay thế..."):
            ada_analyst = get_ada_analyst()
            
            if ada_analyst.model:
                try:
                    scenarios_list = "\n".join([f"- {s}" for s in detail.alternative_scenarios])
                    
                    prompt = f"""Bạn là Ada, chuyên gia quản lý rủi ro giao dịch {asset}.

KỊCH BẢN RỦI RO ĐÃ XÁC ĐỊNH:
{scenarios_list}

VỊ THẾ HIỆN TẠI:
- Bias: {detail.trade_plan.bias}
- Entry trigger: {detail.trade_plan.trigger}
- Invalidation: {detail.trade_plan.invalidation}

Viết 2 đoạn văn ngắn gọn (mỗi đoạn 3-4 câu):

**Đoạn 1**: Phân tích các kịch bản rủi ro trên - kịch bản nào có xác suất cao nhất và tại sao? Tác động của từng kịch bản lên vị thế giao dịch hiện tại.

**Đoạn 2**: Khuyến nghị cụ thể về quản lý rủi ro - nên đặt stop-loss ở đâu, có nên giảm tỷ trọng không, và các tín hiệu cảnh báo cần theo dõi (ví dụ: nếu break level X thì kịch bản bullish bị vô hiệu).

Viết bằng tiếng Việt, thực tế, có số liệu và levels cụ thể."""
                    
                    response = ada_analyst.model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    # Fallback
                    scenarios_narrative = format_scenarios_narrative(detail.alternative_scenarios, asset)
                    st.markdown(scenarios_narrative)
            else:
                # Fallback when AI unavailable
                scenarios_narrative = format_scenarios_narrative(detail.alternative_scenarios, asset)
                st.markdown(scenarios_narrative)
        
        # Hiển thị danh sách gốc trong expander
        with st.expander("📊 Xem kịch bản chi tiết (dạng danh sách)"):
            for scenario in detail.alternative_scenarios:
                st.markdown(f"- {scenario}")
        
        scenarios_text = "\n".join([f"- {s}" for s in detail.alternative_scenarios])
        copy_section(f"{asset} - Scenarios", scenarios_text, show_preview=False, key_suffix=f"{key_prefix}_scen")
    
    if detail.notes:
        st.info(f"📝 **Notes:** {detail.notes}")
    
    st.markdown("---")


# ============== TAB 1: VÀNG ==============
with tabs[0]:
    st.markdown("## 🥇 Vàng (XAUUSD)")
    
    with st.spinner("Đang tải dữ liệu vàng..."):
        gold_detail = build_detail("GC=F")
    
    render_asset_detail("GC=F (Gold Futures)", gold_detail, "gold")
    
    # Thêm chỉ báo phụ
    st.markdown("### Chỉ báo liên quan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.spinner("Loading DXY..."):
            dxy_detail = build_detail("DX-Y.NYB")
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


# ============== TAB 2: FX MAJORS ==============
with tabs[1]:
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


# ============== TAB 3: CRYPTO ==============
with tabs[2]:
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


# ============== TAB 4: DẦU ==============
with tabs[3]:
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


# ============== TAB 5: CHỈ SỐ ==============
with tabs[4]:
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
