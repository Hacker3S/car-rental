class Customer:
    def __init__(self, customer_id, name, contact, license_number, rental_history=None):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact
        self.license_number = license_number
        self.rental_history = rental_history if rental_history is not None else []

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "contact": self.contact,
            "license_number": self.license_number,
            "rental_history": self.rental_history
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def add_rental_history(self, transaction_id):
        if transaction_id not in self.rental_history:
            self.rental_history.append(transaction_id)

    def __str__(self):
        return f"Customer [{self.customer_id}]: {self.name} (Contact: {self.contact})"

    def __repr__(self):
        return f"Customer({self.customer_id}, {self.name})"
