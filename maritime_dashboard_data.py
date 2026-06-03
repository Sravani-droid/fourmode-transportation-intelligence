import pandas as pd
import json

kpis = pd.read_csv(
    "Cleaned_Data/maritime_outputs/maritime_kpis.csv"
)

ports = pd.read_csv(
    "Cleaned_Data/maritime_outputs/top_ports.csv"
)

countries = pd.read_csv(
    "Cleaned_Data/maritime_outputs/top_countries.csv"
)

cargo = pd.read_csv(
    "Cleaned_Data/maritime_outputs/cargo_types.csv"
)

dashboard_data = {

    "kpis": {
        "total_portcalls":
            float(kpis["total_portcalls"][0]),

        "total_imports":
            float(kpis["total_imports"][0]),

        "total_exports":
            float(kpis["total_exports"][0]),

        "total_trade":
            float(kpis["total_trade"][0])
    },

    "top_ports":
        ports.head(10).to_dict(
            orient="records"
        ),

    "top_countries":
        countries.head(10).to_dict(
            orient="records"
        ),

    "cargo_mix":
        cargo.to_dict(
            orient="records"
        )
}

with open(
    "dashboard/maritime_dashboard.json",
    "w"
) as f:

    json.dump(
        dashboard_data,
        f,
        indent=4
    )

print("Maritime dashboard JSON created.")