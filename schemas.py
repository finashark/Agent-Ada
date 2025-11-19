"""
Schemas cho ứng dụng báo cáo thị trường
Định nghĩa các models Pydantic để đảm bảo tính nhất quán dữ liệu
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class CalendarItem(BaseModel):
    """Item trong lịch kinh tế"""
    time_local: str
    region: str
    event: str
    consensus: Optional[float] = None
    prior: Optional[float] = None
    actual: Optional[float] = None
    impact: Optional[str] = None  # "High", "Medium", "Low"
    source_url: Optional[str] = None


class RiskSentiment(BaseModel):
    """Chỉ số tâm lý rủi ro thị trường"""
    vix: float
    dxy: float
    us10y: float
    last_updated: str


class MarketOverview(BaseModel):
    """Tổng quan thị trường cho Trang 1"""
    date: str
    highlights: List[str] = Field(default_factory=list, description="Điểm nhấn qua đêm")
    macro_briefs: List[str] = Field(default_factory=list, description="Tóm tắt vĩ mô")
    risk_sentiment: Dict[str, float] = Field(default_factory=dict)
    market_snapshot: Dict[str, Dict[str, float]] = Field(default_factory=dict, description="Snapshot thị trường cho AI analysis")
    economic_calendar: List[CalendarItem] = Field(default_factory=list)
    session: str = Field(description="Phiên đang theo dõi")
    last_updated: str
    objectivity_notes: List[str] = Field(default_factory=list)
    money_flow: Optional[str] = None
    market_view: Optional[str] = None


class TradePlan(BaseModel):
    """Kế hoạch giao dịch theo chuẩn khách quan"""
    bias: str = Field(description="Xu hướng: Bullish/Bearish/Neutral")
    levels: Dict[str, Optional[float]] = Field(
        default_factory=dict,
        description="R1, R2, S1, S2"
    )
    trigger: str = Field(description="Điều kiện vào lệnh")
    invalidation: str = Field(description="Điều kiện huỷ kịch bản")
    timeframe: str = Field(description="Khung thời gian: H1, H4, D1...")
    risk_events: Optional[str] = None


class MarketDetail(BaseModel):
    """Chi tiết một tài sản/thị trường cho Trang 2"""
    asset: str
    snapshot: Dict[str, Any] = Field(
        default_factory=dict,
        description="Last, %D1, Range, ATR, MA20, MA50"
    )
    updates: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Tin tức & cập nhật"
    )
    drivers: List[str] = Field(
        default_factory=list,
        description="Yếu tố chi phối với impact_sign"
    )
    trade_plan: TradePlan
    alternative_scenarios: List[str] = Field(
        default_factory=list,
        description="Kịch bản thay thế"
    )
    notes: Optional[str] = None
    impact_sign: Optional[str] = Field(
        default=None,
        description="+ / - / 0"
    )
    confidence: Optional[str] = Field(
        default=None,
        description="Low / Medium / High"
    )
    last_updated: str


class EquityItem(BaseModel):
    """Item trong Top 10 cổ phiếu"""
    ticker: str
    last: float
    pct_change: float
    vol_ratio: float
    catalyst: Optional[str] = None
    source_url: Optional[str] = None
    idea: Optional[str] = None
    score: float


class EquityTop10(BaseModel):
    """Danh sách Top 10 cổ phiếu đáng chú ý"""
    universe: str = Field(description="S&P 500, Nasdaq 100, ...")
    method: str = Field(description="Phương pháp xếp hạng")
    items: List[EquityItem] = Field(default_factory=list)
    score_components: Dict[str, float] = Field(
        default_factory=dict,
        description="Trọng số các thành phần điểm"
    )
    last_updated: str


class HeatmapData(BaseModel):
    """Dữ liệu cho heatmap biến động"""
    assets: List[str]
    periods: List[str]  # D1, WTD, MTD
    data: Dict[str, Dict[str, float]]  # {asset: {period: value}}
    lookback: str
    source: str
    last_updated: str


class TechnicalTable(BaseModel):
    """Bảng kỹ thuật nhanh"""
    assets: List[str]
    data: List[Dict[str, Any]]
    last_updated: str
