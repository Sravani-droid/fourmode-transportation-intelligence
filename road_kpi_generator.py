import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CLEAN = BASE / "Cleaned_Data"
OUTPUT = BASE / "Cleaned_Data" / "road_outputs"
OUTPUT.mkdir(exist_ok=True)

loads = pd.read_csv(CLEAN / "cleaned_loads.csv")
trips = pd.read_csv(CLEAN / "cleaned_trips.csv")
routes = pd.read_csv(CLEAN / "cleaned_routes.csv")
shipments = pd.read_csv(CLEAN / "cleaned_logistics_shipments_dataset.csv")

# Merge loads + trips + routes
road = loads.merge(trips, on="load_id", how="left")
road = road.merge(routes, on="route_id", how="left")

# Calculated fields
road["total_revenue"] = road["revenue"] + road["fuel_surcharge"] + road["accessorial_charges"]
road["revenue_per_mile"] = road["total_revenue"] / road["actual_distance_miles"]
road["idle_risk"] = road["idle_time_hours"].apply(lambda x: "High" if x >= 10 else "Medium" if x >= 5 else "Low")
road["fuel_efficiency_risk"] = road["average_mpg"].apply(lambda x: "High" if x < 6 else "Medium" if x < 7 else "Low")

# Executive KPIs
kpis = {
    "total_loads": len(road),
    "completed_loads": int((road["load_status"] == "Completed").sum()),
    "total_revenue": round(road["total_revenue"].sum(), 2),
    "avg_revenue_per_load": round(road["total_revenue"].mean(), 2),
    "total_miles": round(road["actual_distance_miles"].sum(), 2),
    "avg_distance": round(road["actual_distance_miles"].mean(), 2),
    "total_fuel_gallons": round(road["fuel_gallons_used"].sum(), 2),
    "avg_mpg": round(road["average_mpg"].mean(), 2),
    "total_idle_hours": round(road["idle_time_hours"].sum(), 2),
    "avg_idle_hours": round(road["idle_time_hours"].mean(), 2),
    "avg_revenue_per_mile": round(road["revenue_per_mile"].mean(), 2),
}

pd.DataFrame([kpis]).to_csv(OUTPUT / "road_kpis.csv", index=False)

# Route analysis
route_analysis = (
    road.groupby(["route_id", "origin_city", "origin_state", "destination_city", "destination_state"])
    .agg(
        loads=("load_id", "count"),
        total_revenue=("total_revenue", "sum"),
        total_miles=("actual_distance_miles", "sum"),
        avg_mpg=("average_mpg", "mean"),
        total_idle_hours=("idle_time_hours", "sum"),
        avg_idle_hours=("idle_time_hours", "mean"),
        avg_revenue_per_mile=("revenue_per_mile", "mean"),
    )
    .reset_index()
)

route_analysis["total_revenue"] = route_analysis["total_revenue"].round(2)
route_analysis["avg_mpg"] = route_analysis["avg_mpg"].round(2)
route_analysis["avg_idle_hours"] = route_analysis["avg_idle_hours"].round(2)
route_analysis["avg_revenue_per_mile"] = route_analysis["avg_revenue_per_mile"].round(2)
route_analysis.to_csv(OUTPUT / "road_route_analysis.csv", index=False)

# Driver analysis
driver_analysis = (
    road.groupby("driver_id")
    .agg(
        loads=("load_id", "count"),
        total_revenue=("total_revenue", "sum"),
        total_miles=("actual_distance_miles", "sum"),
        avg_mpg=("average_mpg", "mean"),
        total_idle_hours=("idle_time_hours", "sum"),
        avg_idle_hours=("idle_time_hours", "mean"),
    )
    .reset_index()
)

driver_analysis["revenue_per_mile"] = driver_analysis["total_revenue"] / driver_analysis["total_miles"]
driver_analysis = driver_analysis.round(2)
driver_analysis.to_csv(OUTPUT / "road_driver_analysis.csv", index=False)

# Carrier analysis from shipment dataset
shipments["shipment_date"] = pd.to_datetime(shipments["shipment_date"], errors="coerce")
shipments["delivery_date"] = pd.to_datetime(shipments["delivery_date"], errors="coerce")

carrier_analysis = (
    shipments.groupby("carrier")
    .agg(
        shipments=("shipment_id", "count"),
        avg_cost=("cost", "mean"),
        total_cost=("cost", "sum"),
        avg_distance=("distance_miles", "mean"),
        avg_transit_days=("transit_days", "mean"),
    )
    .reset_index()
    .round(2)
)

carrier_analysis.to_csv(OUTPUT / "road_carrier_analysis.csv", index=False)

# Risk summary
risk_summary = road.groupby(["idle_risk", "fuel_efficiency_risk"]).agg(
    loads=("load_id", "count"),
    total_revenue=("total_revenue", "sum"),
    avg_idle_hours=("idle_time_hours", "mean"),
    avg_mpg=("average_mpg", "mean"),
).reset_index().round(2)

risk_summary.to_csv(OUTPUT / "road_risk_summary.csv", index=False)

print("Road KPI files created successfully.")
print(f"Saved in: {OUTPUT}")