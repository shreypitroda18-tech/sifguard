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
      <div className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 bg-card border-r border-border transform transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:block",
        isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex h-16 shrink-0 items-center px-6 border-b border-border">
          <ShieldAlert className="h-6 w-6 text-primary mr-2" />
          <span className="text-lg font-bold tracking-tight">SIFGUARD AI</span>
        </div>
        
        <div className="px-4 py-4 overflow-y-auto h-[calc(100vh-4rem-4rem)]">
          {categories.map((category, idx) => (
            <div key={idx} className="mb-6">
              <h3 className="px-2 mb-2 text-xs font-semibold text-muted-foreground tracking-wider">
                {category}
              </h3>
              <div className="space-y-1">
                {navItems.filter(item => item.category === category).map((item) => {
                  const isActive = pathname.startsWith(item.href)
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={cn(
                        "flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors",
                        isActive 
                          ? "bg-primary/10 text-primary" 
                          : "text-muted-foreground hover:bg-muted hover:text-foreground"
                      )}
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      <item.icon className={cn("mr-3 h-4 w-4", isActive ? "text-primary" : "text-muted-foreground")} />
                      {item.name}
                    </Link>
                  )
                })}
              </div>
            </div>
          ))}
        </div>

        <div className="absolute bottom-0 w-full p-4 border-t border-border bg-card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center">
                <User className="h-4 w-4 text-primary" />
              </div>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-foreground">Safety Officer</p>
              <p className="text-xs text-muted-foreground">Demo Mode</p>
            </div>
            <button className="ml-auto text-muted-foreground hover:text-foreground">
              <LogOut className="h-4 w-4" />
            </button>
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
