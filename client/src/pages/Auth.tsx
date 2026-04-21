import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { toast } from 'sonner'
import { Label, Input, Button } from '../components'
import type { AuthUser } from '../authApi'
import { loginUser, registerUser, resetPasswordWithToken, verifyEmailForReset } from '../authApi'
import { isValidEmail, isValidPassword } from '../utils/validation'

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

export function Login({
  onLogin,
}: {
  onLogin: (token: string, user: AuthUser) => void
}) {
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [warn, setWarn] = useState('')

  useEffect(() => {
    const st = location.state as { registered?: boolean } | null
    if (st?.registered) {
      toast.success('Account created. You can log in with your email and password.')
      navigate(location.pathname, { replace: true, state: {} })
    }
  }, [location.pathname, location.state, navigate])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const trimmedEmail = email.trim()
    const trimmedPassword = password

    if (!trimmedEmail || !trimmedPassword) {
      setWarn('Please enter email and password.')
      return
    }

    try {
      const { token, user } = await loginUser(trimmedEmail, trimmedPassword)
      onLogin(token, user)
      navigate('/dashboard')
    } catch (err) {
      setWarn(err instanceof Error ? err.message : 'Invalid login credentials')
    }
  }

  return (
    <AuthLayout>
      <div className="w-full max-w-[260px] self-center">
        <div className="text-center">
          <h1 className="text-2xl font-semibold tracking-tight text-text-primary mb-1">Welcome to Mole Monitor</h1>
          <h3 className="text-lg font-medium text-text-primary mb-6">Log in to Your Account</h3>
        </div>
        <form className="w-full" onSubmit={handleSubmit}>
          <Label>Email address</Label>
          <Input type="email" placeholder="user@example.com" value={email} onChange={(e) => setEmail(e.target.value)} className="mb-4" autoComplete="email" />
          <Label>Password</Label>
          <Input type="password" placeholder="********" value={password} onChange={(e) => setPassword(e.target.value)} className="mb-4" autoComplete="current-password" />
          {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
          <div className="flex flex-col gap-2 mt-3">
            <Button type="submit">Log in</Button>
            <Button variant="secondary" type="button" onClick={() => navigate('/forgot-password')}>
              Forgot your password?
            </Button>
            <Button variant="ghost" type="button" onClick={() => navigate('/register')}>
              Don&apos;t have an account? Register
            </Button>
          </div>
        </form>
      </div>
    </AuthLayout>
  )
}

export function Register() {
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [warn, setWarn] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const name = fullName.trim()
    const em = email.trim()
    const pw = password

    if (!name || !em || !pw) {
      setWarn('Full name, email, and password are required.')
      return
    }
    if (!isValidEmail(em)) {
      setWarn('Please enter a valid email address.')
      return
    }
    if (!isValidPassword(pw)) {
      setWarn('Password must be more than 6 characters and include a special character.')
      return
    }
    try {
      await registerUser({
        full_name: name,
        email: em,
        password: pw,
      })
      navigate('/login', { replace: true, state: { registered: true } })
    } catch (err) {
      setWarn(err instanceof Error ? err.message : 'Registration failed')
    }
  }

  return (
    <AuthLayout>
      <div className="w-full max-w-[280px] self-center">
        <div className="text-center">
          <h1 className="text-2xl font-semibold tracking-tight text-text-primary mb-1">MoleMonitor</h1>
          <h3 className="text-lg font-medium text-text-primary mb-6">Create account</h3>
        </div>
        <form className="w-full" onSubmit={handleSubmit}>
          <Label>Full name</Label>
          <Input type="text" placeholder="Your full name" value={fullName} onChange={(e) => setFullName(e.target.value)} className="mb-4" autoComplete="name" />
          <Label>Email address</Label>
          <Input type="email" placeholder="user@example.com" value={email} onChange={(e) => setEmail(e.target.value)} className="mb-4" autoComplete="email" />
          <Label>Password</Label>
          <Input type="password" placeholder="********" value={password} onChange={(e) => setPassword(e.target.value)} className="mb-4" autoComplete="new-password" />
          {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
          <div className="flex flex-col gap-2 mt-3">
            <Button type="submit">Register</Button>
            <Button variant="secondary" type="button" onClick={() => navigate('/login')}>
              Already have an account? Log in
            </Button>
          </div>
        </form>
      </div>
    </AuthLayout>
  )
}

export function ForgotPassword() {
  const navigate = useNavigate()
  const location = useLocation()
  const [step, setStep] = useState<'email' | 'reset'>('email')
  const [email, setEmail] = useState('')
  const [resetToken, setResetToken] = useState<string | null>(null)
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [warn, setWarn] = useState('')
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    const raw = location.hash.startsWith('#') ? location.hash.slice(1) : location.hash
    if (raw) {
      const hp = new URLSearchParams(raw)
      const err = hp.get('error')
      const errCode = hp.get('error_code')
      if (err === 'access_denied' || errCode === 'otp_expired') {
        setWarn(
          'This email link has expired or was already used. Request a new reset link and open it soon. ' +
            'If the address bar shows port 3000 but you run MoleMonitor with npm start, set Supabase Site URL and redirect URLs to http://localhost:5173 (see API README).'
        )
        setStep('email')
        setResetToken(null)
        setSuccess(false)
        window.history.replaceState(null, '', `${location.pathname}${location.search}`)
        return
      }
    }
    const params = new URLSearchParams(location.search)
    const token = params.get('reset_token')
    if (token) {
      setResetToken(token)
      setStep('reset')
      setWarn('')
    } else {
      setResetToken(null)
      setStep('email')
    }
  }, [location.search, location.hash])

  const handleVerifyEmail = async (e: React.FormEvent) => {
    e.preventDefault()
    const trimmedEmail = email.trim()
    if (!isValidEmail(trimmedEmail)) {
      setWarn('Please enter a valid email address.')
      return
    }
    try {
      await verifyEmailForReset(trimmedEmail)
      setWarn('')
      setSuccess(true)
    } catch (err) {
      setWarn(err instanceof Error ? err.message : 'Could not send reset link. Please try again.')
    }
  }

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!resetToken) {
      setWarn('Session expired. Start again.')
      return
    }
    if (!newPassword || !confirmPassword) {
      setWarn('Please fill in both password fields.')
      return
    }
    if (newPassword !== confirmPassword) {
      setWarn('Passwords must match.')
      return
    }
    if (!isValidPassword(newPassword)) {
      setWarn('Password must be more than 6 characters and include a special character.')
      return
    }
    try {
      await resetPasswordWithToken(resetToken, newPassword)
      setSuccess(true)
      setWarn('')
      setTimeout(() => navigate('/login'), 1500)
    } catch (err) {
      setWarn(err instanceof Error ? err.message : 'Could not reset password.')
    }
  }

  return (
    <AuthLayout>
      <div className="w-full max-w-[280px] self-center">
        <div className="text-center">
          <h1 className="text-2xl font-semibold tracking-tight text-text-primary mb-1">MoleMonitor</h1>
          <h3 className="text-lg font-medium text-text-primary mb-6">Forgot your password?</h3>
        </div>
        {step === 'email' ? (
          <form className="w-full" onSubmit={handleVerifyEmail}>
            <p className="text-sm text-text-muted mb-4 m-0">Enter the email address you used when registering.</p>
            <Label>Email address</Label>
            <Input type="email" placeholder="user@example.com" value={email} onChange={(e) => setEmail(e.target.value)} className="mb-4" autoComplete="email" />
            {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
            {success && <p className="text-semantic-success font-medium mb-2">If your email exists in our system, a reset link has been sent.</p>}
            <div className="flex flex-col gap-2 mt-3">
              <Button type="submit">Send reset link</Button>
              <Button variant="secondary" type="button" onClick={() => navigate('/login')}>
                Back to Log in
              </Button>
            </div>
          </form>
        ) : (
          <form className="w-full" onSubmit={handleResetPassword}>
            <p className="text-sm text-text-muted mb-4 m-0">Enter your new password below.</p>
            <Label>New password</Label>
            <Input type="password" placeholder="********" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className="mb-4" autoComplete="new-password" />
            <Label>Confirm password</Label>
            <Input type="password" placeholder="********" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="mb-4" autoComplete="new-password" />
            {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
            {success && <p className="text-semantic-success font-medium mb-2">Password updated. Redirecting to log in…</p>}
            <div className="flex flex-col gap-2 mt-3">
              <Button type="submit" disabled={success}>
                Reset password
              </Button>
              <Button variant="secondary" type="button" onClick={() => { navigate('/forgot-password', { replace: true }); setWarn(''); setSuccess(false) }}>
                Back
              </Button>
              <Button variant="ghost" type="button" onClick={() => navigate('/login')}>
                Back to Log in
              </Button>
            </div>
          </form>
        )}
      </div>
    </AuthLayout>
  )
}
