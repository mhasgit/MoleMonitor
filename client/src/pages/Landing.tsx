import { useNavigate } from 'react-router-dom'
import { Button } from '../components'

export function Landing({ authenticated }: { authenticated: boolean }) {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-surface text-text-primary">
      <header className="w-full border-b border-border bg-card/90 backdrop-blur">
        <div className="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
          <p className="m-0 text-xl font-bold tracking-tight text-text-primary">MoleMonitor</p>
          <div className="flex items-center gap-2">
            {authenticated ? (
              <Button onClick={() => navigate('/dashboard')}>Go to dashboard</Button>
            ) : (
              <>
                <Button variant="secondary" onClick={() => navigate('/login')}>
                  Login
                </Button>
                <Button onClick={() => navigate('/register')}>Register</Button>
              </>
            )}
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-12 md:py-20">
        <section className="relative overflow-hidden rounded-2xl border border-border bg-card px-8 py-14 md:px-14 shadow-card">
          <div className="absolute -top-24 -right-16 h-64 w-64 rounded-full bg-accent/20 blur-3xl" aria-hidden />
          <div className="absolute -bottom-24 -left-16 h-64 w-64 rounded-full bg-semantic-success/20 blur-3xl" aria-hidden />

          <div className="relative z-10 max-w-3xl">
            <span className="inline-flex rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-sm font-medium text-accent">
              Skin image tracking made simple
            </span>
            <h1 className="mt-5 text-4xl leading-tight md:text-5xl font-semibold text-text-primary">
              Track mole photo changes in one secure place
            </h1>
            <p className="mt-4 mb-0 text-base md:text-lg text-text-muted">
              Upload before and after images, run comparisons, and keep your history organized over time.
              MoleMonitor helps you monitor your records while reminding you to consult professionals for
              medical concerns.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              {!authenticated && (
                <>
                  <Button className="px-6 py-3 text-base" onClick={() => navigate('/register')}>
                    Create account
                  </Button>
                  <Button variant="secondary" className="px-6 py-3 text-base" onClick={() => navigate('/login')}>
                    Login
                  </Button>
                </>
              )}
              {authenticated && (
                <Button className="px-6 py-3 text-base" onClick={() => navigate('/dashboard')}>
                  Open dashboard
                </Button>
              )}
            </div>
          </div>
        </section>

        <section className="mt-10 grid gap-4 md:grid-cols-3">
          <div className="rounded-xl border border-border bg-card p-5 shadow-card">
            <p className="m-0 text-lg font-semibold text-text-primary">Easy comparisons</p>
            <p className="mt-2 mb-0 text-text-muted">
              Pair old and new mole photos quickly and keep each comparison grouped for review.
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card p-5 shadow-card">
            <p className="m-0 text-lg font-semibold text-text-primary">Timeline history</p>
            <p className="mt-2 mb-0 text-text-muted">
              See saved report dates and revisit prior uploads whenever you need context.
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card p-5 shadow-card">
            <p className="m-0 text-lg font-semibold text-text-primary">Privacy focused</p>
            <p className="mt-2 mb-0 text-text-muted">
              Your workspace is centered on your data so you can monitor progress with confidence.
            </p>
          </div>
        </section>
      </main>
    </div>
  )
}
