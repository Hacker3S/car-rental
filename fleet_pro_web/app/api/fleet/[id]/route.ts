import { NextRequest, NextResponse } from 'next/server'
import { getDb } from '@/lib/db'

export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const db = await getDb()
  const { id } = await params
  const { brand, model, year, category, price_per_day, mileage, supplier_id, status } = await req.json()
  await db.run(
    `UPDATE cars SET brand=?, model=?, year=?, category=?, price_per_day=?, mileage=?, supplier_id=?, status=? WHERE id=?`,
    [brand, model, year, category, price_per_day, mileage, supplier_id || null, status, id]
  )
  return NextResponse.json({ ok: true })
}

export async function DELETE(_req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const db = await getDb()
  const { id } = await params
  await db.run(`DELETE FROM cars WHERE id=?`, [id])
  return NextResponse.json({ ok: true })
}
