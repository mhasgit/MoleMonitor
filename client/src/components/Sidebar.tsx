import { Link, useLocation, useNavigate } from 'react-router-dom'
import {
  LayoutDashboard,
  Upload,
  History,
  BookOpen,
  Info,
  LogOut,
} from 'lucide-react'
import { useContext } from 'react'
import { AuthContext } from '../contexts/AuthContext'

const SIDEBAR_PAGES = [
  { label: 'Home', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Compare Moles', path: '/home', icon: Upload },
  { label: 'Moles History', path: '/history', icon: History },
  { label: 'Instructions', path: '/instructions', icon: BookOpen },
  { label: 'About', path: '/about', icon: Info },
]

export function Sidebar() {
  const location = useLocation()
  const navigate = useNavigate()
  const auth = useContext(AuthContext)

  const handleLogout = () => {
    auth?.logout()
    navigate('/login')
  }

  return (
    <aside className="sidebar-nav w-[220px] shrink-0 flex flex-col h-full overflow-hidden bg-surface border-r border-border">
      <nav className="flex flex-col flex-1 gap-1 pt-4 px-3 min-h-0">
        {SIDEBAR_PAGES.map(({ label, path, icon: Icon }) => {
          const isActive = location.pathname === path
          return (
            <Link
              key={path}
              to={path}
              className={`flex items-center gap-2 w-full px-4 py-2.5 rounded-lg font-medium no-underline transition-colors duration-200 text-text-primary ${
                isActive
                  ? 'bg-accent/20 text-accent border border-accent/60 shadow-sm'
                  : 'bg-transparent border border-transparent hover:bg-hover-surface hover:border-border'
              }`}
            >
              <Icon className="w-4 h-4 shrink-0" />
              {label}
            </Link>
          )
        })}
      </nav>
      <div className="mt-auto pt-4 border-t border-border shrink-0 pb-4 px-3">
        <button
          type="button"
          onClick={handleLogout}
          className="flex items-center gap-2 w-full px-4 py-2.5 rounded-lg font-medium bg-transparent border border-transparent hover:bg-hover-surface transition-colors duration-200 cursor-pointer text-left text-text-primary"
        >
          <LogOut className="w-4 h-4 shrink-0" />
          Log out
        </button>
      </div>
    </aside>
  )
}
