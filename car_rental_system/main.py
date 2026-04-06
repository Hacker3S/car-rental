import sys
from colorama import init, Fore, Style
import pyfiglet

from storage.file_handler import FileHandler
from models.car import Car
from models.customer import Customer
from models.supplier import Supplier
from managers.inventory import Inventory
from managers.rental_manager import RentalManager
from managers.supplier_manager import SupplierManager
from managers.report_generator import ReportGenerator

init(autoreset=True)

class CLI:
    def __init__(self):
        self.file_handler = FileHandler(data_dir="data")
        self.inventory = Inventory(self.file_handler)
        self.rental_manager = RentalManager(self.file_handler, self.inventory)
        self.supplier_manager = SupplierManager(self.file_handler, self.inventory)
        self.report_generator = ReportGenerator(self.inventory, self.rental_manager)

    def print_banner(self):
        ascii_banner = pyfiglet.figlet_format("Car Rental System")
        print(Fore.CYAN + ascii_banner)
        print(Style.BRIGHT + "Welcome to the Car Rental & Inventory Management System\n")

    def run(self):
        self.print_banner()
        while True:
            print(Fore.BLUE + "\n--- Main Menu ---")
            print("1. Fleet Inventory Management")
            print("2. Customer Management")
            print("3. Supplier Management")
            print("4. Rental Booking & Returns")
            print("5. Reports")
            print("0. Exit")
            choice = input(Fore.YELLOW + "Select an option: ")

            try:
                if choice == "1":
                    self.fleet_menu()
                elif choice == "2":
                    self.customer_menu()
                elif choice == "3":
                    self.supplier_menu()
                elif choice == "4":
                    self.rental_menu()
                elif choice == "5":
                    self.reports_menu()
                elif choice == "0":
                    print(Fore.GREEN + "Exiting... Goodbye!")
                    sys.exit(0)
                else:
                    print(Fore.RED + "Invalid option, please try again.")
            except Exception as e:
                print(Fore.RED + f"Error: {str(e)}")

    def fleet_menu(self):
        while True:
            print(Fore.BLUE + "\n--- Fleet Inventory Options ---")
            print("1. Add Car")
            print("2. Update Car")
            print("3. Remove Car")
            print("4. View All Cars")
            print("5. Filter Cars")
            print("0. Back to Main Menu")
            choice = input(Fore.YELLOW + "Select an option: ")

            try:
                if choice == "1":
                    car_id = input("Car ID: ")
                    brand = input("Brand: ")
                    model = input("Model: ")
                    year = int(input("Year: "))
                    category = input("Category (sedan/SUV/luxury): ")
                    price = float(input("Rental Price per Day: "))
                    car = Car(car_id, brand, model, year, category, price)
                    self.inventory.add_car(car)
                    print(Fore.GREEN + "Car added successfully.")
                elif choice == "2":
                    car_id = input("Car ID to update: ")
                    status = input("New Status (available/rented/maintenance) [Leave blank to skip]: ")
                    price_str = input("New Price [Leave blank to skip]: ")
                    kwargs = {}
                    if status: kwargs["status"] = status
                    if price_str: kwargs["rental_price_per_day"] = float(price_str)
                    if kwargs:
                        self.inventory.update_car(car_id, **kwargs)
                        print(Fore.GREEN + "Car updated successfully.")
                    else:
                        print("No updates applied.")
                elif choice == "3":
                    car_id = input("Car ID to remove: ")
                    self.inventory.remove_car(car_id)
                    print(Fore.GREEN + "Car removed successfully.")
                elif choice == "4":
                    cars = self.inventory.get_all_cars()
                    for car in cars: print(car)
                elif choice == "5":
                    category = input("Category [Skip]: ") or None
                    status = input("Status [Skip]: ") or None
                    price_str = input("Max Price [Skip]: ")
                    max_price = float(price_str) if price_str else None
                    cars = self.inventory.filter_cars(category, status, max_price)
                    for car in cars: print(car)
                elif choice == "0":
                    break
                else:
                    print(Fore.RED + "Invalid option.")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")

    def customer_menu(self):
        while True:
            print(Fore.BLUE + "\n--- Customer Management ---")
            print("1. Register New Customer")
            print("2. View Customer")
            print("3. View All Customers")
            print("0. Back to Main Menu")
            choice = input(Fore.YELLOW + "Select an option: ")
            
            try:
                if choice == "1":
                    c_id = input("Customer ID: ")
                    name = input("Name: ")
                    contact = input("Contact: ")
                    lic = input("License Number: ")
                    cust = Customer(c_id, name, contact, lic)
                    self.rental_manager.register_customer(cust)
                    print(Fore.GREEN + "Customer registered.")
                elif choice == "2":
                    c_id = input("Customer ID: ")
                    cust = self.rental_manager.get_customer(c_id)
                    if cust:
                        print(cust)
                        history = self.report_generator.customer_rental_history(c_id)
                        print("Rental History:")
                        for tx in history:
                            print(f"  {tx}")
                    else:
                        print(Fore.RED + "Customer not found.")
                elif choice == "3":
                    for cust in self.rental_manager.get_all_customers():
                        print(cust)
                elif choice == "0":
                    break
                else:
                    print(Fore.RED + "Invalid option.")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")

    def supplier_menu(self):
        while True:
            print(Fore.BLUE + "\n--- Supplier Management ---")
            print("1. Add Supplier")
            print("2. Add Car From Supplier")
            print("3. View Suppliers")
            print("0. Back to Main Menu")
            choice = input(Fore.YELLOW + "Select an option: ")
            
            try:
                if choice == "1":
                    s_id = input("Supplier ID: ")
                    name = input("Name: ")
                    contact = input("Contact: ")
                    sup = Supplier(s_id, name, contact)
                    self.supplier_manager.add_supplier(sup)
                    print(Fore.GREEN + "Supplier added.")
                elif choice == "2":
                    s_id = input("Supplier ID: ")
                    car_id = input("New Car ID: ")
                    brand = input("Brand: ")
                    model = input("Model: ")
                    year = int(input("Year: "))
                    category = input("Category: ")
                    price = float(input("Rental Price per Day: "))
                    car = Car(car_id, brand, model, year, category, price)
                    self.supplier_manager.add_car_from_supplier(s_id, car)
                    print(Fore.GREEN + "Car added from supplier.")
                elif choice == "3":
                    for sup in self.supplier_manager.get_all_suppliers():
                        print(sup)
                elif choice == "0":
                    break
                else:
                    print(Fore.RED + "Invalid option.")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")

    def rental_menu(self):
        while True:
            print(Fore.BLUE + "\n--- Rental Booking & Returns ---")
            print("1. Book a Car")
            print("2. Return a Car")
            print("0. Back to Main Menu")
            choice = input(Fore.YELLOW + "Select an option: ")
            
            try:
                if choice == "1":
                    cust_id = input("Customer ID: ")
                    car_id = input("Car ID: ")
                    start = input("Start Date (YYYY-MM-DD): ")
                    end = input("End Date (YYYY-MM-DD): ")
                    tx = self.rental_manager.book_car(cust_id, car_id, start, end)
                    print(Fore.GREEN + f"Booking successful. Transaction ID: {tx.transaction_id}, Cost: ${tx.total_cost:.2f}")
                elif choice == "2":
                    tx_id = input("Transaction ID: ")
                    return_date = input("Return Date (YYYY-MM-DD): ")
                    mileage = int(input("Added Mileage: "))
                    tx, penalty = self.rental_manager.return_car(tx_id, return_date, mileage)
                    print(Fore.GREEN + f"Car returned successfully.")
                    if penalty > 0:
                        print(Fore.RED + f"Late penalty applied: ${penalty:.2f}")
                    print(Fore.CYAN + f"Final Cost: ${tx.total_cost:.2f}")
                elif choice == "0":
                    break
                else:
                    print(Fore.RED + "Invalid option.")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")

    def reports_menu(self):
        while True:
            print(Fore.BLUE + "\n--- Reports ---")
            print("1. Currently Available Cars")
            print("2. Total Revenue")
            print("3. Most Rented Cars")
            print("4. Low-Fleet Alert")
            print("5. Category-wise Summary")
            print("0. Back to Main Menu")
            choice = input(Fore.YELLOW + "Select an option: ")
            
            try:
                if choice == "1":
                    for c in self.report_generator.available_cars_report(): print(c)
                elif choice == "2":
                    print(Fore.GREEN + f"Total Revenue: ${self.report_generator.revenue_report():.2f}")
                elif choice == "3":
                    for car_id, count in self.report_generator.most_rented_cars():
                        print(f"Car {car_id} rented {count} times")
                elif choice == "4":
                    is_low, count = self.report_generator.low_fleet_alert()
                    if is_low:
                        print(Fore.RED + f"ALERT: Only {count} available cars left!")
                    else:
                        print(Fore.GREEN + f"Fleet is healthy. {count} cars available.")
                elif choice == "5":
                    for cat, data in self.report_generator.category_inventory_summary().items():
                        print(f"{cat.capitalize()}: {data['available']}/{data['total']} available")
                elif choice == "0":
                    break
                else:
                    print(Fore.RED + "Invalid option.")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")

if __name__ == "__main__":
    app = CLI()
    app.run()
