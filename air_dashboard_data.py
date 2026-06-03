import pandas as pd
import json
import os

air_kpis = pd.read_csv(
    "Cleaned_Data/air_outputs/air_kpis.csv"
)

airlines = pd.read_csv(
    "Cleaned_Data/air_outputs/airline_analysis.csv"
)

passenger_airlines = pd.read_csv(
    "Cleaned_Data/air_outputs/passenger_airlines.csv"
)

regions = pd.read_csv(
    "Cleaned_Data/air_outputs/region_analysis.csv"
)

dashboard_data = {

    "kpis": {
        "total_cargo_tons":
            float(air_kpis["total_cargo_tons"][0]),

        "total_passengers":
            int(air_kpis["total_passengers"][0])
    },

    "top_airlines":
        airlines.head(10).to_dict(
            orient="records"
        ),

    "top_passenger_airlines":
        passenger_airlines.head(10).to_dict(
            orient="records"
        ),

    "regions":
        regions.head(10).to_dict(
            orient="records"
        )
}

os.makedirs("dashboard", exist_ok=True)

with open(
    "dashboard/air_dashboard.json",
    "w"
) as f:

    json.dump(
        dashboard_data,
        f,
        indent=4
    )

print("Air dashboard JSON created.")