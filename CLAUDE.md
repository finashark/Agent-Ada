# Agent Ada - Claude Context Guide

## 🎯 Project Overview

**Agent Ada** là hệ thống báo cáo thị trường tài chính chuyên nghiệp được xây dựng cho môi giới CFDs tại sàn HFM. Ứng dụng sử dụng Streamlit + Gemini AI để tạo báo cáo phân tích thị trường bằng tiếng Việt.

### Công nghệ sử dụng:
- **Frontend**: Streamlit (Python web framework)
- **AI**: Google Gemini 2.5 Flash
- **Data Sources**: yfinance, NewsAPI, Alpha Vantage, Finnhub, Bold.Report API
- **Export**: CSV, JSON, Markdown (PDF đang phát triển)

---

## 📁 Project Structure

```
Agent-Ada/
├── Home.py                    # Trang chủ - overview nhanh
├── pages/
│   ├── 1_Nhan_dinh_thi_truong_chung.py  # Trang 1: Nhận định thị trường
│   ├── 2_Chi_tiet_theo_thi_truong.py    # Trang 2: Chi tiết tài sản
│   └── 3_Phu_luc_du_lieu.py             # Trang 3: Phụ lục dữ liệu
├── data_providers/
│   ├── overview.py            # Fetch dữ liệu tổng quan (yfinance)
│   ├── market_details.py      # Chi tiết từng tài sản
│   ├── news_provider.py       # Tin tức từ nhiều API
│   ├── ai_analyst.py          # Gemini AI analysis
│   └── derivatives_wrappers.py # Crypto derivatives
├── components/
│   ├── session_cache.py       # Shared cache system (4 sessions/day)
│   ├── session_badge.py       # Trading session display
│   ├── copy.py               # Copy to clipboard functionality
│   ├── exporters.py          # Export CSV/JSON/Markdown
│   └── timestamp.py          # Timestamp formatting
├── schemas.py                 # Pydantic models
├── requirements.txt           # Python dependencies
└── .streamlit/secrets.toml    # API keys (gitignored)
```

---

## 🔧 Key Features (Current)

### 1. Trang chủ (Home.py)
- Giới thiệu Agent Ada
- Session info hiển thị
- Links đến các trang con
- **Đã tối ưu**: Lazy loading (<1s load time)

### 2. Trang 1: Nhận định thị trường chung
- **Điểm nhấn qua đêm**: Highlights từ overnight markets
- **Bảng chỉ số cross-asset**: S&P 500, NASDAQ, DXY, VIX, Gold, Oil, BTC
- **Lịch kinh tế**: Events quan trọng trong ngày
- **Dòng tiền & tâm lý rủi ro**: VIX analysis, DXY, US10Y
- **AI Analysis**: Gemini tạo nhận định bằng tiếng Việt

### 3. Trang 2: Chi tiết theo thị trường
- **Phân tích VÀNG (XAUUSD)**: Giá, drivers, trade plan
- **FX Majors**: EUR/USD, GBP/USD, USD/JPY
- **Crypto**: BTC, ETH với AI analysis
- **Dầu**: WTI, Brent
- **Chỉ số toàn cầu**: US, EU, Asia indexes

### 4. Trang 3: Phụ lục dữ liệu
- **Lịch kinh tế chi tiết**
- **Heatmap biến động**
- **Bảng kỹ thuật nhanh**: ATR, MA20, MA50, Z-score
- **Export**: CSV, JSON, Markdown

---

## 🗄️ Data Sources

### Current Sources:
| Source | Data Type | Rate Limit |
|--------|-----------|------------|
| yfinance | Market prices, indicators | Free, no key |
| NewsAPI | News headlines | 100 req/day (free) |
| Alpha Vantage | News, fundamentals | 25 req/day (free) |
| Finnhub | Market news | 60 req/min (free) |

### Planned: Bold.Report API
```
Base URL: https://bold.report/data-api

Endpoints:
- combined/all (JSON/CSV): All daily data
- bold/performance: BOLD index performance
- gold/price: Gold prices
- gold/flows/summary: Gold ETF fund flows
- gold/funds/aum: Gold ETF AUM
- bitcoin/price: Bitcoin prices  
- bitcoin/flows/summary: Bitcoin ETF flows
- bitcoin/funds/aum: Bitcoin ETF AUM
- performance/gold-bitcoin: BOLD vs Gold vs BTC
- performance/bold-macro: BOLD vs macro assets

Rate limit: 1 request/hour per IP
Format: JSON with header {version, updated, data[]}
```

---

## 💾 Caching Strategy

### Session-based Shared Cache
- **4 phiên giao dịch/ngày**: Asia, Europe, US, After-Hours
- **Shared cache**: Tất cả users dùng chung cache
- **Auto-invalidate**: Khi sang phiên mới
- **Implementation**: `@st.cache_data` with session-based cache keys

```python
# Cache key format: {type}_{date}_{session}
# Example: market_data_2025-12-01_Asia
```

---

## 🔑 API Keys Configuration

File: `.streamlit/secrets.toml` (gitignored)
```toml
[gemini]
api_key = "AIza..."

[news]
newsapi_key = "..."
alphavantage_key = "..."
finnhub_key = "..."
```

---

## 🚀 Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run Home.py

# Clear cache
# In sidebar: Click "🔄 Xóa cache & tải lại"
```

---

## ⚠️ Known Issues

1. **News API failures**: Handled with try-except, fallback to mock data
2. **yfinance rate limits**: Use shared cache to reduce API calls
3. **Gemini API quotas**: Monitor usage, implement fallback

---

## 📋 TODO / Improvements

### High Priority
- [ ] **PDF Export**: Generate professional PDF reports
- [ ] **Bold.Report API**: Integrate Gold/BTC ETF flows data
- [ ] **Error handling**: More robust validation

### Medium Priority
- [ ] **Report templates**: Pre-formatted report layouts
- [ ] **Charts**: Interactive charts with Plotly
- [ ] **Alerts**: Market condition notifications

### Low Priority
- [ ] **Multi-language**: EN/VI toggle
- [ ] **Dark mode**: Theme support
- [ ] **Mobile optimization**: Responsive design

---

## 🎨 Coding Conventions

- **Language**: Code in English, UI/comments in Vietnamese
- **Type hints**: Use Python type annotations
- **Models**: Pydantic for data validation
- **Logging**: Use `logging` module, not print()
- **Error handling**: Always use try-except with meaningful messages
- **Cache**: Use session-based caching for API calls

---

## 📝 Git Workflow

```bash
# Branch naming
feature/xxx    # New features
fix/xxx        # Bug fixes
refactor/xxx   # Code improvements

# Commit messages
feat: Add PDF export
fix: Handle empty news list
refactor: Optimize data loading
```

---

## 🔗 Resources

- **Repo**: https://github.com/finashark/Agent-Ada
- **Streamlit Docs**: https://docs.streamlit.io
- **Gemini API**: https://ai.google.dev/docs
- **Bold.Report API**: https://bold.report/data-api
