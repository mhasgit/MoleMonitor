import { useEffect, useMemo, useState } from 'react'
import { getPairs } from '../api'
import type { Pair } from '../api'
import { Card, Layout, ReportDatesCalendar } from '../components'

function toYYYYMMDD(d: Date): string {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

export function Dashboard({ userName: _userName, history, setHistory }: { userName: string; history: Pair[]; setHistory: React.Dispatch<React.SetStateAction<Pair[]>> }) {
  const [calendarYear, setCalendarYear] = useState(() => new Date().getFullYear())
  const [calendarMonth, setCalendarMonth] = useState(() => new Date().getMonth())

  useEffect(() => {
    getPairs().then(setHistory).catch(() => setHistory([]))
  }, [setHistory])

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
    // Mock report dates for demo (current month + previous + next)
    const now = new Date()
    const y = now.getFullYear()
    const m = now.getMonth() // 0-11
    const currMonth = String(m + 1).padStart(2, '0')
    const prevMonth = m === 0 ? '12' : String(m).padStart(2, '0')
    const prevYear = m === 0 ? y - 1 : y
    const nextMonth = m === 11 ? '01' : String(m + 2).padStart(2, '0')
    const nextYear = m === 11 ? y + 1 : y
    const mockDates = [
      `${y}-${currMonth}-05`,
      `${y}-${currMonth}-12`,
      `${y}-${currMonth}-19`,
      `${y}-${currMonth}-25`,
      `${prevYear}-${prevMonth}-15`,
      `${prevYear}-${prevMonth}-28`,
      `${nextYear}-${nextMonth}-03`,
      `${nextYear}-${nextMonth}-17`,
    ]
    mockDates.forEach((d) => set.add(d))
    return set
  }, [history])

  const reportCount = history.length
  const totalImages = reportCount * 2

  return (
    <Layout>
      <div className="w-full flex-1 min-h-0 flex flex-col gap-6">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 shrink-0">
            <Card className="border-l-4 border-l-accent">
              <p className="text-xs font-semibold uppercase tracking-wide text-text-muted m-0">Reports generated</p>
              <p className="text-2xl font-bold text-text-primary mt-2 m-0">{reportCount}</p>
            </Card>
            <Card className="border-l-4 border-l-accent">
              <p className="text-xs font-semibold uppercase tracking-wide text-text-muted m-0">Overall changes</p>
              <p className="text-2xl font-bold text-text-primary mt-2 m-0">{Math.min(reportCount * 2, 7)}</p>
            </Card>
            <Card className="border-l-4 border-l-accent">
              <p className="text-xs font-semibold uppercase tracking-wide text-text-muted m-0">Total images uploaded</p>
              <p className="text-2xl font-bold text-text-primary mt-2 m-0">{totalImages}</p>
            </Card>
          </div>
          <Card className="border-l-4 border-l-accent flex-1 min-h-0 flex flex-col">
            <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-2 shrink-0">Report dates</p>
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
