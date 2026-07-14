import sqlite3
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = Path("db/nifty100.db")
OUTPUT  = Path("output")
OUTPUT.mkdir(exist_ok=True)

LOG_PATH = OUTPUT / "ratio_edge_cases.log"


def run_edge_case_review():
    conn = sqlite3.connect(DB_PATH)

    # Load data
    companies = pd.read_sql("SELECT id, company_name, roce_percentage, roe_percentage FROM companies", conn)
    ratios    = pd.read_sql("""
        SELECT company_id, year, return_on_equity_pct, return_on_capital_pct
        FROM financial_ratios
        WHERE year = (SELECT MAX(year) FROM financial_ratios WHERE company_id = financial_ratios.company_id)
    """, conn)
    sectors   = pd.read_sql("SELECT company_id, broad_sector FROM sectors", conn)

    conn.close()

    edge_cases = []

    # Merge
    merged = ratios.merge(companies, left_on="company_id", right_on="id", how="left")
    merged = merged.merge(sectors, on="company_id", how="left")

    for _, row in merged.iterrows():
        company  = row["company_id"]
        name     = row["company_name"]
        sector   = row["broad_sector"]
        is_fin   = sector == "Financials"

        # ROCE cross-check
        computed_roce = row["return_on_capital_pct"]
        source_roce   = row["roce_percentage"]

        if pd.notna(computed_roce) and pd.notna(source_roce) and source_roce != 0:
            diff = abs(computed_roce - source_roce)
            if diff > 5:
                category = "data_source_issue" if is_fin else "formula_discrepancy"
                edge_cases.append({
                    "company_id":   company,
                    "company_name": name,
                    "sector":       sector,
                    "metric":       "ROCE",
                    "computed":     round(computed_roce, 2),
                    "source":       source_roce,
                    "diff":         round(diff, 2),
                    "category":     category,
                    "note": "Financial sector uses sector-relative benchmark" if is_fin
                            else "Possible version difference or formula discrepancy"
                })

        # ROE cross-check
        computed_roe = row["return_on_equity_pct"]
        source_roe   = row["roe_percentage"]

        if pd.notna(computed_roe) and pd.notna(source_roe) and source_roe != 0:
            diff = abs(computed_roe - source_roe)
            if diff > 5:
                edge_cases.append({
                    "company_id":   company,
                    "company_name": name,
                    "sector":       sector,
                    "metric":       "ROE",
                    "computed":     round(computed_roe, 2),
                    "source":       source_roe,
                    "diff":         round(diff, 2),
                    "category":     "version_difference",
                    "note": f"Source ROE={source_roe} may be from different year or methodology"
                })

    # Write log
    with open(LOG_PATH, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("RATIO EDGE CASES LOG — NIFTY 100 Analytics\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total edge cases found: {len(edge_cases)}\n\n")

        for i, ec in enumerate(edge_cases, 1):
            f.write(f"[{i}] {ec['company_id']} — {ec['company_name']}\n")
            f.write(f"    Sector   : {ec['sector']}\n")
            f.write(f"    Metric   : {ec['metric']}\n")
            f.write(f"    Computed : {ec['computed']}%\n")
            f.write(f"    Source   : {ec['source']}%\n")
            f.write(f"    Diff     : {ec['diff']}%\n")
            f.write(f"    Category : {ec['category']}\n")
            f.write(f"    Note     : {ec['note']}\n\n")

    logger.info(f"ratio_edge_cases.log: {len(edge_cases)} entries saved")

    # Summary
    df = pd.DataFrame(edge_cases)
    if len(df) > 0:
        print("\n=== Edge Case Summary ===")
        print(df["category"].value_counts().to_string())
        print(f"\nTotal: {len(df)} edge cases logged")
    else:
        print("No edge cases found!")

    return df


if __name__ == "__main__":
    run_edge_case_review()