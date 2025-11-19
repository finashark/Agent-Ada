# 🔧 Fix: Top 10 US Equities Logic

**Ngày sửa:** 2025-11-19  
**Issue:** "Không có dữ liệu Top 10 cổ phiếu US"

---

## 🐛 Vấn đề cũ

Hàm `build_top10_equities()` trong `data_providers/market_details.py` có 3 vấn đề:

1. ❌ **Random sampling** 50 tickers từ S&P 500
   ```python
   sample_tickers = np.random.choice(tickers, size=min(50, len(tickers)), replace=False)
   ```
   → Kết quả không ổn định, mỗi lần chạy khác nhau

2. ❌ **Universe sai:** S&P 500 thay vì NASDAQ large-cap
   → Không đúng yêu cầu "cổ phiếu vốn hóa lớn và phổ biến trên sàn NASDAQ"

3. ❌ **Xếp hạng sai:** Sort theo `score` phức tạp thay vì % tăng đơn giản
   ```python
   score = calculate_stock_score(ticker, pct_change, vol_ratio, has_news=False)
   items.sort(key=lambda x: x.score, reverse=True)
   ```
   → Không đúng yêu cầu "top 10 tăng mạnh nhất trong phiên gần nhất"

---

## ✅ Giải pháp mới

### 1. **Thêm hàm `get_nasdaq_large_caps()`**

Danh sách cố định ~100 cổ phiếu NASDAQ large-cap:

```python
def get_nasdaq_large_caps() -> List[str]:
    """
    Lấy danh sách cổ phiếu vốn hóa lớn và phổ biến trên NASDAQ
    
    Returns:
        List tickers NASDAQ large-cap
    """
    nasdaq_tickers = [
        # Tech Giants
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA",
        # Semiconductors
        "AVGO", "AMD", "INTC", "QCOM", "MU", "AMAT", "LRCX", "KLAC", ...
        # Software & Cloud
        "ORCL", "ADBE", "CRM", "NOW", "INTU", "PANW", ...
        # E-commerce & Consumer
        "COST", "SBUX", "ABNB", "BKNG", "EBAY", ...
        # Biotech & Healthcare
        "GILD", "AMGN", "REGN", "VRTX", "BIIB", "MRNA", ...
        # ... (total ~100 stocks)
    ]
    
    return nasdaq_tickers
```

**Đặc điểm:**
- ✅ Danh sách cố định, không random
- ✅ Bao gồm NASDAQ-100 + thêm blue-chips
- ✅ Nhóm theo sectors (Tech, Semi, Software, Biotech, etc.)

### 2. **Sửa logic `build_top10_equities()`**

**Thay đổi chính:**

```python
def build_top10_equities(universe: str = "NASDAQ Large-Cap") -> EquityTop10:
    # 1. Lấy NASDAQ large-caps (thay vì random S&P 500)
    tickers = get_nasdaq_large_caps()
    
    # 2. Fetch giá cho TẤT CẢ tickers
    for ticker in tickers:
        df = fetch_ohlc(ticker, period="1mo", interval="1d")
        
        # Tính % change D/D
        pct_change = ((last / prev) - 1) * 100
        
        # Score = pct_change (đơn giản, không weighted)
        score = pct_change
        
    # 3. Sắp xếp theo % tăng (không phải score phức tạp)
    items.sort(key=lambda x: x.pct_change, reverse=True)
    
    # 4. Lấy top 10 tăng mạnh nhất
    top_items = items[:10]
```

**Improvements:**
- ✅ Universe: NASDAQ Large-Cap (~100 stocks)
- ✅ Ranking: Top 10 cổ phiếu tăng mạnh nhất theo %D/D
- ✅ Score đơn giản = % Change
- ✅ Không random, deterministic

### 3. **Cập nhật UI Text**

File `pages/2_Chi_tiet_theo_thi_truong.py`:

```python
# Cũ
st.markdown("## 🇺🇸 US Equities - Top 10 cổ phiếu đáng chú ý")
with st.spinner("Đang phân tích S&P 500..."):
    top10 = build_top10_equities(universe="S&P 500")

# Mới
st.markdown("## 🇺🇸 US Equities - Top 10 cổ phiếu tăng mạnh nhất")
with st.spinner("Đang phân tích NASDAQ Large-Cap..."):
    top10 = build_top10_equities(universe="NASDAQ Large-Cap")
```

---

## 📊 Kết quả mong đợi

### Output mẫu:

| Rank | Ticker | Last | %D/D | Vol/20D | Idea |
|------|--------|------|------|---------|------|
| 1 | NVDA | 485.20 | +8.34% | 1.82x | Tăng đột biến - cảnh báo profit-taking |
| 2 | AMD | 178.45 | +6.12% | 1.45x | Momentum mạnh - theo dõi pullback |
| 3 | TSLA | 242.80 | +5.67% | 2.01x | Momentum mạnh - theo dõi pullback |
| 4 | AVGO | 1520.30 | +4.89% | 1.23x | Momentum mạnh - theo dõi pullback |
| 5 | AAPL | 189.95 | +3.21% | 0.98x | Momentum mạnh - theo dõi pullback |
| ... | ... | ... | ... | ... | ... |

### Phân loại `idea` tự động:

```python
if pct_change > 5:
    idea = "Tăng đột biến - cảnh báo profit-taking"
elif pct_change > 3:
    idea = "Momentum mạnh - theo dõi pullback"
elif pct_change > 1:
    idea = "Tăng nhẹ - xu hướng tích cực"
elif pct_change > 0:
    idea = "Tăng yếu - consolidation"
else:
    idea = "Điều chỉnh - chờ entry"
```

---

## 🔍 So sánh Before/After

| Aspect | Before | After |
|--------|--------|-------|
| **Universe** | S&P 500 (500 stocks) | NASDAQ Large-Cap (~100 stocks) |
| **Sampling** | Random 50 stocks | All ~100 stocks |
| **Ranking** | Complex score (zscore + vol + news) | Simple % Change D/D |
| **Top 10** | "Đáng chú ý" (unclear) | "Tăng mạnh nhất" (clear) |
| **Deterministic** | ❌ (random mỗi lần) | ✅ (cố định cho cùng data) |
| **Performance** | Slow (Wikipedia fetch + random) | Fast (hardcoded list) |

---

## ⚙️ Các files đã sửa

1. **`data_providers/market_details.py`**
   - ✅ Added: `get_nasdaq_large_caps()` function
   - ✅ Modified: `build_top10_equities()` logic
   - Lines changed: ~80 lines

2. **`pages/2_Chi_tiet_theo_thi_truong.py`**
   - ✅ Updated: Title text
   - ✅ Updated: Spinner text
   - ✅ Updated: Universe parameter
   - Lines changed: 3 lines

---

## 🧪 Testing

### Test locally:

```powershell
streamlit run Home.py
```

### Kiểm tra:

1. Navigate to **Trang 2: Chi tiết theo thị trường**
2. Click tab **US Equities**
3. Verify:
   - ✅ Universe: "NASDAQ Large-Cap"
   - ✅ Method: "Top 10 cổ phiếu tăng mạnh nhất trong phiên gần nhất"
   - ✅ Table shows 10 rows sorted by %D/D descending
   - ✅ All tickers are NASDAQ stocks (AAPL, NVDA, TSLA, etc.)
   - ✅ No random sampling error

---

## 📝 Notes

### Universe rationale:

- **NASDAQ Large-Cap** phù hợp với yêu cầu "vốn hóa lớn và phổ biến"
- Tập trung vào Tech/Growth stocks (NASDAQ đặc trưng)
- Dễ theo dõi hơn S&P 500 (500 stocks quá nhiều)

### Performance:

- Hardcoded list → no Wikipedia fetch → faster
- ~100 stocks → reasonable scan time (1-2 phút)
- Cache TTL = 600s → không re-fetch quá thường xuyên

### Future improvements:

- [ ] Thêm market cap filter (chỉ lấy > $10B)
- [ ] Thêm liquidity filter (ADV > 5M shares)
- [ ] Tích hợp news sentiment từ API
- [ ] WebSocket real-time price updates

---

## 🎯 Kết luận

**Issue resolved:** ✅

Hàm `build_top10_equities()` giờ đã:
- ✅ Lấy đúng universe (NASDAQ Large-Cap)
- ✅ Sắp xếp đúng logic (top 10 tăng mạnh nhất)
- ✅ Deterministic (không random)
- ✅ Đúng yêu cầu từ user

---

**Developed by Ken © 2025**
