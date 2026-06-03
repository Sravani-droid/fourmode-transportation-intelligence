import pandas as pd

state = pd.read_csv(
    "Dataset/Rail_raw/FAF4.4_State.csv",
    low_memory=False
)

regional = pd.read_csv(
    "Dataset/Rail_raw/FAF4_Regional.csv",
    low_memory=False
)

print("\nSTATE DATASET")
print("=" * 80)
print("Rows:", len(state))
print("Columns:")
print(state.columns.tolist())
print("\nFirst 5 Rows:")
print(state.head())

print("\n\nREGIONAL DATASET")
print("=" * 80)
print("Rows:", len(regional))
print("Columns:")
print(regional.columns.tolist())
print("\nFirst 5 Rows:")
print(regional.head())