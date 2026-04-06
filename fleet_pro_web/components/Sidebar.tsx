import Link from 'next/link'
import { Car, LayoutDashboard, Users, UserSquare2, CalendarDays } from 'lucide-react'

export function Sidebar({ className }: { className?: string }) {
  const links = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Fleet', href: '/fleet', icon: Car },
    { name: 'Customers', href: '/customers', icon: Users },
    { name: 'Suppliers', href: '/suppliers', icon: UserSquare2 },
    { name: 'Bookings', href: '/bookings', icon: CalendarDays },
  ]
  
  return (
    <div className={`p-6 flex flex-col gap-6 ${className}`}>
      <div className="flex items-center gap-2 font-bold text-2xl text-primary">
        <Car size={32} />
        <span>FleetPro Web</span>
      </div>
      <nav className="flex flex-col gap-2 mt-4">
        {links.map(l => (
           <Link key={l.name} href={l.href} className="flex items-center gap-3 px-4 py-3 rounded-md hover:bg-accent text-muted-foreground hover:text-foreground transition-colors font-medium">
             <l.icon size={20} />
             {l.name}
           </Link>
        ))}
      </nav>
    </div>
  )
}
