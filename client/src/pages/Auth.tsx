import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Label, Input, Button } from '../components'

export function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-surface">
      <div className="flex-[0_0_50%] w-1/2 relative min-h-screen overflow-hidden bg-surface">
        <img src="/login.png" alt="" className="absolute inset-0 w-full h-full object-cover block" onError={(e) => { (e.target as HTMLImageElement).style.display = 'none' }} />
        <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-black/75 to-black/95 flex flex-col justify-end p-8 pb-10">
          <h2 className="text-2xl font-semibold text-white mb-2">Track mole changes over time</h2>
          <p className="text-white/90 text-sm mb-5">Upload pairs of photos, compare them, and keep a simple history in one place.</p>
          <div className="flex flex-wrap gap-2">
            <span className="inline-block text-xs font-semibold px-2.5 py-1.5 rounded-lg bg-accent/20 text-white">Photo comparison</span>
            <span className="inline-block text-xs font-semibold px-2.5 py-1.5 rounded-lg bg-accent/20 text-white">Simple reports</span>
            <span className="inline-block text-xs font-semibold px-2.5 py-1.5 rounded-lg bg-accent/20 text-white">Your data stays private</span>
          </div>
        </div>
      </div>
      <div className="flex-[0_0_50%] w-1/2 min-w-[280px] p-8 flex flex-col justify-center bg-card border-l border-border box-border">
        {children}
      </div>
    </div>
  )
}

export function Login({ onLogin }: { onLogin: (userName: string) => void }) {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [warn, setWarn] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if ((email || '').trim() && (password || '').trim()) {
      onLogin((email || '').trim())
      navigate('/dashboard')
    } else {
      setWarn('Please enter email and password.')
    }
  }
  return (
    <AuthLayout>
      <h1 className="text-2xl font-semibold tracking-tight text-text-primary mb-1">MoleMonitor</h1>
      <h3 className="text-lg font-medium text-text-primary mb-6">Log in</h3>
      <form className="max-w-[260px] w-full mx-auto" onSubmit={handleSubmit}>
        <Label>Email address</Label>
        <Input type="email" placeholder="user@example.com" value={email} onChange={(e) => setEmail(e.target.value)} className="mb-4" />
        <Label>Password</Label>
        <Input type="password" placeholder="********" value={password} onChange={(e) => setPassword(e.target.value)} className="mb-4" />
        {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
        <div className="flex flex-col gap-2 mt-3">
          <Button type="submit">Log in</Button>
          <Button variant="secondary" type="button" onClick={() => navigate('/forgot-password')}>Forgot your password?</Button>
          <Button variant="ghost" type="button" onClick={() => navigate('/register')}>Don&apos;t have an account? Register</Button>
        </div>
      </form>
    </AuthLayout>
  )
}

export function Register({ onLogin }: { onLogin: (userName: string) => void }) {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [phone, setPhone] = useState('')
  const [warn, setWarn] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if ((email || '').trim() && (password || '').trim()) {
      onLogin((name || email || '').trim())
      navigate('/dashboard')
    } else {
      setWarn('Please enter at least email and password.')
    }
  }
  return (
    <AuthLayout>
      <h1 className="text-2xl font-semibold tracking-tight text-text-primary mb-1">MoleMonitor</h1>
      <h3 className="text-lg font-medium text-text-primary mb-6">Create account</h3>
      <form className="max-w-[260px] w-full mx-auto" onSubmit={handleSubmit}>
        <Label>Name</Label>
        <Input type="text" placeholder="Your name" value={name} onChange={(e) => setName(e.target.value)} className="mb-4" />
        <Label>Email address</Label>
        <Input type="email" placeholder="user@example.com" value={email} onChange={(e) => setEmail(e.target.value)} className="mb-4" />
        <Label>Password</Label>
        <Input type="password" placeholder="********" value={password} onChange={(e) => setPassword(e.target.value)} className="mb-4" />
        <Label>Phone number</Label>
        <Input type="tel" placeholder="Used for password recovery" value={phone} onChange={(e) => setPhone(e.target.value)} className="mb-4" />
        {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
        <div className="flex flex-col gap-2 mt-3">
          <Button type="submit">Register</Button>
          <Button variant="secondary" type="button" onClick={() => navigate('/login')}>Already have an account? Log in</Button>
        </div>
      </form>
    </AuthLayout>
  )
}

export function ForgotPassword() {
  const navigate = useNavigate()
  const [step, setStep] = useState<'phone' | 'reset'>('phone')
  const [phone, setPhone] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [warn, setWarn] = useState('')
  const [success, setSuccess] = useState(false)

  const handleContinue = (e: React.FormEvent) => {
    e.preventDefault()
    if ((phone || '').trim()) {
      setStep('reset')
      setWarn('')
    } else {
      setWarn('Please enter your phone number.')
    }
  }
  const handleReset = (e: React.FormEvent) => {
    e.preventDefault()
    if (newPassword && newPassword === confirmPassword) {
      setSuccess(true)
      setStep('phone')
      setWarn('')
      setTimeout(() => navigate('/login'), 1500)
    } else {
      setWarn('Passwords must match and not be empty.')
    }
  }
  return (
    <AuthLayout>
      <h1 className="text-2xl font-semibold tracking-tight text-text-primary mb-1">MoleMonitor</h1>
      <h3 className="text-lg font-medium text-text-primary mb-6">Forgot your password?</h3>
      {step === 'phone' ? (
        <form className="max-w-[260px] w-full mx-auto" onSubmit={handleContinue}>
          <Label>Phone number</Label>
          <Input type="tel" placeholder="Enter the number used for registration" value={phone} onChange={(e) => setPhone(e.target.value)} className="mb-4" />
          {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
          <div className="flex flex-col gap-2 mt-3">
            <Button type="submit">Continue</Button>
          </div>
        </form>
      ) : (
        <form className="max-w-[260px] w-full mx-auto" onSubmit={handleReset}>
          <p className="text-sm text-text-muted mb-4">If this number is registered, you can reset your password below.</p>
          <Label>New password</Label>
          <Input type="password" placeholder="********" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className="mb-4" />
          <Label>Confirm password</Label>
          <Input type="password" placeholder="********" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="mb-4" />
          {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
          {success && <p className="text-semantic-success font-medium mb-2">Password reset (mock). You can log in now.</p>}
          <div className="flex flex-col gap-2 mt-3">
            <Button type="submit">Reset password</Button>
            <Button variant="secondary" type="button" onClick={() => { setStep('phone'); navigate('/login') }}>Back to Log in</Button>
          </div>
        </form>
      )}
    </AuthLayout>
  )
}
