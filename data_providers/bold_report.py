"""
Bold.Report API Provider
Nguồn dữ liệu chất lượng cao về Gold/Bitcoin ETF Flows
API Docs: https://bold.report/data-api
"""
import requests
import streamlit as st
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from components.session_cache import get_cached_data

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BoldReportProvider:
    """
    Provider for Bold.Report Data API
    Provides Gold/Bitcoin ETF flows, performance data, and BOLD index
    
    Rate limit: 1 request/hour per IP
    """
    
    BASE_URL = "https://bold.report/data-api"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "AgentAda/1.0"
        })
        logger.info("BoldReportProvider initialized")
    
    def _fetch_json(self, endpoint: str) -> Optional[Dict]:
        """
        Fetch JSON data from Bold.Report API
        
        Args:
            endpoint: API endpoint (e.g., "gold/flows/summary")
            
        Returns:
            Parsed JSON data or None on error
        """
        url = f"{self.BASE_URL}/{endpoint}.json"
        
        try:
            logger.info(f"Fetching Bold.Report: {endpoint}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ Bold.Report {endpoint}: {len(str(data))} bytes")
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"❌ Bold.Report timeout: {endpoint}")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.warning(f"⚠️ Bold.Report rate limited: {endpoint}")
            else:
                logger.error(f"❌ Bold.Report HTTP error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Bold.Report error: {e}")
            return None
    
    # ==================== GOLD DATA ====================
    
    def get_gold_price(self) -> Optional[Dict]:
        """
        Get gold price history
        
        Returns:
            {version, updated, data: [{date, price, ...}]}
        """
        def _fetch():
            return self._fetch_json("gold/price")
        return get_cached_data(_fetch)
    
    def get_gold_flows_summary(self) -> Optional[Dict]:
        """
        Get Gold ETF fund flows summary (latest snapshot)
        
        Returns:
            {version, updated, date, total_flow_oz, total_flow_usd, ...}
        """
        def _fetch():
            return self._fetch_json("gold/flows/summary")
        return get_cached_data(_fetch)
    
    def get_gold_flows_history(self) -> Optional[Dict]:
        """
        Get Gold ETF fund flows history
        
        Returns:
            {version, updated, data: [{date, flow_oz, flow_usd, ...}]}
        """
        def _fetch():
            return self._fetch_json("gold/flows/all")
        return get_cached_data(_fetch)
    
    def get_gold_holdings_summary(self) -> Optional[Dict]:
        """
        Get Gold ETF holdings summary
        
        Returns:
            {version, updated, date, total_oz, total_usd, ...}
        """
        def _fetch():
            return self._fetch_json("gold/summary")
        return get_cached_data(_fetch)
    
    def get_gold_funds_aum(self) -> Optional[Dict]:
        """
        Get Gold ETF AUM by fund
        
        Returns:
            {version, updated, data: [{date, fund_name, aum, ...}]}
        """
        def _fetch():
            return self._fetch_json("gold/funds/aum")
        return get_cached_data(_fetch)
    
    # ==================== BITCOIN DATA ====================
    
    def get_bitcoin_price(self) -> Optional[Dict]:
        """
        Get Bitcoin price history
        
        Returns:
            {version, updated, data: [{date, price, ...}]}
        """
        def _fetch():
            return self._fetch_json("bitcoin/price")
        return get_cached_data(_fetch)
    
    def get_bitcoin_flows_summary(self) -> Optional[Dict]:
        """
        Get Bitcoin ETF fund flows summary (latest snapshot)
        
        Returns:
            {version, updated, date, total_flow_btc, total_flow_usd, ...}
        """
        def _fetch():
            return self._fetch_json("bitcoin/flows/summary")
        return get_cached_data(_fetch)
    
    def get_bitcoin_flows_history(self) -> Optional[Dict]:
        """
        Get Bitcoin ETF fund flows history
        
        Returns:
            {version, updated, data: [{date, flow_btc, flow_usd, ...}]}
        """
        def _fetch():
            return self._fetch_json("bitcoin/flows/all")
        return get_cached_data(_fetch)
    
    def get_bitcoin_holdings_summary(self) -> Optional[Dict]:
        """
        Get Bitcoin ETF holdings summary
        
        Returns:
            {version, updated, date, total_btc, total_usd, ...}
        """
        def _fetch():
            return self._fetch_json("bitcoin/summary")
        return get_cached_data(_fetch)
    
    def get_bitcoin_funds_aum(self) -> Optional[Dict]:
        """
        Get Bitcoin ETF AUM by fund
        
        Returns:
            {version, updated, data: [{date, fund_name, aum, ...}]}
        """
        def _fetch():
            return self._fetch_json("bitcoin/funds/aum")
        return get_cached_data(_fetch)
    
    # ==================== PERFORMANCE DATA ====================
    
    def get_performance_gold_bitcoin(self) -> Optional[Dict]:
        """
        Get BOLD vs Gold vs Bitcoin performance comparison
        
        Returns:
            {version, updated, data: [{date, bold, gold, bitcoin, ...}]}
        """
        def _fetch():
            return self._fetch_json("performance/gold-bitcoin")
        return get_cached_data(_fetch)
    
    def get_performance_bold_macro(self) -> Optional[Dict]:
        """
        Get BOLD vs Macro assets performance
        
        Returns:
            {version, updated, data: [{date, bold, spx, bonds, ...}]}
        """
        def _fetch():
            return self._fetch_json("performance/bold-macro")
        return get_cached_data(_fetch)
    
    # ==================== BOLD INDEX DATA ====================
    
    def get_bold_performance(self) -> Optional[Dict]:
        """
        Get BOLD index performance history
        
        Returns:
            {version, updated, data: [{date, value, return, ...}]}
        """
        def _fetch():
            return self._fetch_json("bold/performance")
        return get_cached_data(_fetch)
    
    def get_bold_weights(self) -> Optional[Dict]:
        """
        Get BOLD index daily weights (Gold vs Bitcoin allocation)
        
        Returns:
            {version, updated, data: [{date, gold_weight, btc_weight}]}
        """
        def _fetch():
            return self._fetch_json("bold/daily-weights")
        return get_cached_data(_fetch)
    
    # ==================== COMBINED DATA ====================
    
    def get_all_data(self) -> Optional[Dict]:
        """
        Get all combined daily data
        
        Returns:
            {version, updated, data: [{date, ...all fields...}]}
        """
        def _fetch():
            return self._fetch_json("combined/all")
        return get_cached_data(_fetch)
    
    # ==================== HELPER METHODS ====================
    
    def get_latest_fund_flows(self) -> Dict[str, Any]:
        """
        Get latest fund flows for both Gold and Bitcoin ETFs
        
        Returns:
            {
                gold: {date, flow_oz, flow_usd, ...},
                bitcoin: {date, flow_btc, flow_usd, ...},
                updated: timestamp
            }
        """
        result = {
            "gold": None,
            "bitcoin": None,
            "updated": datetime.utcnow().isoformat()
        }
        
        # Get Gold flows
        gold_data = self.get_gold_flows_summary()
        if gold_data:
            result["gold"] = {
                "date": gold_data.get("date"),
                "updated": gold_data.get("updated"),
                **{k: v for k, v in gold_data.items() 
                   if k not in ["version", "updated", "date"]}
            }
        
        # Get Bitcoin flows
        btc_data = self.get_bitcoin_flows_summary()
        if btc_data:
            result["bitcoin"] = {
                "date": btc_data.get("date"),
                "updated": btc_data.get("updated"),
                **{k: v for k, v in btc_data.items() 
                   if k not in ["version", "updated", "date"]}
            }
        
        return result
    
    def format_flow_for_display(self, flow_usd: float) -> str:
        """
        Format flow amount for display
        
        Args:
            flow_usd: Flow amount in USD
            
        Returns:
            Formatted string like "+$125M" or "-$50M"
        """
        if flow_usd is None:
            return "N/A"
        
        sign = "+" if flow_usd >= 0 else ""
        
        if abs(flow_usd) >= 1_000_000_000:
            return f"{sign}${flow_usd/1_000_000_000:.1f}B"
        elif abs(flow_usd) >= 1_000_000:
            return f"{sign}${flow_usd/1_000_000:.1f}M"
        elif abs(flow_usd) >= 1_000:
            return f"{sign}${flow_usd/1_000:.1f}K"
        else:
            return f"{sign}${flow_usd:.0f}"


# Singleton instance
_bold_provider = None

def get_bold_provider() -> BoldReportProvider:
    """Get singleton instance of BoldReportProvider"""
    global _bold_provider
    if _bold_provider is None:
        _bold_provider = BoldReportProvider()
    return _bold_provider


# ==================== STREAMLIT DISPLAY COMPONENTS ====================

def render_fund_flows_card(st_container=None):
    """
    Render fund flows card in Streamlit
    
    Args:
        st_container: Streamlit container (default: st)
    """
    container = st_container or st
    
    provider = get_bold_provider()
    flows = provider.get_latest_fund_flows()
    
    container.markdown("### 💰 ETF Fund Flows")
    
    col1, col2 = container.columns(2)
    
    with col1:
        container.markdown("#### 🥇 Gold ETFs")
        if flows["gold"]:
            gold = flows["gold"]
            flow_display = provider.format_flow_for_display(
                gold.get("total_flow_usd", 0)
            )
            color = "green" if gold.get("total_flow_usd", 0) >= 0 else "red"
            container.markdown(f"""
            - **Daily Flow**: :{color}[{flow_display}]
            - **Date**: {gold.get('date', 'N/A')}
            """)
        else:
            container.warning("⚠️ Gold flow data unavailable")
    
    with col2:
        container.markdown("#### ₿ Bitcoin ETFs")
        if flows["bitcoin"]:
            btc = flows["bitcoin"]
            flow_display = provider.format_flow_for_display(
                btc.get("total_flow_usd", 0)
            )
            color = "green" if btc.get("total_flow_usd", 0) >= 0 else "red"
            container.markdown(f"""
            - **Daily Flow**: :{color}[{flow_display}]
            - **Date**: {btc.get('date', 'N/A')}
            """)
        else:
            container.warning("⚠️ Bitcoin flow data unavailable")
    
    container.caption(f"📌 Source: Bold.Report | Updated: {flows['updated'][:19]}")
