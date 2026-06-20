import re
import logging

logger = logging.getLogger(__name__)

MONTH_MAP = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12"
}

def normalize_year(raw: str) -> str:
    """Convert raw year label to YYYY-MM format."""
    if not isinstance(raw, str):
        raw = str(raw)
    raw = raw.strip()

    # Already normalized
    if re.match(r'^\d{4}-\d{2}$', raw):
        return raw

    # Mar-23 or Mar 23
    m = re.match(r'^([A-Za-z]{3})[-\s](\d{2})$', raw)
    if m:
        mon, yr = m.group(1).lower(), m.group(2)
        year = "20" + yr if int(yr) < 50 else "19" + yr
        return f"{year}-{MONTH_MAP.get(mon, '03')}"

    # March-2023
    m = re.match(r'^([A-Za-z]+)[-\s](\d{4})$', raw)
    if m:
        mon = m.group(1)[:3].lower()
        return f"{m.group(2)}-{MONTH_MAP.get(mon, '03')}"

    # FY23 or FY2023
    m = re.match(r'^FY(\d{2,4})$', raw, re.IGNORECASE)
    if m:
        yr = m.group(1)
        year = "20" + yr if len(yr) == 2 else yr
        return f"{year}-03"

    # Plain integer year
    if re.match(r'^\d{4}$', raw):
        return f"{raw}-03"

    logger.warning(f"normalize_year: unparseable value '{raw}'")
    return "PARSE_ERROR"


def normalize_ticker(raw: str) -> str:
    """Normalize NSE ticker to uppercase stripped string."""
    if not isinstance(raw, str):
        return "PARSE_ERROR"
    result = raw.strip().upper()
    if len(result) < 2 or len(result) > 12:
        logger.warning(f"normalize_ticker: out-of-range ticker '{raw}'")
        return "PARSE_ERROR"
    return result