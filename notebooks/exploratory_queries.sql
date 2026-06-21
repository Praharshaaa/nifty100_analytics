-- ============================================================
-- NIFTY 100 Analytics — Exploratory SQL Queries
-- Sprint 1 · Day 05 · 10 Business Queries
-- ============================================================

-- Q01: Total row counts for all 10 tables
SELECT 'companies'        AS table_name, COUNT(*) AS row_count FROM companies
UNION ALL
SELECT 'profitandloss',   COUNT(*) FROM profitandloss
UNION ALL
SELECT 'balancesheet',    COUNT(*) FROM balancesheet
UNION ALL
SELECT 'cashflow',        COUNT(*) FROM cashflow
UNION ALL
SELECT 'analysis',        COUNT(*) FROM analysis
UNION ALL
SELECT 'documents',       COUNT(*) FROM documents
UNION ALL
SELECT 'prosandcons',     COUNT(*) FROM prosandcons
UNION ALL
SELECT 'sectors',         COUNT(*) FROM sectors
UNION ALL
SELECT 'stock_prices',    COUNT(*) FROM stock_prices
UNION ALL
SELECT 'financial_ratios',COUNT(*) FROM financial_ratios;

-- Q02: Year coverage per company in profitandloss
SELECT
    company_id,
    COUNT(DISTINCT year) AS years_available,
    MIN(year)            AS earliest_year,
    MAX(year)            AS latest_year
FROM profitandloss
GROUP BY company_id
ORDER BY years_available ASC
LIMIT 20;

-- Q03: Companies with less than 5 years of P&L data
SELECT
    company_id,
    COUNT(DISTINCT year) AS years_available
FROM profitandloss
GROUP BY company_id
HAVING years_available < 5
ORDER BY years_available ASC;

-- Q04: NULL check — key columns in profitandloss
SELECT
    COUNT(*)                          AS total_rows,
    SUM(CASE WHEN sales IS NULL       THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN net_profit IS NULL  THEN 1 ELSE 0 END) AS null_net_profit,
    SUM(CASE WHEN eps IS NULL         THEN 1 ELSE 0 END) AS null_eps,
    SUM(CASE WHEN opm_percentage IS NULL THEN 1 ELSE 0 END) AS null_opm
FROM profitandloss;

-- Q05: NULL check — key columns in balancesheet
SELECT
    COUNT(*)                                  AS total_rows,
    SUM(CASE WHEN total_assets IS NULL        THEN 1 ELSE 0 END) AS null_total_assets,
    SUM(CASE WHEN total_liabilities IS NULL   THEN 1 ELSE 0 END) AS null_total_liabilities,
    SUM(CASE WHEN borrowings IS NULL          THEN 1 ELSE 0 END) AS null_borrowings
FROM balancesheet;

-- Q06: Top 10 companies by latest year sales
SELECT
    p.company_id,
    c.company_name,
    p.year,
    p.sales
FROM profitandloss p
JOIN companies c ON p.company_id = c.id
WHERE p.year = (SELECT MAX(year) FROM profitandloss WHERE company_id = p.company_id)
ORDER BY p.sales DESC
LIMIT 10;

-- Q07: Sector distribution — companies per broad sector
SELECT
    broad_sector,
    COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;

-- Q08: Companies with positive net profit in latest year
SELECT
    p.company_id,
    c.company_name,
    p.year,
    p.net_profit
FROM profitandloss p
JOIN companies c ON p.company_id = c.id
WHERE p.year = (SELECT MAX(year) FROM profitandloss WHERE company_id = p.company_id)
  AND p.net_profit > 0
ORDER BY p.net_profit DESC
LIMIT 10;

-- Q09: Stock price coverage — date range per company
SELECT
    company_id,
    COUNT(*)    AS price_records,
    MIN(date)   AS earliest_date,
    MAX(date)   AS latest_date
FROM stock_prices
GROUP BY company_id
ORDER BY price_records ASC
LIMIT 10;

-- Q10: FK integrity check — orphan records
SELECT 'profitandloss' AS source_table, company_id
FROM profitandloss
WHERE company_id NOT IN (SELECT id FROM companies)
UNION ALL
SELECT 'balancesheet', company_id
FROM balancesheet
WHERE company_id NOT IN (SELECT id FROM companies)
UNION ALL
SELECT 'cashflow', company_id
FROM cashflow
WHERE company_id NOT IN (SELECT id FROM companies)
ORDER BY source_table, company_id;