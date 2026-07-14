import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def free_cash_flow(operating_activity: float, investing_activity: float) -> float:
    """FCF = CFO + CFI. Negative value is allowed."""
    return (operating_activity or 0) + (investing_activity or 0)


def cfo_quality_score(cfo_series: list, pat_series: list) -> Optional[float]:
    """CFO Quality Score = avg(CFO/PAT) over 5 years.
    >1.0 = High Quality, 0.5-1.0 = Moderate, <0.5 = Accrual Risk.
    Returns None if PAT = 0 in any year."""
    if len(cfo_series) < 5 or len(pat_series) < 5:
        return None
    ratios = []
    for cfo, pat in zip(cfo_series[-5:], pat_series[-5:]):
        if (pat or 0) == 0:
            return None
        ratios.append(cfo / pat)
    score = sum(ratios) / len(ratios)
    if score > 1.0:
        logger.info(f"CFO Quality: High Quality ({score:.2f})")
    elif score >= 0.5:
        logger.info(f"CFO Quality: Moderate ({score:.2f})")
    else:
        logger.warning(f"CFO Quality: Accrual Risk ({score:.2f})")
    return round(score, 2)


def capex_intensity(investing_activity: float, sales: float) -> Optional[str]:
    """CapEx Intensity = abs(investing_activity) / sales * 100.
    <3% = Asset Light, 3-8% = Moderate, >8% = Capital Intensive."""
    if (sales or 0) == 0:
        return None
    intensity = abs(investing_activity or 0) / sales * 100
    if intensity < 3:
        return "Asset Light"
    elif intensity <= 8:
        return "Moderate"
    else:
        return "Capital Intensive"


def fcf_conversion_rate(fcf: float, operating_profit: float) -> Optional[float]:
    """FCF Conversion = FCF / operating_profit * 100.
    >60% = Efficient, <30% = CapEx Heavy. None if operating_profit = 0."""
    if (operating_profit or 0) == 0:
        return None
    return round((fcf / operating_profit) * 100, 2)


def capital_allocation_pattern(cfo: float, cfi: float, cff: float) -> str:
    """Classify capital allocation into 8 patterns based on CFO/CFI/CFF signs.
    Pattern: (+,-,-) = Reinvestor
             (+,-,-) with high CFO/PAT = Shareholder Returns
             (+,+,-) = Liquidating Assets
             (-,+,+) = Distress Signal
             (-,-,+) = Growth Funded by Debt
             (+,+,+) = Cash Accumulator
             (-,-,-) = Pre-Revenue
             (+,-,+) = Mixed
    """
    cfo_sign = "+" if (cfo or 0) >= 0 else "-"
    cfi_sign = "+" if (cfi or 0) >= 0 else "-"
    cff_sign = "+" if (cff or 0) >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    pattern_map = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed",
        ("-", "+", "-"): "Mixed",
    }

    label = pattern_map.get(pattern, "Mixed")
    logger.info(f"Capital allocation pattern {pattern}: {label}")
    return label


def classify_fcf_consecutive(fcf_series: list) -> bool:
    """Returns True if FCF has been negative for 3 consecutive years."""
    if len(fcf_series) < 3:
        return False
    return all(f < 0 for f in fcf_series[-3:])