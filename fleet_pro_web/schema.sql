-- TABLE: suppliers
CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL
        );

-- TABLE: sqlite_sequence
CREATE TABLE sqlite_sequence(name,seq);

-- TABLE: cars
CREATE TABLE cars (
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
        );

-- TABLE: customers
CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            license_num TEXT NOT NULL,
            total_rentals INTEGER DEFAULT 0
        );

-- TABLE: transactions
CREATE TABLE transactions (
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
        );

-- TABLE: settings
CREATE TABLE settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

