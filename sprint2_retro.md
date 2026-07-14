# Sprint 2 Retrospective — Financial Ratio Engine
**Date:** 02 July 2026
**Intern:** Praharsha Bheemini | MJ28
**Sprint:** 2 of 6 | Days 08–14

---

## ✅ Exit Criteria — All Passed

| Criteria | Result |
|----------|--------|
| `SELECT COUNT(*) FROM financial_ratios` | 1,161 rows ✅ |
| All 14 KPI columns populated | ✅ |
| 20 KPI formula unit tests pass | 99/99 ✅ |
| Manual spot-check ROE & CAGR | ✅ |
| `ratio_edge_cases.log` exists | 1 entry documented ✅ |
| Screener preview ROE≥15, D/E<1, FCF>0 | 38 companies ✅ |

---

## 📦 Deliverables Completed

| Deliverable | Status |
|-------------|--------|
| `src/analytics/ratios.py` — profitability, leverage, efficiency | ✅ |
| `src/analytics/cagr.py` — CAGR engine with 6 edge cases | ✅ |
| `src/analytics/cashflow_kpis.py` — FCF, CFO quality, CapEx | ✅ |
| `src/analytics/ratio_engine.py` — full KPI engine | ✅ |
| `src/analytics/edge_case_logger.py` — ROCE/ROE cross-check | ✅ |
| `financial_ratios` table — 1,161 rows | ✅ |
| `output/capital_allocation.csv` — 1,142 rows | ✅ |
| `output/ratio_edge_cases.log` — 1 entry | ✅ |
| `tests/kpi/` — 64 KPI unit tests | ✅ |

---

## 📊 KPI Summary

| KPI Module | Functions | Tests |
|------------|-----------|-------|
| Profitability | NPM, OPM, ROE, ROCE, ROA | 16 |
| Leverage & Efficiency | D/E, ICR, Net Debt, Asset Turnover | 12 |
| CAGR Engine | Revenue, PAT, EPS (3yr/5yr/10yr) | 14 |
| Cash Flow KPIs | FCF, CFO Quality, CapEx, Capital Allocation | 22 |
| **Total** | **20+ functions** | **64 tests** |

---

## 🔍 Key Findings

- HAL shows extremely high ROE (3816%) due to very low equity base
- INDIGO shows high ROE (892%) — airline sector characteristic
- Financial sector companies use sector-relative ROCE benchmark
- Only 1 edge case found — SIEMENS ROCE discrepancy (version difference)
- 38 companies pass quality screener (ROE≥15%, D/E<1, FCF>0)
- JIOFIN excluded from CAGR due to insufficient data (<3yr)

## 📚 Lessons Learned

- Bank/NBFC D/E ratios are structurally high — carve-out essential
- CAGR turnaround flags critical for avoiding misleading growth metrics
- CFO quality score reveals earnings quality beyond just profit numbers
- Capital allocation patterns reveal management strategy at a glance

## 🚀 Next Sprint

Sprint 3 — Screener & Peer Comparison Engine
Days 15–21 | Build 6 preset screeners + peer percentile rankings