# 🧪 TEST & VERIFICATION GUIDE

Hướng dẫn kiểm tra ứng dụng sau khi cài đặt

---

## ✅ Pre-flight Checklist

### 1. Kiểm tra Python version
```bash
python --version
# Cần: Python 3.8 trở lên
```

### 2. Kiểm tra pip
```bash
pip --version
```

### 3. Kiểm tra cấu trúc thư mục
```
Agent Ada/
├── Home.py ✓
├── pages/ ✓
│   ├── 1_Nhan_dinh_thi_truong_chung.py ✓
│   ├── 2_Chi_tiet_theo_thi_truong.py ✓
│   └── 3_Phu_luc_du_lieu.py ✓
├── components/ ✓
├── data_providers/ ✓
├── schemas.py ✓
├── requirements.txt ✓
└── README.md ✓
```

---

## 🔧 Installation Test

### Test 1: Install dependencies
```bash
pip install -r requirements.txt
```

**Expected:** Tất cả packages cài đặt thành công

**Common issues:**
- Lỗi network: Kiểm tra kết nối internet
- Lỗi permission: Sử dụng `pip install --user`
- Lỗi conflict: Tạo virtual environment mới

---

## 🚀 Startup Test

### Test 2: Run application
```bash
streamlit run Home.py
```

**Expected:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Common issues:**
- Port 8501 đã được sử dụng: `streamlit run Home.py --server.port 8502`
- Module not found: Kiểm tra lại dependencies
- Import errors: Đảm bảo đang ở đúng thư mục

---

## 📊 Functionality Tests

### Test 3: Home Page
- [ ] Trang Home load thành công
- [ ] Hiển thị thông tin Agent Ada
- [ ] Sidebar có các link đến các trang khác
- [ ] Timezone selector hoạt động

### Test 4: Trang 1 - Nhận định thị trường chung
- [ ] Thanh phiên giao dịch hiển thị
- [ ] Điểm nhấn qua đêm load được
- [ ] Bảng chỉ số cross-asset hiển thị
- [ ] Lịch kinh tế hiển thị
- [ ] Nút Copy hoạt động
- [ ] Risk sentiment metrics hiển thị

### Test 5: Trang 2 - Chi tiết theo thị trường
- [ ] 6 tabs hiển thị: US Equities, Vàng, FX, Crypto, Dầu, Chỉ số
- [ ] Tab US Equities: Top 10 table hiển thị
- [ ] Tab Vàng: Snapshot + trade plan hiển thị
- [ ] Chuyển đổi giữa các tabs mượt mà
- [ ] Nút Copy trong mỗi tab hoạt động

### Test 6: Trang 3 - Phụ lục dữ liệu
- [ ] Lịch kinh tế hiển thị
- [ ] Heatmap biến động render đúng màu
- [ ] Bảng kỹ thuật nhanh có dữ liệu
- [ ] Export CSV/JSON hoạt động
- [ ] Timezone selector hoạt động

---

## 🧩 Component Tests

### Test 7: Copy to Clipboard
1. Click vào nút "📋 Copy" bất kỳ
2. Kiểm tra message "✓ Đã copy!"
3. Paste (Ctrl+V) vào notepad
4. Xác nhận nội dung đúng

### Test 8: Data Refresh
1. Click "🔄 Làm mới dữ liệu" trong sidebar
2. Quan sát spinner loading
3. Dữ liệu cập nhật thành công

### Test 9: Session Badge
1. Kiểm tra thanh phiên giao dịch
2. Xác nhận có 5 phiên: Australia, Japan, Asia, London, New York
3. Trạng thái Open/Closed hiển thị đúng
4. Phiên active được highlight

---

## 📈 Data Tests

### Test 10: yfinance Data Fetch
Open Python console:
```python
import yfinance as yf
data = yf.download("^GSPC", period="1d")
print(data)
```

**Expected:** DataFrame với giá S&P 500

### Test 11: ATR Calculation
```python
from data_providers.market_details import fetch_ohlc, build_snapshot
df = fetch_ohlc("^GSPC", period="1mo")
snapshot = build_snapshot(df)
print(snapshot)
```

**Expected:** Dict với last, pct_d1, atr14, ma20, ma50

### Test 12: S&P 500 Tickers Fetch
```python
from data_providers.market_details import get_sp500_tickers
tickers = get_sp500_tickers()
print(f"Fetched {len(tickers)} tickers")
print(tickers[:10])
```

**Expected:** List ~500 tickers

---

## 🎨 UI/UX Tests

### Test 13: Responsive Layout
- [ ] Resize browser window
- [ ] Columns stack properly on mobile
- [ ] Sidebar collapsible
- [ ] Tables scroll horizontally if needed

### Test 14: Color & Styling
- [ ] Positive values: Green
- [ ] Negative values: Red
- [ ] Cards có background color
- [ ] Buttons có hover effect

---

## ⚡ Performance Tests

### Test 15: Load Time
- **Home:** < 2 seconds
- **Trang 1:** < 5 seconds (với cache)
- **Trang 2:** < 8 seconds (Top 10 tốn thời gian)
- **Trang 3:** < 5 seconds

### Test 16: Cache Behavior
1. Load Trang 1 lần đầu (slow)
2. Reload Trang 1 (fast - from cache)
3. Wait TTL expires
4. Reload Trang 1 (slow - refetch)

---

## 🔒 Security Tests

### Test 17: Secrets Handling
- [ ] `.streamlit/secrets.toml` không commit vào git
- [ ] `.streamlit/secrets.toml.example` có trong repo
- [ ] API keys (nếu có) không xuất hiện trong logs

---

## 📝 Test Results Template

```
DATE: ____________________
TESTER: __________________

✅ PASSED:
- [List passed tests]

❌ FAILED:
- [List failed tests with details]

⚠️ WARNINGS:
- [List any warnings or notes]

OVERALL: PASS / FAIL
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** `pip install -r requirements.txt`

### Issue 2: "Error fetching prices: HTTPError 404"
**Solution:** Ticker symbol không tồn tại hoặc yfinance bị rate limit. Đợi vài phút.

### Issue 3: Copy button không hoạt động
**Solution:** Kiểm tra browser có hỗ trợ Clipboard API không (cần HTTPS hoặc localhost)

### Issue 4: Dữ liệu không cập nhật
**Solution:** Click "🔄 Làm mới dữ liệu" hoặc clear cache: `st.cache_data.clear()`

### Issue 5: Heatmap không hiển thị màu
**Solution:** Kiểm tra styling CSS và pandas styling compatibility

---

## 📊 Performance Benchmarks

### Expected metrics:
- **Initial load:** 3-5 seconds
- **Page navigation:** < 1 second
- **Data fetch (cached):** < 100ms
- **Data fetch (fresh):** 2-5 seconds
- **Top 10 calculation:** 5-10 seconds (50 tickers sample)

---

## ✅ Final Verification

Trước khi deploy hoặc gửi cho user, đảm bảo:

- [x] Tất cả pages load thành công
- [x] Không có error messages
- [x] Copy functionality hoạt động
- [x] Export CSV/JSON hoạt động
- [x] Data hiển thị đúng format
- [x] README.md đầy đủ
- [x] requirements.txt chính xác
- [x] .gitignore đầy đủ

---

## 📞 Support

Nếu test fail, vui lòng:
1. Document lỗi chi tiết
2. Ghi lại error message
3. Screenshot (nếu có)
4. Liên hệ support team

---

**Happy Testing! 🎉**

Developed by Ken © 2025
