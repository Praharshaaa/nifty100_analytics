import pytest
from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
    classify_fcf_consecutive,
)

# ── Free Cash Flow ──────────────────────────────────

def test_fcf_positive():
    assert free_cash_flow(500, -200) == 300

def test_fcf_negative():
    assert free_cash_flow(100, -400) == -300

def test_fcf_both_positive():
    assert free_cash_flow(500, 200) == 700


# ── CFO Quality Score ───────────────────────────────

def test_cfo_quality_high():
    cfo = [120, 130, 140, 150, 160]
    pat = [100, 100, 100, 100, 100]
    score = cfo_quality_score(cfo, pat)
    assert score > 1.0

def test_cfo_quality_accrual_risk():
    cfo = [20, 25, 30, 35, 40]
    pat = [100, 100, 100, 100, 100]
    score = cfo_quality_score(cfo, pat)
    assert score < 0.5

def test_cfo_quality_insufficient():
    assert cfo_quality_score([100, 200], [100, 200]) is None

def test_cfo_quality_zero_pat():
    cfo = [100, 100, 100, 100, 100]
    pat = [100, 0, 100, 100, 100]
    assert cfo_quality_score(cfo, pat) is None


# ── CapEx Intensity ─────────────────────────────────

def test_capex_asset_light():
    assert capex_intensity(-200, 10000) == "Asset Light"

def test_capex_moderate():
    assert capex_intensity(-400, 8000) == "Moderate"

def test_capex_intensive():
    assert capex_intensity(-1000, 5000) == "Capital Intensive"

def test_capex_zero_sales():
    assert capex_intensity(-200, 0) is None


# ── FCF Conversion Rate ─────────────────────────────

def test_fcf_conversion_normal():
    assert fcf_conversion_rate(600, 1000) == 60.0

def test_fcf_conversion_zero_op():
    assert fcf_conversion_rate(600, 0) is None

def test_fcf_conversion_negative():
    assert fcf_conversion_rate(-200, 1000) == -20.0


# ── Capital Allocation Pattern ──────────────────────

def test_pattern_reinvestor():
    assert capital_allocation_pattern(500, -200, -100) == "Reinvestor"

def test_pattern_distress():
    assert capital_allocation_pattern(-200, 100, 300) == "Distress Signal"

def test_pattern_growth_by_debt():
    assert capital_allocation_pattern(-200, -300, 600) == "Growth Funded by Debt"

def test_pattern_cash_accumulator():
    assert capital_allocation_pattern(500, 200, 300) == "Cash Accumulator"

def test_pattern_liquidating():
    assert capital_allocation_pattern(500, 200, -100) == "Liquidating Assets"


# ── FCF Consecutive Negative ────────────────────────

def test_fcf_consecutive_negative():
    assert classify_fcf_consecutive([-100, -200, -300]) is True

def test_fcf_not_consecutive():
    assert classify_fcf_consecutive([-100, 200, -300]) is False

def test_fcf_insufficient_data():
    assert classify_fcf_consecutive([-100, -200]) is False