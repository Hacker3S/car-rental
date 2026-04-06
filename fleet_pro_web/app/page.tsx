import { getDb } from '@/lib/db'
import { Car, CheckCircle, Clock } from 'lucide-react'

export default async function Dashboard() {
  const db = await getDb()
  const totalCarsRaw = await db.get(`SELECT COUNT(*) as c FROM cars`)
  const totalCars = totalCarsRaw?.c || 0
  
  const availableRaw = await db.get(`SELECT COUNT(*) as c FROM cars WHERE status='Available'`)
  const available = availableRaw?.c || 0
  
  const activeRaw = await db.get(`SELECT COUNT(*) as c FROM transactions WHERE status='Active'`)
  const activeRentals = activeRaw?.c || 0
  
  const recentTx = await db.all(`
    SELECT t.id, c.name, cr.brand, cr.model, t.status, t.total_cost 
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    JOIN cars cr ON t.car_id = cr.id
    ORDER BY t.id DESC LIMIT 5
  `) || []

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
                  <td className="p-4 font-medium">${tx.total_cost.toFixed(2)}</td>
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
