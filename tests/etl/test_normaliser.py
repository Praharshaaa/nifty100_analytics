import pytest
from src.etl.normaliser import normalize_year, normalize_ticker

# ── normalize_year: 20 test cases ──────────────────────────────

def test_year_mar23():
    assert normalize_year("Mar-23") == "2023-03"

def test_year_mar_space_23():
    assert normalize_year("Mar 23") == "2023-03"

def test_year_march_2023():
    assert normalize_year("March-2023") == "2023-03"

def test_year_fy23():
    assert normalize_year("FY23") == "2023-03"

def test_year_fy2023():
    assert normalize_year("FY2023") == "2023-03"

def test_year_dec22():
    assert normalize_year("Dec-22") == "2022-12"

def test_year_jun23():
    assert normalize_year("Jun-23") == "2023-06"

def test_year_sep21():
    assert normalize_year("Sep-21") == "2021-09"

def test_year_already_normalised():
    assert normalize_year("2023-03") == "2023-03"

def test_year_plain_integer():
    assert normalize_year("2023") == "2023-03"

def test_year_jan20():
    assert normalize_year("Jan-20") == "2020-01"

def test_year_feb19():
    assert normalize_year("Feb-19") == "2019-02"

def test_year_apr24():
    assert normalize_year("Apr-24") == "2024-04"

def test_year_may22():
    assert normalize_year("May-22") == "2022-05"

def test_year_aug21():
    assert normalize_year("Aug-21") == "2021-08"

def test_year_oct20():
    assert normalize_year("Oct-20") == "2020-10"

def test_year_nov18():
    assert normalize_year("Nov-18") == "2018-11"

def test_year_jul23():
    assert normalize_year("Jul-23") == "2023-07"

def test_year_garbage():
    assert normalize_year("garbage") == "PARSE_ERROR"

def test_year_empty():
    assert normalize_year("xyz") == "PARSE_ERROR"


# ── normalize_ticker: 15 test cases ────────────────────────────

def test_ticker_tcs():
    assert normalize_ticker("TCS") == "TCS"

def test_ticker_lower():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_strip():
    assert normalize_ticker("  TCS  ") == "TCS"

def test_ticker_mixed_case():
    assert normalize_ticker("Tcs") == "TCS"

def test_ticker_hyphen():
    assert normalize_ticker("BAJAJ-AUTO") == "BAJAJ-AUTO"

def test_ticker_ampersand():
    assert normalize_ticker("M&M") == "M&M"

def test_ticker_hdfcbank():
    assert normalize_ticker("hdfcbank") == "HDFCBANK"

def test_ticker_infy():
    assert normalize_ticker("INFY") == "INFY"

def test_ticker_sbin():
    assert normalize_ticker("sbin") == "SBIN"

def test_ticker_reliance():
    assert normalize_ticker("Reliance") == "RELIANCE"

def test_ticker_ntpc():
    assert normalize_ticker("ntpc") == "NTPC"

def test_ticker_wipro():
    assert normalize_ticker("WIPRO") == "WIPRO"

def test_ticker_too_short():
    assert normalize_ticker("A") == "PARSE_ERROR"

def test_ticker_too_long():
    assert normalize_ticker("AVERYLONGTICKER") == "PARSE_ERROR"

def test_ticker_non_string():
    assert normalize_ticker(123) == "PARSE_ERROR"