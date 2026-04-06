# Car Rental Management System (Microproject 11)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Storage](https://img.shields.io/badge/Storage-JSON-orange)

## Project Description
A fully functional, menu-driven Car Rental & Inventory Management System built entirely in Python using Object-Oriented Programming (OOP) principles. The system simulates a real-world vehicle leasing business with comprehensive fleet inventory tracking, overlapping booking conflict prevention, and dynamic billing natively persisted locally via auto-save JSON storage, paired with robust exception handling.

## Industry Focus
**Inventory Management / Supply Chain**

## Features
- **Fleet Management**: Add, update, remove, and filter cars by category, price, or availability status.
- **Customer Management**: Register clients and seamlessly track complete historical leasing records.
- **Supplier Tracking**: Track fleet providers and trace back which cars were sourced from which internal supplier.
- **Rental Booking & Returns**: Smart date-based booking logic that dynamically catches overlapping schedule conflicts and automatically computes daily pricing.
- **Dynamic Billing**: Auto-calculates rental costs, strictly applying standard lateness penalties for past-due return operations.
- **Automated Reports**: Generates overall revenue summaries, top-rented vehicle statistics, category summaries, and available supply audits.
- **Low-Fleet Alerts**: Notifies management instantly if available supply drops below a pre-configured alert threshold.

## Project Structure
```text
car_rental_system/
├── data/
│   ├── cars.json
│   ├── customers.json
│   ├── suppliers.json
│   └── transactions.json
├── managers/
│   ├── inventory.py
│   ├── rental_manager.py
│   ├── report_generator.py
│   └── supplier_manager.py
├── models/
│   ├── car.py
│   ├── customer.py
│   ├── supplier.py
│   └── transaction.py
├── storage/
│   └── file_handler.py
├── main.py
├── test_run.py
└── README.md
```

## How to Run

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd car_rental_system
   ```

2. **Install optional dependencies:**
   The application natively utilizes standard Python libraries, but incorporates `colorama` and `pyfiglet` for aesthetic CLI menus and ASCII banners.
   ```bash
   pip install colorama pyfiglet
   ```

3. **Launch the main application:**
   ```bash
   python main.py
   ```

## OOP Concepts Used
- **Classes & Objects**: Core instances mimicking domain nouns (`Car`, `Customer`, `RentalTransaction`, `Inventory`, etc.).
- **Encapsulation**: State manipulation is encapsulated alongside its related behavior (e.g., `Car.mileage` changes via internal manager integrations, `FileHandler` wraps file logic distinct from operations).
- **Abstraction**: Internal calculation and serialization details are fully abstracted away behind high-level manager methods like `rental_manager.book_car()` and `file_handler.save_data()`.
- **Inheritance**: Flexible architecture setup enabling future expansion (e.g., extending standard entities with specific inherited types of models later on).

## Exception Handling Coverage
Robust error trapping exists across the application tying business logic constraints to graceful CLI error messages.
- **Date Manipulation Constraints**: Gracefully aborting bookings proposing reverse chronologies or structurally broken text input.
- **Overlapping Booking Conflicts**: Intercepting transactions targeting cars effectively rented during the requested span.
- **Unknown/Missed Entities**: Catching modifications and booking requests attached to unregistered users, missing vehicles, or unrecorded databases.
- **Drive Consistency Handling**: Transparently recovering natively via empty instantiation block catches for `FileNotFoundError` or malformed payload reads inside isolated JSON repositories.

## Sample Output

> *(Screenshot of CLI Menu and ascii text placeholder here)*

## Author and License
Created as part of Microproject 11.
Licensed under the MIT License.
