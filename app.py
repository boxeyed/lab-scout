import pandas as pd
 
CSV_PATH = "sample_data.csv"
 
 
def load_records():
    """Read the CSV and return a list of row dictionaries."""
    df = pd.read_csv(CSV_PATH)
    return df.to_dict(orient='records')