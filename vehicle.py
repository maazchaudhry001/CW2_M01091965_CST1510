class Vehicle:
    """Represents a generic vehicle."""

    def __init__(self, make, model, year, fuel_type):
        self.__make = make
        self.__model = model
        self.__year = year
        self.__fuel_type = fuel_type

    def get_make(self):
        return self.__make

    def get_model(self):
        return self.__model

    def get_year(self):
        return self.__year

    def get_fuel_type(self):
        return self.__fuel_type

    def __str__(self):
        return f"{self.__year} {self.__make} {self.__model} ({self.__fuel_type})"


class Car(Vehicle):
    """A car is a specific type of Vehicle with a number of doors."""

    def __init__(self, make, model, year, fuel_type, num_doors):
        super().__init__(make, model, year, fuel_type)
        self.__num_doors = num_doors

    def get_num_doors(self):
        return self.__num_doors

    def is_electric(self):
        return self.get_fuel_type().lower() == "electric"

    def __str__(self):
        base = super().__str__()
        return f"{base} – Car with {self.__num_doors} doors"


if __name__ == "__main__":
    # small self-test similar to the notebook
    generic_vehicle = Vehicle("GenericMake", "ModelX", 2018, "hybrid")
    audi_car = Car("Audi", "A3", 2020, "petrol", num_doors=4)
    tesla = Car("Tesla", "Model 3", 2023, "electric", num_doors=4)

    print(generic_vehicle)
    print(audi_car)
    print(tesla)
    print("Is tesla electric?", tesla.is_electric())
