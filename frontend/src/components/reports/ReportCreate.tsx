"use client"

import React, { useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { ArrowLeft, Mic, Sparkles } from "lucide-react"
import axios from "axios"

export function ReportCreate() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    reportType: "Unsafe Act",
    title: "",
    description: "",
    site: "Site A",
    location: "",
    department: "Operations",
    activity: "",
    originalLanguage: "Auto Detect",
    reportedBy: "Safety Officer",
    severity: "Medium"
  })

  const handleChange = (e: any) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = (e: any) => {
    e.preventDefault()
    setLoading(true)
    
    // Generate a mock report ID
    const reportId = `OIL-${Math.floor(1000 + Math.random() * 9000)}`
    
    const payload = {
      ...formData,
      reportId,
      originalLanguage: formData.originalLanguage === "Auto Detect" ? "English" : formData.originalLanguage
    }

    axios.post("http://127.0.0.1:8000/api/reports", payload)
      .then(res => {
        setLoading(false)
        router.push(`/reports/${res.data.id}`)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">Create Safety Report</h2>
          <p className="text-muted-foreground mt-1">Submit a new observation, near-miss, or incident report.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <Card>
          <CardHeader>
            <CardTitle>Observation Details</CardTitle>
            <CardDescription>Provide detailed information about the safety observation.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="reportType">Report Type</Label>
                <select 
                  id="reportType" name="reportType" 
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                  value={formData.reportType} onChange={handleChange}
                >
                  <option>Unsafe Act</option>
                  <option>Unsafe Condition</option>
                  <option>Near Miss</option>
                  <option>Incident</option>
                  <option>Safety Observation</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="originalLanguage">Report Language</Label>
                <select 
                  id="originalLanguage" name="originalLanguage" 
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                  value={formData.originalLanguage} onChange={handleChange}
                >
                  <option>Auto Detect</option>
                  <option>English</option>
                  <option>Hindi</option>
                  <option>Marathi</option>
                  <option>Gujarati</option>
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="title">Short Title</Label>
              <Input 
                id="title" name="title" required 
                placeholder="e.g., Working at height without harness" 
                value={formData.title} onChange={handleChange}
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-end">
                <Label htmlFor="description">Detailed Description</Label>
                <div className="flex gap-2">
                  <Button type="button" variant="outline" size="sm" className="h-7 text-xs gap-1">
                    <Mic className="h-3 w-3" /> Voice
                  </Button>
                  <Button type="button" variant="outline" size="sm" className="h-7 text-xs gap-1 text-primary border-primary/50">
                    <Sparkles className="h-3 w-3" /> Improve
                  </Button>
                </div>
              </div>
              <Textarea 
                id="description" name="description" required 
                className="min-h-[120px]"
                placeholder="Describe what you observed. Include details about the hazard, people involved, and any immediate actions taken." 
                value={formData.description} onChange={handleChange}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="site">Site</Label>
                <select 
                  id="site" name="site" 
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                  value={formData.site} onChange={handleChange}
                >
                  <option>Site A</option>
                  <option>Site B</option>
                  <option>Site C</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="location">Specific Location</Label>
                <Input 
                  id="location" name="location" required 
                  placeholder="e.g., Boiler Room 2" 
                  value={formData.location} onChange={handleChange}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="department">Department</Label>
                <select 
                  id="department" name="department" 
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                  value={formData.department} onChange={handleChange}
                >
                  <option>Operations</option>
                  <option>Maintenance</option>
                  <option>Electrical</option>
                  <option>Logistics</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="activity">Activity</Label>
                <Input 
                  id="activity" name="activity" required 
                  placeholder="e.g., Routine Inspection" 
                  value={formData.activity} onChange={handleChange}
                />
              </div>
            </div>

            <div className="pt-4 flex justify-end gap-4">
              <Button type="button" variant="outline" onClick={() => router.back()}>Cancel</Button>
              <Button type="submit" disabled={loading}>
                {loading ? "Submitting..." : "Submit Report"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  )
}
