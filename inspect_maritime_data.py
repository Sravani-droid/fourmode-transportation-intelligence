import pandas as pd

df = pd.read_csv(
    "Dataset/Maritime_raw/Daily_Port_Activity_Data_and_Trade_Estimates.csv",
    nrows=5,
    low_memory=False
)

print("COLUMNS:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head())