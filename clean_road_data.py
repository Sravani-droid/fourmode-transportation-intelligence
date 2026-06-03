import pandas as pd
from pathlib import Path

RAW_FOLDER = Path("Dataset/Road_raw")
CLEAN_FOLDER = Path("Cleaned_Data")

CLEAN_FOLDER.mkdir(exist_ok=True)

files = [
    "customers.csv",
    "drivers.csv",
    "driver_monthly_metrics.csv",
    "facilities.csv",
    "fuel_purchases.csv",
    "loads.csv",
    "logistics_shipments_dataset.csv",
    "maintenance_records.csv",
    "routes.csv",
    "safety_incidents.csv",
    "trips.csv",
    "truck_utilization_metrics.csv",
    "trucks.csv"
]

for file in files:
    print(f"\nCleaning {file}...")

    file_path = RAW_FOLDER / file

    if not file_path.exists():
        print(f"Missing file: {file}")
        continue

    df = pd.read_csv(file_path)

    original_rows = len(df)

    df = df.drop_duplicates()
    df = df.dropna(how="all")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    output_file = CLEAN_FOLDER / f"cleaned_{file}"
    df.to_csv(output_file, index=False)

    print(f"Original rows: {original_rows}")
    print(f"Cleaned rows: {len(df)}")
    print(f"Saved to: {output_file}")

print("\nRoad data cleaning completed successfully.")