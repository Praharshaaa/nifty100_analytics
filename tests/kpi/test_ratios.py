import pytest
from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)

# ── Net Profit Margin ──────────────────────────────

def test_npm_normal():
    assert net_profit_margin(100, 1000) == 10.0

def test_npm_zero_sales():
    assert net_profit_margin(100, 0) is None

def test_npm_negative_profit():
    assert net_profit_margin(-50, 1000) == -5.0


# ── Operating Profit Margin ────────────────────────

def test_opm_normal():
    assert operating_profit_margin(200, 1000) == 20.0

def test_opm_zero_sales():
    assert operating_profit_margin(200, 0) is None

def test_opm_crosscheck_match():
    result = operating_profit_margin(215, 1000, source_opm=21.5)
    assert result == 21.5

def test_opm_crosscheck_mismatch_logged(caplog):
    with caplog.at_level("WARNING"):
        result = operating_profit_margin(300, 1000, source_opm=20.0)
    assert result == 30.0
    assert "OPM mismatch" in caplog.text


# ── Return on Equity ────────────────────────────────

def test_roe_positive():
    assert return_on_equity(100, 400, 100) == 20.0

def test_roe_neg_equity():
    assert return_on_equity(100, -200, -50) is None

def test_roe_zero_equity():
    assert return_on_equity(100, 0, 0) is None


# ── Return on Capital Employed ──────────────────────

def test_roce_normal():
    result = return_on_capital_employed(150, 400, 100, 200)
    assert round(result, 2) == 21.43

def test_roce_zero_capital():
    assert return_on_capital_employed(150, 0, 0, 0) is None

def test_roce_financial_sector(caplog):
    with caplog.at_level("INFO"):
        result = return_on_capital_employed(150, 400, 100, 200, is_financial_sector=True)
    assert result is not None
    assert "financial sector" in caplog.text


# ── Return on Assets ────────────────────────────────

def test_roa_normal():
    assert return_on_assets(100, 1000) == 10.0

def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None

def test_roa_negative_profit():
    assert return_on_assets(-50, 1000) == -5.0