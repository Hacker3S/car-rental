import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'fleet_pro.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            category TEXT NOT NULL,
            price_per_day REAL NOT NULL,
            mileage INTEGER NOT NULL,
            supplier_id INTEGER,
            status TEXT NOT NULL,
            FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            license_num TEXT NOT NULL,
            total_rentals INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            car_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            total_cost REAL NOT NULL,
            status TEXT NOT NULL,
            return_date TEXT,
            penalty REAL DEFAULT 0.0,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(car_id) REFERENCES cars(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    
    # Check if we need to seed
    cursor.execute("SELECT COUNT(*) FROM cars")
    if cursor.fetchone()[0] == 0:
        seed_data(conn)
        
    conn.close()

def seed_data(conn):
    cursor = conn.cursor()
    
    # 3 Suppliers
    suppliers = [
        ('AutoCorp', 'contact@autocorp.com'),
        ('Global Fleet', 'sales@globalfleet.com'),
        ('Premium Wheels', 'info@premiumwheels.com')
    ]
    cursor.executemany("INSERT INTO suppliers (name, contact) VALUES (?, ?)", suppliers)
    
    # 5 Customers
    customers = [
        ('Alice Smith', 'alice@example.com', 'LIC12345', 2),
        ('Bob Johnson', 'bob@example.com', 'LIC98765', 1),
        ('Charlie Brown', 'charlie@example.com', 'LIC11111', 1),
        ('Diana Prince', 'diana@example.com', 'LIC22222', 2),
        ('Evan Wright', 'evan@example.com', 'LIC33333', 0)
    ]
    cursor.executemany("INSERT INTO customers (name, contact, license_num, total_rentals) VALUES (?, ?, ?, ?)", customers)
    
    # 8 Cars
    cars = [
        ('Toyota', 'Camry', 2022, 'Sedan', 45.0, 15000, 1, 'Available'),
        ('Honda', 'Civic', 2023, 'Sedan', 40.0, 10000, 1, 'Available'),
        ('Ford', 'Explorer', 2021, 'SUV', 65.0, 30000, 2, 'Available'),
        ('Jeep', 'Grand Cherokee', 2022, 'SUV', 70.0, 25000, 2, 'Available'),
        ('BMW', '3 Series', 2023, 'Luxury', 100.0, 5000, 3, 'Available'),
        ('Mercedes', 'C-Class', 2022, 'Luxury', 110.0, 8000, 3, 'Available'),
        ('Nissan', 'Altima', 2021, 'Sedan', 38.0, 40000, 1, 'Rented'),
        ('Audi', 'Q5', 2023, 'SUV', 85.0, 6000, 3, 'Maintenance')
    ]
    cursor.executemany("INSERT INTO cars (brand, model, year, category, price_per_day, mileage, supplier_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", cars)
    
    # 6 Transactions
    transactions = [
        (1, 1, '2025-01-10', '2025-01-12', 90.0, 'Completed', '2025-01-12', 0.0),
        (2, 2, '2025-02-05', '2025-02-10', 200.0, 'Completed', '2025-02-10', 0.0),
        (3, 3, '2025-03-01', '2025-03-05', 260.0, 'Completed', '2025-03-05', 0.0),
        (1, 4, '2025-03-15', '2025-03-20', 350.0, 'Completed', '2025-03-20', 0.0),
        (4, 5, '2025-03-10', '2025-03-12', 200.0, 'Completed', '2025-03-13', 50.0),
        (4, 7, '2025-03-25', '2025-03-30', 190.0, 'Active', None, 0.0)
    ]
    cursor.executemany("INSERT INTO transactions (customer_id, car_id, start_date, end_date, total_cost, status, return_date, penalty) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", transactions)
    
    # Default settings
    settings = [
        ('low_fleet_threshold', '2'),
        ('late_penalty_rate', '50.0'),
        ('currency_symbol', '$'),
        ('theme', 'Dark')
    ]
    cursor.executemany("INSERT INTO settings (key, value) VALUES (?, ?)", settings)
    
    conn.commit()

if __name__ == '__main__':
    initialize_db()
    print("Database initialized successfully.")
