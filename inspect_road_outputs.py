import pandas as pd
from pathlib import Path

OUTPUT = Path("Cleaned_Data/road_outputs")

files = [
    "road_kpis.csv",
    "road_route_analysis.csv",
    "road_carrier_analysis.csv",
    "road_risk_summary.csv"
]

for file in files:
    print("\n" + "="*80)
    print(file)
    print("="*80)

    df = pd.read_csv(OUTPUT / file)

    print(df.head(10))