import { useState, useCallback, useEffect } from 'react'
import {
  getPairs,
  createPair,
  compare,
  saveReport,
  uploadsUrl,
  type Pair,
  type CompareResult,
} from '../api'
import { CheckCircle, AlertCircle } from 'lucide-react'
import { toast } from 'sonner'
import { useBackendStatus } from '../contexts/BackendStatusContext'
import {
  Button,
  Card,
  Input,
  Label,
  Spinner,
  PageHeader,
  ImageUploader,
  Layout,
  CustomSelect,
} from '../components'
import { buildReportMessage } from '../utils/reportMessage'

export function Home() {
  const setBackendError = useBackendStatus()?.setBackendError
  const [history, setHistory] = useState<Pair[]>([])
  const [fileA, setFileA] = useState<File | null>(null)
  const [fileB, setFileB] = useState<File | null>(null)
  const [previewA, setPreviewA] = useState<string | null>(null)
  const [previewB, setPreviewB] = useState<string | null>(null)
  const [fromHistoryA, setFromHistoryA] = useState<{ pairId: number; slot: 'a' | 'b' } | null>(null)
  const [fromHistoryB, setFromHistoryB] = useState<{ pairId: number; slot: 'a' | 'b' } | null>(null)
  const [customLabel, setCustomLabel] = useState('')
  const [scaleMm, setScaleMm] = useState(0)
  const [useClahe, setUseClahe] = useState(false)
  const [blurKernel, setBlurKernel] = useState(0)
  const [compareResult, setCompareResult] = useState<CompareResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const loadHistory = useCallback(async () => {
    try {
      const list = await getPairs()
      setHistory(list)
      setBackendError?.(false)
    } catch {
      setHistory([])
      setBackendError?.(true)
    }
  }, [setBackendError])

  useEffect(() => {
    loadHistory()
  }, [loadHistory])

  const setFileAWithPreview = useCallback((f: File | null) => {
    setPreviewA((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return f ? URL.createObjectURL(f) : null
    })
    setFileA(f)
    setFromHistoryA(null)
  }, [])
  const setFileBWithPreview = useCallback((f: File | null) => {
    setPreviewB((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return f ? URL.createObjectURL(f) : null
    })
    setFileB(f)
    setFromHistoryB(null)
  }, [])

  const bothOk = (fileA !== null || fromHistoryA !== null) && (fileB !== null || fromHistoryB !== null)

  const handleCompare = async () => {
    if (!bothOk) return
    setError(null)
    setLoading(true)
    try {
      let blobA: Blob, blobB: Blob, nameA: string, nameB: string
      if (fileA && fileB) {
        blobA = fileA
        blobB = fileB
        nameA = fileA.name
        nameB = fileB.name
      } else {
        const getBlob = async (path: string) => {
          const r = await fetch(uploadsUrl(path))
          if (!r.ok) throw new Error('Failed to load image')
          return r.blob()
        }
        if (fromHistoryA && fromHistoryB) {
          const pA = history.find((p) => p.id === fromHistoryA.pairId)!
          const pB = history.find((p) => p.id === fromHistoryB.pairId)!
          const pathA = fromHistoryA.slot === 'a' ? pA.path_a : pA.path_b
          const pathB = fromHistoryB.slot === 'a' ? pB.path_a : pB.path_b
          blobA = await getBlob(pathA)
          blobB = await getBlob(pathB)
          nameA = fromHistoryA.slot === 'a' ? pA.filename_a : pA.filename_b
          nameB = fromHistoryB.slot === 'a' ? pB.filename_a : pB.filename_b
        } else {
          throw new Error('Need both images')
        }
      }
      const fA = blobA instanceof File ? blobA : new File([blobA], nameA || 'a.jpg', { type: 'image/jpeg' })
      const fB = blobB instanceof File ? blobB : new File([blobB], nameB || 'b.jpg', { type: 'image/jpeg' })
      const result = await compare(fA, fB, {
        scaleMm: scaleMm > 0 ? scaleMm : undefined,
        useClahe,
        blurKernelSize: blurKernel || 0,
      })
      setCompareResult(result)
    } catch (e) {
      const msg = String(e)
      setError(msg)
      toast.error(msg)
      setCompareResult(null)
    } finally {
      setLoading(false)
    }
  }

  const handleSavePair = async () => {
    if (!bothOk || !fileA || !fileB) {
      const msg = 'Save pair to history requires both images to be uploaded (not only from history).'
      setError(msg)
      toast.error(msg)
      return
    }
    setError(null)
    setLoading(true)
    try {
      await createPair(fileA, fileB, customLabel || undefined, fileA.name, fileB.name)
      toast.success('Saved.')
      loadHistory()
    } catch (e) {
      const msg = String(e)
      setError(msg)
      toast.error(msg)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveReport = async () => {
    if (!compareResult) return
    setError(null)
    setLoading(true)
    try {
      let pairId: number | null = null
      if (fromHistoryA && fromHistoryB && fromHistoryA.pairId === fromHistoryB.pairId) {
        pairId = fromHistoryA.pairId
      }
      if (pairId == null && fileA && fileB) {
        const created = await createPair(fileA, fileB, customLabel || undefined, fileA.name, fileB.name)
        pairId = created.id
        loadHistory()
      }
      if (pairId != null) {
        await saveReport(pairId, {
          created_at: compareResult.created_at,
          algo_version: compareResult.algo_version,
          metrics: compareResult.metrics,
          decision: compareResult.decision,
          message_text: compareResult.message_text,
        })
        toast.success('Report saved.')
      } else {
        const msg = 'Could not determine pair to save report to.'
        setError(msg)
        toast.error(msg)
      }
    } catch (e) {
      const msg = String(e)
      setError(msg)
      toast.error(msg)
    } finally {
      setLoading(false)
    }
  }

  const decision = compareResult?.decision as { action?: string; confidence?: string; triggered_rules?: string[] } | undefined
  const isWarning = decision && (decision.action === 'RECOMMEND_REVIEW' || decision.confidence === 'LOW' || decision.action === 'MONITOR')
  const triggered = decision?.triggered_rules ?? []
  const colorExceeded = triggered.includes('color_deltaE')
  const sizeExceeded = triggered.includes('area_change_percent') || triggered.includes('diameter_increase_mm')
  const shapeExceeded = triggered.includes('irregularity_delta')

  const previewPairA = fromHistoryA ? history.find((p) => p.id === fromHistoryA.pairId) : null
  const previewPairB = fromHistoryB ? history.find((p) => p.id === fromHistoryB.pairId) : null
  const srcA = previewA ?? (previewPairA ? uploadsUrl(fromHistoryA!.slot === 'a' ? previewPairA.path_a : previewPairA.path_b) : null)
  const srcB = previewB ?? (previewPairB ? uploadsUrl(fromHistoryB!.slot === 'a' ? previewPairB.path_a : previewPairB.path_b) : null)

  const uploadedList: { path: string; label: string }[] = []
  const seen = new Set<string>()
  history.forEach((e) => {
    for (const [path, name] of [[e.path_a, e.filename_a], [e.path_b, e.filename_b]] as [string, string][]) {
      if (path && !seen.has(path)) {
        seen.add(path)
        uploadedList.push({ path, label: name || path.replace(/^.*[/\\]/, '') || 'Unknown' })
      }
    }
  })

  return (
    <Layout>
      <PageHeader title="Upload & Compare" />
      <div className="w-full space-y-8">
      <section className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ImageUploader
            label="Image A"
            file={fileA}
            previewUrl={srcA}
            onFileChange={setFileAWithPreview}
            accept=".jpg,.jpeg,.png,.webp,.bmp"
            disabled={loading}
          />
          <ImageUploader
            label="Image B"
            file={fileB}
            previewUrl={srcB}
            onFileChange={setFileBWithPreview}
            accept=".jpg,.jpeg,.png,.webp,.bmp"
            disabled={loading}
          />
        </div>
      </section>

      {uploadedList.length > 0 && (
        <section className="mt-8">
          <Card className="p-5">
            <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-4">From uploads</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Image A from uploads</Label>
                <CustomSelect
                  value={fromHistoryA ? uploadedList.findIndex((u) => {
                    const entry = history.find((p) => p.id === fromHistoryA.pairId)
                    if (!entry) return -1
                    const path = fromHistoryA.slot === 'a' ? entry.path_a : entry.path_b
                    return u.path === path
                  }) + 1 : 0}
                  onChange={(i) => {
                    if (i <= 0) setFromHistoryA(null)
                    else {
                      const u = uploadedList[i - 1]
                      const entry = history.find((p) => p.path_a === u.path || p.path_b === u.path)
                      if (entry) setFromHistoryA({ pairId: entry.id, slot: entry.path_a === u.path ? 'a' : 'b' })
                    }
                  }}
                  options={[
                    { value: 0, label: '— Select image —' },
                    ...uploadedList.map((u, i) => ({ value: i + 1, label: u.label })),
                  ]}
                  placeholder="— Select image —"
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label>Image B from uploads</Label>
                <CustomSelect
                  value={fromHistoryB ? uploadedList.findIndex((u) => {
                    const entry = history.find((p) => p.id === fromHistoryB.pairId)
                    if (!entry) return -1
                    const path = fromHistoryB.slot === 'a' ? entry.path_a : entry.path_b
                    return u.path === path
                  }) + 1 : 0}
                  onChange={(i) => {
                    if (i <= 0) setFromHistoryB(null)
                    else {
                      const u = uploadedList[i - 1]
                      const entry = history.find((p) => p.path_a === u.path || p.path_b === u.path)
                      if (entry) setFromHistoryB({ pairId: entry.id, slot: entry.path_a === u.path ? 'a' : 'b' })
                    }
                  }}
                  options={[
                    { value: 0, label: '— Select image —' },
                    ...uploadedList.map((u, i) => ({ value: i + 1, label: u.label })),
                  ]}
                  placeholder="— Select image —"
                  className="mt-1.5"
                />
              </div>
            </div>
          </Card>
        </section>
      )}

      <section className="mt-8">
        <Card className="p-5 space-y-5">
          <div>
            <Label>Pair label (optional)</Label>
            <Input
              type="text"
              placeholder="Leave empty for auto (Pair 1, Pair 2, …)"
              value={customLabel}
              onChange={(e) => setCustomLabel(e.target.value)}
              className="mt-1.5"
            />
            <p className="text-sm text-text-muted mt-1">Give this comparison a name, or leave blank to auto-generate.</p>
          </div>

          <div className="border-l-4 border-accent pl-4 rounded-r-lg rounded-l-none bg-hover-surface py-4 pr-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-4">Compare options</p>
            <div className="space-y-4">
              <div>
                <Label>Scale (pixels per mm; leave 0 for unavailable)</Label>
                <Input type="number" min={0} step={0.5} value={scaleMm || ''} onChange={(e) => setScaleMm(Number(e.target.value) || 0)} className="mt-1.5" />
              </div>
              <label className="flex items-center gap-2 cursor-pointer text-text-primary">
                <input type="checkbox" checked={useClahe} onChange={(e) => setUseClahe(e.target.checked)} className="rounded border-border" />
                Use CLAHE (contrast)
              </label>
              <div>
                <Label>Noise reduction (Gaussian blur kernel size): {blurKernel}</Label>
                <input type="range" min={0} max={7} step={2} value={blurKernel} onChange={(e) => setBlurKernel(Number(e.target.value))} className="w-full mt-1" />
              </div>
            </div>
          </div>

          {error && <p className="text-semantic-error font-medium">{error}</p>}
          <div className="flex flex-wrap gap-3 pt-4 border-t border-border">
            <Button disabled={!bothOk || loading} onClick={handleCompare}>
              {loading ? <Spinner size={18} /> : null}
              Compare Images
            </Button>
            <Button variant="secondary" disabled={!bothOk || loading} onClick={handleSavePair}>
              Save Pair
            </Button>
          </div>
        </Card>
      </section>

      {compareResult && (
        <Card className="mt-8 space-y-4">
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
                <h2 className="text-xl font-semibold text-text-primary m-0 mb-1">Comparison result</h2>
                <p
                  className="whitespace-pre-wrap text-base leading-relaxed m-0 font-medium"
                  style={{ color: isWarning ? 'var(--semantic-error)' : 'var(--semantic-success)' }}
                >
                  {buildReportMessage(compareResult.decision as { summary_reason?: string; triggered_rules?: string[] }, compareResult.metrics)}
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
            You can save this result to your Image History for later reference, or run another comparison.
          </p>
          <div className="flex flex-wrap gap-3 pt-2">
            <Button onClick={handleSaveReport}>Save report</Button>
            <Button variant="secondary" onClick={() => { setCompareResult(null); setError(null); }}>Compare again</Button>
          </div>
        </Card>
      )}
      </div>
    </Layout>
  )
}
