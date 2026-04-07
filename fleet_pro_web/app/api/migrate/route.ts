import { NextResponse } from 'next/server'
import { getDb } from '@/lib/db'

export async function GET() {
  try {
    const db = await getDb()
    
    console.log("🚀 Starting database migration...")
    
    // Create tables
    await db.run(`
      CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT NOT NULL
      )
    `)
    
    await db.run(`
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
    `)
    
    await db.run(`
      CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT NOT NULL,
        license_num TEXT NOT NULL,
        total_rentals INTEGER DEFAULT 0
      )
    `)
    
    await db.run(`
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
    `)
    
    await db.run(`
      CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
      )
    `)
    
    // Seed sample data ONLY if cars table is empty
    const check = await db.get("SELECT COUNT(*) as c FROM cars")
    if (Number(check?.c || 0) === 0) {
      console.log("🌱 Seeding sample data...")
      
      // Suppliers
      await db.run("INSERT INTO suppliers (name, contact) VALUES (?, ?)", ["Global Motors", "123-456-789"])
      await db.run("INSERT INTO suppliers (name, contact) VALUES (?, ?)", ["Express Fleet", "987-654-321"])
      
      // Cars
      const cars = [
        ["Toyota", "Camry", 2023, "Sedan", 60.0, 5000, 1, "Available"],
        ["Honda", "Civic", 2022, "Sedan", 55.0, 12000, 1, "Available"],
        ["Ford", "Explorer", 2021, "SUV", 95.0, 25000, 2, "Available"],
        ["Tesla", "Model 3", 2024, "Luxury", 120.0, 1500, 2, "Active"],
        ["BMW", "X5", 2022, "Luxury", 150.0, 18000, 1, "Available"],
        ["Hyundai", "Elantra", 2023, "Compact", 45.0, 8000, 2, "Available"],
        ["Chevrolet", "Tahoe", 2021, "SUV", 110.0, 32000, 1, "Available"],
        ["Nissan", "Altima", 2022, "Sedan", 50.0, 15000, 1, "Active"],
        ["Jeep", "Wrangler", 2023, "SUV", 85.0, 4500, 2, "Available"]
      ]
      
      for (const car of cars) {
        await db.run("INSERT INTO cars (brand, model, year, category, price_per_day, mileage, supplier_id, status) VALUES (?,?,?,?,?,?,?,?)", car)
      }

      // Customers
      await db.run("INSERT INTO customers (name, contact, license_num, total_rentals) VALUES (?, ?, ?, ?)", ["John Doe", "555-0101", "LX123456", 1])
      await db.run("INSERT INTO customers (name, contact, license_num, total_rentals) VALUES (?, ?, ?, ?)", ["Jane Smith", "555-0102", "LX987654", 0])
    }

    return NextResponse.json({ success: true, message: "Database initialized successfully!" })
  } catch (err: any) {
    console.error("❌ Migration failed:", err.message)
    return NextResponse.json({ success: false, error: err.message }, { status: 500 })
  }
}
