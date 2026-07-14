import logging
from typing import Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def compute_cagr(start_val: float, end_val: float, n_years: int) -> Tuple[Optional[float], str]:
    """
    Compute CAGR = ((end/start)^(1/n) - 1) * 100.
    Returns (cagr_value, flag) tuple.

    Edge cases:
    - Positive → Positive: compute normally
    - Positive → Negative: return None, DECLINE_TO_LOSS
    - Negative → Positive: return None, TURNAROUND
    - Negative → Negative: return None, BOTH_NEGATIVE
    - Zero base: return None, ZERO_BASE
    - < n years history: return None, INSUFFICIENT
    """
    if n_years < 1:
        return None, "INSUFFICIENT"

    if start_val is None or end_val is None:
        return None, "INSUFFICIENT"

    if start_val == 0:
        return None, "ZERO_BASE"

    if start_val > 0 and end_val > 0:
        cagr = ((end_val / start_val) ** (1 / n_years) - 1) * 100
        return round(cagr, 2), "OK"

    if start_val > 0 and end_val < 0:
        return None, "DECLINE_TO_LOSS"

    if start_val < 0 and end_val > 0:
        return None, "TURNAROUND"

    if start_val < 0 and end_val < 0:
        return None, "BOTH_NEGATIVE"

    return None, "INSUFFICIENT"


def revenue_cagr(sales_series: list, years: int) -> Tuple[Optional[float], str]:
    """Compute Revenue CAGR for given year window from sales series (ordered oldest to newest)."""
    if len(sales_series) < years + 1:
        return None, "INSUFFICIENT"
    start = sales_series[-(years + 1)]
    end = sales_series[-1]
    return compute_cagr(start, end, years)


def pat_cagr(profit_series: list, years: int) -> Tuple[Optional[float], str]:
    """Compute PAT (Net Profit) CAGR for given year window."""
    if len(profit_series) < years + 1:
        return None, "INSUFFICIENT"
    start = profit_series[-(years + 1)]
    end = profit_series[-1]
    return compute_cagr(start, end, years)


def eps_cagr(eps_series: list, years: int) -> Tuple[Optional[float], str]:
    """Compute EPS CAGR for given year window."""
    if len(eps_series) < years + 1:
        return None, "INSUFFICIENT"
    start = eps_series[-(years + 1)]
    end = eps_series[-1]
    return compute_cagr(start, end, years)


def compute_all_cagrs(sales: list, profit: list, eps: list) -> dict:
    """Compute all 9 CAGRs (3yr, 5yr, 10yr for revenue, PAT, EPS).
    Returns dict with value and flag for each."""
    result = {}
    for years in [3, 5, 10]:
        rev_val, rev_flag = revenue_cagr(sales, years)
        pat_val, pat_flag = pat_cagr(profit, years)
        eps_val, eps_flag = eps_cagr(eps, years)

        result[f"revenue_cagr_{years}yr"] = rev_val
        result[f"revenue_cagr_{years}yr_flag"] = rev_flag
        result[f"pat_cagr_{years}yr"] = pat_val
        result[f"pat_cagr_{years}yr_flag"] = pat_flag
        result[f"eps_cagr_{years}yr"] = eps_val
        result[f"eps_cagr_{years}yr_flag"] = eps_flag

        if rev_flag not in ["OK", "INSUFFICIENT"]:
            logger.warning(f"Revenue CAGR {years}yr flag: {rev_flag}")
        if pat_flag not in ["OK", "INSUFFICIENT"]:
            logger.warning(f"PAT CAGR {years}yr flag: {pat_flag}")

    return result