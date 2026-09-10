"use client"

import React, { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ShieldAlert, AlertTriangle, Activity, CheckSquare } from "lucide-react"
import { motion } from "framer-motion"
import axios from "axios"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell } from 'recharts';

export function Dashboard() {
  const [summary, setSummary] = useState({
    totalReports: 0,
    sifPrecursors: 0,
    criticalRisks: 0,
    openActions: 0
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In demo environment, we will fetch from our local backend, or use mock if unavailable
    axios.get("http://127.0.0.1:8000/api/dashboard/summary")
      .then(res => {
        setSummary(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch dashboard data", err);
        // Fallback demo data
        setSummary({
          totalReports: 12450,
          sifPrecursors: 1842,
          criticalRisks: 126,
          openActions: 347
        });
        setLoading(false);
      });
  }, []);

  const topHazards = [
    { name: 'Working at Height', count: 482, risk: 'High' },
    { name: 'Electrical Isolation', count: 395, risk: 'Critical' },
    { name: 'Confined Space', count: 214, risk: 'Critical' },
    { name: 'Line of Fire', count: 187, risk: 'Medium' },
    { name: 'Vehicle Interaction', count: 156, risk: 'High' },
  ];

  const chartData = [
    { name: 'Mon', Critical: 4, High: 12, Medium: 25 },
    { name: 'Tue', Critical: 6, High: 15, Medium: 30 },
    { name: 'Wed', Critical: 2, High: 8, Medium: 20 },
    { name: 'Thu', Critical: 8, High: 18, Medium: 40 },
    { name: 'Fri', Critical: 3, High: 10, Medium: 22 },
    { name: 'Sat', Critical: 1, High: 5, Medium: 12 },
    { name: 'Sun', Critical: 0, High: 4, Medium: 10 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">Safety Command Center</h2>
          <p className="text-muted-foreground mt-1">Real-time overview of safety observations, SIF precursors, risks, and corrective actions.</p>
        </div>
        <div className="mt-4 md:mt-0 flex gap-2">
          <select className="px-3 py-1.5 bg-card border border-border rounded-md text-sm">
            <option>All Sites</option>
            <option>Site A</option>
            <option>Site B</option>
          </select>
          <select className="px-3 py-1.5 bg-card border border-border rounded-md text-sm">
            <option>Last 7 Days</option>
            <option>Last 30 Days</option>
          </select>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricCard title="Total Reports" value={summary.totalReports} icon={Activity} trend="+12%" />
        <MetricCard title="SIF Precursors" value={summary.sifPrecursors} icon={ShieldAlert} trend="+4%" />
        <MetricCard title="Critical Risks" value={summary.criticalRisks} icon={AlertTriangle} trend="-2%" className="text-red-500" />
        <MetricCard title="Open Actions" value={summary.openActions} icon={CheckSquare} trend="-8%" />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4 border-border bg-card">
          <CardHeader>
            <CardTitle>SIF Precursor Trend</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#333" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#888'}} />
                  <YAxis axisLine={false} tickLine={false} tick={{fill: '#888'}} />
                  <RechartsTooltip contentStyle={{backgroundColor: '#1f2937', border: '1px solid #374151'}} />
                  <Bar dataKey="Critical" stackId="a" fill="#ef4444" radius={[0, 0, 4, 4]} />
                  <Bar dataKey="High" stackId="a" fill="#f97316" />
                  <Bar dataKey="Medium" stackId="a" fill="#eab308" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
        
        <Card className="col-span-3 border-border bg-card">
          <CardHeader>
            <CardTitle>Top SIF Precursors</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {topHazards.map((hazard, index) => (
                <div key={index} className="flex items-center">
                  <div className="ml-4 space-y-1 flex-1">
                    <p className="text-sm font-medium leading-none">{hazard.name}</p>
                    <div className="flex items-center pt-1">
                      <span className={`text-[10px] px-1.5 py-0.5 rounded uppercase font-bold 
                        ${hazard.risk === 'Critical' ? 'bg-red-500/20 text-red-500' : 
                          hazard.risk === 'High' ? 'bg-orange-500/20 text-orange-500' : 'bg-yellow-500/20 text-yellow-500'}`}>
                        {hazard.risk}
                      </span>
                    </div>
                  </div>
                  <div className="font-medium text-lg">{hazard.count}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Critical Alerts */}
      <div className="mt-6">
        <h3 className="text-lg font-medium mb-3">Critical Alerts</h3>
        <div className="space-y-3">
          <AlertPanel 
            level="CRITICAL" 
            message="Gas leakage detected near potential ignition source" 
            site="Site A" 
            time="8 minutes ago" 
          />
          <AlertPanel 
            level="HIGH" 
            message="Electrical maintenance without documented isolation" 
            site="Site B" 
            time="23 minutes ago" 
          />
        </div>
      </div>
    </div>
  )
}

function MetricCard({ title, value, icon: Icon, trend, className }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card className="bg-card border-border">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {title}
          </CardTitle>
          <Icon className={`h-4 w-4 text-muted-foreground ${className}`} />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold tracking-tight">
            {value.toLocaleString()}
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            <span className={trend.startsWith('+') ? 'text-red-400' : 'text-green-400'}>
              {trend}
            </span> from last month
          </p>
        </CardContent>
      </Card>
    </motion.div>
  )
}

function AlertPanel({ level, message, site, time }: any) {
  const isCritical = level === 'CRITICAL';
  return (
    <div className={`p-4 border rounded-lg flex items-start sm:items-center justify-between flex-col sm:flex-row gap-4 
      ${isCritical ? 'border-red-500/50 bg-red-500/5' : 'border-orange-500/50 bg-orange-500/5'}`}>
      <div className="flex items-start gap-4">
        <div className={`mt-1 h-2 w-2 rounded-full ${isCritical ? 'bg-red-500' : 'bg-orange-500'}`} />
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-xs font-bold ${isCritical ? 'text-red-500' : 'text-orange-500'}`}>{level}</span>
            <span className="text-xs text-muted-foreground">• {site} • {time}</span>
          </div>
          <p className="text-sm font-medium">{message}</p>
        </div>
      </div>
      <button className="text-xs px-3 py-1.5 border border-border rounded hover:bg-muted whitespace-nowrap">
        Review Report
      </button>
    </div>
  )
}
