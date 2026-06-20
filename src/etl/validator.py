import pandas as pd
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

failures = []

def log_failure(rule_id, severity, company_id, year, field, issue):
    """Log a DQ failure."""
    failures.append({
        "rule_id": rule_id,
        "severity": severity,
        "company_id": company_id,
        "year": year,
        "field": field,
        "issue": issue
    })

def dq01_company_pk(companies: pd.DataFrame):
    """DQ-01: Company PK uniqueness."""
    dupes = companies[companies["id"].duplicated()]
    for _, row in dupes.iterrows():
        log_failure("DQ-01", "CRITICAL", row["id"], None, "id", "Duplicate company id")
    logger.info(f"DQ-01: {len(dupes)} violations")

def dq02_annual_pk(pl: pd.DataFrame, bs: pd.DataFrame, cf: pd.DataFrame):
    """DQ-02: No duplicate (company_id, year) in time-series tables."""
    for name, df in [("profitandloss", pl), ("balancesheet", bs), ("cashflow", cf)]:
        dupes = df[df.duplicated(subset=["company_id", "year"])]
        for _, row in dupes.iterrows():
            log_failure("DQ-02", "CRITICAL", row["company_id"], row["year"], "company_id,year", f"Duplicate PK in {name}")
    logger.info(f"DQ-02 done")

def dq03_fk_integrity(companies: pd.DataFrame, pl: pd.DataFrame, bs: pd.DataFrame,
                       cf: pd.DataFrame, docs: pd.DataFrame, sectors: pd.DataFrame):
    """DQ-03: FK integrity — all company_id must exist in companies."""
    valid_ids = set(companies["id"])
    for name, df in [("profitandloss", pl), ("balancesheet", bs),
                     ("cashflow", cf), ("documents", docs), ("sectors", sectors)]:
        orphans = df[~df["company_id"].isin(valid_ids)]
        for _, row in orphans.iterrows():
            log_failure("DQ-03", "CRITICAL", row["company_id"], None, "company_id", f"Orphan FK in {name}")
    logger.info(f"DQ-03 done")

def dq04_bs_balance(bs: pd.DataFrame):
    """DQ-04: |total_assets - total_liabilities| / total_assets < 1%"""
    for _, row in bs.iterrows():
        try:
            diff = abs(row["total_assets"] - row["total_liabilities"]) / row["total_assets"]
            if diff >= 0.01:
                log_failure("DQ-04", "WARNING", row["company_id"], row["year"],
                           "total_assets/total_liabilities", f"BS imbalance {diff:.2%}")
        except:
            pass
    logger.info("DQ-04 done")

def dq05_opm_crosscheck(pl: pd.DataFrame):
    """DQ-05: |opm_percentage - computed_opm| < 1%"""
    for _, row in pl.iterrows():
        try:
            computed = (row["operating_profit"] / row["sales"]) * 100
            if abs(computed - row["opm_percentage"]) >= 1.0:
                log_failure("DQ-05", "WARNING", row["company_id"], row["year"],
                           "opm_percentage", f"OPM mismatch: source={row['opm_percentage']:.1f}, computed={computed:.1f}")
        except:
            pass
    logger.info("DQ-05 done")

def dq06_positive_sales(pl: pd.DataFrame):
    """DQ-06: sales > 0"""
    bad = pl[pl["sales"] <= 0]
    for _, row in bad.iterrows():
        log_failure("DQ-06", "WARNING", row["company_id"], row["year"],
                   "sales", f"sales <= 0: {row['sales']}")
    logger.info(f"DQ-06: {len(bad)} violations")

def dq07_year_format(pl: pd.DataFrame, bs: pd.DataFrame, cf: pd.DataFrame):
    """DQ-07: year matches YYYY-MM format."""
    pattern = re.compile(r'^\d{4}-\d{2}$')
    for name, df in [("profitandloss", pl), ("balancesheet", bs), ("cashflow", cf)]:
        bad = df[~df["year"].astype(str).str.match(pattern)]
        for _, row in bad.iterrows():
            log_failure("DQ-07", "CRITICAL", row["company_id"], row["year"],
                       "year", f"Invalid year format in {name}: {row['year']}")
    logger.info("DQ-07 done")

def dq08_ticker_format(companies: pd.DataFrame):
    """DQ-08: ticker length 2-12 chars."""
    bad = companies[(companies["id"].str.len() < 2) | (companies["id"].str.len() > 12)]
    for _, row in bad.iterrows():
        log_failure("DQ-08", "CRITICAL", row["id"], None, "id", f"Ticker length out of range: {row['id']}")
    logger.info(f"DQ-08: {len(bad)} violations")

def dq09_net_cash_check(cf: pd.DataFrame):
    """DQ-09: |net_cash_flow - (CFO+CFI+CFF)| <= 10"""
    for _, row in cf.iterrows():
        try:
            computed = row["operating_activity"] + row["investing_activity"] + row["financing_activity"]
            if abs(computed - row["net_cash_flow"]) > 10:
                log_failure("DQ-09", "WARNING", row["company_id"], row["year"],
                           "net_cash_flow", f"Net cash mismatch: source={row['net_cash_flow']:.1f}, computed={computed:.1f}")
        except:
            pass
    logger.info("DQ-09 done")

def dq10_nonneg_fixed_assets(bs: pd.DataFrame):
    """DQ-10: fixed_assets >= 0"""
    bad = bs[bs["fixed_assets"] < 0]
    for _, row in bad.iterrows():
        log_failure("DQ-10", "WARNING", row["company_id"], row["year"],
                   "fixed_assets", f"Negative fixed_assets: {row['fixed_assets']}")
    logger.info(f"DQ-10: {len(bad)} violations")

def dq11_tax_rate(pl: pd.DataFrame):
    """DQ-11: 0 <= tax_percentage <= 60"""
    bad = pl[(pl["tax_percentage"] < 0) | (pl["tax_percentage"] > 60)]
    for _, row in bad.iterrows():
        log_failure("DQ-11", "WARNING", row["company_id"], row["year"],
                   "tax_percentage", f"Tax rate out of range: {row['tax_percentage']}")
    logger.info(f"DQ-11: {len(bad)} violations")

def dq12_dividend_cap(pl: pd.DataFrame):
    """DQ-12: dividend_payout <= 200%"""
    bad = pl[pl["dividend_payout"] > 200]
    for _, row in bad.iterrows():
        log_failure("DQ-12", "WARNING", row["company_id"], row["year"],
                   "dividend_payout", f"Dividend payout > 200%: {row['dividend_payout']}")
    logger.info(f"DQ-12: {len(bad)} violations")

def dq13_url_validity(docs: pd.DataFrame):
    """DQ-13: Check Annual Report URLs are not null."""
    bad = docs[docs["Annual_Report"].isna()]
    for _, row in bad.iterrows():
        log_failure("DQ-13", "WARNING", row["company_id"], row.get("Year"),
                   "Annual_Report", "Missing URL")
    logger.info(f"DQ-13: {len(bad)} missing URLs")

def dq14_eps_sign(pl: pd.DataFrame):
    """DQ-14: eps > 0 if net_profit > 0"""
    bad = pl[(pl["net_profit"] > 0) & (pl["eps"] <= 0)]
    for _, row in bad.iterrows():
        log_failure("DQ-14", "WARNING", row["company_id"], row["year"],
                   "eps", f"EPS <= 0 but net_profit > 0: eps={row['eps']}")
    logger.info(f"DQ-14: {len(bad)} violations")

def dq15_bs_strict_balance(bs: pd.DataFrame):
    """DQ-15: total_liabilities == total_assets (INFO)"""
    bad = bs[bs["total_assets"] != bs["total_liabilities"]]
    for _, row in bad.iterrows():
        log_failure("DQ-15", "INFO", row["company_id"], row["year"],
                   "total_assets/total_liabilities", "Strict BS mismatch")
    logger.info(f"DQ-15: {len(bad)} informational flags")

def dq16_coverage_check(pl: pd.DataFrame, bs: pd.DataFrame, cf: pd.DataFrame, companies: pd.DataFrame):
    """DQ-16: Each company has >= 5 years of records."""
    for name, df in [("profitandloss", pl), ("balancesheet", bs), ("cashflow", cf)]:
        counts = df.groupby("company_id")["year"].count()
        low = counts[counts < 5]
        for company_id, count in low.items():
            log_failure("DQ-16", "WARNING", company_id, None,
                       "year", f"Only {count} years in {name} (< 5 required)")
    logger.info("DQ-16 done")

def save_failures():
    """Save all failures to output/validation_failures.csv"""
    df = pd.DataFrame(failures)
    path = OUTPUT / "validation_failures.csv"
    df.to_csv(path, index=False)
    logger.info(f"validation_failures.csv saved: {len(df)} rows")
    return df

if __name__ == "__main__":
    from src.etl.loader import (
        load_companies, load_profitandloss, load_balancesheet,
        load_cashflow, load_documents, load_sectors
    )

    companies = load_companies()
    pl        = load_profitandloss()
    bs        = load_balancesheet()
    cf        = load_cashflow()
    docs      = load_documents()
    sectors   = load_sectors()

    dq01_company_pk(companies)
    dq02_annual_pk(pl, bs, cf)
    dq03_fk_integrity(companies, pl, bs, cf, docs, sectors)
    dq04_bs_balance(bs)
    dq05_opm_crosscheck(pl)
    dq06_positive_sales(pl)
    dq07_year_format(pl, bs, cf)
    dq08_ticker_format(companies)
    dq09_net_cash_check(cf)
    dq10_nonneg_fixed_assets(bs)
    dq11_tax_rate(pl)
    dq12_dividend_cap(pl)
    dq13_url_validity(docs)
    dq14_eps_sign(pl)
    dq15_bs_strict_balance(bs)
    dq16_coverage_check(pl, bs, cf, companies)

    df = save_failures()
    critical = df[df["severity"] == "CRITICAL"]
    warning  = df[df["severity"] == "WARNING"]
    logger.info(f"CRITICAL: {len(critical)} | WARNING: {len(warning)}")