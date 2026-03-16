import { AlertCircle } from 'lucide-react'
import { useBackendStatus } from '../contexts/BackendStatusContext'
import { Sidebar } from './Sidebar'
import { HeaderBar } from './HeaderBar'
import { Button } from './Button'

export function Layout({ children }: { children: React.ReactNode }) {
  const status = useBackendStatus()
  return (
    <div className="flex flex-col h-screen overflow-hidden bg-surface">
      <HeaderBar />
      <div className="flex flex-1 min-h-0 overflow-hidden pt-16">
        <Sidebar />
        <main className="flex-1 w-full overflow-y-auto overflow-x-hidden bg-surface min-w-0 px-6 py-8 sm:px-8 md:px-10 lg:px-12 flex flex-col">
          {status?.backendError && (
            <div className="mb-6 flex flex-wrap items-center justify-between gap-3 rounded-card border border-semantic-warning bg-amber-50 dark:bg-amber-950/40 px-4 py-3 text-sm text-text-primary shrink-0">
            <span className="flex items-center gap-2">
              <AlertCircle className="h-4 w-4 shrink-0 text-semantic-warning" />
              Can't connect to the server. Make sure the backend is running (e.g. port 5000) and try again.
            </span>
            <div className="flex gap-2">
              <Button variant="secondary" onClick={status.retry}>Retry</Button>
              <Button variant="ghost" onClick={() => status.setBackendError(false)}>Dismiss</Button>
            </div>
            </div>
          )}
          <div className="flex-1 min-h-0 flex flex-col">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
