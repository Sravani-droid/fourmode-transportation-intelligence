import pandas as pd
import os

df = pd.read_csv(
    "Dataset/Maritime_raw/Daily_Port_Activity_Data_and_Trade_Estimates.csv",
    low_memory=False
)

OUTPUT = "Cleaned_Data/maritime_outputs"
os.makedirs(OUTPUT, exist_ok=True)

# KPIs

kpis = pd.DataFrame({
    "total_portcalls":[df["portcalls"].sum()],
    "total_imports":[df["import"].sum()],
    "total_exports":[df["export"].sum()],
    "total_trade":[
        df["import"].sum()
        + df["export"].sum()
    ]
})

kpis.to_csv(
    f"{OUTPUT}/maritime_kpis.csv",
    index=False
)

# Top Ports

ports = (
    df.groupby("portname")
    .agg({
        "portcalls":"sum",
        "import":"sum",
        "export":"sum"
    })
    .sort_values(
        "portcalls",
        ascending=False
    )
    .head(20)
)

ports.to_csv(
    f"{OUTPUT}/top_ports.csv"
)

# Countries

countries = (
    df.groupby("country")
    .agg({
        "import":"sum",
        "export":"sum"
    })
    .sort_values(
        "import",
        ascending=False
    )
    .head(20)
)

countries.to_csv(
    f"{OUTPUT}/top_countries.csv"
)

# Cargo Types

cargo_types = pd.DataFrame({

    "container":[
        df["import_container"].sum()
        + df["export_container"].sum()
    ],

    "dry_bulk":[
        df["import_dry_bulk"].sum()
        + df["export_dry_bulk"].sum()
    ],

    "general_cargo":[
        df["import_general_cargo"].sum()
        + df["export_general_cargo"].sum()
    ],

    "roro":[
        df["import_roro"].sum()
        + df["export_roro"].sum()
    ],

    "tanker":[
        df["import_tanker"].sum()
        + df["export_tanker"].sum()
    ]
})

cargo_types.to_csv(
    f"{OUTPUT}/cargo_types.csv",
    index=False
)

print("Maritime KPI files created.")