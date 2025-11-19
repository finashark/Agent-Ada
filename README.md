# Agent Ada - Báo Cáo Thị Trường Hằng Ngày

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.35%2B-red.svg)

Ứng dụng Streamlit chuyên nghiệp cho báo cáo thị trường tài chính hằng ngày, được phát triển cho môi giới CFDs tại sàn HFM.

## 🎯 Tính năng chính

### 📋 Trang 1: Nhận định thị trường chung
- Điểm nhấn qua đêm (Fact vs Interpretation)
- Bảng chỉ số cross-asset (D1/WTD/MTD + z-score)
- Lịch kinh tế với múi giờ tùy chỉnh
- Dòng tiền & tâm lý rủi ro (VIX, DXY, US10Y)
- Quan điểm đầu ngày (Bias - Trigger - Invalidation)

### 📊 Trang 2: Chi tiết theo thị trường
- **US Equities**: Top 10 cổ phiếu với ranking score
- **Vàng (XAUUSD)**: Snapshot + drivers + trade plan
- **FX Majors**: 6 cặp tiền tệ chính
- **Crypto**: BTC, ETH, SOL, BNB, XRP, ADA
- **Dầu**: WTI & Brent crude
- **Chỉ số toàn cầu**: S&P 500, Nasdaq, Dow Jones, DAX, FTSE, Nikkei, Hang Seng, Euro Stoxx

### 📈 Trang 3: Phụ lục dữ liệu
- Lịch kinh tế chuẩn hóa
- Heatmap biến động (D1/WTD/MTD)
- Bảng kỹ thuật nhanh (ATR, MA20, MA50)
- **Crypto Funding Rate & Open Interest** (Binance, Bybit, OKX, Deribit)
- Export CSV/JSON

## 🚀 Cài đặt & Chạy

### Yêu cầu hệ thống
- Python 3.8 trở lên
- pip hoặc conda

### Bước 1: Clone hoặc tải về project
```bash
git clone <repository-url>
cd "Agent Ada"
```

### Bước 2: Tạo môi trường ảo (khuyến nghị)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình (tuỳ chọn)
```bash
# Copy file secrets example
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Chỉnh sửa secrets.toml và thêm API keys nếu có
```

### Bước 5: Chạy ứng dụng
```bash
streamlit run Home.py
```

Ứng dụng sẽ mở tại: `http://localhost:8501`

## 📁 Cấu trúc dự án

```
Agent Ada/
├── Home.py                          # Trang chủ
├── pages/
│   ├── 1_Nhan_dinh_thi_truong_chung.py
│   ├── 2_Chi_tiet_theo_thi_truong.py
│   └── 3_Phu_luc_du_lieu.py
├── components/
│   ├── __init__.py
│   ├── copy.py                      # Copy to clipboard
│   ├── timestamp.py                 # Timestamp với timezone
│   ├── session_badge.py             # Phiên giao dịch
│   └── exporters.py                 # Export CSV/JSON
├── data_providers/
│   ├── __init__.py
│   ├── overview.py                  # Data cho Trang 1
│   └── market_details.py            # Data cho Trang 2
├── schemas.py                       # Pydantic models
├── styles.py                        # Formatting utilities
├── requirements.txt
├── README.md
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
└── Prompt/
    └── prompt.md                    # Tài liệu yêu cầu gốc
```

## 🔧 Cấu hình

### Múi giờ
Thay đổi múi giờ mặc định trong sidebar hoặc `.streamlit/secrets.toml`:
```toml
[settings]
default_timezone = "Asia/Ho_Chi_Minh"
```

### API Keys (Tuỳ chọn)
Để sử dụng đầy đủ tính năng lịch kinh tế và tin tức, thêm API keys vào `.streamlit/secrets.toml`:
- Trading Economics: https://tradingeconomics.com/api
- Financial Modeling Prep: https://financialmodelingprep.com/
- News API: https://newsapi.org/

### Auto-refresh
Tự động làm mới dữ liệu khi phiên giao dịch đang mở:
- Phiên mở: TTL = 5 phút (300s)
- Phiên đóng: TTL = 30 phút (1800s)

## 📊 Nguồn dữ liệu

- **Giá & Chỉ số**: yfinance (Yahoo Finance)
- **Lịch kinh tế**: Mock data (có thể tích hợp API)
- **S&P 500 tickers**: Wikipedia
- **Crypto**: Yahoo Finance
- **Crypto Funding & OI**: Native exchange APIs (Binance, Bybit, OKX, Deribit) - Miễn phí
- **Technical indicators**: Tính toán trực tiếp từ OHLC data

## 🎓 Nguyên tắc hoạt động

### Khoa học & Khách quan
- ✓ Tách rõ **Fact** (sự kiện/số liệu) và **Interpretation** (diễn giải)
- ✓ Hiển thị nguồn dữ liệu ngay cạnh số liệu
- ✓ Sử dụng z-score, percentile khi phù hợp
- ✓ Tránh khẳng định tuyệt đối

### Phiên giao dịch
Theo dõi 5 phiên chính:
- 🇦🇺 Australia (Sydney): 08:00-16:00
- 🇯🇵 Japan (Tokyo): 09:00-15:00
- 🌏 Asia (Singapore/HK): 09:00-16:30
- 🇬🇧 London: 08:00-16:30
- 🇺🇸 New York: 09:30-16:00 ET

### Trade Plan Framework
Mỗi asset có khung phân tích chuẩn:
- **Bias**: Xu hướng (Bullish/Bearish/Neutral)
- **Levels**: R1/R2 (resistance), S1/S2 (support)
- **Trigger**: Điều kiện vào lệnh
- **Invalidation**: Điều kiện huỷ kịch bản
- **Timeframe**: Khung thời gian
- **Risk Events**: Sự kiện rủi ro

## 🔍 Chỉ số kỹ thuật

- **ATR(14)**: Average True Range - đo biến động
- **MA20/MA50**: Moving Average 20/50 ngày
- **Z-score**: Số độ lệch chuẩn so với trung bình (window=20)
- **Vol Ratio**: Volume / 20-day average

## 📤 Export & Copy

- Nút **Copy** cho mọi section lớn
- Export **CSV** cho bảng dữ liệu
- Export **JSON** cho toàn bộ dữ liệu
- Copy **toàn trang** ở cuối mỗi trang

## 🚢 Deploy lên Streamlit Cloud

### Bước 1: Push code lên GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### Bước 2: Deploy
1. Truy cập https://share.streamlit.io/
2. Đăng nhập với GitHub
3. Chọn repository và branch
4. Main file path: `Home.py`
5. Click "Deploy"

### Bước 3: Thêm secrets (nếu có)
Trong Streamlit Cloud dashboard, thêm secrets vào "Settings" > "Secrets"

## ⚠️ Lưu ý quan trọng

- **Dữ liệu chỉ mang tính tham khảo**, không phải lời khuyên đầu tư
- **Không có liability** về quyết định đầu tư dựa trên dữ liệu này
- **Kiểm tra kỹ** dữ liệu trước khi gửi cho khách hàng
- **Mock data** được sử dụng cho lịch kinh tế (cần API key cho dữ liệu thực)

## 🛠️ Troubleshooting

### Lỗi khi tải dữ liệu từ yfinance
```python
# Xóa cache và thử lại
st.cache_data.clear()
```

### Lỗi timezone
```python
# Đảm bảo pytz được cài đặt
pip install pytz --upgrade
```

### Lỗi khi fetch S&P 500 tickers
```python
# Cài thêm lxml và html5lib
pip install lxml html5lib beautifulsoup4
```

## 📝 Changelog

### v1.0.0 (2025-11-19)
- ✨ Phát hành phiên bản đầu tiên
- 📋 Trang 1: Nhận định thị trường chung
- 📊 Trang 2: Chi tiết 6 asset classes
- 📈 Trang 3: Phụ lục dữ liệu
- 🎯 Tích hợp 5 phiên giao dịch
- 📋 Copy & Export functionality
- 🔄 Auto-refresh theo phiên

## 👨‍💻 Tác giả

**Agent Ada** - Chuyên gia tài chính chứng khoán
- Được phát triển cho sàn HFM
- Hỗ trợ nhân viên môi giới

## 📄 License

Dự án này được phát triển cho mục đích nội bộ tại sàn HFM.

## 🤝 Đóng góp

Nếu bạn muốn đóng góp:
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần Troubleshooting
2. Xem logs trong terminal
3. Tạo Issue trên GitHub (nếu có)

---

**© 2025 Agent Ada | Developed for HFM**
