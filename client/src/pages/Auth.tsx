import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { toast } from 'sonner'
import { Label, Input, Button } from '../components'
import type { AuthUser } from '../authApi'
import { loginUser, registerUser, resetPasswordWithToken, verifyPhoneForReset } from '../authApi'
import { isValidEmail, isValidPassword, normalizePhone } from '../utils/validation'

export function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-surface">
      <div className="flex-[0_0_50%] w-1/2 min-h-screen bg-[#f3f6fc] flex items-start justify-center px-12 pt-10 pb-8">
  <div className="w-full max-w-[620px]">
    <h2 className="text-[4.5rem] leading-[1.1] font-semibold text-[#25345d] mb-6">
      Monitor changes in your skin safely over time
    </h2>

    <p className="text-[1.35rem] leading-9 text-[#3f4d72] mb-10">
      Upload photos, compare changes, and keep a simple history.
    </p>

    <div className="space-y-4 mb-3">
      <div className="flex items-start gap-4">
        <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#dbe7ff] text-[#6b8fe8] text-lg font-bold">
          ✓
        </div>
        <div>
          <p className="text-[1.2rem] font-semibold text-[#25345d]">Easy photo comparison</p>
          <p className="text-[1rem] leading-7 text-[#5a6785]">Compare mole photos over time in one place.</p>
        </div>
      </div>

      <div className="flex items-start gap-4">
        <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#dbe7ff] text-[#6b8fe8] text-lg font-bold">
          ✓
        </div>
        <div>
          <p className="text-[1.2rem] font-semibold text-[#25345d]">Clear and simple reports</p>
          <p className="text-[1rem] leading-7 text-[#5a6785]">Easy-to-read summaries of visible changes.</p>
        </div>
      </div>

      <div className="flex items-start gap-4">
        <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#dbe7ff] text-[#6b8fe8] text-lg font-bold">
          ✓
        </div>
        <div>
          <p className="text-[1.2rem] font-semibold text-[#25345d]">Private &amp; secure</p>
          <p className="text-[1rem] leading-7 text-[#5a6785]">Your account helps keep your photo history protected.</p>
        </div>
      </div>
    </div>

    <div className="flex justify-end -mt-6 mb-2 pr-8">
  <img
    src="/log_img.png"
    alt="Illustration of mole photo comparison on a tablet"
    className="w-full max-w-[340px] h-auto object-contain"
    onError={(e) => {
      ;(e.target as HTMLImageElement).style.display = 'none'
    }}
  />
</div>

   <div className="rounded-2xl border border-[#d7dfef] bg-white px-5 py-3 shadow-sm max-w-[540px] -mt-2">
  <p className="text-[0.95rem] leading-6 text-[#52607d]">
    This tool is for monitoring visible changes only. It does not provide medical advice or a medical diagnosis.
  </p>
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
  <div className="w-full max-w-[340px] self-center">
    <div className="text-center">
      <h1 className="text-[2.1rem] font-semibold tracking-tight text-[#25345d] mb-2">
        Welcome to Mole Monitor
      </h1>
      <h3 className="text-[1.35rem] font-medium text-[#25345d] mb-8">
        Log in to view your mole history
      </h3>
    </div>

    <form className="w-full" onSubmit={handleSubmit}>
      <Label>Email address</Label>
      <Input
        type="email"
        placeholder="user@example.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="mb-5"
        autoComplete="email"
      />

      <Label>Password</Label>
      <Input
        type="password"
        placeholder="********"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="mb-4"
        autoComplete="current-password"
      />

      {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}

      <div className="flex flex-col gap-3 mt-4">
        <Button type="submit">Log in to view your mole history</Button>

        <Button variant="secondary" type="button" onClick={() => navigate('/forgot-password')}>
          Forgot your password?
        </Button>

        <div className="border-t border-[#d8deea] pt-3">
          <Button variant="ghost" type="button" onClick={() => navigate('/register')}>
            Don&apos;t have an account? Register
          </Button>
        </div>

        <div className="mt-2 rounded-xl border border-[#d8deea] bg-[#f4f6fb] px-4 py-3 flex items-center justify-center gap-2">
          <span className="text-[#64739a]">🔒</span>
          <p className="m-0 text-sm text-[#4f5d7a] font-medium">
            Your data is private and secure
          </p>
        </div>

        <div className="flex items-start justify-center gap-2 mt-1">
          <span className="text-[#d9a441] text-sm">⚠</span>
          <p className="m-0 text-sm text-[#5c6475]">
            This tool does not provide medical diagnosis.
          </p>
        </div>
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
  const [phone, setPhone] = useState('')
  const [warn, setWarn] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const name = fullName.trim()
    const em = email.trim()
    const pw = password
    const ph = normalizePhone(phone)

    if (!name || !em || !pw || !phone.trim()) {
      setWarn('Full name, email, password, and phone are required.')
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
    if (ph.length < 7) {
      setWarn('Please enter a valid phone number (at least 7 digits).')
      return
    }

    try {
      await registerUser({
        full_name: name,
        email: em,
        password: pw,
        phone: phone.trim(),
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
          <Label>Phone number</Label>
          <Input type="tel" placeholder="Used for password recovery" value={phone} onChange={(e) => setPhone(e.target.value)} className="mb-4" autoComplete="tel" />
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
  const [step, setStep] = useState<'phone' | 'reset'>('phone')
  const [phone, setPhone] = useState('')
  const [resetToken, setResetToken] = useState<string | null>(null)
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [warn, setWarn] = useState('')
  const [success, setSuccess] = useState(false)

  const handleVerifyPhone = async (e: React.FormEvent) => {
    e.preventDefault()
    const ph = normalizePhone(phone)
    if (ph.length < 7) {
      setWarn('Please enter a valid phone number.')
      return
    }
    try {
      const { reset_token } = await verifyPhoneForReset(phone.trim())
      setResetToken(reset_token)
      setStep('reset')
      setWarn('')
    } catch {
      setWarn('Could not complete request. Check your phone number.')
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
        {step === 'phone' ? (
          <form className="w-full" onSubmit={handleVerifyPhone}>
            <p className="text-sm text-text-muted mb-4 m-0">Enter the phone number you used when registering.</p>
            <Label>Phone number</Label>
            <Input type="tel" placeholder="Phone number" value={phone} onChange={(e) => setPhone(e.target.value)} className="mb-4" autoComplete="tel" />
            {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
            <div className="flex flex-col gap-2 mt-3">
              <Button type="submit">Continue</Button>
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
              <Button variant="secondary" type="button" onClick={() => { setStep('phone'); setResetToken(null); setWarn('') }}>
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
