import pandas as pd
import os

rail = pd.read_csv(
    "Dataset/Rail_raw/FAF4.4_State.csv",
    low_memory=False
)

OUTPUT = "Cleaned_Data/rail_outputs"
os.makedirs(OUTPUT, exist_ok=True)

# KPIs

kpis = pd.DataFrame({
    "total_tons_2015":[rail["tons_2015"].sum()],
    "total_value_2015":[rail["value_2015"].sum()],
    "total_ton_miles_2015":[rail["tmiles_2015"].sum()],
    "total_tons_2045":[rail["tons_2045"].sum()],
    "total_value_2045":[rail["value_2045"].sum()]
})

kpis.to_csv(
    f"{OUTPUT}/rail_kpis.csv",
    index=False
)

# Top Origins

origins = (
    rail.groupby("dms_orig")
    .agg({
        "tons_2015":"sum",
        "value_2015":"sum"
    })
    .sort_values(
        "tons_2015",
        ascending=False
    )
    .head(20)
)

origins.to_csv(
    f"{OUTPUT}/top_origins.csv"
)

# Top Destinations

destinations = (
    rail.groupby("dms_dest")
    .agg({
        "tons_2015":"sum",
        "value_2015":"sum"
    })
    .sort_values(
        "tons_2015",
        ascending=False
    )
    .head(20)
)

destinations.to_csv(
    f"{OUTPUT}/top_destinations.csv"
)

# Growth Analysis

growth = (
    rail.groupby("trade_type")
    .agg({
        "tons_2015":"sum",
        "tons_2045":"sum"
    })
)

growth["growth_pct"] = (
    (
        growth["tons_2045"]
        - growth["tons_2015"]
    )
    /
    growth["tons_2015"]
) * 100

growth.to_csv(
    f"{OUTPUT}/growth_analysis.csv"
)

print("Rail KPI files created.")