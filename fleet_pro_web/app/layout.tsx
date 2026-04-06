import './globals.css'
import { Sidebar } from '@/components/Sidebar'

export const metadata = {
  title: 'FleetPro Web',
  description: 'Car Rental Management SaaS',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="flex h-screen overflow-hidden bg-background text-foreground">
        <Sidebar className="w-64 border-r border-border shrink-0" />
        <main className="flex-1 overflow-auto p-8">
          {children}
        </main>
      </body>
    </html>
  )
}
