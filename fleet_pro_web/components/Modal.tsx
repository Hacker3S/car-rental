'use client'
import { X } from 'lucide-react'
import { ReactNode } from 'react'

interface ModalProps {
  title: string
  onClose: () => void
  children: ReactNode
}

export function Modal({ title, onClose, children }: ModalProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
         onClick={(e) => { if (e.target === e.currentTarget) onClose() }}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      <div className="relative bg-card border border-border rounded-2xl shadow-2xl w-full max-w-md max-h-[90vh] overflow-auto">
        <div className="flex items-center justify-between p-6 border-b border-border">
          <h2 className="text-lg font-semibold text-foreground">{title}</h2>
          <button onClick={onClose}
            className="text-muted-foreground hover:text-foreground transition-colors p-1 rounded-md hover:bg-accent">
            <X size={20} />
          </button>
        </div>
        <div className="p-6">{children}</div>
      </div>
    </div>
  )
}

interface FieldProps {
  label: string
  name: string
  type?: string
  required?: boolean
  placeholder?: string
  defaultValue?: string | number
  children?: ReactNode
}

export function Field({ label, name, type = 'text', required, placeholder, defaultValue, children }: FieldProps) {
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={name} className="text-sm font-medium text-muted-foreground">{label}</label>
      {children ?? (
        <input id={name} name={name} type={type} required={required}
          placeholder={placeholder} defaultValue={defaultValue}
          className="px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm
                     focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary
                     placeholder:text-muted-foreground/50 transition" />
      )}
    </div>
  )
}
