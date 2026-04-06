from dataclasses import dataclass

@dataclass
class Car:
    car_id: int
    brand: str
    model: str
    year: int
    category: str
    price_per_day: float
    mileage: int
    supplier_id: int
    status: str
