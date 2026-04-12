import { useState, useCallback, useEffect, createContext } from 'react'
import { supabase } from '../supabase'

export type AuthContextType = {
  authenticated: boolean
  userName: string
  login: (userName: string) => void
  logout: () => void
}

export const AuthContext = createContext<AuthContextType | null>(null)

export function useAuth() {
  const [auth, setAuth] = useState<{ authenticated: boolean; userName: string }>({
    authenticated: false,
    userName: 'Demo User',
  })

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      const email = session?.user?.email
      if (email) {
        setAuth({ authenticated: true, userName: email })
      }
    })

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      const email = session?.user?.email
      if (email) {
        setAuth({ authenticated: true, userName: email })
      } else {
        setAuth({ authenticated: false, userName: 'Demo User' })
      }
    })
    return () => subscription.unsubscribe()
  }, [])

  const login = useCallback((userName: string) => {
    setAuth({ authenticated: true, userName })
  }, [])

  const logout = useCallback(async () => {
    await supabase.auth.signOut()
    setAuth({ authenticated: false, userName: 'Demo User' })
  }, [])

  return { ...auth, login, logout }
}
