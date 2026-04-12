import { useState, useCallback, useEffect } from 'react'
import { CheckCircle, AlertCircle } from 'lucide-react'
import {
  getPairs,
  getReports,
  deletePair,
  formatPairTimestamp,
  uploadsUrl,
  type Pair,
  type Report,
} from '../api'
import { toast } from 'sonner'
import { useBackendStatus } from '../contexts/BackendStatusContext'
import {
  Button,
  Card,
  PageHeader,
  Layout,
  CustomSelect,
  Label,
} from '../components'
import { FileText, Trash2 } from 'lucide-react'
import { buildReportMessage } from '../utils/reportMessage'

/** YYYY-MM-DD from pair created_at → readable label for filter dropdown */
function formatDateForDisplay(isoDate: string): string {
  try {
    const d = new Date(`${isoDate}T12:00:00`)
    if (Number.isNaN(d.getTime())) return isoDate
    return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
  } catch {
    return isoDate
  }
}

type DecisionShape = {
  action?: string
  confidence?: string
  summary_reason?: string
  triggered_rules?: string[]
}

function ReportModal({ pairId, pairName, timestamp, onClose }: { pairId: number; pairName: string; timestamp: string; onClose: () => void }) {
  const [reports, setReports] = useState<Report[] | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    getReports(pairId)
      .then((list) => { if (!cancelled) setReports(list) })
      .catch(() => { if (!cancelled) setReports([]) })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [pairId])

  const report: Report | null = reports != null && reports.length > 0
    ? [...reports].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())[0]
    : null

  let isWarning = false
  let decision: DecisionShape | null = null
  let metrics: Record<string, unknown> = {}
  if (report?.decision_json) {
    try {
      decision = JSON.parse(report.decision_json) as DecisionShape
      isWarning = !!(decision?.action === 'RECOMMEND_REVIEW' || decision?.confidence === 'LOW' || decision?.action === 'MONITOR')
    } catch { /* ignore */ }
  }
  if (report?.metrics_json) {
    try {
      metrics = JSON.parse(report.metrics_json) as Record<string, unknown>
    } catch { /* ignore */ }
  }
  const triggered = decision?.triggered_rules ?? []
  const colorExceeded = triggered.includes('color_deltaE')
  const sizeExceeded = triggered.includes('area_change_percent') || triggered.includes('diameter_increase_mm')
  const shapeExceeded = triggered.includes('irregularity_delta')
  const reportMessage = buildReportMessage(decision, metrics)

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-[1000] p-8" onClick={onClose}>
      <div className="bg-card border border-border rounded-card shadow-card-hover max-w-lg w-full max-h-[90vh] overflow-auto p-6" onClick={(e) => e.stopPropagation()}>
        <h2 className="text-xl font-semibold text-text-primary mt-0 mb-1">{pairName || `Pair ${pairId}`}</h2>
        <p className="text-sm text-text-muted mb-4">{formatPairTimestamp(timestamp)}</p>

        {loading && <p className="text-text-muted">Loading report…</p>}

        {!loading && !report && (
          <p className="text-text-muted mb-6">No saved report for this pair.</p>
        )}

        {!loading && report && (
          <div className="space-y-4">
            <div
              className={`rounded-lg p-4 border-l-4 ${
                isWarning
                  ? 'border-semantic-error bg-semantic-error/10'
                  : 'border-semantic-success bg-semantic-success/10'
              }`}
            >
              <div className="flex items-start gap-3">
                {isWarning ? (
                  <AlertCircle className="w-5 h-5 shrink-0 text-semantic-error mt-0.5" aria-hidden />
                ) : (
                  <CheckCircle className="w-5 h-5 shrink-0 text-semantic-success mt-0.5" aria-hidden />
                )}
                <div className="min-w-0 flex-1">
                  <h3 className="text-lg font-semibold text-text-primary m-0 mb-1">Comparison result</h3>
                  <p
                    className="whitespace-pre-wrap text-base leading-relaxed m-0 font-medium"
                    style={{ color: isWarning ? 'var(--semantic-error)' : 'var(--semantic-success)' }}
                  >
                    {reportMessage}
                  </p>
                </div>
              </div>
            </div>
            <div className="rounded-lg border border-border bg-hover-surface p-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-3 m-0">Checks</p>
              <ul className="m-0 p-0 list-none space-y-2">
                <li className="flex items-center gap-2">
                  <span className="text-sm font-medium text-text-primary">Color:</span>
                  <span className={colorExceeded ? 'text-sm font-medium text-semantic-error' : 'text-sm font-medium text-semantic-success'}>
                    {colorExceeded ? 'Change detected' : 'OK'}
                  </span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-sm font-medium text-text-primary">Size:</span>
                  <span className={sizeExceeded ? 'text-sm font-medium text-semantic-error' : 'text-sm font-medium text-semantic-success'}>
                    {sizeExceeded ? 'Change detected' : 'OK'}
                  </span>
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-sm font-medium text-text-primary">Shape:</span>
                  <span className={shapeExceeded ? 'text-sm font-medium text-semantic-error' : 'text-sm font-medium text-semantic-success'}>
                    {shapeExceeded ? 'Change detected' : 'OK'}
                  </span>
                </li>
              </ul>
            </div>
            <p className="text-sm text-text-muted m-0">
              Report saved on {formatPairTimestamp(report.created_at)}
            </p>
          </div>
        )}

        <Button className="mt-6" onClick={onClose}>Close</Button>
      </div>
    </div>
  )
}

function DeleteConfirmModal({ pair, onConfirm, onCancel }: { pair: Pair; onConfirm: () => void; onCancel: () => void }) {
  const name = pair.pair_name || `Pair ${pair.id}`
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-[1000] p-8" onClick={onCancel}>
      <div className="bg-card border border-border rounded-card shadow-card-hover max-w-sm w-full p-6" onClick={(e) => e.stopPropagation()}>
        <h2 className="text-lg font-semibold text-text-primary mt-0 mb-2">Delete image pair?</h2>
        <p className="text-sm text-text-muted mb-1">
          <strong className="text-text-primary">&ldquo;{name}&rdquo;</strong> will be permanently removed from Image History.
        </p>
        <p className="text-sm text-text-muted mb-6 italic">This cannot be undone.</p>
        <div className="flex gap-3 justify-end">
          <Button variant="secondary" onClick={onCancel}>Cancel</Button>
          <Button variant="destructive" onClick={onConfirm}>Delete</Button>
        </div>
      </div>
    </div>
  )
}

function HistoryPage(
  { history, setHistory, setReportModal }: {
    history: Pair[]
    setHistory: React.Dispatch<React.SetStateAction<Pair[]>>
    setReportModal: React.Dispatch<React.SetStateAction<{ pairId: number; pairName: string; timestamp: string } | null>>
  }
) {
  const setBackendError = useBackendStatus()?.setBackendError
  const loadHistory = useCallback(async () => {
    try {
      const list = await getPairs()
      setHistory(list)
      setBackendError?.(false)
    } catch {
      setHistory([])
      setBackendError?.(true)
    }
  }, [setHistory, setBackendError])

  useEffect(() => {
    loadHistory()
  }, [loadHistory])

  const [pairToDelete, setPairToDelete] = useState<Pair | null>(null)
  const [dateFilterValue, setDateFilterValue] = useState(0)
  const [nameFilterValue, setNameFilterValue] = useState(0)

  const uniqueDates = [...new Set(history.map((p) => p.created_at.slice(0, 10)))].sort((a, b) => b.localeCompare(a))
  const uniqueNames = [...new Set(history.map((p) => p.pair_name || `Pair ${p.id}`))].sort((a, b) => a.localeCompare(b))

  const filteredHistory = history.filter((p) => {
    const pairDate = p.created_at.slice(0, 10)
    const pairName = p.pair_name || `Pair ${p.id}`
    const dateMatch = dateFilterValue === 0 || pairDate === uniqueDates[dateFilterValue - 1]
    const nameMatch = nameFilterValue === 0 || pairName === uniqueNames[nameFilterValue - 1]
    return dateMatch && nameMatch
  })

  const handleDeleteClick = useCallback((pair: Pair) => {
    setPairToDelete(pair)
  }, [])

  const handleDeleteConfirm = useCallback(async () => {
    if (!pairToDelete) return
    const name = pairToDelete.pair_name || `Pair ${pairToDelete.id}`
    try {
      await deletePair(pairToDelete.id)
      const list = await getPairs()
      setHistory(list)
      setBackendError?.(false)
      setPairToDelete(null)
      toast.success(`"${name}" has been removed from Image History.`)
    } catch (e) {
      toast.error(String(e))
      setBackendError?.(true)
    }
  }, [pairToDelete, setHistory, setBackendError])

  if (history.length === 0) {
    return (
      <Layout>
        <PageHeader title="Image History" />
        <Card className="border-dashed text-center">
          <p className="m-0 text-text-muted">Upload two images on the <strong className="text-text-primary">Upload / Compare</strong> page to create your first pair.</p>
        </Card>
      </Layout>
    )
  }

  return (
    <Layout>
      {pairToDelete && (
        <DeleteConfirmModal
          pair={pairToDelete}
          onConfirm={handleDeleteConfirm}
          onCancel={() => setPairToDelete(null)}
        />
      )}
      <PageHeader title="Image History" />
      <div className="w-full space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 items-end w-full">
          <div className="min-w-0">
            <Label>Filter by date</Label>
            <CustomSelect
              value={dateFilterValue}
              onChange={setDateFilterValue}
              options={[
                { value: 0, label: 'All dates' },
                ...uniqueDates.map((d, i) => ({ value: i + 1, label: formatDateForDisplay(d) })),
              ]}
              placeholder="All dates"
            />
          </div>
          <div className="min-w-0">
            <Label>Filter by name</Label>
            <CustomSelect
              value={nameFilterValue}
              onChange={setNameFilterValue}
              options={[
                { value: 0, label: 'All names' },
                ...uniqueNames.map((n, i) => ({ value: i + 1, label: n })),
              ]}
              placeholder="All names"
            />
          </div>
        </div>

        {filteredHistory.length === 0 ? (
          <Card className="border-dashed text-center">
            <p className="m-0 text-text-muted">No pairs match the selected filters.</p>
          </Card>
        ) : (
          <div className="overflow-x-auto rounded-card border border-border">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b border-border bg-hover-surface">
                  <th className="text-left text-xs font-semibold uppercase tracking-wider text-text-muted px-4 py-3">Old image</th>
                  <th className="text-left text-xs font-semibold uppercase tracking-wider text-text-muted px-4 py-3">New image</th>
                  <th className="text-left text-xs font-semibold uppercase tracking-wider text-text-muted px-4 py-3">Name</th>
                  <th className="text-left text-xs font-semibold uppercase tracking-wider text-text-muted px-4 py-3">Date</th>
                  <th className="text-right text-xs font-semibold uppercase tracking-wider text-text-muted px-4 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredHistory.map((e, idx) => (
                  <tr
                    key={e.id}
                    className={`border-b border-border ${idx % 2 === 1 ? 'bg-hover-surface' : ''}`}
                  >
                    <td className="px-4 py-3">
                      <div className="w-12 h-12 rounded-lg overflow-hidden bg-hover-surface border border-border shrink-0">
                        <img
                          src={uploadsUrl(e.path_a)}
                          alt="Old image"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="w-12 h-12 rounded-lg overflow-hidden bg-hover-surface border border-border shrink-0">
                        <img
                          src={uploadsUrl(e.path_b)}
                          alt="New image"
                          className="w-full h-full object-cover"
                        />
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <span className="font-bold text-text-primary">{e.pair_name || `Pair ${e.id}`}</span>
                    </td>
                    <td className="px-4 py-3 text-text-muted text-sm">
                      {formatPairTimestamp(e.created_at)}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex justify-end gap-2">
                        <Button
                          variant="primary"
                          onClick={() => setReportModal({ pairId: e.id, pairName: e.pair_name || `Pair ${e.id}`, timestamp: e.created_at })}
                        >
                          <FileText className="w-4 h-4" />
                          View Report
                        </Button>
                        <Button variant="destructive" onClick={() => handleDeleteClick(e)}>
                          <Trash2 className="w-4 h-4" />
                          Delete
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  )
}

export function HistoryPageWithModal(
  { history, setHistory, reportModal, setReportModal }: {
    history: Pair[]
    setHistory: React.Dispatch<React.SetStateAction<Pair[]>>
    reportModal: { pairId: number; pairName: string; timestamp: string } | null
    setReportModal: React.Dispatch<React.SetStateAction<{ pairId: number; pairName: string; timestamp: string } | null>>
  }
) {
  return (
    <>
      {reportModal && (
        <ReportModal
          pairId={reportModal.pairId}
          pairName={reportModal.pairName}
          timestamp={reportModal.timestamp}
          onClose={() => setReportModal(null)}
        />
      )}
      <HistoryPage history={history} setHistory={setHistory} setReportModal={setReportModal} />
    </>
  )
}
