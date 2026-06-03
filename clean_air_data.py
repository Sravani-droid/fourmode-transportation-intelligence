import pandas as pd
import os

RAW_FOLDER = "Dataset/Air_raw"
OUTPUT_FOLDER = "Cleaned_Data"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(RAW_FOLDER):

    if not file.endswith(".csv"):
        continue

    path = os.path.join(RAW_FOLDER, file)

    print(f"\nCleaning {file}...")

    df = pd.read_csv(path)

    print("Original rows:", len(df))

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df = df.drop_duplicates()

    df = df.fillna("Unknown")

    output_name = f"cleaned_{file}"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_name
    )

    df.to_csv(output_path, index=False)

    print("Cleaned rows:", len(df))
    print("Saved:", output_path)

print("\nAir data cleaning completed.")