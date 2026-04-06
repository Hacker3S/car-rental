import { NextRequest, NextResponse } from 'next/server'
import { getDb } from '@/lib/db'

export async function GET() {
  const db = await getDb()
  const cars = await db.all(`
    SELECT c.id, c.brand, c.model, c.year, c.category, c.price_per_day, 
           c.mileage, s.name as supplier, c.status, c.supplier_id
    FROM cars c LEFT JOIN suppliers s ON c.supplier_id = s.id
    ORDER BY c.id DESC
  `)
  return NextResponse.json(cars)
}

export async function POST(req: NextRequest) {
  const db = await getDb()
  const { brand, model, year, category, price_per_day, mileage, supplier_id } = await req.json()
  const result = await db.run(
    `INSERT INTO cars (brand, model, year, category, price_per_day, mileage, supplier_id, status)
     VALUES (?, ?, ?, ?, ?, ?, ?, 'Available')`,
    [brand, model, year, category, price_per_day, mileage, supplier_id || null]
  )
  return NextResponse.json({ id: result.lastID })
}
