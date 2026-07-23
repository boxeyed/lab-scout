import pandas as pd

def test_csv_has_expected_columns():
    df = pd.read_csv("data.csv")
    expected = {"Title", "Topics", "Contact Name", "Contact Email", "Recruiting Status", "Website"}
    assert expected.issubset(set(df.columns))

def test_no_row_has_blank_title():
    df = pd.read_csv("data.csv")
    assert df["Title"].notna().all()
    assert (df["Title"].str.strip() != "").all()

def test_no_row_has_empty_topics():
    df = pd.read_csv("data.csv")
    assert df["Topics"].notna().all()
    assert (df["Topics"].str.strip() != "").all()
