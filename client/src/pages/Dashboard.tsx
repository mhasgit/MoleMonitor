import { useEffect, useMemo, useState } from 'react'
import { getPairs, getReports } from '../api'
import type { Pair } from '../api'
import { Card, Layout, ReportDatesCalendar } from '../components'
import { AlertTriangle } from 'lucide-react'

function toYYYYMMDD(d: Date): string {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

function reportIndicatesChange(decisionJson: string): boolean {
  try {
    const d = JSON.parse(decisionJson) as { action?: string }
    return d.action === 'MONITOR' || d.action === 'RECOMMEND_REVIEW'
  } catch {
    return false
  }
}

export function Dashboard({ userName: _userName, history, setHistory }: { userName: string; history: Pair[]; setHistory: React.Dispatch<React.SetStateAction<Pair[]>> }) {
  const [calendarYear, setCalendarYear] = useState(() => new Date().getFullYear())
  const [calendarMonth, setCalendarMonth] = useState(() => new Date().getMonth())
  const [pairsWithChanges, setPairsWithChanges] = useState(0)

  useEffect(() => {
    getPairs().then(setHistory).catch(() => setHistory([]))
  }, [setHistory])

  useEffect(() => {
    if (history.length === 0) {
      setPairsWithChanges(0)
      return
    }
    let cancelled = false
    Promise.all(history.map((p) => getReports(p.id)))
      .then((allReports) => {
        if (cancelled) return
        let n = 0
        for (const reports of allReports) {
          if (reports.some((r) => reportIndicatesChange(r.decision_json))) n++
        }
        setPairsWithChanges(n)
      })
      .catch(() => {
        if (!cancelled) setPairsWithChanges(0)
      })
    return () => {
      cancelled = true
    }
  }, [history])

  const reportDatesSet = useMemo(() => {
    const set = new Set<string>()
    for (const e of history) {
      const s = e.created_at.replace(/Z$/i, '')
      try {
        const d = new Date(s)
        set.add(toYYYYMMDD(d))
      } catch {
        // skip invalid
      }
    }
    return set
  }, [history])

  const reportCount = history.length
  const totalImages = reportCount * 2

  return (
    <Layout>
      <div className="rounded-card shadow-card-elevated dark:shadow-card-elevated-dark px-6 py-4 mb-6 flex gap-4 items-start bg-yellow-200 bg-yellow-900/8 border border-yellow-300 dark:border-yellow-700/50">
        <AlertTriangle className="w-7 h-7 shrink-0 mt-0.5 text-amber-600 dark:text-amber-400" aria-hidden />
        <div>
          <p className="text-lg font-bold m-0 mb-1 text-amber-600 dark:text-amber-400">Important disclaimer</p>
          <p className="m-0 text-base leading-relaxed text-text-primary font-normal">
            MoleMonitor does not provide medical diagnosis. It only helps you store and compare images. If you have any concern about a mole or your skin health, please consult a healthcare professional.
          </p>
        </div>
      </div>
      <div className="w-full flex-1 min-h-0 flex flex-col gap-6">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 shrink-0">
            <Card className="!border-0 shadow-card-elevated hover:shadow-card-elevated-hover dark:shadow-card-elevated-dark dark:hover:shadow-card-elevated-hover-dark transition-shadow duration-200">
              <p className="text-base font-semibold uppercase tracking-wide m-0" style={{ color: '#22c55e' }}>Reports generated</p>
              <p className="text-sm text-text-muted mt-1 m-0">Mole pair comparisons saved to your history.</p>
              <p className="text-2xl font-bold text-text-primary mt-2 m-0">{reportCount}</p>
            </Card>
            <Card className="!border-0 shadow-card-elevated hover:shadow-card-elevated-hover dark:shadow-card-elevated-dark dark:hover:shadow-card-elevated-hover-dark transition-shadow duration-200">
              <p className="text-base font-semibold uppercase tracking-wide m-0" style={{ color: '#22c55e' }}>Overall changes</p>
              <p className="text-sm text-text-muted mt-1 m-0">Comparisons where the system detected changes.</p>
              <p className="text-2xl font-bold text-text-primary mt-2 m-0">{pairsWithChanges}</p>
            </Card>
            <Card className="!border-0 shadow-card-elevated hover:shadow-card-elevated-hover dark:shadow-card-elevated-dark dark:hover:shadow-card-elevated-hover-dark transition-shadow duration-200">
              <p className="text-base font-semibold uppercase tracking-wide m-0" style={{ color: '#22c55e' }}>Total images uploaded</p>
              <p className="text-sm text-text-muted mt-1 m-0">Old and new photos you&apos;ve uploaded.</p>
              <p className="text-2xl font-bold text-text-primary mt-2 m-0">{totalImages}</p>
            </Card>
          </div>
          <Card className="!border-0 shadow-card-elevated hover:shadow-card-elevated-hover dark:shadow-card-elevated-dark dark:hover:shadow-card-elevated-hover-dark transition-shadow duration-200 flex-1 min-h-0 flex flex-col">
            <p className="text-base font-semibold uppercase tracking-wide m-0 shrink-0" style={{ color: '#22c55e' }}>Report dates</p>
            <p className="text-sm text-text-muted mt-1 mb-2 m-0 shrink-0">Days when you saved comparison reports are highlighted in red.</p>
            <div className="flex-1 min-h-0 flex flex-col">
            <ReportDatesCalendar
              reportDatesSet={reportDatesSet}
              year={calendarYear}
              month={calendarMonth}
              onYearMonthChange={(y, m) => {
                setCalendarYear(y)
                setCalendarMonth(m)
              }}
            />
            {reportDatesSet.size === 0 && (
              <p className="m-0 mt-3 text-sm text-text-muted shrink-0">
                No reports yet. Upload and compare images on the Compare Images page. Days with reports will show in red.
              </p>
            )}
            </div>
          </Card>
      </div>
    </Layout>
  )
}
