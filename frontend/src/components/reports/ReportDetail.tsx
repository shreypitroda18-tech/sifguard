"use client"

import React, { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ArrowLeft, BrainCircuit, ShieldAlert, CheckCircle2, Clock, MapPin, Activity, Shield, AlertTriangle } from "lucide-react"
import axios from "axios"
import Link from "next/link"
import { motion, AnimatePresence } from "framer-motion"

export function ReportDetail() {
  const { id } = useParams()
  const router = useRouter()
  const [report, setReport] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysisSteps, setAnalysisSteps] = useState(0)

  useEffect(() => {
    fetchReport()
  }, [id])

  const fetchReport = () => {
    axios.get(`http://127.0.0.1:8000/api/reports/${id}`)
      .then(res => {
        setReport(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }

  const handleAnalyze = () => {
    setAnalyzing(true)
    setAnalysisSteps(1)
    
    // Simulate steps for the UI
    const intervals = [
      setTimeout(() => setAnalysisSteps(2), 800),
      setTimeout(() => setAnalysisSteps(3), 1600),
      setTimeout(() => setAnalysisSteps(4), 2400),
      setTimeout(() => {
        axios.post(`http://127.0.0.1:8000/api/reports/${id}/analyze`)
          .then(res => {
            setReport({...report, analysis: res.data})
            setAnalyzing(false)
            setAnalysisSteps(0)
          })
          .catch(err => {
            console.error(err)
            setAnalyzing(false)
            setAnalysisSteps(0)
          })
      }, 3200)
    ]
    
    return () => intervals.forEach(clearTimeout)
  }

  if (loading) return <div className="p-8 text-center text-muted-foreground animate-pulse">Loading report details...</div>
  if (!report) return <div className="p-8 text-center text-muted-foreground">Report not found.</div>

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.push('/reports')} className="rounded-full">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-2xl font-bold tracking-tight text-foreground">Report {report.reportId}</h2>
            <Badge variant="outline">{report.reportType}</Badge>
            <Badge variant={report.severity.toLowerCase() as any}>{report.severity}</Badge>
          </div>
          <p className="text-muted-foreground mt-1">Submitted on {new Date(report.createdAt).toLocaleString()} by {report.reportedBy}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Original Observation</CardTitle>
              <CardDescription>The raw observation submitted by the reporter.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="p-4 bg-slate-50 rounded-md border border-border">
                <p className="text-lg leading-relaxed">{report.description}</p>
                <div className="mt-4 flex justify-between items-center text-sm text-muted-foreground">
                  <span>Language: {report.originalLanguage}</span>
                  {report.detectedLanguage && <span>Detected: {report.detectedLanguage}</span>}
                </div>
              </div>
            </CardContent>
          </Card>

          {analyzing ? (
            <Card className="border-primary/50 shadow-[0_0_15px_rgba(37,99,235,0.1)]">
              <CardContent className="pt-6">
                <div className="flex flex-col items-center justify-center py-8">
                  <BrainCircuit className="h-12 w-12 text-primary animate-pulse mb-4" />
                  <h3 className="text-xl font-semibold mb-6">ANALYZING SAFETY REPORT</h3>
                  <div className="space-y-3 w-full max-w-md">
                    <StepItem active={analysisSteps >= 1} done={analysisSteps > 1} text="Reading observation & detecting language" />
                    <StepItem active={analysisSteps >= 2} done={analysisSteps > 2} text="Extracting safety entities & hazards" />
                    <StepItem active={analysisSteps >= 3} done={analysisSteps > 3} text="Evaluating SIF potential" />
                    <StepItem active={analysisSteps >= 4} done={analysisSteps > 4} text="Calculating risk & generating recommendations" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : report.analysis ? (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
              <Card className="border-red-500/30 overflow-hidden relative">
                <div className="absolute top-0 left-0 w-1 h-full bg-red-500"></div>
                <CardHeader className="bg-red-500/5 pb-4 border-b border-border/50">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="flex items-center gap-2">
                        <ShieldAlert className="h-5 w-5 text-red-500" />
                        AI Safety Analysis
                      </CardTitle>
                      <CardDescription className="mt-1">Structured assessment and SIF precursor detection.</CardDescription>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-muted-foreground font-medium">RISK SCORE</div>
                      <div className="text-3xl font-bold text-red-500">{report.analysis.riskScore}<span className="text-lg text-muted-foreground">/100</span></div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    <div className="p-3 bg-slate-50 rounded-lg border border-border/50">
                      <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">SIF PRECURSOR</div>
                      <div className="font-bold text-red-500 flex items-center gap-1">
                        <ShieldAlert className="h-4 w-4" /> DETECTED
                      </div>
                    </div>
                    <div className="p-3 bg-slate-50 rounded-lg border border-border/50">
                      <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">RISK LEVEL</div>
                      <div className="font-bold text-red-500 uppercase">{report.analysis.riskLevel}</div>
                    </div>
                    <div className="p-3 bg-slate-50 rounded-lg border border-border/50">
                      <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">AI CONFIDENCE</div>
                      <div className="font-bold text-foreground">{(report.analysis.confidence * 100).toFixed(0)}%</div>
                    </div>
                    <div className="p-3 bg-slate-50 rounded-lg border border-border/50">
                      <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">HAZARDS</div>
                      <div className="font-bold text-foreground">{report.analysis.hazardCategories.length} Detected</div>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <div>
                      <h4 className="font-medium mb-2 flex items-center gap-2 border-b pb-1">
                        <AlertTriangle className="h-4 w-4 text-orange-500" /> Detected Hazards
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {report.analysis.hazardCategories.map((h: string, i: number) => (
                          <Badge key={i} variant="outline" className="bg-orange-500/10 text-orange-500 border-orange-500/20">{h}</Badge>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2 flex items-center gap-2 border-b pb-1">
                        <Activity className="h-4 w-4 text-red-400" /> Potential Consequences
                      </h4>
                      <ul className="list-disc pl-5 text-sm text-muted-foreground space-y-1">
                        {report.analysis.potentialConsequences.map((c: string, i: number) => (
                          <li key={i}>{c}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2 flex items-center gap-2 border-b pb-1">
                        <Shield className="h-4 w-4 text-green-500" /> Missing Controls
                      </h4>
                      <ul className="list-disc pl-5 text-sm text-muted-foreground space-y-1">
                        {report.analysis.missingControls.map((c: string, i: number) => (
                          <li key={i}>{c}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ) : (
            <Card className="border-dashed border-2 bg-white text-center p-8">
              <BrainCircuit className="h-12 w-12 text-muted-foreground mx-auto mb-4 opacity-50" />
              <h3 className="text-lg font-medium">No AI Analysis Yet</h3>
              <p className="text-muted-foreground mt-1 mb-6 max-w-md mx-auto">
                Run this observation through the SIFGUARD AI engine to detect SIF precursors, extract hazards, and assess risk.
              </p>
              <Button size="lg" onClick={handleAnalyze} className="gap-2">
                <BrainCircuit className="h-5 w-5" /> Analyze With SIF AI
              </Button>
            </Card>
          )}

          {/* Corrective Actions Section */}
          {report.analysis && (
            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle>Corrective Actions</CardTitle>
                  <CardDescription>Actions recommended and created for this report.</CardDescription>
                </div>
                <Button variant="outline" size="sm" className="gap-2">
                  <CheckCircle2 className="h-4 w-4" /> Create Action
                </Button>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {report.analysis.recommendations.map((rec: any, idx: number) => (
                    <div key={idx} className="flex items-start gap-3 p-3 bg-muted/20 border border-border rounded-md">
                      <div className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 ${rec.priority === 'Immediate' ? 'bg-red-500' : 'bg-orange-500'}`} />
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs font-semibold text-muted-foreground uppercase">{rec.priority}</span>
                        </div>
                        <p className="text-sm">{rec.action}</p>
                      </div>
                      <Button variant="ghost" size="sm" className="h-8 text-xs">Convert to Action</Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-sm">
              <div className="flex gap-3 items-start">
                <MapPin className="h-4 w-4 text-muted-foreground mt-0.5" />
                <div>
                  <div className="font-medium">{report.site}</div>
                  <div className="text-muted-foreground">{report.department} • {report.location}</div>
                </div>
              </div>
              <div className="flex gap-3 items-start">
                <Activity className="h-4 w-4 text-muted-foreground mt-0.5" />
                <div>
                  <div className="font-medium">Activity</div>
                  <div className="text-muted-foreground">{report.activity}</div>
                </div>
              </div>
              <div className="flex gap-3 items-start">
                <Clock className="h-4 w-4 text-muted-foreground mt-0.5" />
                <div>
                  <div className="font-medium">Status</div>
                  <div className="text-muted-foreground">{report.status}</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

function StepItem({ active, done, text }: { active: boolean, done: boolean, text: string }) {
  return (
    <div className={`flex items-center gap-3 text-sm transition-all duration-300 ${active ? 'text-foreground font-medium' : 'text-muted-foreground opacity-50'}`}>
      <div className="flex-shrink-0 w-5 h-5 flex items-center justify-center">
        {done ? (
          <CheckCircle2 className="h-5 w-5 text-green-500" />
        ) : active ? (
          <div className="h-2 w-2 rounded-full bg-primary animate-ping" />
        ) : (
          <div className="h-1.5 w-1.5 rounded-full bg-muted-foreground" />
        )}
      </div>
      <span>{text}</span>
    </div>
  )
}
