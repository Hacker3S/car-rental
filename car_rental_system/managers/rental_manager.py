from models.transaction import RentalTransaction
from models.customer import Customer
from datetime import datetime

class RentalManager:
    def __init__(self, file_handler, inventory_manager):
        self.file_handler = file_handler
        self.inventory = inventory_manager
        
        self.customers_data = self.file_handler.load_data("customers")
        self.customers = {c_id: Customer.from_dict(data) for c_id, data in self.customers_data.items()}
        
        self.transactions_data = self.file_handler.load_data("transactions")
        self.transactions = {t_id: RentalTransaction.from_dict(data) for t_id, data in self.transactions_data.items()}

    def _save_customers(self):
        data = {c_id: cust.to_dict() for c_id, cust in self.customers.items()}
        self.file_handler.save_data("customers", data)

    def _save_transactions(self):
        data = {t_id: tx.to_dict() for t_id, tx in self.transactions.items()}
        self.file_handler.save_data("transactions", data)

    def register_customer(self, customer):
        if customer.customer_id in self.customers:
            raise ValueError(f"Customer with ID {customer.customer_id} already exists.")
        self.customers[customer.customer_id] = customer
        self._save_customers()

    def get_customer(self, customer_id):
        return self.customers.get(customer_id)

    def get_all_customers(self):
        return list(self.customers.values())

    def book_car(self, customer_id, car_id, start_date_str, end_date_str):
        if customer_id not in self.customers:
            raise ValueError("Customer not registered.")
        
        car = self.inventory.get_car(car_id)
        if not car:
            raise ValueError("Car not found.")
        if car.status != "available":
            raise ValueError("Car already rented or under maintenance.")
            
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            
        if end_date < start_date:
            raise ValueError("Return date cannot be before start date.")

        # Check overlapping active bookings
        for tx in self.transactions.values():
            if tx.car_id == car_id and tx.status == "active":
                tx_start = datetime.strptime(tx.start_date, "%Y-%m-%d")
                tx_end = datetime.strptime(tx.end_date, "%Y-%m-%d")
                if not (end_date < tx_start or start_date > tx_end):
                    raise ValueError(f"Overlapping booking conflict detected with transaction {tx.transaction_id}.")

        # Generate transaction ID mapping to current amount of records
        tx_id = f"TX{len(self.transactions) + 1:04d}"
        
        # Calculate cost
        days = (end_date - start_date).days + 1  # charge for starting day as well
        total_cost = days * car.rental_price_per_day
        
        tx = RentalTransaction(
            transaction_id=tx_id,
            car_id=car_id,
            customer_id=customer_id,
            start_date=start_date_str,
            end_date=end_date_str,
            total_cost=total_cost,
            status="active"
        )
        self.transactions[tx_id] = tx
        
        # Update Customer history
        self.customers[customer_id].add_rental_history(tx_id)
        
        # Update Car status
        self.inventory.update_car(car_id, status="rented")
        
        self._save_transactions()
        self._save_customers()
        return tx

    def return_car(self, transaction_id, return_date_str, added_mileage):
        if transaction_id not in self.transactions:
            raise ValueError("Transaction not found.")
            
        tx = self.transactions[transaction_id]
        if tx.status != "active":
            raise ValueError("This booking is not active/already returned.")
            
        try:
            actual_return = datetime.strptime(return_date_str, "%Y-%m-%d")
            planned_return = datetime.strptime(tx.end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format.")
            
        # Optional: handling return logic earlier than expected
        # For simplicity, calculate strict extra daily fees if returned late.
        # It says "Apply late return penalty if applicable"
        car = self.inventory.get_car(tx.car_id)
        
        days_diff = (actual_return - planned_return).days
        penalty = 0.0
        
        if days_diff > 0:
            # Simple policy: late penalty is 1.5x the daily rate per extra day
            penalty = days_diff * (car.rental_price_per_day * 1.5)
            tx.total_cost += penalty
            
        tx.status = "completed"
        # don't overwrite the original end_date. Keep actual_return as separate, but the model has end_date.
        # Alternatively, we could add return_date to the transaction model.
        tx.end_date = return_date_str
        
        car.mileage += added_mileage
        self.inventory.update_car(car.car_id, status="available", mileage=car.mileage)
        
        self._save_transactions()
        return tx, penalty
