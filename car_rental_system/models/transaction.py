class RentalTransaction:
    def __init__(self, transaction_id, car_id, customer_id, start_date, end_date=None, total_cost=0.0, status="active"):
        self.transaction_id = transaction_id
        self.car_id = car_id
        self.customer_id = customer_id
        self.start_date = start_date  # ISO format string 'YYYY-MM-DD' OR datetime
        self.end_date = end_date      # ISO format string 'YYYY-MM-DD' OR datetime
        self.total_cost = total_cost
        self.status = status          # active / completed / cancelled

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "car_id": self.car_id,
            "customer_id": self.customer_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_cost": self.total_cost,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        cost_str = f" - Cost: ${self.total_cost:.2f}" if self.status == "completed" else ""
        return f"Transaction {self.transaction_id}: Car {self.car_id} for Customer {self.customer_id} [{self.status.upper()}]{cost_str}"

    def __repr__(self):
        return f"RentalTransaction({self.transaction_id}, Status: {self.status})"
