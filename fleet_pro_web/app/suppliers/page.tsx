'use client'
import { useEffect, useState } from 'react'
import { Plus, UserSquare2 } from 'lucide-react'
import { Modal, Field } from '@/components/Modal'

type Supplier = { id: number; name: string; contact: string; cars_supplied: number }

export default function SuppliersPage() {
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [showAdd, setShowAdd] = useState(false)
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    const data = await fetch('/api/suppliers').then(r => r.json())
    setSuppliers(data); setLoading(false)
  }
  useEffect(() => { load() }, [])

  const handleAdd = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const fd = new FormData(e.currentTarget)
    await fetch('/api/suppliers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: fd.get('name'), contact: fd.get('contact') }),
    })
    setShowAdd(false); load()
  }

  return (
    <div className="flex flex-col gap-6 max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Suppliers</h1>
          <p className="text-muted-foreground mt-1 text-sm">{suppliers.length} active suppliers</p>
        </div>
        <button onClick={() => setShowAdd(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
          <Plus size={16} /> Add Supplier
        </button>
      </div>

      {/* Cards Grid */}
      {loading ? (
        <p className="text-muted-foreground text-sm">Loading...</p>
      ) : suppliers.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-muted-foreground gap-3">
          <UserSquare2 size={48} className="opacity-20" />
          <p>No suppliers yet.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {suppliers.map(s => (
            <div key={s.id}
              className="p-5 rounded-xl border border-border bg-card hover:border-primary/40 transition-colors flex flex-col gap-3">
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-semibold text-foreground">{s.name}</p>
                  <p className="text-sm text-muted-foreground mt-0.5">{s.contact}</p>
                </div>
                <span className="text-xs text-muted-foreground bg-muted px-2 py-0.5 rounded-full border border-border">
                  #{s.id}
                </span>
              </div>
              <div className="flex items-center gap-2 mt-1">
                <span className={`px-2.5 py-1 rounded-lg text-xs font-medium ${s.cars_supplied > 0 ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground'}`}>
                  {s.cars_supplied} car{s.cars_supplied !== 1 ? 's' : ''} supplied
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Table fallback for many suppliers */}
      {suppliers.length > 6 && (
        <div className="border border-border rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-muted text-muted-foreground">
              <tr>
                {['ID', 'Name', 'Contact', 'Cars Supplied'].map(h => (
                  <th key={h} className="text-left p-3 font-medium">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {suppliers.map(s => (
                <tr key={s.id} className="hover:bg-accent/40 transition-colors">
                  <td className="p-3 text-muted-foreground">#{s.id}</td>
                  <td className="p-3 font-medium">{s.name}</td>
                  <td className="p-3 text-muted-foreground">{s.contact}</td>
                  <td className="p-3">{s.cars_supplied}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showAdd && (
        <Modal title="Add Supplier" onClose={() => setShowAdd(false)}>
          <form onSubmit={handleAdd} className="flex flex-col gap-4">
            <Field label="Supplier Name" name="name" required placeholder="AutoFleet Co." />
            <Field label="Contact" name="contact" required placeholder="+1 800 000 0000" />
            <button type="submit"
              className="mt-2 w-full py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
              Add Supplier
            </button>
          </form>
        </Modal>
      )}
    </div>
  )
}
