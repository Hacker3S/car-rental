'use client'
import { useEffect, useState } from 'react'
import { Plus, CalendarDays, RotateCcw } from 'lucide-react'
import { Modal, Field } from '@/components/Modal'

type Transaction = {
  id: number; customer: string; car: string
  start_date: string; end_date: string
  total_cost: number; status: string; penalty?: number; car_id?: number
}
type Customer = { id: number; name: string }
type Car = { id: number; brand: string; model: string; price_per_day: number }

export const dynamic = 'force-dynamic'

export default function BookingsPage() {
  const [active, setActive] = useState<Transaction[]>([])
  const [all, setAll] = useState<Transaction[]>([])
  const [tab, setTab] = useState<'active' | 'all'>('active')
  const [customers, setCustomers] = useState<Customer[]>([])
  const [cars, setCars] = useState<Car[]>([])
  const [showNew, setShowNew] = useState(false)
  const [returning, setReturning] = useState<Transaction | null>(null)
  const [penalty, setPenalty] = useState(0)
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    const [bookings, custsRes, carsRes] = await Promise.all([
      fetch('/api/bookings').then(r => r.json()),
      fetch('/api/customers').then(r => r.json()),
      fetch('/api/fleet').then(r => r.json()),
    ])
    setActive(bookings.active); setAll(bookings.all)
    setCustomers(custsRes)
    setCars(carsRes.filter((c: { status: string }) => c.status === 'Available'))
    setLoading(false)
  }
  useEffect(() => { load() }, [])

  const calcCost = (startDate: string, endDate: string, pricePerDay: number) => {
    const days = Math.max(1, Math.ceil((new Date(endDate).getTime() - new Date(startDate).getTime()) / 86400000))
    return days * pricePerDay
  }

  const handleNewBooking = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const fd = new FormData(e.currentTarget)
    const start = fd.get('start_date') as string
    const end = fd.get('end_date') as string
    const car_id = Number(fd.get('car_id'))
    const car = cars.find(c => c.id === car_id)
    const cost = calcCost(start, end, car?.price_per_day ?? 0)
    await fetch('/api/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customer_id: Number(fd.get('customer_id')), car_id, start_date: start, end_date: end, total_cost: cost }),
    })
    setShowNew(false); load()
  }

  const openReturn = (tx: Transaction) => {
    const today = new Date()
    const end = new Date(tx.end_date)
    const daysLate = Math.max(0, Math.ceil((today.getTime() - end.getTime()) / 86400000))
    setPenalty(daysLate * 50)
    setReturning(tx)
  }

  const handleReturn = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!returning) return
    const fd = new FormData(e.currentTarget)
    await fetch(`/api/bookings/${returning.id}/return`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ car_id: returning.car_id, penalty, mileage: Number(fd.get('mileage')) }),
    })
    setReturning(null); load()
  }

  const STATUS_COLORS: Record<string, string> = {
    Active: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    Completed: 'bg-green-500/10 text-green-400 border-green-500/20',
  }

  return (
    <div className="flex flex-col gap-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Bookings</h1>
          <p className="text-muted-foreground mt-1 text-sm">{active.length} active rental{active.length !== 1 ? 's' : ''}</p>
        </div>
        <button onClick={() => setShowNew(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
          <Plus size={16} /> New Booking
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 p-1 bg-muted rounded-lg w-fit">
        {(['active', 'all'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-1.5 rounded-md text-sm font-medium transition ${tab === t ? 'bg-background shadow text-foreground' : 'text-muted-foreground hover:text-foreground'}`}>
            {t === 'active' ? `Active Rentals (${active.length})` : `All Transactions (${all.length})`}
          </button>
        ))}
      </div>

      {/* Active Rentals Table */}
      {tab === 'active' && (
        <div className="border border-border rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-muted text-muted-foreground">
              <tr>
                {['ID', 'Customer', 'Car', 'Start Date', 'End Date', 'Total Cost', 'Actions'].map(h => (
                  <th key={h} className="text-left p-3 font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {loading ? (
                <tr><td colSpan={7} className="p-8 text-center text-muted-foreground">Loading...</td></tr>
              ) : active.length === 0 ? (
                <tr><td colSpan={7} className="p-8 text-center text-muted-foreground">
                  <CalendarDays size={36} className="mx-auto mb-2 opacity-30" />No active rentals.
                </td></tr>
              ) : active.map(tx => (
                <tr key={tx.id} className="hover:bg-accent/40 transition-colors">
                  <td className="p-3 text-muted-foreground">#{tx.id}</td>
                  <td className="p-3 font-medium">{tx.customer}</td>
                  <td className="p-3">{tx.car}</td>
                  <td className="p-3 text-muted-foreground">{tx.start_date}</td>
                  <td className="p-3 text-muted-foreground">{tx.end_date}</td>
                  <td className="p-3 font-medium">${Number(tx.total_cost || 0).toFixed(2)}</td>
                  <td className="p-3">
                    <button onClick={() => openReturn(tx)}
                      className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-primary/10 text-primary border border-primary/20 rounded-lg hover:bg-primary/20 transition">
                      <RotateCcw size={12} /> Return Car
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* All Transactions Table */}
      {tab === 'all' && (
        <div className="border border-border rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-muted text-muted-foreground">
              <tr>
                {['ID', 'Customer', 'Car', 'Start', 'End', 'Status', 'Cost', 'Penalty'].map(h => (
                  <th key={h} className="text-left p-3 font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {loading ? (
                <tr><td colSpan={8} className="p-8 text-center text-muted-foreground">Loading...</td></tr>
              ) : all.length === 0 ? (
                <tr><td colSpan={8} className="p-8 text-center text-muted-foreground">No transactions yet.</td></tr>
              ) : all.map(tx => (
                <tr key={tx.id} className="hover:bg-accent/40 transition-colors">
                  <td className="p-3 text-muted-foreground">#{tx.id}</td>
                  <td className="p-3 font-medium">{tx.customer}</td>
                  <td className="p-3">{tx.car}</td>
                  <td className="p-3 text-muted-foreground">{tx.start_date}</td>
                  <td className="p-3 text-muted-foreground">{tx.end_date}</td>
                  <td className="p-3">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium border ${STATUS_COLORS[tx.status] ?? ''}`}>
                      {tx.status}
                    </span>
                  </td>
                  <td className="p-3 font-medium">${Number(tx.total_cost || 0).toFixed(2)}</td>
                  <td className="p-3 text-muted-foreground">
                    {tx.penalty ? <span className="text-amber-400">${Number(tx.penalty || 0).toFixed(2)}</span> : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* New Booking Modal */}
      {showNew && (
        <Modal title="New Booking" onClose={() => setShowNew(false)}>
          <form onSubmit={handleNewBooking} className="flex flex-col gap-4">
            <Field label="Customer" name="customer_id">
              <select name="customer_id" required
                className="px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/40">
                <option value="">Select customer...</option>
                {customers.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </Field>
            <Field label="Car (Available Only)" name="car_id">
              <select name="car_id" required
                className="px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/40">
                <option value="">Select car...</option>
                {cars.map(c => <option key={c.id} value={c.id}>{c.brand} {c.model} — ${c.price_per_day}/day</option>)}
              </select>
            </Field>
            <div className="grid grid-cols-2 gap-4">
              <Field label="Start Date" name="start_date" type="date" required />
              <Field label="End Date" name="end_date" type="date" required />
            </div>
            <button type="submit"
              className="mt-2 w-full py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
              Confirm Booking
            </button>
          </form>
        </Modal>
      )}

      {/* Return Car Modal */}
      {returning && (
        <Modal title={`Return Car — Transaction #${returning.id}`} onClose={() => setReturning(null)}>
          <form onSubmit={handleReturn} className="flex flex-col gap-4">
            <div className="p-4 rounded-lg bg-muted border border-border text-sm flex flex-col gap-1.5">
              <p><span className="text-muted-foreground">Customer:</span> <strong>{returning.customer}</strong></p>
              <p><span className="text-muted-foreground">Car:</span> <strong>{returning.car}</strong></p>
              <p><span className="text-muted-foreground">Due Date:</span> {returning.end_date}</p>
              {penalty > 0 && (
                <p className="text-amber-400 font-medium mt-1">⚠️ Late return penalty: ${penalty.toFixed(2)}</p>
              )}
            </div>
            <Field label="Current Mileage (km)" name="mileage" type="number" required placeholder="e.g. 25000" />
            <button type="submit"
              className="mt-2 w-full py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
              Confirm Return
            </button>
          </form>
        </Modal>
      )}
    </div>
  )
}
