import { useState, useCallback, useEffect, createContext } from 'react'
import type { AuthUser } from '../authApi'
import { getMe, getStoredToken, setStoredToken } from '../authApi'

export type AuthContextType = {
  authenticated: boolean
  user: AuthUser | null
  /** Display name: full name or email */
  userName: string
  authReady: boolean
  login: (token: string, user: AuthUser) => void
  logout: () => void
}

export const AuthContext = createContext<AuthContextType | null>(null)

function displayName(user: AuthUser | null): string {
  if (!user) return 'Demo User'
  const n = (user.full_name || '').trim()
  return n || user.email
}

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [authReady, setAuthReady] = useState(false)

  useEffect(() => {
    const token = getStoredToken()
    if (!token) {
      setUser(null)
      setAuthReady(true)
      return
    }
    getMe()
      .then((u) => {
        setUser({
          id: u.id,
          email: u.email,
          full_name: u.full_name,
        })
      })
      .catch(() => {
        setStoredToken(null)
        setUser(null)
      })
      .finally(() => setAuthReady(true))
  }, [])

  const login = useCallback((token: string, u: AuthUser) => {
    setStoredToken(token)
    setUser(u)
  }, [])

  const logout = useCallback(() => {
    setStoredToken(null)
    setUser(null)
  }, [])

  return {
    authenticated: !!user,
    user,
    userName: displayName(user),
    authReady,
    login,
    logout,
  }
}
