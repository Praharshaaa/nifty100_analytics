import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """Net Profit Margin % = net_profit / sales * 100. None if sales = 0."""
    if sales == 0 or sales is None:
        return None
    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit: float, sales: float,
                              source_opm: Optional[float] = None) -> Optional[float]:
    """Operating Profit Margin % = operating_profit / sales * 100.
    Cross-checks against source_opm field if provided; logs if diff > 1%."""
    if sales == 0 or sales is None:
        return None
    computed = (operating_profit / sales) * 100
    if source_opm is not None:
        diff = abs(computed - source_opm)
        if diff > 1.0:
            logger.warning(f"OPM mismatch: computed={computed:.2f}, source={source_opm:.2f}, diff={diff:.2f}")
    return computed


def return_on_equity(net_profit: float, equity_capital: float, reserves: float) -> Optional[float]:
    """ROE % = net_profit / (equity_capital + reserves) * 100. None if equity+reserves <= 0."""
    total_equity = (equity_capital or 0) + (reserves or 0)
    if total_equity <= 0:
        return None
    return (net_profit / total_equity) * 100


def return_on_capital_employed(ebit: float, equity_capital: float, reserves: float,
                                 borrowings: float, is_financial_sector: bool = False) -> Optional[float]:
    """ROCE % = EBIT / (equity + reserves + borrowings) * 100.
    For Financials sector, use sector-relative benchmark instead of absolute threshold."""
    capital_employed = (equity_capital or 0) + (reserves or 0) + (borrowings or 0)
    if capital_employed <= 0:
        return None
    roce = (ebit / capital_employed) * 100
    if is_financial_sector:
        logger.info(f"ROCE for financial sector company computed: {roce:.2f}% (sector-relative benchmark applies)")
    return roce


def return_on_assets(net_profit: float, total_assets: float) -> Optional[float]:
    """ROA % = net_profit / total_assets * 100. None if total_assets = 0."""
    if total_assets == 0 or total_assets is None:
        return None
    return (net_profit / total_assets) * 100