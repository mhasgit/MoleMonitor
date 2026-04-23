import { Moon, Sun, User } from 'lucide-react'
import { useContext, useEffect, useRef, useState } from 'react'
import { AuthContext } from '../contexts/AuthContext'
import { useTheme } from '../contexts/ThemeContext'

export function HeaderBar() {
  const { theme, toggleTheme } = useTheme()
  const auth = useContext(AuthContext)
  const [showUserCard, setShowUserCard] = useState(false)
  const userCardRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const onDocMouseDown = (event: MouseEvent) => {
      if (!userCardRef.current) return
      if (event.target instanceof Node && !userCardRef.current.contains(event.target)) {
        setShowUserCard(false)
      }
    }
    document.addEventListener('mousedown', onDocMouseDown)
    return () => document.removeEventListener('mousedown', onDocMouseDown)
  }, [])

  const fullName = auth?.user?.full_name?.trim() || auth?.userName || 'User'
  const email = auth?.user?.email || 'No email'

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-16 flex items-center justify-between px-6 py-4 bg-surface border-b border-border">
      <h1 className="text-xl font-semibold tracking-tight text-text-primary">
        MoleMonitor
      </h1>
      <div className="flex items-center gap-3">
        <div className="relative" ref={userCardRef}>
          <button
            type="button"
            onClick={() => setShowUserCard((v) => !v)}
            className="inline-flex items-center gap-2 h-10 px-3 rounded-button border border-border bg-card text-text-primary hover:bg-hover-surface focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-surface transition-colors"
            aria-label="Open user details"
            aria-expanded={showUserCard}
          >
            <User className="w-4 h-4" />
            <span className="text-sm font-semibold">{fullName}</span>
          </button>
          {showUserCard && (
            <div className="absolute right-0 mt-2 w-64 rounded-card border border-border bg-card shadow-card-hover p-3">
              <p className="m-0 text-xs font-semibold uppercase tracking-wider text-text-muted">User details</p>
              <p className="m-0 mt-2 text-sm text-text-primary"><span className="font-semibold">Full name:</span> {fullName}</p>
              <p className="m-0 mt-1 text-sm text-text-primary break-all"><span className="font-semibold">Email:</span> {email}</p>
            </div>
          )}
        </div>
        <button
          type="button"
          onClick={toggleTheme}
          className="flex items-center justify-center w-10 h-10 rounded-button border border-border bg-card text-text-primary hover:bg-hover-surface focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-surface transition-colors"
          aria-label={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
        >
          {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
        </button>
      </div>
    </header>
  )
}
