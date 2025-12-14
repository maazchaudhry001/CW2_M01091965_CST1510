from models.vehicle import Vehicle, Car


def test_vehicle_str():
    v = Vehicle("Volvo", "Bus7700", 2015, "diesel")
    assert str(v) == "2015 Volvo Bus7700 (diesel)"


def test_car_str_and_is_electric():
    c = Car("Tesla", "Model 3", 2023, "electric", 4)
    assert "Tesla" in str(c)
    assert c.is_electric() is True


def test_non_electric_car():
    c = Car("Audi", "A3", 2020, "petrol", 4)
    assert c.is_electric() is False
