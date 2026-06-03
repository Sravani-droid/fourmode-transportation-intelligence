import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUTPUT = BASE / "Cleaned_Data" / "road_outputs"
DASHBOARD = BASE / "dashboard"
DASHBOARD.mkdir(exist_ok=True)

kpis = pd.read_csv(OUTPUT / "road_kpis.csv").iloc[0].to_dict()
routes = pd.read_csv(OUTPUT / "road_route_analysis.csv")
carriers = pd.read_csv(OUTPUT / "road_carrier_analysis.csv")
risk = pd.read_csv(OUTPUT / "road_risk_summary.csv")

def money(value):
    return round(float(value), 2)

# Executive KPI formatting
executive = {
    "total_loads": int(kpis["total_loads"]),
    "completed_loads": int(kpis["completed_loads"]),
    "total_revenue": money(kpis["total_revenue"]),
    "total_revenue_millions": round(kpis["total_revenue"] / 1_000_000, 1),
    "avg_revenue_per_load": money(kpis["avg_revenue_per_load"]),
    "total_miles": money(kpis["total_miles"]),
    "avg_distance": money(kpis["avg_distance"]),
    "total_fuel_gallons": money(kpis["total_fuel_gallons"]),
    "avg_mpg": money(kpis["avg_mpg"]),
    "total_idle_hours": money(kpis["total_idle_hours"]),
    "avg_idle_hours": money(kpis["avg_idle_hours"]),
    "avg_revenue_per_mile": money(kpis["avg_revenue_per_mile"]),
    "recoverable_idle_hours_10pct": money(kpis["total_idle_hours"] * 0.10),
    "recoverable_idle_hours_15pct": money(kpis["total_idle_hours"] * 0.15),
}

# Top routes
top_revenue_routes = (
    routes.sort_values("total_revenue", ascending=False)
    .head(8)
    .to_dict(orient="records")
)

highest_idle_routes = (
    routes.sort_values("avg_idle_hours", ascending=False)
    .head(8)
    .to_dict(orient="records")
)

best_revenue_per_mile_routes = (
    routes.sort_values("avg_revenue_per_mile", ascending=False)
    .head(8)
    .to_dict(orient="records")
)

lowest_mpg_routes = (
    routes.sort_values("avg_mpg", ascending=True)
    .head(8)
    .to_dict(orient="records")
)

# Carrier rankings
lowest_cost_carriers = (
    carriers.sort_values("avg_cost", ascending=True)
    .to_dict(orient="records")
)

fastest_carriers = (
    carriers.sort_values("avg_transit_days", ascending=True)
    .to_dict(orient="records")
)

highest_volume_carriers = (
    carriers.sort_values("shipments", ascending=False)
    .to_dict(orient="records")
)

# Risk summary
risk["risk_segment"] = risk["idle_risk"] + " Idle / " + risk["fuel_efficiency_risk"] + " Fuel Risk"

risk_records = risk.sort_values("loads", ascending=False).to_dict(orient="records")

high_idle = risk[risk["idle_risk"] == "High"]

risk_insight = {
    "high_idle_loads": int(high_idle["loads"].sum()),
    "high_idle_revenue": money(high_idle["total_revenue"].sum()),
    "high_idle_avg_hours": money(high_idle["avg_idle_hours"].mean()),
    "high_idle_revenue_millions": round(high_idle["total_revenue"].sum() / 1_000_000, 1),
}

dashboard_data = {
    "project": {
        "title": "Transportation Intelligence Platform",
        "module": "Road Logistics Intelligence",
        "subtitle": "Operational decision intelligence for freight, fleet, route, and carrier optimization",
        "source": "Logistics Operations Database + US Logistics Performance Dataset",
    },
    "executive_kpis": executive,
    "routes": {
        "top_revenue_routes": top_revenue_routes,
        "highest_idle_routes": highest_idle_routes,
        "best_revenue_per_mile_routes": best_revenue_per_mile_routes,
        "lowest_mpg_routes": lowest_mpg_routes,
    },
    "carriers": {
        "lowest_cost_carriers": lowest_cost_carriers,
        "fastest_carriers": fastest_carriers,
        "highest_volume_carriers": highest_volume_carriers,
    },
    "risk": {
        "risk_summary": risk_records,
        "risk_insight": risk_insight,
    },
    "recommendations": [
        {
            "problem": "High idle capacity",
            "evidence": f"{executive['total_idle_hours']:,.0f} total idle hours identified across road operations.",
            "action": "Improve dispatch planning, driver scheduling, and route sequencing.",
            "impact": f"A 10% idle reduction could recover approximately {executive['recoverable_idle_hours_10pct']:,.0f} productive hours."
        },
        {
            "problem": "Fuel efficiency variation",
            "evidence": f"Average fleet MPG is {executive['avg_mpg']}. Low-MPG routes create avoidable fuel leakage.",
            "action": "Prioritize low-MPG routes for routing review and equipment assignment optimization.",
            "impact": "Improved MPG reduces fuel spend and increases route margin."
        },
        {
            "problem": "Carrier cost variation",
            "evidence": "Carrier average costs vary meaningfully across the shipment dataset.",
            "action": "Shift non-urgent shipments toward lower-cost carriers where service levels are acceptable.",
            "impact": "Carrier mix optimization can reduce transportation spend without reducing service reliability."
        }
    ]
}

output_file = DASHBOARD / "road_dashboard.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, indent=2)

print("Road dashboard JSON created successfully.")
print(f"Saved to: {output_file}")