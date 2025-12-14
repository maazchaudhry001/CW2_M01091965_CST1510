from database.schema import create_connection, create_tables
from database.seed_data import seed
from database.loader import load_vehicles


def test_loader_loads_correct_types():
    conn = create_connection(":memory:")
    create_tables(conn)
    seed(conn)
    vehicles = load_vehicles(conn)
    # Expect 3 rows as defined in seed
    assert len(vehicles) == 3
    # First is a generic Vehicle (num_doors None)
    assert type(vehicles[0]).__name__ == "Vehicle"
    # Second and third are Cars
    assert type(vehicles[1]).__name__ == "Car"
    assert type(vehicles[2]).__name__ == "Car"
