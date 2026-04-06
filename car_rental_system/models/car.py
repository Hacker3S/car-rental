class Car:
    def __init__(self, car_id, brand, model, year, category, rental_price_per_day, status="available", mileage=0, supplier_id=None):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.year = year
        self.category = category  # sedan/SUV/luxury
        self.rental_price_per_day = rental_price_per_day
        self.status = status      # available/rented/maintenance
        self.mileage = mileage
        self.supplier_id = supplier_id

    def to_dict(self):
        return {
            "car_id": self.car_id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "category": self.category,
            "rental_price_per_day": self.rental_price_per_day,
            "status": self.status,
            "mileage": self.mileage,
            "supplier_id": self.supplier_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) [{self.status.upper()}] - ${self.rental_price_per_day:.2f}/day"

    def __repr__(self):
        return f"Car({self.car_id}, {self.brand}, {self.model})"
