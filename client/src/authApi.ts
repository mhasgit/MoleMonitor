/** Flask JWT auth API. */

const API = '/api'
const TOKEN_KEY = 'molemonitor_access_token'

export type AuthUser = {
  id: number
  email: string
  full_name: string
}

export function getStoredToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setStoredToken(token: string | null): void {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    /* ignore */
  }
}

export function authHeaders(json = false): HeadersInit {
  const h: Record<string, string> = {}
  if (json) h['Content-Type'] = 'application/json'
  const t = getStoredToken()
  if (t) h['Authorization'] = `Bearer ${t}`
  return h
}

async function parseError(r: Response): Promise<string> {
  const j = await r.json().catch(() => ({}))
  return (j as { error?: string }).error ?? r.statusText
}

export async function registerUser(body: {
  full_name: string
  email: string
  password: string
  phone: string
}): Promise<void> {
  const r = await fetch(`${API}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!r.ok) throw new Error(await parseError(r))
}

export async function loginUser(email: string, password: string): Promise<{ token: string; user: AuthUser }> {
  const r = await fetch(`${API}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!r.ok) throw new Error(await parseError(r))
  return r.json()
}

export async function getMe(): Promise<AuthUser & { phone?: string | null }> {
  const r = await fetch(`${API}/auth/me`, { headers: authHeaders() })
  if (!r.ok) throw new Error(await parseError(r))
  return r.json()
}

export async function verifyPhoneForReset(phone: string): Promise<{ reset_token: string }> {
  const r = await fetch(`${API}/auth/forgot/verify-phone`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ phone }),
  })
  if (!r.ok) throw new Error(await parseError(r))
  return r.json()
}

export async function resetPasswordWithToken(resetToken: string, newPassword: string): Promise<void> {
  const r = await fetch(`${API}/auth/forgot/reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reset_token: resetToken, new_password: newPassword }),
  })
  if (!r.ok) throw new Error(await parseError(r))
}
