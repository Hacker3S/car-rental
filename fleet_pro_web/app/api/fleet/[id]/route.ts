import { NextRequest, NextResponse } from 'next/server'
import { getDb } from '@/lib/db'

export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const db = await getDb()
  const { id } = await params
  const data = await req.json()
  const { brand, model, year, category, price_per_day, mileage, supplier_id, status } = data
  
  const mid = Number(id)
  const safe_year = Number(year || 0)
  const safe_price = Number(price_per_day || 0)
  const safe_mileage = Number(mileage || 0)
  const safe_supplier = supplier_id ? Number(supplier_id) : null

  console.log("🛠️ UPDATING CAR:", { mid, brand, model, safe_year, safe_price, safe_mileage, status })

  await db.run(
    `UPDATE cars SET brand=?, model=?, year=?, category=?, price_per_day=?, mileage=?, supplier_id=?, status=? WHERE id=?`,
    [brand || '', model || '', safe_year, category || '', safe_price, safe_mileage, safe_supplier, status || 'Available', mid]
  )
  return NextResponse.json({ ok: true })
}

export async function DELETE(_req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const db = await getDb()
  const { id } = await params
  await db.run(`DELETE FROM cars WHERE id=?`, [id])
  return NextResponse.json({ ok: true })
}
