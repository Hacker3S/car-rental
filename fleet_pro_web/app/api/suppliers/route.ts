import { NextRequest, NextResponse } from 'next/server'
import { getDb } from '@/lib/db'

export async function GET() {
  const db = await getDb()
  const suppliers = await db.all(`
    SELECT s.id, s.name, s.contact, COUNT(c.id) as cars_supplied
    FROM suppliers s LEFT JOIN cars c ON s.id = c.supplier_id
    GROUP BY s.id ORDER BY s.id DESC
  `)
  return NextResponse.json(suppliers)
}

export async function POST(req: NextRequest) {
  const db = await getDb()
  const { name, contact } = await req.json()
  const result = await db.run(
    `INSERT INTO suppliers (name, contact) VALUES (?, ?)`,
    [name, contact]
  )
  return NextResponse.json({ id: result.lastID })
}
