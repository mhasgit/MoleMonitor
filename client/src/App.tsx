import { useState, useCallback, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'sonner'
import { AuthContext, useAuth } from './contexts/AuthContext'
import { BackendStatusContext } from './contexts/BackendStatusContext'
import { ThemeProvider, useTheme } from './contexts/ThemeContext'
import { getPairs, ApiError } from './api'
import type { Pair } from './api'
import {
  Home,
  Dashboard,
  HistoryPageWithModal,
  Instructions,
  About,
  Landing,
  Login,
  Register,
  ForgotPassword,
} from './pages'

function ToasterWithTheme() {
  const { theme } = useTheme()
  return (
    <Toaster
      theme={theme}
      position="top-right"
      richColors
      toastOptions={{
        style: {
          background: 'var(--card)',
          border: '1px solid var(--border)',
          color: 'var(--text-primary)',
        },
      }}
    />
  )
}

export default function App() {
  const auth = useAuth()
  const [history, setHistory] = useState<Pair[]>([])
  const [reportModal, setReportModal] = useState<{ pairId: number; pairName: string; timestamp: string } | null>(null)
  const [backendError, setBackendError] = useState(false)

  const retryBackend = useCallback(async () => {
    try {
      const list = await getPairs()
      setHistory(list)
      setBackendError(false)
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        auth.logout()
        setBackendError(false)
        return
      }
      setBackendError(true)
    }
  }, [auth.logout])

  useEffect(() => {
    if (auth.authenticated && auth.authReady) {
      getPairs()
        .then((list) => {
          setHistory(list)
          setBackendError(false)
        })
        .catch(() => {
          setHistory([])
          setBackendError(true)
        })
    }
    if (!auth.authenticated && auth.authReady) {
      setHistory([])
    }
  }, [auth.authenticated, auth.authReady, auth.logout])

  if (!auth.authReady) {
    return (
      <ThemeProvider>
        <div className="min-h-screen bg-surface" aria-busy="true" />
      </ThemeProvider>
    )
  }

  return (
    <ThemeProvider>
      <ToasterWithTheme />
      <AuthContext.Provider value={auth}>
        <BackendStatusContext.Provider value={{ backendError, setBackendError, retry: retryBackend }}>
          <Routes>
          <Route path="/login" element={auth.authenticated ? <Navigate to="/dashboard" replace /> : <Login onLogin={auth.login} />} />
          <Route path="/register" element={auth.authenticated ? <Navigate to="/dashboard" replace /> : <Register />} />
          <Route path="/forgot-password" element={auth.authenticated ? <Navigate to="/dashboard" replace /> : <ForgotPassword />} />
          <Route path="/" element={<Landing authenticated={auth.authenticated} />} />
          <Route path="/dashboard" element={auth.authenticated ? <Dashboard userName={auth.userName} history={history} setHistory={setHistory} /> : <Navigate to="/login" replace />} />
          <Route path="/home" element={auth.authenticated ? <Home /> : <Navigate to="/login" replace />} />
          <Route path="/history" element={auth.authenticated ? <HistoryPageWithModal history={history} setHistory={setHistory} reportModal={reportModal} setReportModal={setReportModal} /> : <Navigate to="/login" replace />} />
          <Route path="/instructions" element={auth.authenticated ? <Instructions /> : <Navigate to="/login" replace />} />
          <Route path="/about" element={auth.authenticated ? <About /> : <Navigate to="/login" replace />} />
        </Routes>
        </BackendStatusContext.Provider>
      </AuthContext.Provider>
    </ThemeProvider>
  )
}
