import { PageHeader, Card, Layout } from '../components'

export function About() {
  return (
    <Layout>
      <PageHeader title="About MoleMonitor" />
      <div className="w-full space-y-6">
          <Card>
            <p className="text-base font-bold uppercase tracking-wider mb-2" style={{ color: '#eab308' }}>What MoleMonitor does</p>
            <p className="m-0 leading-relaxed text-text-primary">
              MoleMonitor is an MVP app for tracking skin mole images over time.
              You can upload pairs of photos, compare them, and keep a simple history of your records.
              It is designed to help you monitor changes in a single place.
            </p>
          </Card>
          <Card>
            <p className="text-base font-bold uppercase tracking-wider mb-2" style={{ color: '#eab308' }}>Why consistent images matter</p>
            <p className="m-0 leading-relaxed text-text-primary">
              Taking photos in similar lighting, from the same angle, and at a similar distance
              makes it easier to spot real changes over time. Small differences in how you take the photo
              can look like changes when they are not. Consistency improves the usefulness of your history.
            </p>
          </Card>
          <Card>
            <p className="text-base font-bold uppercase tracking-wider mb-2" style={{ color: '#eab308' }}>Important disclaimer</p>
            <p className="m-0 leading-relaxed text-text-primary italic">
              MoleMonitor does not provide medical diagnosis.
              It only helps you store and compare images.
              If you have any concern about a mole or your skin health, please consult a healthcare professional.
            </p>
          </Card>
      </div>
    </Layout>
  )
}
