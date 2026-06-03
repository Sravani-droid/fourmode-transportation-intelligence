import pandas as pd
import json
import os

kpis = pd.read_csv(
    "Cleaned_Data/rail_outputs/rail_kpis.csv"
)

origins = pd.read_csv(
    "Cleaned_Data/rail_outputs/top_origins.csv"
)

destinations = pd.read_csv(
    "Cleaned_Data/rail_outputs/top_destinations.csv"
)

growth = pd.read_csv(
    "Cleaned_Data/rail_outputs/growth_analysis.csv"
)

dashboard_data = {

    "kpis": {
        "total_tons_2015":
            float(kpis["total_tons_2015"][0]),

        "total_value_2015":
            float(kpis["total_value_2015"][0]),

        "total_ton_miles_2015":
            float(kpis["total_ton_miles_2015"][0]),

        "total_tons_2045":
            float(kpis["total_tons_2045"][0]),

        "total_value_2045":
            float(kpis["total_value_2045"][0])
    },

    "top_origins":
        origins.head(10).to_dict(
            orient="records"
        ),

    "top_destinations":
        destinations.head(10).to_dict(
            orient="records"
        ),

    "growth":
        growth.to_dict(
            orient="records"
        )
}

with open(
    "dashboard/rail_dashboard.json",
    "w"
) as f:

    json.dump(
        dashboard_data,
        f,
        indent=4
    )

print("Rail dashboard JSON created.")