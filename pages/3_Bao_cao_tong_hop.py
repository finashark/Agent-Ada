"""
Trang 3: Báo cáo tổng hợp - 3 trang A4 canvas format
Template màu HFM với disclaimer đầy đủ
"""
import streamlit as st
import pandas as pd
import html
from datetime import datetime
import pytz
import sys
sys.path.insert(0, '..')

from data_providers.overview import build_overview
from data_providers.news_provider import NewsProvider
from data_providers.market_details import build_detail, FX_MAJORS, CRYPTO_MAJORS
from data_providers.ai_analyst import get_ada_analyst
from components.session_cache import get_current_session

# Cấu hình trang
st.set_page_config(
    page_title="Báo cáo tổng hợp",
    page_icon="📋",
    layout="wide"
)

# Get current time
tz = pytz.timezone("Asia/Ho_Chi_Minh")
now = datetime.now(tz)
report_date = now.strftime("%d/%m/%Y")
report_time = now.strftime("%H:%M")

# Get session info
session_name, session_start = get_current_session()
session_name_vi = {
    "Asia": "Châu Á",
    "Europe": "Châu Âu",
    "US": "Mỹ",
    "After-Hours": "Sau giờ",
    "Off-Market": "Ngoài giờ"
}.get(session_name, session_name)

# CSS for A4 pages with HFM branding
st.markdown("""
<style>
    @media print {
        .page-break { page-break-after: always; }
    }
    
    .a4-page {
        width: 210mm;
        min-height: 297mm;
        margin: 0 auto 20px auto;
        background: white;
        padding: 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* HFM Brand Colors - Black & Red */
    .hfm-header {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        color: white;
        padding: 25px 30px;
        position: relative;
    }
    
    .hfm-accent {
        background: linear-gradient(90deg, #D32F2F 0%, #E53935 100%);
        height: 8px;
        width: 100%;
    }
    
    .report-title {
        font-size: 32px;
        font-weight: 700;
        margin: 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .report-subtitle {
        font-size: 16px;
        margin: 8px 0 0 0;
        color: #e3f2fd;
        font-weight: 400;
    }
    
    .report-meta {
        position: absolute;
        top: 25px;
        right: 30px;
        text-align: right;
        color: white;
    }
    
    .report-date {
        font-size: 18px;
        font-weight: 600;
        margin: 0;
    }
    
    .report-session {
        font-size: 13px;
        margin: 4px 0 0 0;
        color: #b3e5fc;
    }
    
    /* Content sections */
    .content-section {
        padding: 25px 30px;
        background: white;
    }
    
    .section-header {
        background: white;
        color: #000000;
        font-size: 20px;
        font-weight: 700;
        padding: 12px 15px;
        margin: 0 0 15px 0;
        border-left: 5px solid #D32F2F;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    .news-item {
        background: #f8f9fa;
        padding: 12px 15px;
        margin: 0 0 10px 0;
        border-radius: 6px;
        border-left: 3px solid #D32F2F;
    }
    
    .news-title {
        font-size: 14px;
        font-weight: 600;
        color: #000000;
        margin: 0 0 5px 0;
    }
    
    .news-meta {
        font-size: 11px;
        color: #607d8b;
    }
    
    .analysis-box {
        background: linear-gradient(135deg, #ffebee 0%, #f5f5f5 100%);
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #D32F2F;
        margin: 10px 0;
    }
    
    .analysis-text {
        font-size: 13px;
        line-height: 1.7;
        color: #263238;
        margin: 0;
    }
    
    .market-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin: 15px 0;
    }
    
    .market-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .market-card-header {
        font-size: 15px;
        font-weight: 700;
        color: #000000;
        margin: 0 0 10px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #D32F2F;
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 6px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .metric-label {
        font-size: 12px;
        color: #546e7a;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 13px;
        font-weight: 700;
        color: #000000;
    }
    
    .metric-positive {
        color: #2e7d32;
    }
    
    .metric-negative {
        color: #c62828;
    }
    
    .calendar-item {
        background: white;
        border-left: 4px solid #D32F2F;
        padding: 10px 12px;
        margin: 0 0 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .calendar-time {
        font-size: 12px;
        font-weight: 700;
        color: #D32F2F;
        margin: 0 0 4px 0;
    }
    
    .calendar-event {
        font-size: 13px;
        color: #263238;
        margin: 0;
    }
    
    .impact-high {
        background: #ffebee;
        color: #c62828;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        display: inline-block;
        margin-left: 8px;
    }
    
    .impact-medium {
        background: #fff3e0;
        color: #ef6c00;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 700;
        display: inline-block;
        margin-left: 8px;
    }
    
    /* Footer */
    .report-footer {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: #263238;
        color: white;
        padding: 20px 30px;
    }
    
    .disclaimer-title {
        font-size: 13px;
        font-weight: 700;
        color: #D32F2F;
        margin: 0 0 10px 0;
        text-transform: uppercase;
    }
    
    .disclaimer-text {
        font-size: 11px;
        line-height: 1.6;
        color: #b0bec5;
        margin: 0 0 8px 0;
    }
    
    .footer-brand {
        text-align: center;
        padding-top: 12px;
        border-top: 1px solid #37474f;
        margin-top: 12px;
    }
    
    .footer-logo {
        font-size: 18px;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    
    .footer-meta {
        font-size: 10px;
        color: #78909c;
        margin: 4px 0 0 0;
    }
    
    /* Utilities */
    .spacer {
        height: 15px;
    }
    
    .text-center {
        text-align: center;
    }
    
    .mb-10 {
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📋 Báo cáo tổng hợp")
st.markdown("---")

# Load data
with st.spinner("Đang tải dữ liệu báo cáo..."):
    # Overview data
    overview_obj = build_overview()
    overview_data = overview_obj.model_dump()  # Convert Pydantic model to dict
    
    # News
    news_provider = NewsProvider()
    news_items = news_provider.get_news(hours_back=24, max_items=8)
    
    # Debug: Check news items
    if not news_items or len(news_items) == 0:
        st.warning("⚠️ Không lấy được tin tức mới. Đang sử dụng highlights từ market data.")
        # Fallback to highlights if no news
        news_items = []
    
    # Market details
    gold_detail = build_detail("GC=F")
    
    # AI Analysis
    ada_analyst = get_ada_analyst()

# Generate AI opening analysis
opening_analysis = ""
if ada_analyst.model:
    try:
        # Convert DataFrame to list if needed
        if isinstance(news_items, pd.DataFrame):
            news_items = news_items.to_dict('records')
        
        # Use news if available, otherwise use highlights
        if news_items and len(news_items) > 0:
            news_summary = "\n".join([f"- {item.get('title', 'N/A')}" for item in news_items[:5] if item])
        else:
            highlights = overview_data.get('highlights', [])
            news_summary = "\n".join([f"- {h}" for h in highlights[:5]]) if highlights else "Không có tin tức đáng chú ý"
        
        # Get risk sentiment values directly (they are floats, not dicts)
        risk_sentiment = overview_data.get('risk_sentiment', {})
        vix = risk_sentiment.get('vix', 0)
        dxy = risk_sentiment.get('dxy', 0)
        us10y = risk_sentiment.get('us10y', 0)
        
        prompt = f"""Bạn là Ada, chuyên gia phân tích thị trường tài chính.

THÔNG TIN THỊ TRƯỜNG:
{news_summary}

CHỈ SỐ RỦI RO:
- VIX: {vix:.2f}
- DXY: {dxy:.2f}
- US10Y: {us10y:.2f}%

Viết 1 đoạn văn ngắn gọn (4-5 câu) NHẬN ĐỊNH ĐẦU NGÀY bằng tiếng Việt:
- Tóm tắt diễn biến quan trọng qua đêm
- Đánh giá tâm lý thị trường (risk-on/risk-off) dựa trên VIX, DXY, US10Y
- Nhận định xu hướng ngắn hạn cho phiên giao dịch hôm nay

Viết chuyên nghiệp, rõ ràng, dễ hiểu cho môi giới CFDs."""
        
        response = ada_analyst.model.generate_content(prompt)
        opening_analysis = response.text.strip()
    except Exception as e:
        # Better fallback using actual data
        risk_sentiment = overview_data.get('risk_sentiment', {})
        vix = risk_sentiment.get('vix', 0)
        opening_analysis = f"Thị trường đang trong giai đoạn quan sát với VIX ở mức {vix:.2f}. Các yếu tố vĩ mô và tin tức địa chính trị đang tác động đến tâm lý nhà đầu tư. Khuyến nghị theo dõi sát các chỉ số rủi ro và diễn biến thị trường trong ngày."

# ========== PAGE 1: TIN TỨC VÀ NHẬN ĐỊNH ==========
page1_html = f"""
<div class="a4-page">
    <!-- Header -->
    <div class="hfm-header">
        <div class="report-meta">
            <p class="report-date">{report_date}</p>
            <p class="report-session">Phiên: {session_name_vi}</p>
            <p class="report-session">{report_time} ICT</p>
        </div>
        <h1 class="report-title">BÁO CÁO THỊ TRƯỜNG</h1>
        <p class="report-subtitle">Phân tích & Nhận định từ Agent Ada</p>
    </div>
    <div class="hfm-accent"></div>
    
    <!-- Content -->
    <div class="content-section">
        <!-- Section 1: Tin tức quan trọng -->
        <div class="section-header">📰 TIN TỨC QUAN TRỌNG QUA ĐÊM</div>
        
        <div style="max-height: 280px; overflow: hidden;">
"""

# Add news items
if news_items and isinstance(news_items, list) and len(news_items) > 0:
    for idx, item in enumerate(news_items[:6]):
        if item and isinstance(item, dict):
            title = html.escape(item.get('title', 'N/A'))[:100]  # Escape HTML characters
            source = html.escape(item.get('source', 'Unknown'))
            time = item.get('published_at', '')[:10] if item.get('published_at') else ''
            
            page1_html += f"""
            <div class="news-item">
                <div class="news-title">{idx+1}. {title}</div>
                <div class="news-meta">Nguồn: {source} | {time}</div>
            </div>
"""
else:
    # Fallback to market highlights if no news available
    highlights = overview_data.get('highlights', [])
    if highlights:
        for idx, highlight in enumerate(highlights[:6]):
            page1_html += f"""
            <div class="news-item">
                <div class="news-title">{idx+1}. {html.escape(highlight)}</div>
                <div class="news-meta">Nguồn: Market Data Analysis</div>
            </div>
"""
    else:
        page1_html += """
            <div class="news-item">
                <div class="news-title">Đang cập nhật tin tức...</div>
            </div>
"""

page1_html += f"""
        </div>
        
        <div class="spacer"></div>
        
        <!-- Section 2: Nhận định đầu ngày -->
        <div class="section-header">💡 NHẬN ĐỊNH ĐẦU NGÀY</div>
        
        <div class="analysis-box">
            <p class="analysis-text">{html.escape(opening_analysis) if opening_analysis else 'Đang cập nhật phân tích...'}</p>
        </div>
        
        <div class="spacer"></div>
        
        <!-- Risk Sentiment -->
        <div class="section-header">📊 CHỈ SỐ RỦI RO</div>
        
        <div class="market-grid">
"""

# Add risk sentiment metrics
risk_sentiment = overview_data.get('risk_sentiment', {})
for key, label in [('vix', 'VIX (Biến động)'), ('dxy', 'DXY (USD Index)'), ('us10y', 'US 10Y Yield')]:
    value = risk_sentiment.get(key, 0)
    
    # Get change from market_snapshot if available
    snapshot = overview_data.get('market_snapshot', {})
    ticker_map = {'vix': '^VIX', 'dxy': 'DXY', 'us10y': '^TNX'}
    ticker = ticker_map.get(key)
    change = 0
    if ticker and ticker in snapshot:
        change = snapshot[ticker].get('d1', 0)
    
    change_class = 'metric-positive' if change > 0 else 'metric-negative' if change < 0 else ''
    
    page1_html += f"""
            <div class="market-card">
                <div class="market-card-header">{label}</div>
                <div class="metric-row">
                    <span class="metric-label">Giá trị</span>
                    <span class="metric-value">{value:.2f}{'%' if key == 'us10y' else ''}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Thay đổi 1D</span>
                    <span class="metric-value {change_class}">{change:+.2f}%</span>
                </div>
            </div>
"""

page1_html += """
        </div>
    </div>
    
    <!-- Footer -->
    <div class="report-footer">
        <div class="disclaimer-title">⚠️ TUYÊN BỐ MIỄN TRÁCH NHIỆM</div>
        <p class="disclaimer-text">
            <strong>Thông tin khách quan:</strong> Báo cáo này được tổng hợp từ các nguồn tin tức công khai và dữ liệu thị trường, 
            chỉ mang tính chất tham khảo và không cấu thành lời khuyên đầu tư. Mọi quyết định đầu tư thuộc về nhà đầu tư 
            và nhà đầu tư tự chịu trách nhiệm về kết quả đầu tư của mình.
        </p>
        <p class="disclaimer-text">
            <strong>Miễn trách:</strong> Agent Ada và HFM không chịu trách nhiệm về bất kỳ tổn thất hoặc thiệt hại nào 
            phát sinh từ việc sử dụng thông tin trong báo cáo này. Giao dịch CFDs có rủi ro cao và có thể không phù hợp 
            với tất cả nhà đầu tư.
        </p>
        <div class="footer-brand">
            <p class="footer-logo">HFM • Agent Ada</p>
            <p class="footer-meta">Trang 1/3 | Được tạo tự động bởi Agent Ada</p>
        </div>
    </div>
</div>
"""

st.markdown(page1_html, unsafe_allow_html=True)

st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)

# ========== PAGE 2: LỊCH KINH TẾ & TIN TỨC ==========

# Get economic calendar from overview data
calendar_items = overview_data.get('economic_calendar', [])[:8]

page2_html = f"""
<div class="a4-page">
    <!-- Header -->
    <div class="hfm-header">
        <div class="report-meta">
            <p class="report-date">{report_date}</p>
            <p class="report-session">Phiên: {session_name_vi}</p>
        </div>
        <h1 class="report-title">LỊCH KINH TẾ</h1>
        <p class="report-subtitle">Các sự kiện cần chú ý trong ngày</p>
    </div>
    <div class="hfm-accent"></div>
    
    <!-- Content -->
    <div class="content-section">
        <div class="section-header">📅 LỊCH KINH TẾ QUAN TRỌNG</div>
        
        <div style="max-height: 350px; overflow: hidden;">
"""

if calendar_items:
    for event in calendar_items:
        time_local = event.get('time_local', 'N/A')[:5]
        region = event.get('region', 'N/A')
        event_name = event.get('event', 'N/A')
        impact = event.get('impact', 'Medium')
        impact_class = 'impact-high' if impact == 'High' else 'impact-medium'
        
        page2_html += f"""
            <div class="calendar-item">
                <div class="calendar-time">{time_local} - {region}</div>
                <div class="calendar-event">
                    {event_name}
                    <span class="{impact_class}">{impact}</span>
                </div>
            </div>
"""
else:
    page2_html += """
            <div class="calendar-item">
                <div class="calendar-event">Không có sự kiện kinh tế quan trọng trong ngày</div>
            </div>
"""

page2_html += f"""
        </div>
        
        <div class="spacer"></div>
        
        <!-- Market Watch -->
        <div class="section-header">👀 CÁC CHỈ SỐ CẦN THEO DÕI</div>
        
        <div class="market-grid">
"""

# Add key markets to watch
watch_list = [
    ('XAUUSD', 'Vàng', gold_detail),
    ('DXY', 'USD Index', overview_data.get('risk_sentiment', {}).get('dxy', {})),
]

for ticker, name, data in watch_list:
    if isinstance(data, dict):
        last = data.get('value', 0) if ticker == 'DXY' else (data.snapshot.get('last', 0) if hasattr(data, 'snapshot') and data.snapshot else 0)
        change = data.get('change_pct', 0) if ticker == 'DXY' else (data.snapshot.get('pct_d1', 0) if hasattr(data, 'snapshot') and data.snapshot else 0)
        change_class = 'metric-positive' if change > 0 else 'metric-negative' if change < 0 else ''
        
        page2_html += f"""
            <div class="market-card">
                <div class="market-card-header">{name} ({ticker})</div>
                <div class="metric-row">
                    <span class="metric-label">Giá hiện tại</span>
                    <span class="metric-value">{last:.2f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Thay đổi D1</span>
                    <span class="metric-value {change_class}">{change:+.2f}%</span>
                </div>
            </div>
"""

page2_html += """
        </div>
        
        <div class="spacer"></div>
        
        <!-- Key Points -->
        <div class="section-header">🎯 ĐIỂM NHẤN CẦN CHÚ Ý</div>
        
        <div class="analysis-box">
            <p class="analysis-text">
"""

# Add highlights from overview data instead of hardcoded text
highlights = overview_data.get('highlights', [])
if highlights:
    for highlight in highlights[:4]:  # Top 4 highlights for page 2
        page2_html += f"                • {html.escape(highlight)}<br>\n"
else:
    page2_html += """                • Theo dõi các số liệu kinh tế quan trọng có thể gây biến động mạnh<br>
                • Chú ý đến diễn biến địa chính trị ảnh hưởng tâm lý thị trường<br>
"""

page2_html += """
            </p>
        </div>
    </div>
    
    <!-- Footer -->
    <div class="report-footer">
        <div class="disclaimer-title">⚠️ TUYÊN BỐ MIỄN TRÁCH NHIỆM</div>
        <p class="disclaimer-text">
            <strong>Thông tin khách quan:</strong> Lịch kinh tế và dữ liệu được tổng hợp từ các nguồn công khai. 
            Thời gian có thể thay đổi mà không cần báo trước. Nhà đầu tư nên tự xác minh thông tin trước khi đưa ra quyết định.
        </p>
        <p class="disclaimer-text">
            <strong>Miễn trách:</strong> Thông tin trong báo cáo chỉ mang tính tham khảo. Agent Ada và HFM không chịu trách nhiệm 
            về bất kỳ quyết định đầu tư nào dựa trên thông tin này.
        </p>
        <div class="footer-brand">
            <p class="footer-logo">HFM • Agent Ada</p>
            <p class="footer-meta">Trang 2/3 | Được tạo tự động bởi Agent Ada</p>
        </div>
    </div>
</div>
"""

st.markdown(page2_html, unsafe_allow_html=True)

st.markdown('<div class="page-break"></div>', unsafe_allow_html=True)

# ========== PAGE 3: PHÂN TÍCH CHI TIẾT ==========

page3_html = f"""
<div class="a4-page">
    <!-- Header -->
    <div class="hfm-header">
        <div class="report-meta">
            <p class="report-date">{report_date}</p>
            <p class="report-session">Phiên: {session_name_vi}</p>
        </div>
        <h1 class="report-title">PHÂN TÍCH THỊ TRƯỜNG</h1>
        <p class="report-subtitle">Chi tiết các tài sản chính</p>
    </div>
    <div class="hfm-accent"></div>
    
    <!-- Content -->
    <div class="content-section" style="padding-bottom: 180px;">
        <div class="section-header">🥇 VÀNG (XAUUSD)</div>
        
        <div class="market-grid">
"""

# Gold analysis
if gold_detail and gold_detail.snapshot:
    snapshot = gold_detail.snapshot
    plan = gold_detail.trade_plan
    
    page3_html += f"""
            <div class="market-card">
                <div class="market-card-header">Snapshot</div>
                <div class="metric-row">
                    <span class="metric-label">Giá hiện tại</span>
                    <span class="metric-value">${snapshot.get('last', 0):.2f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Thay đổi D1</span>
                    <span class="metric-value {'metric-positive' if snapshot.get('pct_d1', 0) > 0 else 'metric-negative'}">{snapshot.get('pct_d1', 0):+.2f}%</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">ATR(14)</span>
                    <span class="metric-value">${snapshot.get('atr14', 0):.2f}</span>
                </div>
            </div>
            
            <div class="market-card">
                <div class="market-card-header">Kế hoạch giao dịch</div>
                <div class="metric-row">
                    <span class="metric-label">Bias</span>
                    <span class="metric-value">{plan.bias if plan else 'N/A'}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Support (S1)</span>
                    <span class="metric-value">{plan.levels.get('S1', 'N/A') if plan and plan.levels else 'N/A'}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Resistance (R1)</span>
                    <span class="metric-value">{plan.levels.get('R1', 'N/A') if plan and plan.levels else 'N/A'}</span>
                </div>
            </div>
"""

page3_html += """
        </div>
        
        <div class="spacer"></div>
        
        <!-- FX Majors -->
        <div class="section-header">💱 FX MAJORS</div>
        
        <div class="market-grid">
"""

# Add FX pairs
for fx_pair in ['EURUSD=X', 'GBPUSD=X']:
    try:
        fx_detail = build_detail(fx_pair)
        if fx_detail and fx_detail.snapshot:
            snap = fx_detail.snapshot
            page3_html += f"""
            <div class="market-card">
                <div class="market-card-header">{fx_pair[:6]}</div>
                <div class="metric-row">
                    <span class="metric-label">Last</span>
                    <span class="metric-value">{snap.get('last', 0):.4f}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">D1</span>
                    <span class="metric-value {'metric-positive' if snap.get('pct_d1', 0) > 0 else 'metric-negative'}">{snap.get('pct_d1', 0):+.2f}%</span>
                </div>
            </div>
"""
    except:
        continue

page3_html += """
        </div>
        
        <div class="spacer"></div>
        
        <!-- Summary Analysis -->
        <div class="section-header">📝 TÓM TẮT PHÂN TÍCH</div>
        
        <div class="analysis-box">
            <p class="analysis-text">
                <strong>Vàng:</strong> Duy trì xu hướng theo dõi chỉ số DXY và lợi suất trái phiếu Mỹ. 
                Mức hỗ trợ quan trọng cần theo dõi để xác định điểm vào lệnh.<br><br>
                
                <strong>FX:</strong> Các cặp tiền chính diễn biến ổn định. Chú ý đến các phát biểu của 
                ngân hàng trung ương có thể tạo biến động.<br><br>
                
                <strong>Khuyến nghị:</strong> Quản lý rủi ro chặt chẽ với stop-loss. Theo dõi tin tức 
                trong ngày trước khi vào lệnh mới.
            </p>
        </div>
    </div>
    
    <!-- Footer -->
    <div class="report-footer">
        <div class="disclaimer-title">⚠️ TUYÊN BỐ MIỄN TRÁCH NHIỆM - BẮT BUỘC ĐỌC</div>
        <p class="disclaimer-text">
            <strong>1. Tính chất thông tin:</strong> Báo cáo này được tổng hợp tự động từ các nguồn dữ liệu công khai 
            với mục đích THAM KHẢO. Đây KHÔNG phải lời khuyên đầu tư, không phải khuyến nghị mua/bán cụ thể.
        </p>
        <p class="disclaimer-text">
            <strong>2. Trách nhiệm nhà đầu tư:</strong> Nhà đầu tư TỰ CHỊU TRÁCH NHIỆM hoàn toàn với mọi quyết định 
            đầu tư của mình. Vui lòng tự nghiên cứu, đánh giá rủi ro và tham khảo cố vấn tài chính độc lập.
        </p>
        <p class="disclaimer-text">
            <strong>3. Miễn trách:</strong> Agent Ada, HFM và các bên liên quan KHÔNG CHỊU TRÁCH NHIỆM về bất kỳ 
            tổn thất, thiệt hại trực tiếp hay gián tiếp phát sinh từ việc sử dụng thông tin này. Giao dịch CFDs 
            có rủi ro cao về vốn.
        </p>
        <div class="footer-brand">
            <p class="footer-logo">HFM • Agent Ada</p>
            <p class="footer-meta">Trang 3/3 | © 2025 HFM | Chỉ dành cho mục đích giáo dục</p>
        </div>
    </div>
</div>
"""

st.markdown(page3_html, unsafe_allow_html=True)

# Download buttons
st.markdown("---")
st.markdown("### 📥 Tải xuống báo cáo")

col1, col2 = st.columns(2)

with col1:
    if st.button("🖨️ In báo cáo", key="print_report"):
        st.info("Sử dụng Ctrl+P (Windows) hoặc Cmd+P (Mac) để in báo cáo")

with col2:
    st.markdown(f"**Báo cáo ngày:** {report_date} | **Phiên:** {session_name_vi}")

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ️ Thông tin báo cáo")
    st.success(f"""
    **Định dạng:** 3 trang A4
    
    **Màu HFM:**
    - Xanh dương đậm (#1a237e)
    - Cam (#ff6b35)
    
    **Nội dung:**
    ✅ Tin tức & Nhận định
    ✅ Lịch kinh tế
    ✅ Phân tích chi tiết
    ✅ Disclaimer đầy đủ
    """)
    
    st.markdown("---")
    
    if st.button("🔄 Làm mới dữ liệu"):
        st.cache_data.clear()
        st.rerun()
