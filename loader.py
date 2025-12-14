"""Helpers to load Vehicle/Car objects from the vehicles table."""

from typing import List
from models.vehicle import Vehicle, Car


def load_vehicles(conn) -> List[Vehicle]:
    cur = conn.cursor()
    cur.execute("SELECT id, make, model, year, fuel_type, num_doors FROM vehicles;")
    rows = cur.fetchall()
    results = []
    for _id, make, model, year, fuel_type, num_doors in rows:
        if num_doors is None:
            results.append(Vehicle(make, model, year, fuel_type))
        else:
            results.append(Car(make, model, year, fuel_type, num_doors))
    return results
