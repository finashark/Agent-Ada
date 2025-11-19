
# DERIVS_WRAPPERS — Free native exchange wrappers (Funding & OI)

**Mục tiêu:** Miễn phí, độ trễ thấp, gọi thẳng **API gốc** của sàn (Binance, Bybit, OKX, Deribit) để lấy **Funding Rate** & **Open Interest** cho perpetuals.

## Cài đặt nhanh

```bash
pip install requests
```

Sao chép file `derivatives_wrappers.py` vào dự án của bạn (ví dụ `data_providers/derivatives_wrappers.py`).

## Ví dụ sử dụng

```python
from derivatives_wrappers import DerivsClient

c = DerivsClient()  # hoặc DerivsClient(binance_api_key="...") nếu cần cho một số endpoint

# --- Funding latest ---
print(c.funding_latest("binance", "BTCUSDT"))
print(c.funding_latest("bybit", "BTCUSDT"))
print(c.funding_latest("okx", "BTCUSDT"))
print(c.funding_latest("deribit", "BTCUSDT"))  # map sang BTC-PERPETUAL

# --- Funding history ---
hist = c.funding_history("binance", "BTCUSDT", limit=1000)
print("Funding points:", len(hist))

# --- Open interest snapshot ---
print(c.oi_snapshot("binance", "BTCUSDT"))
print(c.oi_snapshot("bybit", "BTCUSDT"))
print(c.oi_snapshot("okx", "BTCUSDT"))
print(c.oi_snapshot("deribit", "BTCUSDT"))

# --- Open interest history (where supported) ---
binance_oi = c.oi_history("binance", "BTCUSDT", period="1h", limit=200)
bybit_oi   = c.oi_history("bybit", "BTCUSDT", interval="1h", limit=200)
```

## Chuẩn hoá symbols

- **OKX** yêu cầu `BTC-USDT-SWAP`. Wrapper đã tự chuyển đổi từ `BTCUSDT` → `BTC-USDT-SWAP`.
- **Deribit** perpetual là `BTC-PERPETUAL`. Wrapper đã tự map.

## Lưu ý & hạn chế

- **Binance**: endpoint `/futures/data/openInterestHist` có thể yêu cầu header `X-MBX-APIKEY` (tùy thời điểm). Nếu gặp 4xx, cung cấp API key trong `DerivsClient(binance_api_key="...")`.
- **OKX**: REST public cung cấp funding **hiện tại** và OI **snapshot**. Dữ liệu **lịch sử** có thể cần kênh WS hoặc endpoint khác (không bắt buộc cho báo cáo nhanh).
- **Deribit**: Funding history có sẵn; OI **snapshot** qua `public/ticker`.

## Tích hợp vào Streamlit

- Gọi các hàm wrapper trong `st.cache_data(ttl=...)` theo TTL **theo phiên** như bạn đã định nghĩa.
- Hiển thị **timestamp** (`ts`) theo múi giờ người dùng và gắn **nút Copy** cho từng block dữ liệu.
