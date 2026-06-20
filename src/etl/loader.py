import pandas as pd
import logging
from pathlib import Path
from src.etl.normaliser import normalize_year, normalize_ticker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RAW = Path("data/raw")
SUP = Path("data/supporting")

def load_companies() -> pd.DataFrame:
    """Load companies.xlsx"""
    df = pd.read_excel(RAW / "companies.xlsx", header=1)
    df["id"] = df["id"].apply(normalize_ticker)
    logger.info(f"companies: {len(df)} rows loaded")
    return df

def load_profitandloss() -> pd.DataFrame:
    """Load profitandloss.xlsx"""
    df = pd.read_excel(RAW / "profitandloss.xlsx", header=1)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    df["year"] = df["year"].apply(normalize_year)
    df = df[df["year"] != "PARSE_ERROR"]
    df = df.drop_duplicates(subset=["company_id", "year"], keep="last")
    logger.info(f"profitandloss: {len(df)} rows loaded")
    return df

def load_balancesheet() -> pd.DataFrame:
    """Load balancesheet.xlsx"""
    df = pd.read_excel(RAW / "balancesheet.xlsx", header=1)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    df["year"] = df["year"].apply(normalize_year)
    df = df[df["year"] != "PARSE_ERROR"]
    df = df.drop_duplicates(subset=["company_id", "year"], keep="last")
    logger.info(f"balancesheet: {len(df)} rows loaded")
    return df

def load_cashflow() -> pd.DataFrame:
    """Load cashflow.xlsx"""
    df = pd.read_excel(RAW / "cashflow.xlsx", header=1)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    df["year"] = df["year"].apply(normalize_year)
    df = df[df["year"] != "PARSE_ERROR"]
    df = df.drop_duplicates(subset=["company_id", "year"], keep="last")
    logger.info(f"cashflow: {len(df)} rows loaded")
    return df

def load_analysis() -> pd.DataFrame:
    """Load analysis.xlsx"""
    df = pd.read_excel(RAW / "analysis.xlsx", header=1)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    logger.info(f"analysis: {len(df)} rows loaded")
    return df

def load_documents() -> pd.DataFrame:
    """Load documents.xlsx"""
    df = pd.read_excel(RAW / "documents.xlsx", header=1)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    logger.info(f"documents: {len(df)} rows loaded")
    return df

def load_prosandcons() -> pd.DataFrame:
    """Load prosandcons.xlsx"""
    df = pd.read_excel(RAW / "prosandcons.xlsx", header=1)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    logger.info(f"prosandcons: {len(df)} rows loaded")
    return df

def load_sectors() -> pd.DataFrame:
    """Load sectors.xlsx"""
    df = pd.read_excel(SUP / "sectors.xlsx", header=0)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    logger.info(f"sectors: {len(df)} rows loaded")
    return df

def load_stock_prices() -> pd.DataFrame:
    """Load stock_prices.xlsx"""
    df = pd.read_excel(SUP / "stock_prices.xlsx", header=0)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    logger.info(f"stock_prices: {len(df)} rows loaded")
    return df

def load_market_cap() -> pd.DataFrame:
    """Load market_cap.xlsx"""
    df = pd.read_excel(SUP / "market_cap.xlsx", header=0)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    logger.info(f"market_cap: {len(df)} rows loaded")
    return df

def load_financial_ratios() -> pd.DataFrame:
    """Load financial_ratios.xlsx"""
    df = pd.read_excel(SUP / "financial_ratios.xlsx", header=0)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    logger.info(f"financial_ratios: {len(df)} rows loaded")
    return df

def load_peer_groups() -> pd.DataFrame:
    """Load peer_groups.xlsx"""
    df = pd.read_excel(SUP / "peer_groups.xlsx", header=0)
    df["company_id"] = df["company_id"].apply(normalize_ticker)
    logger.info(f"peer_groups: {len(df)} rows loaded")
    return df

if __name__ == "__main__":
    load_companies()
    load_profitandloss()
    load_balancesheet()
    load_cashflow()
    load_analysis()
    load_documents()
    load_prosandcons()
    load_sectors()
    load_stock_prices()
    load_market_cap()
    load_financial_ratios()
    load_peer_groups()
    logger.info("All 12 files loaded successfully!")