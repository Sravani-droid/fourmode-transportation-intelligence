import json

with open("dashboard/road_dashboard.json") as f:
    road = json.load(f)

with open("dashboard/air_dashboard.json") as f:
    air = json.load(f)

with open("dashboard/rail_dashboard.json") as f:
    rail = json.load(f)

with open("dashboard/maritime_dashboard.json") as f:
    maritime = json.load(f)

master = {
    "road": road,
    "air": air,
    "rail": rail,
    "maritime": maritime
}

with open(
    "dashboard/transportation_master.json",
    "w"
) as f:
    json.dump(
        master,
        f,
        indent=4
    )

print("Transportation master JSON created.")