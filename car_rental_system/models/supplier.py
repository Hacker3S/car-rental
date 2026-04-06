class Supplier:
    def __init__(self, supplier_id, name, contact, cars_supplied=None):
        self.supplier_id = supplier_id
        self.name = name
        self.contact = contact
        self.cars_supplied = cars_supplied if cars_supplied is not None else []

    def to_dict(self):
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact": self.contact,
            "cars_supplied": self.cars_supplied
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def add_car_supplied(self, car_id):
        if car_id not in self.cars_supplied:
            self.cars_supplied.append(car_id)

    def __str__(self):
        return f"Supplier [{self.supplier_id}]: {self.name} (Supplies {len(self.cars_supplied)} cars)"

    def __repr__(self):
        return f"Supplier({self.supplier_id}, {self.name})"
