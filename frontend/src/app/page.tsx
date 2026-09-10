import Link from "next/link"
import { ShieldAlert, Activity, ArrowRight, Brain, AlertTriangle, CheckCircle2 } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground dark selection:bg-primary/30">
      <header className="absolute inset-x-0 top-0 z-50">
        <nav className="flex items-center justify-between p-6 lg:px-8" aria-label="Global">
          <div className="flex lg:flex-1 items-center gap-2">
            <ShieldAlert className="h-8 w-8 text-primary" />
            <span className="font-bold text-xl tracking-tight">SIFGUARD AI</span>
          </div>
          <div className="flex flex-1 justify-end">
            <Link
              href="/login"
              className="text-sm font-semibold leading-6 text-foreground hover:text-primary transition-colors flex items-center gap-1"
            >
              Sign In <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </nav>
      </header>

      <div className="relative isolate pt-14 h-screen flex flex-col justify-center overflow-hidden">
        {/* Subtle grid background */}
        <div className="absolute inset-0 -z-10 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
        <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-primary/20 opacity-20 blur-[100px]"></div>

        <div className="mx-auto max-w-5xl px-6 py-24 sm:py-32 lg:px-8">
          <div className="text-center">
            <div className="mb-8 flex justify-center">
              <div className="relative rounded-full px-3 py-1 text-sm leading-6 text-muted-foreground ring-1 ring-border/50 hover:ring-border/80">
                SIH 26165 Prototype Environment <span className="text-primary ml-2 font-semibold">Active</span>
              </div>
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-6xl mb-6">
              Detect Risk Before It <br className="hidden sm:block" />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-orange-500">
                Becomes an Incident.
              </span>
            </h1>
            <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl mx-auto">
              AI-powered safety intelligence for identifying Serious Injury & Fatality (SIF) precursors from workplace observations, unsafe acts, unsafe conditions, and near-miss reports.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/login"
                className="rounded-md bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground shadow-sm hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 transition-all flex items-center gap-2"
              >
                Explore Demo <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </div>

        {/* Workflow Visualization */}
        <div className="mt-8 flex justify-center pb-24">
          <div className="flex flex-col sm:flex-row items-center gap-4 sm:gap-8 text-sm font-medium text-muted-foreground">
            <div className="flex items-center gap-2"><FileText className="h-4 w-4" /> Safety Report</div>
            <ArrowRight className="hidden sm:block h-4 w-4 text-border" />
            <div className="flex items-center gap-2 text-primary"><Brain className="h-4 w-4" /> AI Analysis</div>
            <ArrowRight className="hidden sm:block h-4 w-4 text-border" />
            <div className="flex items-center gap-2"><AlertTriangle className="h-4 w-4" /> Risk Score</div>
            <ArrowRight className="hidden sm:block h-4 w-4 text-border" />
            <div className="flex items-center gap-2 text-green-500"><CheckCircle2 className="h-4 w-4" /> Preventive Action</div>
          </div>
        </div>
      </div>
    </div>
  )
}

function FileText(props: any) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><line x1="10" x2="8" y1="9" y2="9"/></svg>
  )
}
