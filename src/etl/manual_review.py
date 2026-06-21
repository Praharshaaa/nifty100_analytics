import sqlite3
import pandas as pd

conn = sqlite3.connect('db/nifty100.db')
companies = ['POWERGRID', 'BAJFINANCE', 'COALINDIA', 'CHOLAFIN', 'SHRIRAMFIN']

for c in companies:
    print(f'\n=== {c} ===')
    
    # Year coverage
    pl = pd.read_sql(
        f'SELECT year, sales, net_profit, eps FROM profitandloss WHERE company_id = "{c}" ORDER BY year',
        conn
    )
    print(f'P&L rows: {len(pl)} | Years: {pl["year"].min()} to {pl["year"].max()}')
    print(pl.to_string(index=False))
    
    # BS and CF check
    bs = pd.read_sql(f'SELECT COUNT(*) as bs_rows FROM balancesheet WHERE company_id = "{c}"', conn)
    cf = pd.read_sql(f'SELECT COUNT(*) as cf_rows FROM cashflow WHERE company_id = "{c}"', conn)
    print(f'BS rows: {bs["bs_rows"][0]} | CF rows: {cf["cf_rows"][0]}')
    # Companies with < 5 years coverage
print('\n=== Companies with < 5 years P&L coverage ===')
low = pd.read_sql('''
    SELECT company_id, COUNT(DISTINCT year) as years
    FROM profitandloss
    GROUP BY company_id
    HAVING years < 5
    ORDER BY years ASC
''', conn)
print(low.to_string(index=False))

conn.close()