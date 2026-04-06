from collections import Counter
from datetime import datetime

class ReportGenerator:
    def __init__(self, inventory_manager, rental_manager):
        self.inventory = inventory_manager
        self.rental_manager = rental_manager

    def available_cars_report(self):
        return self.inventory.filter_cars(status="available")

    def revenue_report(self):
        total = sum(tx.total_cost for tx in self.rental_manager.transactions.values() if tx.status == "completed")
        return total

    def monthly_revenue_report(self, year, month):
        total = 0.0
        for tx in self.rental_manager.transactions.values():
            if tx.status == "completed":
                end_date = datetime.strptime(tx.end_date, "%Y-%m-%d")
                if end_date.year == int(year) and end_date.month == int(month):
                    total += tx.total_cost
        return total

    def most_rented_cars(self, top_n=5):
        rented_car_ids = [tx.car_id for tx in self.rental_manager.transactions.values()]
        counter = Counter(rented_car_ids)
        return counter.most_common(top_n)

    def low_fleet_alert(self, threshold=5):
        avail = len(self.available_cars_report())
        return avail < threshold, avail

    def category_inventory_summary(self):
        summary = {}
        for car in self.inventory.get_all_cars():
            summary.setdefault(car.category, {"total": 0, "available": 0})
            summary[car.category]["total"] += 1
            if car.status == "available":
                summary[car.category]["available"] += 1
        return summary

    def customer_rental_history(self, customer_id):
        cust = self.rental_manager.get_customer(customer_id)
        if not cust:
            raise ValueError("Customer not found.")
        return [self.rental_manager.transactions.get(tx_id) for tx_id in cust.rental_history if self.rental_manager.transactions.get(tx_id)]
