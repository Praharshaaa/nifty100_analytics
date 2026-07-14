import sqlite3
import pandas as pd
import logging
from pathlib import Path
from src.analytics.ratios import (
    net_profit_margin, operating_profit_margin,
    return_on_equity, return_on_capital_employed,
    return_on_assets, debt_to_equity,
    interest_coverage_ratio, net_debt, asset_turnover
)
from src.analytics.cagr import compute_all_cagrs
from src.analytics.cashflow_kpis import (
    free_cash_flow, capital_allocation_pattern
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = Path("db/nifty100.db")
OUTPUT  = Path("output")
OUTPUT.mkdir(exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def run_ratio_engine():
    conn = get_conn()

    # Load all tables
    pl      = pd.read_sql("SELECT * FROM profitandloss ORDER BY company_id, year", conn)
    bs      = pd.read_sql("SELECT * FROM balancesheet ORDER BY company_id, year", conn)
    cf      = pd.read_sql("SELECT * FROM cashflow ORDER BY company_id, year", conn)
    sectors = pd.read_sql("SELECT company_id, broad_sector FROM sectors", conn)

    financial_sector = set(
        sectors[sectors["broad_sector"] == "Financials"]["company_id"]
    )

    companies = pl["company_id"].unique()
    logger.info(f"Running ratio engine for {len(companies)} companies")

    ratio_rows = []
    cap_alloc_rows = []

    for company in companies:
        pl_c  = pl[pl["company_id"] == company].sort_values("year")
        bs_c  = bs[bs["company_id"] == company].sort_values("year")
        cf_c  = cf[cf["company_id"] == company].sort_values("year")
        is_fin = company in financial_sector

        # CAGR series
        sales_series  = pl_c["sales"].tolist()
        profit_series = pl_c["net_profit"].tolist()
        eps_series    = pl_c["eps"].tolist()
        cagrs         = compute_all_cagrs(sales_series, profit_series, eps_series)

        for _, pl_row in pl_c.iterrows():
            year = pl_row["year"]

            # Match BS and CF rows
            bs_row = bs_c[bs_c["year"] == year]
            cf_row = cf_c[cf_c["year"] == year]

            bs_r = bs_row.iloc[0] if len(bs_row) > 0 else None
            cf_r = cf_row.iloc[0] if len(cf_row) > 0 else None

            # Profitability
            npm  = net_profit_margin(pl_row["net_profit"], pl_row["sales"])
            opm  = operating_profit_margin(pl_row["operating_profit"],
                                           pl_row["sales"], pl_row.get("opm_percentage"))
            roe  = return_on_equity(pl_row["net_profit"],
                                    bs_r["equity_capital"] if bs_r is not None else None,
                                    bs_r["reserves"] if bs_r is not None else None)
            roa  = return_on_assets(pl_row["net_profit"],
                                    bs_r["total_assets"] if bs_r is not None else None)

            # EBIT for ROCE
            ebit = (pl_row["operating_profit"] or 0) - (pl_row.get("depreciation") or 0)
            roce = return_on_capital_employed(
                ebit,
                bs_r["equity_capital"] if bs_r is not None else None,
                bs_r["reserves"] if bs_r is not None else None,
                bs_r["borrowings"] if bs_r is not None else None,
                is_financial_sector=is_fin
            ) if bs_r is not None else None

            # Leverage
            de  = debt_to_equity(
                bs_r["borrowings"] if bs_r is not None else None,
                bs_r["equity_capital"] if bs_r is not None else None,
                bs_r["reserves"] if bs_r is not None else None,
                is_financial_sector=is_fin
            ) if bs_r is not None else None

            icr = interest_coverage_ratio(
                pl_row["operating_profit"],
                pl_row.get("other_income"),
                pl_row.get("interest")
            )

            nd  = net_debt(
                bs_r["borrowings"] if bs_r is not None else None,
                bs_r["investments"] if bs_r is not None else None
            ) if bs_r is not None else None

            at  = asset_turnover(
                pl_row["sales"],
                bs_r["total_assets"] if bs_r is not None else None
            ) if bs_r is not None else None

            # Cash Flow KPIs
            fcf = free_cash_flow(
                cf_r["operating_activity"] if cf_r is not None else None,
                cf_r["investing_activity"] if cf_r is not None else None
            ) if cf_r is not None else None

            cfo = cf_r["operating_activity"] if cf_r is not None else None
            cfi = cf_r["investing_activity"] if cf_r is not None else None
            cff = cf_r["financing_activity"] if cf_r is not None else None

            # Capital allocation
            if cfo is not None and cfi is not None and cff is not None:
                pattern = capital_allocation_pattern(cfo, cfi, cff)
                cap_alloc_rows.append({
                    "company_id": company, "year": year,
                    "cfo_sign": "+" if cfo >= 0 else "-",
                    "cfi_sign": "+" if cfi >= 0 else "-",
                    "cff_sign": "+" if cff >= 0 else "-",
                    "pattern_label": pattern
                })

            ratio_rows.append({
                "company_id":                   company,
                "year":                         year,
                "net_profit_margin_pct":        npm,
                "operating_profit_margin_pct":  opm,
                "return_on_equity_pct":         roe,
                "return_on_assets_pct":         roa,
                "return_on_capital_pct":        roce,
                "debt_to_equity":               de,
                "interest_coverage":            icr,
                "net_debt_cr":                  nd,
                "asset_turnover":               at,
                "free_cash_flow_cr":            fcf,
                "earnings_per_share":           pl_row.get("eps"),
                "dividend_payout_ratio_pct":    pl_row.get("dividend_payout"),
                "revenue_cagr_5yr":             cagrs.get("revenue_cagr_5yr"),
                "revenue_cagr_5yr_flag":        cagrs.get("revenue_cagr_5yr_flag"),
                "pat_cagr_5yr":                 cagrs.get("pat_cagr_5yr"),
                "pat_cagr_5yr_flag":            cagrs.get("pat_cagr_5yr_flag"),
                "eps_cagr_5yr":                 cagrs.get("eps_cagr_5yr"),
                "eps_cagr_5yr_flag":            cagrs.get("eps_cagr_5yr_flag"),
            })

    # Save to SQLite
    ratios_df = pd.DataFrame(ratio_rows)
    ratios_df.to_sql("financial_ratios", conn, if_exists="replace", index=False)
    logger.info(f"financial_ratios table: {len(ratios_df)} rows written")

    # Save capital allocation
    cap_df = pd.DataFrame(cap_alloc_rows)
    cap_df.to_csv(OUTPUT / "capital_allocation.csv", index=False)
    logger.info(f"capital_allocation.csv: {len(cap_df)} rows saved")

    # Verify row count
    count = pd.read_sql("SELECT COUNT(*) as c FROM financial_ratios", conn)["c"][0]
    logger.info(f"SELECT COUNT(*) FROM financial_ratios = {count}")

    conn.commit()
    conn.close()

    print(f"\n✅ financial_ratios table: {count} rows")
    print(f"✅ capital_allocation.csv: {len(cap_df)} rows")
    return ratios_df


if __name__ == "__main__":
    run_ratio_engine()