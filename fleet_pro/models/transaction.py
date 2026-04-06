from dataclasses import dataclass
from typing import Optional

@dataclass
class Transaction:
    transaction_id: int
    customer_id: int
    car_id: int
    start_date: str
    end_date: str
    total_cost: float
    status: str
    return_date: Optional[str] = None
    penalty: float = 0.0
