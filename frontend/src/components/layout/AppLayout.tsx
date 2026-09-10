"use client"

import * as React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { 
  ShieldAlert, 
  LayoutDashboard, 
  FileText, 
  BrainCircuit, 
  ActivitySquare, 
  CheckSquare, 
  MessageSquareWarning,
  Bell,
  Settings,
  User,
  LogOut,
  Menu
} from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

export function AppLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false)

  const navItems = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard, category: "COMMAND CENTER" },
    { name: "Reports", href: "/reports", icon: FileText, category: "SAFETY INTELLIGENCE" },
    { name: "Risk Intelligence", href: "/intelligence", icon: ActivitySquare, category: "SAFETY INTELLIGENCE" },
    { name: "Corrective Actions", href: "/actions", icon: CheckSquare, category: "ACTION MANAGEMENT" },
    { name: "SIF Copilot", href: "/copilot", icon: BrainCircuit, category: "AI" },
  ]

  const categories = Array.from(new Set(navItems.map(item => item.category)))

  return (
    <div className="flex h-screen bg-background text-foreground dark">
      {/* Mobile sidebar overlay */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-border transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex h-16 items-center px-6 border-b border-border">
          <ShieldAlert className="h-8 w-8 text-primary" />
          <span className="ml-3 font-bold text-xl tracking-tight text-foreground">SIFGUARD AI</span>
        </div>
        
        <div className="flex flex-col h-[calc(100vh-4rem)] justify-between pb-6">
          <nav className="mt-6 px-4 space-y-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href || (pathname.startsWith(item.href) && item.href !== '/dashboard')
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`group flex items-center px-3 py-3 text-sm font-medium rounded-xl transition-colors ${
                    isActive 
                      ? 'bg-primary text-white shadow-sm' 
                      : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                  }`}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <item.icon className={`mr-3 h-5 w-5 ${isActive ? 'text-white' : 'text-muted-foreground group-hover:text-foreground'}`} />
                  {item.name}
                </Link>
              )
            })}
          </nav>

          <div className="px-4">
            <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
              <div className="flex items-center gap-3 mb-2">
                <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center">
                  <span className="text-primary font-bold text-xs">AI</span>
                </div>
                <div>
                  <p className="text-sm font-semibold text-foreground">NLP Engine</p>
                  <p className="text-xs text-muted-foreground">Active (v2.4)</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-border bg-card px-4 lg:px-6">
          <div className="flex items-center">
            <button 
              className="mr-4 lg:hidden text-muted-foreground hover:text-foreground"
              onClick={() => setIsMobileMenuOpen(true)}
            >
              <Menu className="h-6 w-6" />
            </button>
            <h1 className="text-lg font-semibold tracking-tight hidden sm:block">
              {navItems.find(item => pathname.startsWith(item.href))?.name || "Dashboard"}
            </h1>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-sm font-medium hidden sm:flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500"></span>
              Demo Environment
            </div>
            <Button variant="ghost" size="icon" className="text-muted-foreground">
              <Bell className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" className="text-muted-foreground">
              <Settings className="h-5 w-5" />
            </Button>
            <select className="bg-transparent text-sm border-none focus:ring-0 text-muted-foreground cursor-pointer outline-none">
              <option value="en">EN</option>
              <option value="hi">HI</option>
              <option value="mr">MR</option>
              <option value="gu">GU</option>
            </select>
          </div>
        </header>
        
        <main className="flex-1 overflow-y-auto p-4 lg:p-8 bg-background">
          <div className="mx-auto max-w-7xl">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
