from dataclasses import dataclass

@dataclass
class Customer:
    customer_id: int
    name: str
    contact: str
    license_num: str
    total_rentals: int
