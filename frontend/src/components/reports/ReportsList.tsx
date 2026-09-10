"use client"

import React, { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Search, Plus, Filter, Eye } from "lucide-react"
import axios from "axios"
import Link from "next/link"

export function ReportsList() {
  const [reports, setReports] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/reports")
      .then(res => {
        setReports(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">Safety Reports</h2>
          <p className="text-muted-foreground mt-1">Manage and analyze submitted safety observations.</p>
        </div>
        <Link href="/reports/create">
          <Button className="gap-2">
            <Plus className="h-4 w-4" /> Create Report
          </Button>
        </Link>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 mb-4">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input placeholder="Search reports..." className="pl-9" />
        </div>
        <Button variant="outline" className="gap-2">
          <Filter className="h-4 w-4" /> Filters
        </Button>
      </div>

      <div className="border border-border rounded-2xl overflow-hidden bg-white shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-muted-foreground uppercase bg-slate-50 border-b border-border">
              <tr>
                <th className="px-6 py-4 font-semibold tracking-wider">Report ID</th>
                <th className="px-6 py-4 font-semibold tracking-wider">Date</th>
                <th className="px-6 py-4 font-semibold tracking-wider">Site</th>
                <th className="px-6 py-4 font-semibold tracking-wider">Hazard</th>
                <th className="px-6 py-4 font-semibold tracking-wider">Risk</th>
                <th className="px-6 py-4 font-semibold tracking-wider text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {reports.map((report) => (
                <tr key={report.id} className="hover:bg-muted/50 transition-colors">
                  <td className="px-6 py-4 font-medium font-mono text-primary">{report.reportId}</td>
                  <td className="px-6 py-4 text-muted-foreground">{new Date(report.createdAt).toLocaleDateString()}</td>
                  <td className="px-6 py-4">{report.site}</td>
                  <td className="px-6 py-4 truncate max-w-[200px]">{report.title}</td>
                  <td className="px-6 py-4">
                    <Badge variant={report.severity.toLowerCase() as any}>
                      {report.severity}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link href={`/reports/${report.id}`}>
                      <Button variant="ghost" size="sm">
                        <Eye className="h-4 w-4 mr-2" /> View
                      </Button>
                    </Link>
                  </td>
                </tr>
              ))}
              {reports.length === 0 && !loading && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-muted-foreground">
                    No safety reports found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
