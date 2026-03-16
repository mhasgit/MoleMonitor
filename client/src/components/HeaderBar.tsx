import { Moon, Sun } from 'lucide-react'
import { useTheme } from '../contexts/ThemeContext'

export function HeaderBar() {
  const { theme, toggleTheme } = useTheme()

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-16 flex items-center justify-between px-6 py-4 bg-surface border-b border-border">
      <h1 className="text-xl font-semibold tracking-tight text-text-primary">
        MoleMonitor
      </h1>
      <button
        type="button"
        onClick={toggleTheme}
        className="flex items-center justify-center w-10 h-10 rounded-button border border-border bg-card text-text-primary hover:bg-hover-surface focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 focus:ring-offset-surface transition-colors"
        aria-label={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
      >
        {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
      </button>
    </header>
  )
}
