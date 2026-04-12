import { useNavigate } from 'react-router-dom'
import { Link } from 'react-router-dom'
import { PageHeader, Card, Button, Layout } from '../components'
import { ArrowRight, Sun, Focus, Square, Eye, Coins } from 'lucide-react'

const TIPS = [
  { title: 'Good lighting', icon: Sun, body: 'Use natural or bright indoor light. Do not use flash.' },
  { title: 'Keep it sharp', icon: Focus, body: 'Hold your phone steady and tap the screen to focus on the mole.' },
  { title: 'Straight angle', icon: Square, body: 'Take the photo directly above the mole. Avoid angled photos.' },
  { title: 'Clear skin', icon: Eye, body: 'Make sure the mole is fully visible. Move hair away and avoid creams or makeup.' },
  { title: 'Reference coin (optional)', icon: Coins, body: 'Place a small coin (e.g. a 5p coin) near the mole to help measure size changes.' },
]

export function Instructions() {
  const navigate = useNavigate()

  return (
    <Layout>
      <PageHeader
        title="Take a Clear Mole Photo"
        subtitle="A few simple tips for consistent, comparable photos."
      />
      <div className="w-full space-y-8">
        <p className="text-base leading-relaxed text-text-primary">
          Follow these tips to help the system compare your mole images accurately.
        </p>

        <Card className="p-6 sm:p-8">
          <ul className="m-0 p-0 list-none space-y-0">
            {TIPS.map((tip, i) => {
              const Icon = tip.icon
              return (
                <li
                  key={tip.title}
                  className={`flex gap-4 py-5 ${i < TIPS.length - 1 ? 'border-b border-border' : ''}`}
                >
                  <span
                    className="flex shrink-0 w-11 h-11 rounded-lg bg-accent/10 text-accent flex items-center justify-center"
                    aria-hidden
                  >
                    <Icon className="w-5 h-5" />
                  </span>
                  <div className="min-w-0">
                    <h3 className="text-base font-medium text-text-primary m-0 mb-1">
                      {tip.title}
                    </h3>
                    <p className="m-0 text-sm leading-relaxed text-text-muted">
                      {tip.body}
                    </p>
                  </div>
                </li>
              )
            })}
          </ul>
        </Card>

        <div className="flex flex-col sm:flex-row gap-4 pt-2">
          <Button onClick={() => navigate('/home')}>
            Continue to Upload Photo
            <ArrowRight className="w-4 h-4" />
          </Button>
          <Link
            to="/about"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-accent hover:underline"
          >
            About MoleMonitor
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </Layout>
  )
}
