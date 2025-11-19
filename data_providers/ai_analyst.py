"""
AI Analyst - Gemini-powered market analysis
Generates detailed Vietnamese commentary for brokers
"""
import logging
import streamlit as st
from typing import Dict, List, Optional
import google.generativeai as genai

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdaAIAnalyst:
    """
    Ada AI Analyst powered by Google Gemini
    Generates detailed market commentary in Vietnamese for HFM brokers
    """
    
    def __init__(self):
        """Initialize Gemini AI with API key from secrets"""
        try:
            # Load API key from secrets or environment
            if hasattr(st, 'secrets') and 'gemini' in st.secrets:
                api_key = st.secrets['gemini']['api_key']
            else:
                import os
                api_key = os.getenv('GEMINI_API_KEY')
            
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini AI initialized successfully")
            else:
                self.model = None
                logger.warning("Gemini API key not found")
                
        except Exception as e:
            logger.error(f"Error initializing Gemini: {e}")
            self.model = None
    
    
    def _build_market_context(self, 
                             snapshot: Dict, 
                             news: List[Dict],
                             calendar: Optional[List] = None) -> str:
        """
        Build market context from snapshot, news, and calendar
        
        Args:
            snapshot: Market snapshot data (VIX, S&P, DXY, etc.)
            news: List of news items with title, description, sentiment
            calendar: Economic calendar events
            
        Returns:
            Formatted context string
        """
        context = "=== THÔNG TIN THỊ TRƯỜNG ===\n\n"
        
        # Market snapshot
        if snapshot:
            context += "Dữ liệu thị trường hiện tại:\n"
            for ticker, data in snapshot.items():
                context += f"- {ticker}: ${data.get('last', 0):.2f} ({data.get('d1', 0):+.2f}% D1)\n"
            context += "\n"
        
        # News
        if news:
            context += "Tin tức mới nhất:\n"
            for i, item in enumerate(news[:10], 1):  # Top 10 news
                context += f"{i}. {item.get('title', 'N/A')}\n"
                if item.get('description'):
                    context += f"   {item['description']}\n"
                context += f"   Sentiment: {item.get('sentiment', 'Neutral')} | Impact: {item.get('impact', 'Medium')}\n"
                context += f"   Assets: {', '.join(item.get('assets', ['General']))}\n\n"
        
        # Calendar (if provided)
        if calendar:
            context += "Lịch kinh tế quan trọng:\n"
            for event in calendar[:5]:  # Top 5 events
                context += f"- {event.get('event', 'N/A')} ({event.get('region', 'N/A')}) - Impact: {event.get('impact', 'N/A')}\n"
            context += "\n"
        
        return context
    
    
    def generate_market_overview_analysis(self,
                                         snapshot: Dict,
                                         news: List[Dict],
                                         vix_level: float,
                                         spx_change: float,
                                         dxy_level: float) -> str:
        """
        Generate detailed market overview analysis for Trang 1
        
        Args:
            snapshot: Market data
            news: News items
            vix_level: VIX level
            spx_change: S&P 500 % change
            dxy_level: DXY level
            
        Returns:
            Vietnamese analysis text
        """
        if not self.model:
            return self._fallback_overview_analysis(vix_level, spx_change, dxy_level)
        
        try:
            context = self._build_market_context(snapshot, news)
            
            prompt = f"""Bạn là Ada, chuyên gia phân tích tài chính với 10+ năm kinh nghiệm tại các quỹ đầu tư lớn. 
Nhiệm vụ: Viết nhận định thị trường chi tiết cho nhân viên môi giới HFM, giúp họ tư vấn khách hàng.

{context}

Dựa trên dữ liệu trên, hãy viết nhận định thị trường theo cấu trúc sau:

**1. Tóm tắt thị trường (2-3 câu)**
- Đánh giá tổng quan: Risk-on hay Risk-off?
- Xu hướng chính: Tăng/giảm/sideway?

**2. Phân tích sâu (4-5 đoạn văn)**
- VIX {vix_level:.2f}: Ý nghĩa về tâm lý thị trường? So sánh với ngưỡng 20?
- S&P 500 {spx_change:+.2f}%: Nguyên nhân tăng/giảm? Liên hệ với tin tức nào?
- DXY {dxy_level:.2f}: Tác động đến vàng, dầu, crypto?
- Tin tức quan trọng nhất: Giải thích chi tiết 2-3 tin tức có impact cao, phân tích tác động đến từng loại tài sản.

**3. Kết luận và khuyến nghị (2-3 câu)**
- Bias thị trường: Bullish/Bearish/Neutral?
- Rủi ro cần lưu ý
- Cơ hội giao dịch

Viết bằng tiếng Việt chuyên nghiệp, giọng điệu tự tin nhưng thận trọng. Mỗi luận điểm cần có bằng chứng từ số liệu hoặc tin tức."""

            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating overview analysis: {e}")
            return self._fallback_overview_analysis(vix_level, spx_change, dxy_level)
    
    
    def generate_asset_detailed_analysis(self,
                                        asset: str,
                                        snapshot: Dict,
                                        drivers: List[str],
                                        news: List[Dict],
                                        technical_levels: Dict) -> str:
        """
        Generate detailed asset-specific analysis for Trang 2
        
        Args:
            asset: Asset ticker (e.g., "GC=F", "BTC-USD")
            snapshot: Asset snapshot data
            drivers: List of price drivers
            news: Relevant news items
            technical_levels: Support/Resistance levels
            
        Returns:
            Vietnamese analysis text
        """
        if not self.model:
            return self._fallback_asset_analysis(asset, snapshot, drivers)
        
        try:
            # Build news context
            news_context = ""
            if news:
                news_context = "Tin tức liên quan:\n"
                for i, item in enumerate(news[:5], 1):
                    news_context += f"{i}. {item.get('title', 'N/A')} - {item.get('sentiment', 'Neutral')}\n"
            
            # Build drivers context
            drivers_context = "\n".join(drivers) if drivers else "Chưa xác định drivers"
            
            prompt = f"""Bạn là Ada, chuyên gia phân tích tài sản {asset}.

DỮ LIỆU TÀI SẢN:
- Giá hiện tại: ${snapshot.get('last', 0):.2f}
- Thay đổi D1: {snapshot.get('pct_d1', 0):+.2f}%
- MA20: ${snapshot.get('ma20', 0):.2f}
- MA50: ${snapshot.get('ma50', 0):.2f}
- ATR(14): ${snapshot.get('atr14', 0):.2f}

CÁC YẾU TỐ CHI PHỐI:
{drivers_context}

{news_context}

LEVELS KỸ THUẬT:
- Resistance 1: ${technical_levels.get('R1', 0):.2f}
- Support 1: ${technical_levels.get('S1', 0):.2f}

Viết phân tích chi tiết cho {asset} theo cấu trúc:

**1. Đánh giá xu hướng hiện tại (2-3 câu)**
- Giá so với MA20/MA50 → Xu hướng?
- Momentum: Mạnh/Yếu/Sideway?

**2. Giải thích các yếu tố chi phối (3-4 đoạn)**
- Phân tích từng driver (+), (0), (-): Tại sao nó ảnh hưởng đến giá?
- Kết nối driver với tin tức cụ thể
- Đánh giá độ tin cậy của từng driver

**3. Phân tích kỹ thuật (2-3 câu)**
- Entry point tốt: Gần S1 hay R1?
- Stop loss nên đặt ở đâu?
- Target price hợp lý?

**4. Kịch bản giao dịch (2 kịch bản)**
- Kịch bản Bullish (60%): Điều kiện kích hoạt, target, stoploss
- Kịch bản Bearish (40%): Điều kiện kích hoạt, target, stoploss

Viết bằng tiếng Việt chuyên nghiệp, chi tiết, dễ hiểu cho nhân viên môi giới."""

            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating asset analysis: {e}")
            return self._fallback_asset_analysis(asset, snapshot, drivers)
    
    
    def _fallback_overview_analysis(self, vix: float, spx: float, dxy: float) -> str:
        """Fallback analysis when Gemini unavailable"""
        analysis = f"""**Tóm tắt thị trường:**

Thị trường đang trong trạng thái {'risk-off' if vix > 20 else 'risk-on'} với VIX ở mức {vix:.2f}. 
S&P 500 {'tăng' if spx > 0 else 'giảm'} {abs(spx):.2f}%, phản ánh {'tâm lý tích cực' if spx > 0 else 'áp lực bán'}.

**Phân tích:**

VIX {vix:.2f} cho thấy độ biến động {'cao' if vix > 20 else 'thấp'}, nhà đầu tư nên {'thận trọng với rủi ro' if vix > 20 else 'tận dụng cơ hội'}.

DXY ở {dxy:.2f} đang {'tạo áp lực lên' if dxy > 105 else 'hỗ trợ'} vàng và hàng hóa.

**Khuyến nghị:**

Ưu tiên {'tài sản an toàn' if vix > 20 else 'tài sản rủi ro cao'}. Theo dõi sát tin tức Fed và earnings.

*Lưu ý: Phân tích này được tạo tự động do Gemini AI không khả dụng. Vui lòng cấu hình API key để có phân tích chi tiết hơn.*"""
        
        return analysis
    
    
    def _fallback_asset_analysis(self, asset: str, snapshot: Dict, drivers: List[str]) -> str:
        """Fallback asset analysis when Gemini unavailable"""
        pct = snapshot.get('pct_d1', 0)
        
        analysis = f"""**Đánh giá {asset}:**

Giá hiện tại: ${snapshot.get('last', 0):.2f} ({'tăng' if pct > 0 else 'giảm'} {abs(pct):.2f}%)

**Các yếu tố chi phối:**
{chr(10).join(drivers) if drivers else '- Chưa xác định rõ drivers'}

**Phân tích kỹ thuật:**

{'Giá trên MA20, xu hướng tích cực' if snapshot.get('last', 0) > snapshot.get('ma20', 0) else 'Giá dưới MA20, áp lực giảm'}.

**Khuyến nghị:**

{'Chờ pullback về MA20 để mua' if pct > 2 else 'Theo dõi breakout resistance để vào lệnh'}.

*Lưu ý: Phân tích này được tạo tự động do Gemini AI không khả dụng. Vui lòng cấu hình API key để có phân tích chi tiết hơn.*"""
        
        return analysis


# Singleton instance
_ada_analyst = None

def get_ada_analyst() -> AdaAIAnalyst:
    """Get singleton Ada AI Analyst instance"""
    global _ada_analyst
    if _ada_analyst is None:
        _ada_analyst = AdaAIAnalyst()
    return _ada_analyst
