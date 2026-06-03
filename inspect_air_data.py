import pandas as pd

files = [
    "Cleaned_Data/cleaned_Air_Traffic_Cargo_Statistics.csv",
    "Cleaned_Data/cleaned_Air_Traffic_Passenger_Statistics.csv"
]

for file in files:

    print("\n" + "="*80)
    print(file)
    print("="*80)

    df = pd.read_csv(file)

    print("\nROWS:")
    print(len(df))

    print("\nCOLUMNS:")
    print(df.columns.tolist())

    print("\nFIRST 5 ROWS:")
    print(df.head())