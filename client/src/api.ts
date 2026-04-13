/** API client for MoleMonitor backend. */

import { authHeaders } from './authApi'

const API = '/api'

/** Thrown for non-OK HTTP responses so callers can distinguish 401 from network failures. */
export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function jsonErrorBody(r: Response): Promise<never> {
  let msg = r.statusText
  const t = await r.text()
  try {
    const j = JSON.parse(t) as { error?: string }
    msg = j.error ?? t
  } catch {
    msg = t || msg
  }
  throw new ApiError(String(msg), r.status)
}

async function apiFetch(path: string, init?: RequestInit): Promise<Response> {
  const headers = new Headers(init?.headers)
  const base = authHeaders(false) as Record<string, string>
  if (base.Authorization) headers.set('Authorization', base.Authorization)
  return fetch(path, { ...init, headers })
}

export type Pair = {
  id: number
  pair_name: string
  filename_a: string
  filename_b: string
  path_a: string
  path_b: string
  created_at: string
}

export type Report = {
  id: number
  pair_id: number
  created_at: string
  algo_version: string
  metrics_json: string
  decision_json: string
  message_text: string
  overlay_path: string | null
  mask_a_path: string | null
  mask_b_path: string | null
}

export type CompareResult = {
  created_at: string
  algo_version: string
  metrics: Record<string, unknown>
  decision: Record<string, unknown>
  message_text: string
  mask_a_b64: string | null
  mask_b_b64: string | null
  contour_a_b64: string | null
  contour_b_b64: string | null
  change_highlight_b64: string | null
}

export async function getPairs(): Promise<Pair[]> {
  const r = await apiFetch(`${API}/pairs`)
  if (!r.ok) return jsonErrorBody(r)
  return r.json()
}

export async function getPair(id: number): Promise<Pair | null> {
  const r = await apiFetch(`${API}/pairs/${id}`)
  if (r.status === 404) return null
  if (!r.ok) throw new Error(await r.text().catch(() => r.statusText))
  return r.json()
}

export async function createPair(
  imageA: File,
  imageB: File,
  pairName?: string,
  filenameA?: string,
  filenameB?: string
): Promise<{ id: number; pair_name: string }> {
  const form = new FormData()
  form.append('image_a', imageA)
  form.append('image_b', imageB)
  if (pairName != null) form.append('pair_name', pairName)
  form.append('filename_a', filenameA ?? imageA.name ?? 'upload')
  form.append('filename_b', filenameB ?? imageB.name ?? 'upload')
  const r = await apiFetch(`${API}/pairs`, { method: 'POST', body: form })
  if (!r.ok) {
    const j = await r.json().catch(() => ({}))
    throw new Error((j as { error?: string }).error ?? r.statusText)
  }
  return r.json()
}

export async function deletePair(id: number): Promise<void> {
  const r = await apiFetch(`${API}/pairs/${id}`, { method: 'DELETE' })
  if (!r.ok) throw new Error(await r.text().catch(() => r.statusText))
}

export async function clearPairs(): Promise<void> {
  const r = await apiFetch(`${API}/pairs`, { method: 'DELETE' })
  if (!r.ok) throw new Error(await r.text().catch(() => r.statusText))
}

export async function compare(
  imageA: File | Blob,
  imageB: File | Blob,
  options: { scaleMm?: number; useClahe?: boolean; blurKernelSize?: number } = {}
): Promise<CompareResult> {
  const form = new FormData()
  const fileA = imageA instanceof File ? imageA : new File([imageA], 'image_a.jpg', { type: 'image/jpeg' })
  const fileB = imageB instanceof File ? imageB : new File([imageB], 'image_b.jpg', { type: 'image/jpeg' })
  form.append('image_a', fileA)
  form.append('image_b', fileB)
  if (options.scaleMm != null && options.scaleMm > 0) form.append('scale_mm', String(options.scaleMm))
  form.append('use_clahe', options.useClahe ? '1' : '0')
  form.append('blur_kernel_size', String(options.blurKernelSize ?? 0))
  const r = await apiFetch(`${API}/compare`, { method: 'POST', body: form })
  if (!r.ok) {
    const j = await r.json().catch(() => ({}))
    throw new Error((j as { error?: string }).error ?? r.statusText)
  }
  return r.json()
}

/** Basename of stored path for /uploads/ URL */
function uploadsPath(path: string): string {
  return path.replace(/^.*[/\\]/, '')
}

/** Full URL for an uploaded file (for img src, etc.) */
export function uploadsUrl(path: string): string {
  return `/uploads/${uploadsPath(path)}`
}

/** Re-compare using images from a saved pair (fetches by path then calls compare). */
export async function compareFromPair(
  pair: Pair,
  options: { scaleMm?: number; useClahe?: boolean; blurKernelSize?: number } = {}
): Promise<CompareResult> {
  const [blobA, blobB] = await Promise.all([
    fetch(`/uploads/${uploadsPath(pair.path_a)}`).then((r) => (r.ok ? r.blob() : Promise.reject(new Error('Failed to load old image')))),
    fetch(`/uploads/${uploadsPath(pair.path_b)}`).then((r) => (r.ok ? r.blob() : Promise.reject(new Error('Failed to load new image')))),
  ])
  return compare(blobA, blobB, options)
}

export async function getReports(pairId: number): Promise<Report[]> {
  const r = await apiFetch(`${API}/pairs/${pairId}/reports`)
  if (!r.ok) throw new Error(await r.text().catch(() => r.statusText))
  return r.json()
}

export async function saveReport(
  pairId: number,
  snapshot: {
    created_at: string
    algo_version: string
    metrics: Record<string, unknown>
    decision: Record<string, unknown>
    message_text: string
    overlay_path?: string | null
    mask_a_path?: string | null
    mask_b_path?: string | null
  }
): Promise<{ id: number }> {
  const r = await apiFetch(`${API}/pairs/${pairId}/reports`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ snapshot }),
  })
  if (!r.ok) throw new Error(await r.text().catch(() => r.statusText))
  return r.json()
}

/** Format pair created_at for display */
export function formatPairTimestamp(iso: string): string {
  if (!iso) return 'Unknown date'
  try {
    const s = iso.replace(/Z$/i, '')
    const d = new Date(s)
    return d.toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    })
  } catch {
    return iso || 'Unknown date'
  }
}
