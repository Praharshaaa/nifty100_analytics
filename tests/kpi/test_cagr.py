import pytest
from src.analytics.cagr import compute_cagr, revenue_cagr, pat_cagr, eps_cagr, compute_all_cagrs

# ── compute_cagr edge cases ─────────────────────────

def test_cagr_normal():
    val, flag = compute_cagr(100, 161, 5)
    assert round(val, 1) == 10.0
    assert flag == "OK"

def test_cagr_turnaround():
    val, flag = compute_cagr(-100, 200, 5)
    assert val is None
    assert flag == "TURNAROUND"

def test_cagr_decline_to_loss():
    val, flag = compute_cagr(100, -50, 5)
    assert val is None
    assert flag == "DECLINE_TO_LOSS"

def test_cagr_both_negative():
    val, flag = compute_cagr(-100, -200, 5)
    assert val is None
    assert flag == "BOTH_NEGATIVE"

def test_cagr_zero_base():
    val, flag = compute_cagr(0, 200, 5)
    assert val is None
    assert flag == "ZERO_BASE"

def test_cagr_insufficient():
    val, flag = compute_cagr(100, 200, 0)
    assert val is None
    assert flag == "INSUFFICIENT"

# ── revenue_cagr ────────────────────────────────────

def test_revenue_cagr_3yr():
    sales = [100, 110, 120, 133]
    val, flag = revenue_cagr(sales, 3)
    assert val is not None
    assert flag == "OK"

def test_revenue_cagr_insufficient():
    sales = [100, 110]
    val, flag = revenue_cagr(sales, 5)
    assert val is None
    assert flag == "INSUFFICIENT"

# ── pat_cagr ────────────────────────────────────────

def test_pat_cagr_normal():
    profit = [50, 60, 70, 80, 90, 100]
    val, flag = pat_cagr(profit, 5)
    assert val is not None
    assert flag == "OK"

def test_pat_cagr_turnaround():
    profit = [-50, 60, 70, 80, 90, 100]
    val, flag = pat_cagr(profit, 5)
    assert val is None
    assert flag == "TURNAROUND"

# ── eps_cagr ────────────────────────────────────────

def test_eps_cagr_normal():
    eps = [10, 12, 14, 16, 18, 20]
    val, flag = eps_cagr(eps, 5)
    assert val is not None
    assert flag == "OK"

def test_eps_cagr_insufficient():
    eps = [10, 12]
    val, flag = eps_cagr(eps, 10)
    assert val is None
    assert flag == "INSUFFICIENT"

# ── compute_all_cagrs ───────────────────────────────

def test_compute_all_cagrs_keys():
    sales  = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    profit = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    eps    = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    result = compute_all_cagrs(sales, profit, eps)
    assert "revenue_cagr_3yr" in result
    assert "pat_cagr_5yr" in result
    assert "eps_cagr_10yr" in result
    assert "revenue_cagr_3yr_flag" in result

def test_compute_all_cagrs_values():
    sales  = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
    profit = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    eps    = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    result = compute_all_cagrs(sales, profit, eps)
    assert result["revenue_cagr_3yr_flag"] == "OK"
    assert result["pat_cagr_5yr_flag"] == "OK"
    assert result["eps_cagr_10yr_flag"] == "OK"