'use client'
import { useEffect, useState } from 'react'
import { Plus, Pencil, Trash2, Wrench, Car } from 'lucide-react'
import { Modal, Field } from '@/components/Modal'

type CarRow = {
  id: number; brand: string; model: string; year: number; category: string
  price_per_day: number; mileage: number; supplier: string | null; status: string; supplier_id: number | null
}
type Supplier = { id: number; name: string }

const STATUS_COLORS: Record<string, string> = {
  Available: 'bg-green-500/10 text-green-400 border-green-500/20',
  Rented: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  Maintenance: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
}

export const dynamic = 'force-dynamic'

export default function FleetPage() {
  const [cars, setCars] = useState<CarRow[]>([])
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [filter, setFilter] = useState({ category: 'All', status: 'All' })
  const [showAdd, setShowAdd] = useState(false)
  const [editing, setEditing] = useState<CarRow | null>(null)
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    const [carsRes, supRes] = await Promise.all([
      fetch('/api/fleet').then(r => r.json()),
      fetch('/api/suppliers').then(r => r.json()),
    ])
    setCars(carsRes); setSuppliers(supRes); setLoading(false)
  }
  useEffect(() => { load() }, [])

  const filtered = cars.filter(c =>
    (filter.category === 'All' || c.category === filter.category) &&
    (filter.status === 'All' || c.status === filter.status)
  )

  const handleAdd = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const fd = new FormData(e.currentTarget)
    await fetch('/api/fleet', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        brand: fd.get('brand'), model: fd.get('model'), year: Number(fd.get('year')),
        category: fd.get('category'), price_per_day: Number(fd.get('price_per_day')),
        mileage: Number(fd.get('mileage')), supplier_id: fd.get('supplier_id') || null,
      }),
    })
    setShowAdd(false); load()
  }

  const handleEdit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!editing) return
    const fd = new FormData(e.currentTarget)
    await fetch(`/api/fleet/${editing.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        brand: fd.get('brand'), model: fd.get('model'), year: Number(fd.get('year')),
        category: fd.get('category'), price_per_day: Number(fd.get('price_per_day')),
        mileage: Number(fd.get('mileage')), supplier_id: fd.get('supplier_id') || null,
        status: editing.status,
      }),
    })
    setEditing(null); load()
  }

  const handleDelete = async (car: CarRow) => {
    if (!confirm(`Delete ${car.brand} ${car.model}?`)) return
    await fetch(`/api/fleet/${car.id}`, { method: 'DELETE' })
    load()
  }

  const toggleMaintenance = async (car: CarRow) => {
    const newStatus = car.status === 'Maintenance' ? 'Available' : 'Maintenance'
    await fetch(`/api/fleet/${car.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...car, status: newStatus }),
    })
    load()
  }

  return (
    <div className="flex flex-col gap-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Fleet Management</h1>
          <p className="text-muted-foreground mt-1 text-sm">{cars.length} vehicles total</p>
        </div>
        <button onClick={() => setShowAdd(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
          <Plus size={16} /> Add Car
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-3 flex-wrap">
        {(['All','Sedan','SUV','Luxury'] as const).map(c => (
          <button key={c} onClick={() => setFilter(f => ({...f, category: c}))}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition ${filter.category === c ? 'bg-primary text-primary-foreground border-primary' : 'border-border text-muted-foreground hover:text-foreground hover:border-foreground/30'}`}>
            {c}
          </button>
        ))}
        <div className="w-px bg-border self-stretch mx-1" />
        {(['All','Available','Rented','Maintenance'] as const).map(s => (
          <button key={s} onClick={() => setFilter(f => ({...f, status: s}))}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition ${filter.status === s ? 'bg-primary text-primary-foreground border-primary' : 'border-border text-muted-foreground hover:text-foreground hover:border-foreground/30'}`}>
            {s}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="border border-border rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-muted text-muted-foreground">
            <tr>
              {['ID','Brand','Model','Year','Category','$/Day','Mileage','Supplier','Status','Actions'].map(h => (
                <th key={h} className="text-left p-3 font-medium whitespace-nowrap">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {loading ? (
              <tr><td colSpan={10} className="p-8 text-center text-muted-foreground">Loading...</td></tr>
            ) : filtered.length === 0 ? (
              <tr><td colSpan={10} className="p-8 text-center text-muted-foreground">
                <Car size={36} className="mx-auto mb-2 opacity-30" />No cars found.
              </td></tr>
            ) : filtered.map(car => (
              <tr key={car.id} className="hover:bg-accent/40 transition-colors">
                <td className="p-3 text-muted-foreground">#{car.id}</td>
                <td className="p-3 font-medium">{car.brand}</td>
                <td className="p-3">{car.model}</td>
                <td className="p-3 text-muted-foreground">{car.year}</td>
                <td className="p-3 text-muted-foreground">{car.category}</td>
                <td className="p-3 font-medium">${Number(car.price_per_day || 0).toFixed(2)}</td>
                <td className="p-3 text-muted-foreground">{car.mileage?.toLocaleString()} km</td>
                <td className="p-3 text-muted-foreground">{car.supplier ?? '—'}</td>
                <td className="p-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium border ${STATUS_COLORS[car.status] ?? ''}`}>
                    {car.status}
                  </span>
                </td>
                <td className="p-3">
                  <div className="flex items-center gap-1">
                    <button onClick={() => setEditing(car)} title="Edit"
                      className="p-1.5 rounded-md hover:bg-accent text-muted-foreground hover:text-foreground transition">
                      <Pencil size={14} />
                    </button>
                    <button onClick={() => toggleMaintenance(car)} title="Toggle Maintenance"
                      className={`p-1.5 rounded-md transition ${car.status === 'Maintenance' ? 'text-amber-400 hover:bg-amber-400/10' : 'text-muted-foreground hover:bg-accent hover:text-foreground'}`}>
                      <Wrench size={14} />
                    </button>
                    <button onClick={() => handleDelete(car)} title="Delete"
                      className="p-1.5 rounded-md hover:bg-red-500/10 text-muted-foreground hover:text-red-400 transition">
                      <Trash2 size={14} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Add Modal */}
      {showAdd && (
        <Modal title="Add New Car" onClose={() => setShowAdd(false)}>
          <form onSubmit={handleAdd} className="flex flex-col gap-4">
            <div className="grid grid-cols-2 gap-4">
              <Field label="Brand" name="brand" required placeholder="Toyota" />
              <Field label="Model" name="model" required placeholder="Camry" />
              <Field label="Year" name="year" type="number" required placeholder="2023" />
              <Field label="Price / Day ($)" name="price_per_day" type="number" required placeholder="80" />
              <Field label="Mileage (km)" name="mileage" type="number" required placeholder="0" />
              <Field label="Category" name="category">
                <select name="category" className="px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/40">
                  {['Sedan','SUV','Luxury'].map(c => <option key={c}>{c}</option>)}
                </select>
              </Field>
            </div>
            <Field label="Supplier" name="supplier_id">
              <select name="supplier_id" className="px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/40">
                <option value="">— None —</option>
                {suppliers.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
              </select>
            </Field>
            <button type="submit"
              className="mt-2 w-full py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
              Add Car
            </button>
          </form>
        </Modal>
      )}

      {/* Edit Modal */}
      {editing && (
        <Modal title={`Edit — ${editing.brand} ${editing.model}`} onClose={() => setEditing(null)}>
          <form onSubmit={handleEdit} className="flex flex-col gap-4">
            <div className="grid grid-cols-2 gap-4">
              <Field label="Brand" name="brand" required defaultValue={editing.brand} />
              <Field label="Model" name="model" required defaultValue={editing.model} />
              <Field label="Year" name="year" type="number" required defaultValue={editing.year} />
              <Field label="Price / Day ($)" name="price_per_day" type="number" required defaultValue={editing.price_per_day} />
              <Field label="Mileage (km)" name="mileage" type="number" required defaultValue={editing.mileage} />
              <Field label="Category" name="category">
                <select name="category" defaultValue={editing.category}
                  className="px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/40">
                  {['Sedan','SUV','Luxury'].map(c => <option key={c}>{c}</option>)}
                </select>
              </Field>
            </div>
            <Field label="Supplier" name="supplier_id">
              <select name="supplier_id" defaultValue={editing.supplier_id ?? ''}
                className="px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/40">
                <option value="">— None —</option>
                {suppliers.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
              </select>
            </Field>
            <button type="submit"
              className="mt-2 w-full py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:opacity-90 transition">
              Save Changes
            </button>
          </form>
        </Modal>
      )}
    </div>
  )
}
