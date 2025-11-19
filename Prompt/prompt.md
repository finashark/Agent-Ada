
# App Báo Cáo Thị Trường Hằng Ngày cho Môi Giới CFDs  
**Prompts & Snippets triển khai bằng Streamlit**  
Phiên bản: 2025-11-19 • Ngôn ngữ: Tiếng Việt

---

## Mục lục
1. [Giới thiệu nhanh & cấu trúc dự án](#gioi-thieu-nhanh--cau-truc-du-an)  
2. [Prompt 1 — Orchestrator (Hướng dẫn quy trình thực hiện app)](#prompt-1--orchestrator-huong-dan-quy-trinh-thuc-hien-app)  
3. [Prompt 2 — Trang 1: Nhận định thị trường chung](#prompt-2--trang-1-nhan-dinh-thi-truong-chung)  
4. [Prompt 3 — Trang 2: Thông tin chi tiết theo thị trường](#prompt-3--trang-2-thong-tin-chi-tiet-theo-thi-truong)  
5. [Prompt 4 — Trang 3: Phụ lục dữ liệu & bảng biểu (Quốc tế)](#prompt-4--trang-3-phu-luc-du-lieu--bang-bieu-quoc-te)  
6. [Snippets mẫu (components, providers, schemas, pages, requirements)](#snippets-mau-components-providers-schemas-pages-requirements)  

---

## Giới thiệu nhanh & cấu trúc dự án

Mục tiêu: tạo ứng dụng **Streamlit** đa trang, **tự động cập nhật theo từng phiên** (Úc, Nhật, Châu Á, London, Mỹ), hiển thị **khoa học khách quan**, gắn **timestamp** và **nút Copy** cho mọi mục lớn.

**Cấu trúc thư mục khuyến nghị**
```
your-app/
├─ streamlit_app.py  (hoặc Home.py)
├─ pages/
│  ├─ 1_Nhan_dinh_thi_truong_chung.py
│  ├─ 2_Chi_tiet_theo_thi_truong.py
│  └─ 3_Phu_luc_du_lieu.py
├─ components/
│  ├─ copy.py
│  ├─ timestamp.py
│  ├─ session_badge.py
│  └─ exporters.py
├─ data_providers/
│  ├─ overview.py
│  └─ market_details.py
├─ schemas.py
├─ styles.py
├─ requirements.txt
└─ .streamlit/
   └─ secrets.toml.example
```

---

## Prompt 1 — Orchestrator (Hướng dẫn quy trình thực hiện app)

**Sao chép toàn bộ đoạn dưới đây và dán vào Claude Sonnet:**

```
[ROLE] Bạn là kỹ sư–biên tập viên tài chính. Xây dựng ứng dụng Streamlit đa trang cho báo cáo thị trường hằng ngày, tự động cập nhật theo phiên (Úc, Nhật, Châu Á, London, Mỹ), hiển thị khoa học–khách quan, có timestamp và nút Copy tại mọi mục lớn.

[OUTPUT] Repo/Folder hoàn chỉnh gồm: Home.py (hoặc streamlit_app.py), pages/, data_providers/, components/, styles.py, editorial.py, schemas.py, requirements.txt, README.md, .streamlit/secrets.toml.example.

[SESSIONS] Định nghĩa 5 phiên (auto DST qua pytz): 
- Úc (Sydney) 08:00–16:00 địa phương
- Nhật (Tokyo) 09:00–15:00 địa phương
- Châu Á (Singapore/HK) 09:00–16:30 địa phương
- London 08:00–16:30 địa phương
- Mỹ (New York) 09:30–16:00 ET
Cơ chế: xác định phiên hiện tại, cấp TTL cache theo phiên (Open: 300s; Closed: 1800s) và auto-refresh với st_autorefresh khi phiên đang mở.

[OBJECTIVITY] Chuẩn hiển thị khoa học–khách quan (bắt buộc):
1) Mọi số liệu có mốc thời gian + múi giờ + nguồn. 
2) Tách Fact (sự kiện/thực tế) ↔ Interpretation (diễn giải). 
3) Dùng %D1/WTD/MTD, z-score khi hữu ích; ghi rõ lookback trên biểu đồ. 
4) “Yếu tố chi phối” kèm impact_sign (+/−/0) & confidence (Low/Med/High). 
5) Khung khuyến nghị chuẩn: Bias – Trigger – Invalidation – Timeframe – Rủi ro sự kiện. 
6) Tránh khẳng định tuyệt đối.
7) Hiển thị nguồn/URL ngay gần dữ liệu (nếu có).
8) Bảng Top 10 cổ phiếu: công thức xếp hạng minh bạch (z-score %D1, Vol/20D, news_flag).

[TIMESTAMP & COPY]
- Mọi mục lớn/tab hiển thị: “Cập nhật lần cuối: {{datetime}} ({{tz}}) | Phiên: {{session}}”.
- Có nút “Copy nội dung” cho từng phần và “Copy toàn trang”.

[DATA PROVIDERS]
- yfinance: giá/chỉ số/FX/crypto/commodities.
- Lịch kinh tế: Trading Economics / FMP (có key). Nếu không có key → form nhập tay + lưu JSON làm mock.
- Tất cả request có timeout, retry, cache TTL; khi lỗi → placeholder + hướng dẫn.

[SCHEMAS]
- MarketOverview {{date, highlights[], macro_briefs[], risk_sentiment{{vix,dxy,us10y}}, economic_calendar[], session, last_updated, objectivity_notes[]}}
- MarketDetail {{asset, snapshot{{last,%d1,range,atr,ma20,ma50}}, updates[], drivers[], trade_plan{{bias,levels,trigger,invalidation,timeframe}}, alternative_scenarios[], notes, impact_sign, confidence, last_updated}}
- EquityTop10 {{universe, method, items[], score_components}}

[UI PAGES]
- Trang 1: Nhận định thị trường chung (cards điểm nhấn; bảng chỉ số cross-asset; lịch kinh tế; dòng tiền & tâm lý; quan điểm đầu ngày).
- Trang 2: Thông tin chi tiết theo thị trường (Tabs: US Equities, Vàng, FX Majors, Crypto, Dầu, Chỉ số). 
- Trang 3: Phụ lục dữ liệu & bảng biểu (Quốc tế): lịch kinh tế chuẩn hóa; heatmap D1/WTD/MTD; bảng kỹ thuật nhanh; funding/OI crypto (nếu có).

[DEV RULES]
- Cache: st.cache_data/resource; TTL theo phiên; st_autorefresh khi phiên mở.
- Logging INFO cho mọi fetch (thời gian, TTL còn lại, cache hit/miss).
- README: hướng dẫn run local & deploy Streamlit Cloud; mock nếu thiếu key.
```

---

## Prompt 2 — Trang 1: Nhận định thị trường chung

**Sao chép toàn bộ đoạn dưới đây và dán vào Claude Sonnet:**

```
[GOAL] Tạo trang “Nhận định thị trường chung” (pages/1_Nhan_dinh_thi_truong_chung.py) với thanh phiên, timestamp, nút Copy, và các cards/bảng theo chuẩn khoa học–khách quan.

[FEATURES]
1) Thanh phiên (Úc, Nhật, Châu Á, London, Mỹ): badge trạng thái, phiên đang theo dõi; auto-refresh theo TTL của phiên.
2) Cards “Điểm nhấn qua đêm” (3–6 bullet): chia Fact vs Interpretation; mỗi card có timestamp + nút Copy.
3) Bảng chỉ số & tài sản chính (D1/WTD/MTD, z-score khi hữu ích):
   - ^GSPC, ^NDX hoặc QQQ, ^DJI, ^DXY, ^VIX, ^TNX (proxy US10Y), GC=F, CL=F, BTC-USD.
   - Mỗi bảng có timestamp, nguồn, nút Copy.
4) Lịch kinh tế hôm nay (UTC+7; cho phép đổi TZ): cột Giờ, Khu vực, Sự kiện, Ước tính, Trước đó, Ảnh hưởng, Link; Export CSV + Copy JSON.
5) Dòng tiền & tâm lý: VIX, DXY, US10Y với sparkline + objectivity_notes.
6) Quan điểm đầu ngày (2–4 bullet): Bias – Trigger – Invalidation – Timeframe – Rủi ro sự kiện; nút Copy Markdown.

[DATA] Dùng data_providers/overview.py (yfinance + API lịch kinh tế; fallback form nhập tay + JSON).

[EDIT] Khách quan, không dùng từ tuyệt đối; gắn mốc thời gian và nguồn cạnh số liệu.

[DELIVERABLES]
- pages/1_Nhan_dinh_thi_truong_chung.py
- data_providers/overview.py (hàm get_overview(date, tz) → MarketOverview)
- components: copy.py, timestamp.py, session_badge.py, exporters.py
```

---

## Prompt 3 — Trang 2: Thông tin chi tiết theo thị trường

**Sao chép toàn bộ đoạn dưới đây và dán vào Claude Sonnet:**

```
[GOAL] Tạo trang “Chi tiết theo thị trường” (pages/2_Chi_tiet_theo_thi_truong.py) với Tabs: US Equities, Vàng (XAUUSD), FX Majors, Crypto (large caps), Dầu (WTI/Brent), Chỉ số. Mỗi tab có timestamp + nút Copy (tab-level) và nút Copy từng phần A–E.

[STRUCT] Chuẩn A→E cho mỗi tab:
(A) Snapshot: Last, %D1, Range, ATR(14), MA20/50 (tính từ dữ liệu lịch sử), z-score (tuỳ).
(B) Cập nhật & Link: 2–5 headlines Fact + URL.
(C) Yếu tố chi phối: bullets có impact_sign (+/−/0) & confidence (Low/Med/High).
(D) Kế hoạch giao dịch (khách quan): Bias – Levels (R1/R2, S1/S2) – Trigger – Invalidation – Timeframe – Sự kiện rủi ro.
(E) Rủi ro & kịch bản thay thế: 1–3 bullet.

[US EQUITIES SPECIFIC]
- Bảng Top 10 mã quan tâm (Ticker | Last | %d/d | Vol/20D | Catalyst/Link | Ý tưởng | score_components); nút Copy Top10 (Markdown list).
- Universe: S&P 500 (load từ Wikipedia, cache 24h).
- Xếp hạng: rank = zscore(%d/d) + zscore(Vol/20D ratio) + news_flag.

[OTHER TABS]
- Vàng: GC=F + ^DXY + ^TNX; hiển thị chỉ báo phụ kèm impact_sign.
- FX Majors: EURUSD=X, GBPUSD=X, USDJPY=X, AUDUSD=X, USDCAD=X, USDCHF=X, ^DXY.
- Crypto: BTC-USD, ETH-USD, SOL-USD, BNB-USD (ẩn nếu không có), XRP-USD, ADA-USD.
- Dầu: CL=F, BZ=F; tồn kho API nếu có, không thì ẩn + chú thích.
- Chỉ số: ^GSPC, ^NDX/QQQ, ^DJI, ^GDAXI, ^FTSE, ^N225, ^HSI, ^STOXX50E; trạng thái trên/dưới MA20/50.

[DATA] data_providers/market_details.py (tính ATR(14), MA20/50). TTL theo phiên; autorefresh khi phiên mở.

[EDIT] Tách Fact vs Interpretation; hiển thị nguồn; không khẳng định tuyệt đối.

[DELIVERABLES]
- pages/2_Chi_tiet_theo_thi_truong.py
- data_providers/market_details.py
- components/ (copy, timestamp, session badges)
```

---

## Prompt 4 — Trang 3: Phụ lục dữ liệu & bảng biểu (Quốc tế)

**Sao chép toàn bộ đoạn dưới đây và dán vào Claude Sonnet:**

```
[GOAL] Tạo trang “Phụ lục dữ liệu & bảng biểu (Quốc tế)” (pages/3_Phu_luc_du_lieu.py). Không bao gồm nội dung riêng Việt Nam.

[MODULES]
1) Lịch kinh tế (UTC+7, đổi TZ được): bảng chuẩn; Export CSV/JSON; Copy.
2) Heatmap biến động cross-asset (D1/WTD/MTD): ghi lookback + nguồn + timestamp; Copy.
3) Bảng kỹ thuật nhanh: Last, %D1, Range, ATR(14), MA20, MA50; Copy.
4) (Tuỳ) Crypto funding/OI: nếu không có API → ẩn + chú thích.
5) Nguồn & versioning: giờ cập nhật, danh sách providers, phiên hiện tại; Copy toàn trang.

[DATA/UI] Dùng components/timestamp.py, components/copy.py, exporters.py. TTL theo phiên; autorefresh khi phiên mở.

[EDIT] Mọi bảng/đồ thị có mốc thời gian, múi giờ, nguồn; làm tròn số nhất quán.

[DELIVERABLES]
- pages/3_Phu_luc_du_lieu.py
- cập nhật schemas.py nếu cần
```

---

## Snippets mẫu (components, providers, schemas, pages, requirements)

> **Lưu ý:** Đây là mẫu rút gọn để khởi tạo nhanh. Tuỳ dự án, bạn cần bổ sung xử lý ngoại lệ, logging chi tiết, và hoàn thiện giao diện.

### `components/copy.py`
```python
import streamlit as st

def copy_to_clipboard(text: str, label: str = "Copy"):
    # Dùng components.html để gọi navigator.clipboard
    safe_text = text.replace("`", "\`").replace("\n", "\\n")
    html = f"""
    <button onclick="navigator.clipboard.writeText(`{safe_text}`)"
            style="padding:6px 10px;border:1px solid #ddd;border-radius:6px;cursor:pointer;">
        {label}
    </button>
    """
    st.components.v1.html(html, height=40)

def copy_section(title: str, text: str):
    st.markdown(f"### {title}")
    st.text_area("Nội dung", text, height=150, key=f"ta_{title}", label_visibility="collapsed")
    copy_to_clipboard(text, label="Copy nội dung")

def copy_page(assembled_text: str):
    st.markdown("## Copy toàn trang")
    copy_to_clipboard(assembled_text, label="Copy toàn trang")
```

### `components/timestamp.py`
```python
from datetime import datetime
import pytz
import streamlit as st

def render_timestamp(last_updated: datetime, tz_name: str, session_name: str):
    tz = pytz.timezone(tz_name)
    local_dt = last_updated.astimezone(tz)
    st.caption(f"Cập nhật lần cuối: {local_dt.strftime('%Y-%m-%d %H:%M:%S')} ({tz_name}) | Phiên: {session_name}")
```

### `components/session_badge.py`
```python
from datetime import datetime, time
import pytz
import streamlit as st

SESSIONS = [
    {"name": "Australia", "city": "Australia/Sydney", "open": time(8,0), "close": time(16,0)},
    {"name": "Japan", "city": "Asia/Tokyo", "open": time(9,0), "close": time(15,0)},
    {"name": "Asia", "city": "Asia/Singapore", "open": time(9,0), "close": time(16,30)},
    {"name": "London", "city": "Europe/London", "open": time(8,0), "close": time(16,30)},
    {"name": "New York", "city": "America/New_York", "open": time(9,30), "close": time(16,0)},
]

def session_status(now_utc: datetime):
    badges = []
    active = None
    for s in SESSIONS:
        tz = pytz.timezone(s["city"])
        local_now = now_utc.astimezone(tz)
        open_dt = local_now.replace(hour=s["open"].hour, minute=s["open"].minute, second=0, microsecond=0)
        close_dt = local_now.replace(hour=s["close"].hour, minute=s["close"].minute, second=0, microsecond=0)
        is_open = open_dt <= local_now <= close_dt
        status = "Open" if is_open else "Closed"
        badges.append(f"{s['name']}: {status}")
        if is_open:
            active = s["name"]
    return badges, active or "Asia"

def session_ttl(is_open: bool) -> int:
    return 300 if is_open else 1800

def render_session_bar(now_utc: datetime):
    badges, active = session_status(now_utc)
    st.markdown(" | ".join([f"**{b}**" for b in badges]))
    return active
```

### `schemas.py` (Pydantic mẫu)
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class CalendarItem(BaseModel):
    time_local: str
    region: str
    event: str
    consensus: Optional[float] = None
    prior: Optional[float] = None
    impact: Optional[str] = None
    source_url: Optional[str] = None

class MarketOverview(BaseModel):
    date: str
    highlights: List[str] = []
    macro_briefs: List[str] = []
    risk_sentiment: Dict[str, float] = {}
    economic_calendar: List[CalendarItem] = []
    session: str
    last_updated: str
    objectivity_notes: List[str] = []

class TradePlan(BaseModel):
    bias: str
    levels: Dict[str, float] = {}
    trigger: str
    invalidation: str
    timeframe: str

class MarketDetail(BaseModel):
    asset: str
    snapshot: Dict[str, float] = {}
    updates: List[Dict] = []
    drivers: List[str] = []
    trade_plan: TradePlan
    alternative_scenarios: List[str] = []
    notes: Optional[str] = None
    impact_sign: Optional[str] = None   # "+", "-", "0"
    confidence: Optional[str] = None    # "Low","Medium","High"
    last_updated: str

class EquityTop10(BaseModel):
    universe: str
    method: str
    items: List[Dict] = []
    score_components: Dict[str, float] = {}
```

### `data_providers/overview.py` (rút gọn)
```python
import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
import streamlit as st
from schemas import MarketOverview, CalendarItem
from components.session_badge import session_status, session_ttl

ASSETS = ["^GSPC","^NDX","^DJI","^DXY","^VIX","^TNX","GC=F","CL=F","BTC-USD"]

@st.cache_data(ttl=600, show_spinner=False)
def fetch_prices(tickers):
    data = yf.download(tickers=tickers, period="1mo", interval="1d", auto_adjust=False, progress=False, threads=True)
    if isinstance(data.columns, pd.MultiIndex):
        data = data["Close"]
    return data

def pct_change_period(df, days: int):
    if len(df) <= days+1:
        return (df.iloc[-1] / df.iloc[0] - 1.0) * 100.0
    return (df.iloc[-1] / df.iloc[-(days+1)] - 1.0) * 100.0

def build_overview(tz_name="Asia/Ho_Chi_Minh"):
    now_utc = datetime.now(timezone.utc)
    badges, active = session_status(now_utc)

    px = fetch_prices(ASSETS)
    latest = px.iloc[-1]
    d1 = (px.iloc[-1] / px.iloc[-2] - 1) * 100
    wtd = pct_change_period(px, 5)
    mtd = pct_change_period(px, 22)

    risk = {"vix": float(latest.get("^VIX", float("nan"))),
            "dxy": float(latest.get("^DXY", float("nan"))),
            "us10y": float(latest.get("^TNX", float("nan")))}

    cal = [CalendarItem(time_local="20:30", region="US", event="CPI (YoY)",
                        consensus=None, prior=None, impact="High", source_url=None)]

    ov = MarketOverview(
        date=now_utc.date().isoformat(),
        highlights=["(Fact) SPX biến động ...", "(Interpretation) Tâm lý ..."],
        macro_briefs=["Fed speakers ...", "PMI ..."],
        risk_sentiment=risk,
        economic_calendar=cal,
        session=active,
        last_updated=now_utc.isoformat(),
        objectivity_notes=["Tách Fact vs Interpretation", "Hiển thị nguồn & mốc thời gian"]
    )
    return ov
```

### `data_providers/market_details.py` (rút gọn + ATR/MA)
```python
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import streamlit as st
from schemas import MarketDetail, TradePlan

def atr14(high, low, close):
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(14).mean()

@st.cache_data(ttl=600, show_spinner=False)
def fetch_ohlc(ticker, period="6mo", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
    return df

def build_detail(asset):
    df = fetch_ohlc(asset, period="6mo", interval="1d")
    last = float(df["Close"].iloc[-1])
    d1 = (df["Close"].iloc[-1] / df["Close"].iloc[-2] - 1) * 100
    rng = f"({float(df['Low'].iloc[-1]):.2f}–{float(df['High'].iloc[-1]):.2f})"
    atr = float(atr14(df["High"], df["Low"], df["Close"]).iloc[-1])
    ma20 = float(df["Close"].rolling(20).mean().iloc[-1])
    ma50 = float(df["Close"].rolling(50).mean().iloc[-1])

    snapshot = {"last":last, "%d1":float(d1), "range":rng, "atr":atr, "ma20":ma20, "ma50":ma50}
    trade = TradePlan(bias="Neutral", levels={"R1":None,"R2":None,"S1":None,"S2":None},
                      trigger="Đóng nến H1 vượt ...", invalidation="Thủng ...", timeframe="H1")

    md = MarketDetail(
        asset=asset,
        snapshot=snapshot,
        updates=[{"title":"Earnings/catalyst ...","url":""}],
        drivers=["DXY +", "Real yields 0"],
        trade_plan=trade,
        alternative_scenarios=["Nếu ... thì ..."],
        notes=None,
        impact_sign="0",
        confidence="Medium",
        last_updated=datetime.now(timezone.utc).isoformat()
    )
    return md
```

### `pages/1_Nhan_dinh_thi_truong_chung.py` (khung tối thiểu)
```python
import streamlit as st
from datetime import datetime, timezone
from components.session_badge import render_session_bar
from components.timestamp import render_timestamp
from components.copy import copy_page, copy_section
from data_providers.overview import build_overview

st.set_page_config(page_title="Nhận định thị trường chung", layout="wide")
now_utc = datetime.now(timezone.utc)

session_name = render_session_bar(now_utc)
ov = build_overview()

col1, col2 = st.columns([3,2])
with col1:
    st.subheader("Điểm nhấn qua đêm")
    render_timestamp(datetime.fromisoformat(ov.last_updated), "Asia/Ho_Chi_Minh", ov.session)
    fact = "\n".join([f"- {h}" for h in ov.highlights])
    copy_section("Điểm nhấn qua đêm", fact)

with col2:
    st.subheader("Dòng tiền & Tâm lý")
    render_timestamp(datetime.fromisoformat(ov.last_updated), "Asia/Ho_Chi_Minh", ov.session)
    st.write(ov.risk_sentiment)
    copy_section("Dòng tiền & Tâm lý", str(ov.risk_sentiment))

st.subheader("Lịch kinh tế hôm nay")
render_timestamp(datetime.fromisoformat(ov.last_updated), "Asia/Ho_Chi_Minh", ov.session)
st.table([i.dict() for i in ov.economic_calendar])
copy_section("Lịch kinh tế", str([i.dict() for i in ov.economic_calendar]))
```

### `pages/2_Chi_tiet_theo_thi_truong.py` (khung tối thiểu)
```python
import streamlit as st
from datetime import datetime, timezone
from components.timestamp import render_timestamp
from components.copy import copy_section
from data_providers.market_details import build_detail

st.set_page_config(page_title="Chi tiết theo thị trường", layout="wide")

tabs = st.tabs(["US Equities","Vàng","FX Majors","Crypto","Dầu","Chỉ số"])

with tabs[1]:
    st.subheader("Vàng (XAUUSD)")
    md = build_detail("GC=F")
    render_timestamp(datetime.fromisoformat(md.last_updated), "Asia/Ho_Chi_Minh", "Asia")
    st.write("Snapshot:", md.snapshot)
    copy_section("Vàng - Snapshot", str(md.snapshot))
    st.write("Drivers:", md.drivers)
    copy_section("Vàng - Drivers", "\n".join(md.drivers))
    st.write("Trade plan:", md.trade_plan.dict())
    copy_section("Vàng - Trade plan", str(md.trade_plan.dict()))
```

### `pages/3_Phu_luc_du_lieu.py` (khung tối thiểu)
```python
import streamlit as st
from datetime import datetime, timezone
from components.timestamp import render_timestamp
from components.copy import copy_section, copy_page

st.set_page_config(page_title="Phụ lục dữ liệu & bảng biểu (Quốc tế)", layout="wide")

now = datetime.now(timezone.utc)
render_timestamp(now, "Asia/Ho_Chi_Minh", "Asia")

st.subheader("Heatmap biến động (D1/WTD/MTD)")
# TODO: tính toán & hiển thị heatmap
copy_section("Heatmap", "Bảng heatmap (Markdown/CSV)")

st.subheader("Bảng kỹ thuật nhanh")
# TODO: fetch dữ liệu & tính ATR/MA
copy_section("Bảng kỹ thuật", "Danh sách tài sản + ATR/MA")

copy_page("Heatmap...\n\nBảng kỹ thuật...")
```

### `styles.py` (gợi ý cực ngắn)
```python
def fmt_percent(x: float) -> str:
    return f"{x:.2f} %"

def fmt_price(x: float) -> str:
    return f"{x:,.2f}"
```

### `requirements.txt` (tham khảo)
```
streamlit>=1.35
yfinance>=0.2.40
pandas>=2.2
numpy>=1.26
pydantic>=2.6
pytz>=2024.1
requests>=2.32
```

---

## Ghi chú sử dụng
- Dán **Prompt 1 → 2 → 3 → 4** theo thứ tự vào Claude Sonnet để sinh code.  
- Thay khóa API cho lịch kinh tế (nếu dùng Trading Economics/FMP). Nếu không có, dùng **mock**/nhập tay.  
- Kiểm thử chức năng **Copy** và **Timestamp** tại mọi mục lớn trước khi triển khai.
