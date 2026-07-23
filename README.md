# Lab Scout — v1.5
 
A small command-line-interface tool for finding and adding university research labs by topic. This version reads and writes directly to a CSV file using pandas.
 
## What v1.5 does
- Search labs by topic (exact match against a comma-separated `Topics` column)
- Add a new lab, appended to the CSV
- Simple terminal menu: search, add, quit
## Setup
```bash
pip install pandas
python lab_scout.py
```
 
## Files
| File | Purpose |
|---|---|
| `lab_scout.py` | Everything — CSV reading/writing, search, add, and the terminal menu |
| `data.csv` | Lab data: Title, Topics, Contact Name, Contact Email, Recruiting Status, Website |
| `tests/test_v1.py` | Guard-rail checks on `data.csv`'s shape (see below) |
 
## Tests
`tests/test_v1.py` has 3 checks. Run with `pytest tests/test_v1.py`.
- `test_csv_has_expected_columns` — **passes**
- `test_no_row_has_blank_title` — **passes**
- `test_no_row_has_empty_topics` — **passes**
## Known limitations
- Search is exact-match only (no partial or fuzzy matching)
- The entire CSV is re-read from disk on every search so it won't scale well
- Missing optional fields are stored as the literal string `"-"` rather than left blank
- No validation beyond "are the fields non-empty" when adding a lab

## Next: v2.0
The planned next step is migrating this from a flat CSV to a proper SQLite database.