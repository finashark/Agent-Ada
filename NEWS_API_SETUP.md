# 🔑 Hướng dẫn cấu hình API Keys trên Streamlit Cloud

## ❗ Vấn đề: "Không thể tải tin tức" hoặc "AI Analysis không khả dụng"

Nếu bạn thấy warning này trên Streamlit Cloud, nghĩa là **secrets chưa được cấu hình**.

---

## ✅ Giải pháp: Thêm Secrets trên Streamlit Cloud

### Bước 1: Truy cập App Settings
1. Vào https://share.streamlit.io/
2. Chọn app **Agent Ada**
3. Click **Settings** (⚙️ icon) ở góc phải
4. Chọn **Secrets**

### Bước 2: Paste nội dung sau vào Secrets

```
[news]
newsapi_key = "ab2c6f479852474a87498b70d7d2b38e"
alphavantage_key = "YX8BR3SF06HM130H"
finnhub_key = "ciujme9r01qi3i2j92q0ciujme9r01qi3i2j92qg"

[gemini]
api_key = "AIzaSyBQUuZ8V5VycCBfg0XJ-U9bFszqxi_xmFY"
```

### Bước 3: Save và Restart
1. Click **Save**
2. App sẽ tự động restart
3. Đợi 30 giây
4. Refresh browser (F5)

---

## 🧪 Kiểm tra

Sau khi cấu hình xong:

1. Vào trang Home
2. Expand **"🔍 Debug: API Status"**
3. Phải thấy:
   ```
   Secrets available: True
   NewsAPI key: ✓ Present
   Alpha Vantage key: ✓ Present
   Finnhub key: ✓ Present
   Gemini key: ✓ Present
   ```

4. Tin tức sẽ load trong vòng 3-5 giây
5. Thấy message: **"✅ Đã tải X tin tức mới nhất..."**
6. **Trang 1 - Quan điểm đầu ngày:** Phải thấy "🤖 Ada đang phân tích thị trường với AI Gemini..." → Nhận định chi tiết bằng tiếng Việt

---

## 🔄 Nếu vẫn chưa load

1. Click button **"🔄 Xóa cache & tải lại tin tức"** trong sidebar
2. Hoặc clear browser cache và F5
3. Hoặc restart app từ Streamlit Cloud dashboard

---

## 📝 Lưu ý

- **Free tier limits:**
  - NewsAPI: 100 requests/day
  - Alpha Vantage: 25 requests/day
  - Finnhub: 60 calls/minute
  - Gemini AI: 60 requests/minute (free tier)

- **Cache:** Tin tức được cache 30 phút → Chỉ dùng ~48 requests/day
- **AI Analysis:** Cached 1 giờ, tự động regenerate khi có tin tức mới

- **Fallback:** 
  - Nếu NewsAPI hết quota, app tự động dùng Alpha Vantage hoặc Finnhub
  - Nếu Gemini unavailable, app dùng phân tích tự động dựa trên rules

---

## 🆘 Troubleshooting

### "Secrets available: False"
→ Chưa cấu hình secrets trên Streamlit Cloud. Làm theo Bước 1-3 ở trên.

### "Received 0 items"
→ API có thể bị rate limit. Đợi 1 giờ rồi thử lại.

### "HTTP 401 Unauthorized"
→ API key không hợp lệ. Check lại key trong secrets.

### "HTTP 429 Too Many Requests"
→ Vượt quota. Đợi 24h hoặc upgrade plan.

---

**Developed by Ken © 2025**
