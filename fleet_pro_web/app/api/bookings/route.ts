import { NextRequest, NextResponse } from 'next/server'
import { getDb } from '@/lib/db'

export async function GET() {
  const db = await getDb()
  const active = await db.all(`
    SELECT t.id, c.name as customer, cr.brand || ' ' || cr.model as car,
           t.start_date, t.end_date, t.total_cost, t.status, cr.id as car_id
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    JOIN cars cr ON t.car_id = cr.id
    WHERE t.status='Active'
    ORDER BY t.id DESC
  `)
  const all = await db.all(`
    SELECT t.id, c.name as customer, cr.brand || ' ' || cr.model as car,
           t.start_date, t.end_date, t.total_cost, t.status, t.penalty
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    JOIN cars cr ON t.car_id = cr.id
    ORDER BY t.id DESC
  `)
  return NextResponse.json({ active, all })
}

export async function POST(req: NextRequest) {
  const db = await getDb()
  const data = await req.json()
  const { customer_id, car_id, start_date, end_date, total_cost } = data
  
  const mid = Number(customer_id || 0)
  const cid = Number(car_id || 0)
  const cost = Number(total_cost || 0)

  if (!mid || !cid) {
    return NextResponse.json({ error: "Missing customer_id or car_id" }, { status: 400 })
  }

  console.log("🛠️ BOOKING DATA:", { mid, cid, start_date, end_date, cost })

  const result = await db.run(
    `INSERT INTO transactions (customer_id, car_id, start_date, end_date, total_cost, status) VALUES (?, ?, ?, ?, ?, 'Active')`,
    [mid, cid, start_date || '', end_date || '', cost]
  )
  await db.run(`UPDATE cars SET status='Rented' WHERE id=?`, [cid])
  await db.run(`UPDATE customers SET total_rentals=total_rentals+1 WHERE id=?`, [mid])
  return NextResponse.json({ id: result.lastID })
}
