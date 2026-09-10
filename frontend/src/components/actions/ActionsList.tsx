"use client"

import React, { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckSquare, Clock, ArrowRight } from "lucide-react"
import axios from "axios"
import Link from "next/link"

export function ActionsList() {
  const [actions, setActions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchActions()
  }, [])

  const fetchActions = () => {
    axios.get("http://127.0.0.1:8000/api/actions")
      .then(res => {
        setActions(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }

  const updateStatus = (id: number, newStatus: string) => {
    axios.patch(`http://127.0.0.1:8000/api/actions/${id}?status=${newStatus}`)
      .then(() => fetchActions())
      .catch(err => console.error(err))
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Open': return 'bg-slate-500'
      case 'In Progress': return 'bg-blue-500'
      case 'Completed': return 'bg-green-500'
      case 'Verified': return 'bg-emerald-600'
      default: return 'bg-slate-500'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">Corrective Actions</h2>
          <p className="text-muted-foreground mt-1">Manage and track recommended safety interventions.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {['Open', 'In Progress', 'Completed'].map(statusColumn => (
          <div key={statusColumn} className="bg-slate-50 p-4 rounded-2xl border border-border flex flex-col h-[calc(100vh-14rem)]">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-semibold text-lg flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${getStatusColor(statusColumn)}`} />
                {statusColumn}
              </h3>
              <Badge variant="secondary">{actions.filter(a => a.status === statusColumn || (statusColumn === 'Completed' && a.status === 'Verified')).length}</Badge>
            </div>
            
            <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
              {actions
                .filter(a => statusColumn === 'Completed' ? ['Completed', 'Verified'].includes(a.status) : a.status === statusColumn)
                .map(action => (
                <Card key={action.id} className="cursor-pointer hover:border-primary/50 transition-colors">
                  <CardHeader className="p-4 pb-2">
                    <div className="flex justify-between items-start mb-1">
                      <Badge variant="outline" className="text-[10px] uppercase font-bold tracking-wider text-muted-foreground">ACT-{action.id}</Badge>
                      <Badge variant={action.priority.toLowerCase() as any} className="text-[10px]">{action.priority}</Badge>
                    </div>
                    <CardTitle className="text-sm leading-tight">{action.title}</CardTitle>
                  </CardHeader>
                  <CardContent className="p-4 pt-0">
                    <div className="text-xs text-muted-foreground mt-2 flex items-center gap-1">
                      <Clock className="h-3 w-3" /> Due {new Date(action.dueDate).toLocaleDateString()}
                    </div>
                    <div className="mt-4 flex justify-between items-center pt-3 border-t border-border">
                      <div className="text-xs font-medium bg-primary/10 text-primary px-2 py-1 rounded">
                        {action.assignedTo}
                      </div>
                      
                      {statusColumn === 'Open' && (
                        <Button variant="ghost" size="sm" className="h-7 text-xs" onClick={() => updateStatus(action.id, 'In Progress')}>
                          Start <ArrowRight className="h-3 w-3 ml-1" />
                        </Button>
                      )}
                      {statusColumn === 'In Progress' && (
                        <Button variant="ghost" size="sm" className="h-7 text-xs text-green-500 hover:text-green-600" onClick={() => updateStatus(action.id, 'Completed')}>
                          <CheckSquare className="h-3 w-3 mr-1" /> Complete
                        </Button>
                      )}
                      {statusColumn === 'Completed' && action.status !== 'Verified' && (
                        <Button variant="ghost" size="sm" className="h-7 text-xs text-emerald-500" onClick={() => updateStatus(action.id, 'Verified')}>
                          Verify
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
