PRAGMA foreign_keys = ON;

-- Table 1: companies (master reference)
CREATE TABLE IF NOT EXISTS companies (
    id                  TEXT PRIMARY KEY,
    company_name        TEXT NOT NULL,
    company_logo        TEXT,
    chart_link          TEXT,
    about_company       TEXT,
    website             TEXT,
    nse_profile         TEXT,
    bse_profile         TEXT,
    face_value          REAL,
    book_value          REAL,
    roce_percentage     REAL,
    roe_percentage      REAL
);

-- Table 2: profitandloss
CREATE TABLE IF NOT EXISTS profitandloss (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id          TEXT NOT NULL,
    year                TEXT NOT NULL,
    sales               REAL,
    expenses            REAL,
    operating_profit    REAL,
    opm_percentage      REAL,
    other_income        REAL,
    interest            REAL,
    depreciation        REAL,
    profit_before_tax   REAL,
    tax_percentage      REAL,
    net_profit          REAL,
    eps                 REAL,
    dividend_payout     REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, year)
);

-- Table 3: balancesheet
CREATE TABLE IF NOT EXISTS balancesheet (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id          TEXT NOT NULL,
    year                TEXT NOT NULL,
    equity_capital      REAL,
    reserves            REAL,
    borrowings          REAL,
    other_liabilities   REAL,
    total_liabilities   REAL,
    fixed_assets        REAL,
    cwip                REAL,
    investments         REAL,
    other_asset         REAL,
    total_assets        REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, year)
);

-- Table 4: cashflow
CREATE TABLE IF NOT EXISTS cashflow (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id          TEXT NOT NULL,
    year                TEXT NOT NULL,
    operating_activity  REAL,
    investing_activity  REAL,
    financing_activity  REAL,
    net_cash_flow       REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, year)
);

-- Table 5: analysis
CREATE TABLE IF NOT EXISTS analysis (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id                  TEXT NOT NULL,
    compounded_sales_growth     TEXT,
    compounded_profit_growth    TEXT,
    stock_price_cagr            TEXT,
    roe                         TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Table 6: documents
CREATE TABLE IF NOT EXISTS documents (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      TEXT NOT NULL,
    Year            INTEGER,
    Annual_Report   TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Table 7: prosandcons
CREATE TABLE IF NOT EXISTS prosandcons (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id  TEXT NOT NULL,
    pros        TEXT,
    cons        TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Table 8: sectors
CREATE TABLE IF NOT EXISTS sectors (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id          TEXT NOT NULL UNIQUE,
    broad_sector        TEXT,
    sub_sector          TEXT,
    index_weight_pct    REAL,
    market_cap_category TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Table 9: stock_prices
CREATE TABLE IF NOT EXISTS stock_prices (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      TEXT NOT NULL,
    date            TEXT NOT NULL,
    open_price      REAL,
    high_price      REAL,
    low_price       REAL,
    close_price     REAL,
    volume          INTEGER,
    adjusted_close  REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, date)
);

-- Table 10: financial_ratios
CREATE TABLE IF NOT EXISTS financial_ratios (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id                  TEXT NOT NULL,
    year                        TEXT NOT NULL,
    net_profit_margin_pct       REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct        REAL,
    debt_to_equity              REAL,
    interest_coverage           REAL,
    asset_turnover              REAL,
    free_cash_flow_cr           REAL,
    capex_cr                    REAL,
    earnings_per_share          REAL,
    book_value_per_share        REAL,
    dividend_payout_ratio_pct   REAL,
    total_debt_cr               REAL,
    cash_from_operations_cr     REAL,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, year)
);