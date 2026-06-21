# Sprint 1 Retrospective — Data Foundation
**Date:** 21 June 2026  
**Intern:** Praharsha Bheemini | MJ28  
**Sprint:** 1 of 6 | Days 01–07  

---

## ✅ Exit Criteria — All Passed

| Criteria | Result |
|----------|--------|
| `SELECT COUNT(*) FROM companies` | 92 ✅ |
| `PRAGMA foreign_key_check` | 0 rows ✅ |
| `load_audit.csv` zero CRITICAL rejections | ✅ |
| 35+ ETL unit tests pass | 35/35 ✅ |
| Manual review: 5 companies correct | ✅ |

---

## 📦 Deliverables Completed

| Deliverable | Status |
|-------------|--------|
| `nifty100.db` — 10 tables populated | ✅ |
| `output/load_audit.csv` | ✅ |
| `output/validation_failures.csv` | ✅ |
| `src/etl/loader.py` | ✅ |
| `src/etl/normaliser.py` | ✅ |
| `src/etl/validator.py` | ✅ |
| `src/etl/db_loader.py` | ✅ |
| `db/schema.sql` | ✅ |
| `tests/etl/test_normaliser.py` | ✅ |
| `notebooks/exploratory_queries.sql` | ✅ |

---

## 📊 Load Summary

| Table | Rows |
|-------|------|
| companies | 92 |
| profitandloss | 1161 |
| balancesheet | 1220 |
| cashflow | 1152 |
| analysis | 20 |
| documents | 1585 |
| prosandcons | 16 |
| sectors | 92 |
| stock_prices | 5520 |
| financial_ratios | 1184 |

---

## 🔍 Key Findings

- TTM and 2024.5 year values filtered correctly by normaliser
- 8 companies missing from companies.xlsx but present in child tables — known source data gap
- JIOFIN has only 2 years of P&L — newly listed company, expected
- DQ-03 CRITICAL violations are source data gaps, not loader bugs
- All 5 manually reviewed companies show correct and business-logical data

## 📚 Lessons Learned

- PowerShell requires different commands than bash (New-Item vs mkdir)
- `header=1` is critical for core Excel files — Row 0 is metadata
- TTM rows in source data must be filtered before DB load
- `conftest.py` needed for pytest to resolve src module imports

## 🚀 Next Sprint

Sprint 2 — Financial Ratio Engine  
Days 08–14 | Build 50+ KPIs for all 92 companies