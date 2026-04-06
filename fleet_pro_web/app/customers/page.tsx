'use client'
import { useEffect, useState } from 'react'
import { Plus, Users } from 'lucide-react'
import { Modal, Field } from '@/components/Modal'

type Customer = { id: number; name: string; contact: string; license_num: string; total_rentals: number }

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [showAdd, setShowAdd] = useState(false)
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  const load = async () => {
    setLoading(true)
    const data = await fetch('/api/customers').then(r => r.json())
    setCustomers(data); setLoading(false)
  }
  useEffect(() => { load() }, [])

  const filtered = customers.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.contact.includes(search) ||
    c.license_num.toLowerCase().includes(search.toLowerCase())
  )

  const handleAdd = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const fd = new FormData(e.currentTarget)
    await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: fd.get('name'), contact: fd.get('contact'), license_num: fd.get('license_num') }),
    })
    setShowAdd(false); load()
  }

  return (
    <div className="flex flex-col gap-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Customers</h1>
          <p className="text-muted-foreground mt-1 text-sm">{customers.length} registered customers</p>
        </div>
        <button onClick={() => setShowAdd(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
          <Plus size={16} /> Register Customer
        </button>
      </div>

      {/* Search */}
      <input value={search} onChange={e => setSearch(e.target.value)}
        placeholder="Search by name, contact, or license..."
        className="px-4 py-2.5 rounded-lg border border-border bg-background text-foreground text-sm w-full max-w-sm
                   focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary placeholder:text-muted-foreground/50 transition" />

      {/* Table */}
      <div className="border border-border rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-muted text-muted-foreground">
            <tr>
              {['ID', 'Name', 'Contact', 'License No.', 'Total Rentals'].map(h => (
                <th key={h} className="text-left p-3 font-medium">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {loading ? (
              <tr><td colSpan={5} className="p-8 text-center text-muted-foreground">Loading...</td></tr>
            ) : filtered.length === 0 ? (
              <tr><td colSpan={5} className="p-8 text-center text-muted-foreground">
                <Users size={36} className="mx-auto mb-2 opacity-30" />No customers found.
              </td></tr>
            ) : filtered.map(c => (
              <tr key={c.id} className="hover:bg-accent/40 transition-colors">
                <td className="p-3 text-muted-foreground">#{c.id}</td>
                <td className="p-3 font-medium">{c.name}</td>
                <td className="p-3 text-muted-foreground">{c.contact}</td>
                <td className="p-3 font-mono text-xs text-muted-foreground">{c.license_num}</td>
                <td className="p-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium border ${c.total_rentals > 0 ? 'bg-primary/10 text-primary border-primary/20' : 'bg-muted text-muted-foreground border-border'}`}>
                    {c.total_rentals} rental{c.total_rentals !== 1 ? 's' : ''}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showAdd && (
        <Modal title="Register Customer" onClose={() => setShowAdd(false)}>
          <form onSubmit={handleAdd} className="flex flex-col gap-4">
            <Field label="Full Name" name="name" required placeholder="Jane Doe" />
            <Field label="Contact Number" name="contact" required placeholder="+1 555 000 0000" />
            <Field label="License No." name="license_num" required placeholder="DL-1234567" />
            <button type="submit"
              className="mt-2 w-full py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
              Register
            </button>
          </form>
        </Modal>
      )}
    </div>
  )
}
