import { useNavigate } from 'react-router-dom'
import { Focus, Square, Eye, Coins, Sun, AlertCircle } from 'lucide-react'
import { Button } from '../components'
import demoVideo from '../components/mole-demo.mp4'

const TIPS = [
  { title: 'Good lighting', icon: Sun, body: 'Use natural or bright indoor light. Do not use flash.' },
  { title: 'Keep it sharp', icon: Focus, body: 'Hold your phone steady and tap the screen to focus on the mole.' },
  { title: 'Straight angle', icon: Square, body: 'Take the photo directly above the mole. Avoid angled photos.' },
  { title: 'Clear skin', icon: Eye, body: 'Make sure the mole is fully visible. Move hair away and avoid creams or makeup.' },
  { title: 'Reference coin (optional)', icon: Coins, body: 'Place a small coin (e.g. a 5p coin) near the mole to help measure size changes.' },
]

export function Landing({ authenticated }: { authenticated: boolean }) {
  const navigate = useNavigate()

  return (
    <div className="relative min-h-screen overflow-hidden bg-surface text-text-primary">
      <div
        className="pointer-events-none absolute inset-0 bg-cover bg-center bg-no-repeat opacity-100"
        style={{ backgroundImage: 'url("/log_img.png")' }}
        aria-hidden
      />
      <div className="absolute inset-0 bg-surface/75" aria-hidden />
      <header className="w-full border-b border-border bg-card/90 backdrop-blur">
        <div className="relative z-10 mx-auto w-full max-w-[90rem] px-6 py-4 flex items-center justify-between">
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

      <main className="relative z-10 w-full px-6 py-12 md:py-20">
        <section className="relative mx-auto w-full max-w-[90rem] overflow-hidden rounded-2xl border border-border/70 bg-card/65 px-6 py-10 sm:px-8 sm:py-12 md:px-10 backdrop-blur-sm">
          <div className="absolute -top-24 -right-16 h-64 w-64 rounded-full bg-accent/20 blur-3xl" aria-hidden />
          <div className="absolute -bottom-24 -left-16 h-64 w-64 rounded-full bg-semantic-success/20 blur-3xl" aria-hidden />

          <div className="relative z-10 max-w-3xl">
            <h1 className="m-0 text-4xl leading-tight md:text-5xl font-semibold text-text-primary">
              Track mole photo changes in one secure place
            </h1>
            <p className="mt-4 mb-0 text-base md:text-lg text-text-muted">
              MoleMonitor helps you upload and compare photos over time so you can keep a clear visual history.
              The system is designed to make repeated tracking easier, more organized, and more consistent.
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

          <section className="mt-10 border-t border-border pt-8">
            <div className="rounded-lg border-l-4 border-semantic-error bg-semantic-error/10 p-4">
              <div className="flex items-start gap-3">
                <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-semantic-error" aria-hidden />
                <div className="min-w-0 flex-1">
                  <h2 className="m-0 mb-1 text-xl font-semibold text-text-primary">
                  Important: this is a tracking and support tool, not a medical diagnosis
                  </h2>
                  <p className="m-0 text-base leading-relaxed text-text-muted">
                    MoleMonitor is intended to help you organize and compare images. It does not diagnose skin
                    conditions. If you notice concerning changes, please consult a qualified healthcare professional.
                  </p>
                </div>
              </div>
            </div>
          </section>

          <section className="mt-10 border-t border-border pt-8">
            <h2 className="m-0 text-2xl font-bold text-text-primary sm:text-3xl">
              Follow these tips to help the system compare your mole images accurately.
            </h2>
            <ul className="m-0 mt-5 list-none space-y-0 rounded-xl border border-border bg-card/40 p-4 sm:p-5">
              {TIPS.map((tip, i) => {
                const Icon = tip.icon
                return (
                  <li
                    key={tip.title}
                    className={`flex gap-4 py-5 ${i < TIPS.length - 1 ? 'border-b border-border' : ''}`}
                  >
                    <span
                      className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-accent/10 text-accent"
                      aria-hidden
                    >
                      <Icon className="h-5 w-5" />
                    </span>
                    <div className="min-w-0">
                      <h3 className="m-0 mb-1 text-base font-medium text-text-primary">{tip.title}</h3>
                      <p className="m-0 text-sm leading-relaxed text-text-muted">{tip.body}</p>
                    </div>
                  </li>
                )
              })}
            </ul>
          </section>

          <section className="mt-10 border-t border-border pt-8">
            <p className="m-0 text-sm font-semibold uppercase tracking-wide text-accent">Video guide</p>
            <h2 className="m-0 mt-1 text-lg font-semibold text-text-primary">How to Take a Good Mole Photo</h2>
            <p className="m-0 mt-1 text-sm text-text-muted">
              Watch this quick demo after reading the instructions to reinforce best photo-taking steps.
            </p>
            <div className="mx-auto mt-4 max-w-3xl overflow-hidden rounded-xl border border-border/80 bg-black shadow-inner">
              <video src={demoVideo} controls className="aspect-video h-auto w-full" />
            </div>
          </section>
        </section>
      </main>
    </div>
  )
}
