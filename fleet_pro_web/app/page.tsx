import { getDb } from '@/lib/db'
import { Car, CheckCircle, Clock } from 'lucide-react'

export const dynamic = 'force-dynamic'

export default async function Dashboard() {
  let totalCars = 0
  let available = 0
  let activeRentals = 0
  let recentTx: any[] = []
  let error: string | null = null

  try {
    const db = await getDb()
    const totalCarsRaw = await db.get(`SELECT COUNT(*) as c FROM cars`)
    totalCars = Number(totalCarsRaw?.c || 0)
    
    const availableRaw = await db.get(`SELECT COUNT(*) as c FROM cars WHERE status='Available'`)
    available = Number(availableRaw?.c || 0)
    
    const activeRaw = await db.get(`SELECT COUNT(*) as c FROM transactions WHERE status='Active'`)
    activeRentals = Number(activeRaw?.c || 0)
    
    recentTx = await db.all(`
      SELECT t.id, c.name, cr.brand, cr.model, t.status, t.total_cost 
      FROM transactions t
      JOIN customers c ON t.customer_id = c.id
      JOIN cars cr ON t.car_id = cr.id
      ORDER BY t.id DESC LIMIT 5
    `) || []
  } catch (err: any) {
    console.error("❌ Dashboard Load Error:", err.message)
    error = err.message
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4 text-center p-8 border border-dashed border-border rounded-2xl bg-card/50">
        <div className="text-4xl">🛠️</div>
        <h1 className="text-2xl font-bold text-white">Database Setup Required</h1>
        <p className="text-muted-foreground max-w-md">
          It looks like your database tables haven't been created yet or the connection is missing.
        </p>
        <a 
          href="/api/migrate" 
          className="mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-colors"
        >
          Initialize Database Schema
        </a>
        {error.includes('400') && (
           <p className="text-xs text-muted-foreground/60 mt-4 italic">
             Note: HTTP 400 errors from Turso usually indicate missing tables in the remote database.
           </p>
        )}
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold tracking-tight text-white mb-2">Dashboard</h1>
      
      {available < 2 && (
         <div className="bg-destructive/15 text-destructive border border-destructive p-4 rounded-lg font-medium">
            ⚠️ Low Fleet Alert: Available cars below threshold!
         </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-xl border border-border bg-card text-card-foreground shadow-sm flex flex-col gap-2">
          <div className="flex items-center gap-2 text-muted-foreground"><Car size={18}/> Total Cars</div>
          <div className="text-3xl font-bold">{totalCars}</div>
        </div>
        <div className="p-6 rounded-xl border border-border bg-card text-card-foreground shadow-sm flex flex-col gap-2">
          <div className="flex items-center gap-2 text-muted-foreground"><CheckCircle size={18}/> Available</div>
          <div className="text-3xl font-bold text-green-500">{available}</div>
        </div>
        <div className="p-6 rounded-xl border border-border bg-card text-card-foreground shadow-sm flex flex-col gap-2">
          <div className="flex items-center gap-2 text-muted-foreground"><Clock size={18}/> Active Rentals</div>
          <div className="text-3xl font-bold text-blue-500">{activeRentals}</div>
        </div>
      </div>
      
      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4 text-white">Recent Transactions</h2>
        <div className="border border-border rounded-lg overflow-hidden relative">
          <table className="w-full text-left bg-card text-sm">
            <thead className="bg-muted text-muted-foreground">
              <tr>
                <th className="p-4 font-medium">ID</th>
                <th className="p-4 font-medium">Customer</th>
                <th className="p-4 font-medium">Car</th>
                <th className="p-4 font-medium">Status</th>
                <th className="p-4 font-medium">Amount</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-foreground">
              {recentTx.map((tx: any) => (
                <tr key={tx.id} className="hover:bg-accent/50 transition-colors">
                  <td className="p-4">#{tx.id}</td>
                  <td className="p-4">{tx.name}</td>
                  <td className="p-4">{tx.brand} {tx.model}</td>
                  <td className="p-4">
                     <span className={`px-2 py-1 rounded-full text-xs font-medium ${tx.status==='Active' ? 'bg-blue-500/10 text-blue-500' : 'bg-green-500/10 text-green-500'}`}>
                       {tx.status}
                     </span>
                  </td>
                  <td className="p-4 font-medium">${Number(tx.total_cost || 0).toFixed(2)}</td>
                </tr>
              ))}
              {recentTx.length === 0 && (
                <tr><td colSpan={5} className="p-4 text-center text-muted-foreground">No transactions yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
