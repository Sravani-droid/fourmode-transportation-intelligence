import pandas as pd
from pathlib import Path

CLEAN_FOLDER = Path("Cleaned_Data")

files = [
    "cleaned_loads.csv",
    "cleaned_trips.csv",
    "cleaned_routes.csv",
    "cleaned_logistics_shipments_dataset.csv"
]

for file in files:
    print("\n" + "="*80)
    print(file)
    print("="*80)

    df = pd.read_csv(CLEAN_FOLDER / file)

    print("\nROWS:", len(df))
    print("\nCOLUMNS:")
    print(df.columns.tolist())

    print("\nFIRST 5 ROWS:")
    print(df.head())