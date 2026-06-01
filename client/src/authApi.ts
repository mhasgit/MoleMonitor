/** Flask JWT auth API. */

const API = '/api'
const TOKEN_KEY = 'molemonitor_access_token'

export type AuthUser = {
  id: number
  email: string
  full_name: string
}

export function getStoredToken(): string | null {
  // Read JWT from local storage; gracefully handle storage access failures.
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setStoredToken(token: string | null): void {
  // Persist or clear JWT used by authenticated API requests.
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    /* ignore */
  }
}

export function authHeaders(json = false): HeadersInit {
  // Build common headers, optionally with JSON content-type and bearer token.
  const h: Record<string, string> = {}
  if (json) h['Content-Type'] = 'application/json'
  const t = getStoredToken()
  if (t) h['Authorization'] = `Bearer ${t}`
  return h
}

async function parseError(r: Response): Promise<string> {
  // Normalize backend error responses to a plain user-facing message.
  const j = await r.json().catch(() => ({}))
  return (j as { error?: string }).error ?? r.statusText
}

export async function registerUser(body: {
  full_name: string
  email: string
  password: string
}): Promise<void> {
  // Create a new account in backend auth service.
  const r = await fetch(`${API}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!r.ok) throw new Error(await parseError(r))
}

export async function loginUser(email: string, password: string): Promise<{ token: string; user: AuthUser }> {
  // Exchange credentials for a JWT and minimal user profile.
  const r = await fetch(`${API}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!r.ok) throw new Error(await parseError(r))
  return r.json()
}

export async function getMe(): Promise<AuthUser> {
  // Validate current token and fetch the authenticated user's profile.
  const r = await fetch(`${API}/auth/me`, { headers: authHeaders() })
  if (!r.ok) throw new Error(await parseError(r))
  return r.json()
}

export async function verifyEmailForReset(email: string): Promise<void> {
  // Request a password-reset email for the supplied account address.
  const r = await fetch(`${API}/auth/forgot/verify-email`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })
  if (!r.ok) throw new Error(await parseError(r))
}

export async function resetPasswordWithToken(resetToken: string, newPassword: string): Promise<void> {
  // Complete password reset by sending reset token and new password.
  const r = await fetch(`${API}/auth/forgot/reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reset_token: resetToken, new_password: newPassword }),
  })
  if (!r.ok) throw new Error(await parseError(r))
}
