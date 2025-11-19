# 🆕 Cập nhật: Crypto Funding Rate & Open Interest

**Ngày cập nhật:** 2025-11-19  
**Version:** 1.1.0

---

## ✨ Tính năng mới

Đã tích hợp module **Crypto Funding Rate & Open Interest** vào **Trang 3: Phụ lục dữ liệu**.

### 📊 Dữ liệu cung cấp:

#### 1. **Funding Rate (Lãi suất tài trợ)**
- Funding rate hiện tại cho BTC và ETH
- Dữ liệu từ 3 sàn chính: Binance, Bybit, OKX
- Tính toán annual rate (365 days × 3 funding/day)
- Phân tích sentiment (Longs trả / Shorts trả)

#### 2. **Open Interest (Vị thế mở)**
- Open Interest snapshot cho BTC và ETH
- Dữ liệu từ Binance, Bybit, OKX
- Giá trị USD (nếu có)
- Giải thích ý nghĩa OI trong các tình huống

---

## 🔧 Triển khai kỹ thuật

### Module sử dụng: `derivatives_wrappers.py`

**Đặc điểm:**
- ✅ **Miễn phí 100%** - Sử dụng public APIs của các sàn
- ✅ **Không cần API key** - Chỉ cần cho một số endpoint nâng cao
- ✅ **Low latency** - Gọi trực tiếp REST API native
- ✅ **Retry logic** - Tự động retry khi gặp lỗi
- ✅ **Normalized data** - Dữ liệu được chuẩn hóa qua các sàn

### Các sàn hỗ trợ:

1. **Binance USDⓈ-M Futures**
   - Funding history & latest
   - Open Interest snapshot & history
   - Base: https://fapi.binance.com

2. **Bybit v5**
   - Funding history & latest (linear/inverse)
   - Open Interest with intervals
   - Base: https://api.bybit.com

3. **OKX v5**
   - Current funding rate
   - Open Interest snapshot
   - Base: https://www.okx.com

4. **Deribit v2** (Optional)
   - Funding history (BTC-PERPETUAL)
   - Open Interest from ticker
   - Base: https://www.deribit.com

---

## 📍 Vị trí trong ứng dụng

**Trang 3: Phụ lục dữ liệu → Module 4**

```
Phụ lục dữ liệu
├─ Module 1: Lịch kinh tế
├─ Module 2: Heatmap biến động
├─ Module 3: Bảng kỹ thuật
├─ Module 4: Crypto Funding & OI  ← MỚI
└─ Module 5: Nguồn & versioning
```

---

## 💡 Cách sử dụng

### Trong ứng dụng:

1. Chạy ứng dụng: `streamlit run Home.py`
2. Điều hướng đến **Trang 3: Phụ lục dữ liệu**
3. Cuộn xuống **Module 4: Crypto Funding Rate & Open Interest**
4. Xem 2 tabs:
   - **📈 Funding Rate:** Lãi suất tài trợ hiện tại
   - **📊 Open Interest:** Vị thế mở hiện tại

### Sử dụng module trực tiếp:

```python
from data_providers.derivatives_wrappers import DerivsClient

# Khởi tạo client
client = DerivsClient()

# Lấy funding rate
funding = client.funding_latest("binance", "BTCUSDT")
print(f"Rate: {funding.rate * 100}%")

# Lấy open interest
oi = client.oi_snapshot("binance", "BTCUSDT")
print(f"OI: {oi.open_interest:,.0f}")
```

---

## 📊 Giải thích chỉ số

### Funding Rate

**Là gì?**
- Phí định kỳ được trao đổi giữa traders long và short
- Thanh toán mỗi 8 giờ (3 lần/ngày)

**Ý nghĩa:**
- **Funding > 0 (dương):** Long positions trả cho Short positions
  → Market sentiment Bullish (nhiều người long)
  
- **Funding < 0 (âm):** Short positions trả cho Long positions
  → Market sentiment Bearish (nhiều người short)
  
- **Funding ≈ 0:** Market balanced, neutral

**Ngưỡng quan trọng:**
- `> 0.05%`: Rất bullish (cảnh báo overheated)
- `0.01% - 0.05%`: Bullish bình thường
- `-0.01% - 0.01%`: Neutral
- `-0.05% - -0.01%`: Bearish bình thường
- `< -0.05%`: Rất bearish (cảnh báo oversold)

### Open Interest (OI)

**Là gì?**
- Tổng số hợp đồng futures đang mở (chưa đóng)
- Đo lường tính thanh khoản và sự quan tâm của thị trường

**Phân tích kết hợp giá:**

| OI | Price | Ý nghĩa |
|----|-------|---------|
| ↑ | ↑ | 🟢 Bullish - Tiền mới vào, xu hướng tăng mạnh |
| ↑ | ↓ | 🔴 Bearish - Short positions mới mở |
| ↓ | ↑ | 🟡 Short covering - Đóng short, uptrend yếu |
| ↓ | ↓ | 🟡 Long liquidation - Đóng long, downtrend yếu |

---

## ⚠️ Lưu ý

1. **Rate Limits**
   - Các sàn có giới hạn số request/phút
   - Nếu gặp lỗi, đợi vài giây rồi thử lại

2. **API Keys** (Optional)
   - Không bắt buộc cho public endpoints
   - Cần thiết cho historical data trên một số sàn
   - Cấu hình trong `.streamlit/secrets.toml` nếu cần

3. **Data Accuracy**
   - Dữ liệu từ public APIs, có thể có độ trễ nhỏ
   - Luôn cross-check với nhiều nguồn
   - Chỉ mang tính tham khảo

---

## 🔄 Cache Strategy

Module sử dụng Streamlit caching:
- TTL theo phiên (300s khi mở / 1800s khi đóng)
- Auto-refresh khi có request mới sau TTL expire
- Cache key dựa trên exchange + symbol

---

## 🚀 Roadmap

### Phase 2:
- [ ] Thêm nhiều crypto pairs (SOL, BNB, XRP, ADA)
- [ ] Historical chart cho Funding Rate
- [ ] Historical chart cho Open Interest
- [ ] Tính toán correlation giữa Funding & Price
- [ ] Alert khi Funding Rate vượt ngưỡng

### Phase 3:
- [ ] WebSocket real-time updates
- [ ] Funding Rate arbitrage detector
- [ ] OI Delta (thay đổi OI theo thời gian)
- [ ] Liquidation heatmap

---

## 📚 Tài liệu tham khảo

- [Binance Futures API](https://binance-docs.github.io/apidocs/futures/en/)
- [Bybit v5 API](https://bybit-exchange.github.io/docs/v5/intro)
- [OKX v5 API](https://www.okx.com/docs-v5/en/)
- [Deribit v2 API](https://docs.deribit.com/)

---

**Developed by Ken © 2025**

Nâng cấp từ v1.0.0 → v1.1.0 với tính năng Crypto Derivatives tracking! 🚀
