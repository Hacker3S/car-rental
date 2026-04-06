from storage.file_handler import FileHandler
from models.car import Car
from models.customer import Customer
from models.supplier import Supplier
from managers.inventory import Inventory
from managers.rental_manager import RentalManager
from managers.supplier_manager import SupplierManager
from managers.report_generator import ReportGenerator

def run_tests():
    print("Setting up test environment in 'test_data'...")
    fh = FileHandler(data_dir="test_data")
    inv = Inventory(fh)
    rm = RentalManager(fh, inv)
    sm = SupplierManager(fh, inv)
    rg = ReportGenerator(inv, rm)

    print("--- Testing Inventory Add ---")
    try:
        c1 = Car("C001", "Toyota", "Camry", 2022, "sedan", 50.0)
        c2 = Car("C002", "Honda", "CRV", 2021, "SUV", 70.0)
        inv.add_car(c1)
        inv.add_car(c2)
        print("Cars added successfully.")
    except Exception as e:
        print(f"Inventory Add failed: {e}")

    print("--- Testing Customer/Supplier Add ---")
    cu1 = Customer("U001", "Alice", "123-456", "DL123")
    rm.register_customer(cu1)
    s1 = Supplier("S001", "FleetCo", "contact@fleet.com")
    sm.add_supplier(s1)
    print("Users added successfully.")

    print("--- Testing Booking ---")
    tx1 = rm.book_car("U001", "C001", "2023-10-01", "2023-10-05")
    # Should cost 50.0 * 5 days = 250.0
    print(f"Booked! TX: {tx1.transaction_id}, Cost: {tx1.total_cost}")

    print("--- Testing Overlapping Conflict ---")
    try:
        rm.book_car("U001", "C001", "2023-10-04", "2023-10-08")
        print("FAIL: Conflict not detected")
    except ValueError as e:
        print(f"SUCCESS: Conflict detected - {e}")

    print("--- Testing Return & Billing (Late Return) ---")
    # Return 1 day late (2023-10-06 instead of 2023-10-05)
    # 1 day late * (50 * 1.5) = 75
    # Total = 250 + 75 = 325
    tx1_ret, penalty = rm.return_car(tx1.transaction_id, "2023-10-06", 150)
    print(f"Returned! Final cost: {tx1_ret.total_cost}, Late Penalty: {penalty}")

    print("--- Testing Reports ---")
    print(f"Available cars: {len(rg.available_cars_report())}") # should be 2
    print(f"Total revenue: {rg.revenue_report()}") # should be 325.0
    print(f"Most rented cars: {rg.most_rented_cars()}") # C001: 1

    print("\nAll integration tests complete. You may verify the test_data/ folder contents.")

if __name__ == "__main__":
    run_tests()
