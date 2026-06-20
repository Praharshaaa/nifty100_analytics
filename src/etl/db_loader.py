import sqlite3
import pandas as pd
import logging
from pathlib import Path
from src.etl.loader import (
    load_companies, load_profitandloss, load_balancesheet,
    load_cashflow, load_analysis, load_documents, load_prosandcons,
    load_sectors, load_stock_prices, load_financial_ratios
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = Path("db/nifty100.db")
SCHEMA_PATH = Path("db/schema.sql")
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

def get_connection():
    """Get SQLite connection with FK enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_schema(conn):
    """Create all 10 tables from schema.sql."""
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    logger.info("Schema created successfully")

def load_table(conn, df: pd.DataFrame, table: str, audit: list):
    """Load a DataFrame into SQLite table."""
    try:
        rows_in = len(df)
        df.to_sql(table, conn, if_exists="replace", index=False)
        rows_out = pd.read_sql(f"SELECT COUNT(*) as c FROM {table}", conn)["c"][0]
        rejected = rows_in - rows_out
        audit.append({
            "table": table,
            "rows_in": rows_in,
            "rows_out": rows_out,
            "rejected": rejected,
            "status": "OK" if rejected == 0 else "PARTIAL"
        })
        logger.info(f"{table}: {rows_out} rows loaded")
    except Exception as e:
        audit.append({
            "table": table,
            "rows_in": len(df),
            "rows_out": 0,
            "rejected": len(df),
            "status": f"ERROR: {e}"
        })
        logger.error(f"{table}: FAILED — {e}")

def save_audit(audit: list):
    """Save load audit to output/load_audit.csv."""
    df = pd.DataFrame(audit)
    df.to_csv(OUTPUT / "load_audit.csv", index=False)
    logger.info(f"load_audit.csv saved: {len(df)} tables")
    return df

def run():
    """Main ETL pipeline — load all 10 tables."""
    conn = get_connection()
    create_schema(conn)
    audit = []

    load_table(conn, load_companies(),       "companies",       audit)
    load_table(conn, load_profitandloss(),   "profitandloss",   audit)
    load_table(conn, load_balancesheet(),    "balancesheet",    audit)
    load_table(conn, load_cashflow(),        "cashflow",        audit)
    load_table(conn, load_analysis(),        "analysis",        audit)
    load_table(conn, load_documents(),       "documents",       audit)
    load_table(conn, load_prosandcons(),     "prosandcons",     audit)
    load_table(conn, load_sectors(),         "sectors",         audit)
    load_table(conn, load_stock_prices(),    "stock_prices",    audit)
    load_table(conn, load_financial_ratios(),"financial_ratios",audit)

    conn.commit()
    conn.close()

    audit_df = save_audit(audit)
    print("\n=== LOAD AUDIT ===")
    print(audit_df.to_string(index=False))

    # FK check
    conn2 = get_connection()
    fk_check = pd.read_sql("PRAGMA foreign_key_check", conn2)
    conn2.close()
    print(f"\nPRAGMA foreign_key_check → {len(fk_check)} rows")
    if len(fk_check) == 0:
        print("✅ FK integrity PASSED")
    else:
        print("❌ FK violations found!")
        print(fk_check)

if __name__ == "__main__":
    run()