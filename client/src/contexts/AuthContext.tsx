import { useState, useCallback, createContext } from 'react'

const AUTH_KEY = 'molemonitor_auth'

export type AuthContextType = {
  authenticated: boolean
  userName: string
  login: (userName: string) => void
  logout: () => void
}

export const AuthContext = createContext<AuthContextType | null>(null)

export function useAuth() {
  const [auth, setAuth] = useState<{ authenticated: boolean; userName: string }>(() => {
    try {
      const raw = localStorage.getItem(AUTH_KEY)
      if (raw) {
        const data = JSON.parse(raw)
        if (data && data.userName) return { authenticated: true, userName: data.userName }
      }
    } catch (_) {}
    return { authenticated: false, userName: 'Demo User' }
  })
  const login = useCallback((userName: string) => {
    setAuth({ authenticated: true, userName })
    localStorage.setItem(AUTH_KEY, JSON.stringify({ userName }))
  }, [])
  const logout = useCallback(() => {
    setAuth({ authenticated: false, userName: 'Demo User' })
    localStorage.removeItem(AUTH_KEY)
  }, [])
  return { ...auth, login, logout }
}
