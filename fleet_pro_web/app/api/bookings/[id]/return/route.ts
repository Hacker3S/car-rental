import { NextRequest, NextResponse } from 'next/server'
import { getDb } from '@/lib/db'

export async function POST(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const db = await getDb()
  const { id } = await params
  const data = await req.json()
  const { car_id, penalty, mileage } = data
  const today = new Date().toISOString().split('T')[0]
  
  const mid = Number(id)
  const cid = Number(car_id || 0)
  const safe_penalty = Number(penalty || 0)
  const safe_mileage = Number(mileage || 0)

  console.log("🛠️ RETURNING CAR:", { mid, cid, safe_penalty, safe_mileage })

  await db.run(
    `UPDATE transactions SET status='Completed', return_date=?, penalty=? WHERE id=?`,
    [today, safe_penalty, mid]
  )
  await db.run(`UPDATE cars SET status='Available', mileage=? WHERE id=?`, [safe_mileage, cid])
  return NextResponse.json({ ok: true })
}
