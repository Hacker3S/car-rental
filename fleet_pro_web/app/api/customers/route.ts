import { NextRequest, NextResponse } from 'next/server'
import { getDb } from '@/lib/db'

export async function GET() {
  const db = await getDb()
  const customers = await db.all(
    `SELECT id, name, contact, license_num, total_rentals FROM customers ORDER BY id DESC`
  )
  return NextResponse.json(customers)
}

export async function POST(req: NextRequest) {
  const db = await getDb()
  const { name, contact, license_num } = await req.json()
  const result = await db.run(
    `INSERT INTO customers (name, contact, license_num) VALUES (?, ?, ?)`,
    [name, contact, license_num]
  )
  return NextResponse.json({ id: result.lastID })
}
