import pandas as pd
import os

cargo = pd.read_csv(
    "Cleaned_Data/cleaned_Air_Traffic_Cargo_Statistics.csv"
)

passengers = pd.read_csv(
    "Cleaned_Data/cleaned_Air_Traffic_Passenger_Statistics.csv"
)

OUTPUT_FOLDER = "Cleaned_Data/air_outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------
# Main KPIs
# -------------------

total_cargo_tons = cargo["cargo_metric_tons"].sum()

total_passengers = passengers["passenger_count"].sum()

air_kpis = pd.DataFrame({
    "total_cargo_tons":[total_cargo_tons],
    "total_passengers":[total_passengers]
})

air_kpis.to_csv(
    f"{OUTPUT_FOLDER}/air_kpis.csv",
    index=False
)

# -------------------
# Airline Analysis
# -------------------

airline_analysis = (
    cargo.groupby("operating_airline")
    .agg({
        "cargo_metric_tons":"sum"
    })
    .sort_values(
        "cargo_metric_tons",
        ascending=False
    )
    .head(20)
)

airline_analysis.to_csv(
    f"{OUTPUT_FOLDER}/airline_analysis.csv"
)

# -------------------
# Region Analysis
# -------------------

region_analysis = (
    cargo.groupby("geo_region")
    .agg({
        "cargo_metric_tons":"sum"
    })
    .sort_values(
        "cargo_metric_tons",
        ascending=False
    )
)

region_analysis.to_csv(
    f"{OUTPUT_FOLDER}/region_analysis.csv"
)

# -------------------
# Passenger Airlines
# -------------------

passenger_airlines = (
    passengers.groupby("operating_airline")
    .agg({
        "passenger_count":"sum"
    })
    .sort_values(
        "passenger_count",
        ascending=False
    )
    .head(20)
)

passenger_airlines.to_csv(
    f"{OUTPUT_FOLDER}/passenger_airlines.csv"
)

print("Air KPI files created successfully.")