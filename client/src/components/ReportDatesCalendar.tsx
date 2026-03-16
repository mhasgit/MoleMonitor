import { ChevronLeft, ChevronRight } from 'lucide-react'
import { CustomSelect } from './CustomSelect'

const MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

function toYYYYMMDD(d: Date): string {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

function getDaysInMonth(year: number, month: number): number {
  return new Date(year, month + 1, 0).getDate()
}

function getFirstWeekday(year: number, month: number): number {
  return new Date(year, month, 1).getDay()
}

export type ReportDatesCalendarProps = {
  reportDatesSet: Set<string>
  year: number
  month: number
  onYearMonthChange: (year: number, month: number) => void
}

export function ReportDatesCalendar({ reportDatesSet, year, month, onYearMonthChange }: ReportDatesCalendarProps) {
  const daysInMonth = getDaysInMonth(year, month)
  const firstWeekday = getFirstWeekday(year, month)
  const paddingStart = firstWeekday
  const totalCells = 42
  const cells: { day: number | null; dateKey: string | null }[] = []

  for (let i = 0; i < paddingStart; i++) {
    cells.push({ day: null, dateKey: null })
  }
  for (let day = 1; day <= daysInMonth; day++) {
    const d = new Date(year, month, day)
    cells.push({ day, dateKey: toYYYYMMDD(d) })
  }
  while (cells.length < totalCells) {
    cells.push({ day: null, dateKey: null })
  }

  const goPrev = () => {
    if (month === 0) onYearMonthChange(year - 1, 11)
    else onYearMonthChange(year, month - 1)
  }
  const goNext = () => {
    if (month === 11) onYearMonthChange(year + 1, 0)
    else onYearMonthChange(year, month + 1)
  }

  const currentYear = new Date().getFullYear()
  const years = [currentYear - 2, currentYear - 1, currentYear, currentYear + 1, currentYear + 2]

  return (
    <div className="report-dates-calendar flex-1 flex flex-col min-h-0">
      <div className="flex items-center justify-between gap-2 mb-4 shrink-0">
        <button
          type="button"
          onClick={goPrev}
          className="calendar-nav-btn flex items-center justify-center w-8 h-8 rounded-lg border border-border hover:bg-hover-surface transition-colors text-text-primary"
          aria-label="Previous month"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>
        <div className="flex items-center gap-2 flex-1 justify-center">
          <div className="min-w-[7rem] calendar-month-select">
            <CustomSelect
              value={month}
              onChange={(m) => onYearMonthChange(year, m)}
              options={MONTH_NAMES.map((name, i) => ({ value: i, label: name }))}
              triggerClassName="text-sm font-medium py-1.5 px-2"
            />
          </div>
          <div className="min-w-[5rem] calendar-year-select">
            <CustomSelect
              value={year}
              onChange={(y) => onYearMonthChange(y, month)}
              options={years.map((y) => ({ value: y, label: String(y) }))}
              triggerClassName="text-sm font-medium py-1.5 px-2"
            />
          </div>
        </div>
        <button
          type="button"
          onClick={goNext}
          className="calendar-nav-btn flex items-center justify-center w-8 h-8 rounded-lg border border-border hover:bg-hover-surface transition-colors text-text-primary"
          aria-label="Next month"
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
      <div className="grid grid-cols-7 gap-0.5 text-center text-sm flex-1 min-h-0 auto-rows-fr">
        {WEEKDAYS.map((wd) => (
          <div key={wd} className="calendar-weekday py-1 font-medium flex items-center justify-center text-text-primary">
            {wd}
          </div>
        ))}
        {cells.map(({ day, dateKey }, i) => {
          const isReportDate = dateKey != null && reportDatesSet.has(dateKey)
          return (
            <div
              key={i}
              className="min-h-[32px] flex items-center justify-center"
            >
              {day != null ? (
                <span
                  className={`inline-flex items-center justify-center w-8 h-8 rounded-full font-medium transition-colors text-text-primary ${
                    isReportDate
                      ? 'calendar-day border-2 border-semantic-error bg-transparent hover:bg-red-500/10'
                      : 'calendar-day hover:bg-hover-surface'
                  }`}
                >
                  {day}
                </span>
              ) : null}
            </div>
          )
        })}
      </div>
    </div>
  )
}
