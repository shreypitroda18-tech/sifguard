import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertTriangle, Activity } from "lucide-react"

export default function IntelligencePage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-foreground">Risk Intelligence Center</h2>
          <p className="text-muted-foreground mt-1">Advanced analytics, emerging risks, and similar incident detection.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-primary" /> Emerging Risks
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-orange-500/10 border border-orange-500/20 rounded-lg">
                <h4 className="font-semibold text-orange-500 mb-1">Electrical Isolation Anomalies</h4>
                <p className="text-sm">Electrical isolation observations increased by 28% over the previous period, specifically in Maintenance Area B.</p>
              </div>
              <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                <h4 className="font-semibold text-yellow-500 mb-1">Working at Height Incidents</h4>
                <p className="text-sm">Similar working-at-height observations detected 12 times across 4 locations in the last 7 days.</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-destructive" /> Top High-Risk Locations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { site: 'Site A', reports: 42, score: 87 },
                { site: 'Site B', reports: 31, score: 74 },
                { site: 'Site C', reports: 19, score: 68 },
              ].map((loc, i) => (
                <div key={i} className="flex justify-between items-center p-3 bg-muted/50 rounded-lg border border-border">
                  <div>
                    <div className="font-medium">{loc.site}</div>
                    <div className="text-xs text-muted-foreground">{loc.reports} critical reports</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-muted-foreground mb-1">Risk Score</div>
                    <div className="font-bold text-red-500">{loc.score}</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
