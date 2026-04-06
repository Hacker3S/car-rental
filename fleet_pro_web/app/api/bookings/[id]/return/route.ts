import { NextRequest, NextResponse } from 'next/server'
import { getDb } from '@/lib/db'

export async function POST(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const db = await getDb()
  const { id } = await params
  const { car_id, penalty, mileage } = await req.json()
  const today = new Date().toISOString().split('T')[0]
  await db.run(
    `UPDATE transactions SET status='Completed', return_date=?, penalty=? WHERE id=?`,
    [today, penalty, id]
  )
  await db.run(`UPDATE cars SET status='Available', mileage=? WHERE id=?`, [mileage, car_id])
  return NextResponse.json({ ok: true })
}
