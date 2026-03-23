import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Label, Input, Button } from '../components'
import { supabase } from '../supabase'

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
//password validation logic
const isValidPassword = (password: string) => {
  const minLength = password.length >=12
  const hasUpper = /[A-Z]/.test(password)
  const hasLower = /[a-z]/.test(password)
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password)
  const hasNumber = /\d/.test(password)

  return minLength && hasUpper && hasLower && hasSpecialChar && hasNumber
}


export function Login({ onLogin }: { onLogin: (userName: string) => void }) {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [warn, setWarn] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const trimmedEmail = email.trim()
    const trimmedPassword = password.trim()

    if (!trimmedEmail || !trimmedPassword) {
      setWarn('Please enter email and password.')
      return
    }

    const {error} = await supabase.auth.signInWithPassword({
      email: trimmedEmail,
      password: trimmedPassword
    })

    if (error) {
      setWarn('Invalid login credentials')
      return
    }
    navigate('/dashboard')
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
  const [warn, setWarn] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    const trimmedName = name.trim()
    const trimmedEmail = email.trim()
    const trimmedPassword = password.trim()

    //validation of login form
    //required fields
    if (!trimmedEmail || !trimmedPassword) {
      setWarn('All fields are required.')
      return
    }
    //email format
    if(!trimmedEmail.includes('@')) {
      setWarn('Invalid email format.')
      return
    }
    //password strength
    if(!isValidPassword(trimmedPassword)) {
      setWarn('Password must be at least 12 characters and include uppercase, lowercase, number and special character.')
      return
    }

    const { error } = await supabase.auth.signUp({
      email: trimmedEmail,
      password: trimmedPassword
    })

    if (error) {
      setWarn(error.message)
      return
    }
    //success
    onLogin(trimmedName || trimmedEmail)
    navigate('/dashboard')
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
  const [searchParams] = useSearchParams()
  const [step, setStep] = useState<'email' | 'reset'>('email')
  const [email, setEmail] = useState('')
  const [newPassword, setNewPassword] = useState ('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [warn, setWarn] = useState('')
  const [success, setSuccess] = useState(false)

//reset email link forward to reset password page
  useEffect(() => {
    const hashParams = new URLSearchParams(window.location.hash.slice(1))
    const accessToken = hashParams.get('access_token')
    const refreshToken = hashParams.get('refresh_token')
    const type = hashParams.get('type')

    if (accessToken && refreshToken && type === 'recovery') {
      supabase.auth.setSession({
        access_token: accessToken,
        refresh_token: refreshToken
      })
      setStep('reset')
    }
  }, [])

  //send reset email
  const handleSendEmail = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const trimmedEmail = email.trim()
    if (!trimmedEmail) {
        setWarn('Please enter your email.')
        return
    }
  
    const { error } = await supabase.auth.resetPasswordForEmail(trimmedEmail, {
      redirectTo: `http://localhost:5174/forgot-password?type=recovery`
    })

    if (error) {
      setWarn(error.message)
    } else {
      setSuccess(true)
      setWarn('')
    }
  }

  //reset password using access tokens
  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault()

    const trimmedNewPassword = newPassword.trim()
    const trimmedConfirmPassword = confirmPassword.trim()

    //Required fields
    if (!trimmedNewPassword || !trimmedConfirmPassword) {
      setWarn('Please fill in both password fields.')
      return
    }
    //passwords match validation
    if (trimmedNewPassword !== trimmedConfirmPassword) {
      setWarn('Passwords must match.')
      return
    }
    //password strength check 
    if (!isValidPassword(trimmedNewPassword)) {
      setWarn('Passwords must be at least 12 characters and include uppercase, lowercase, special character and a number.')
      return
    }

    //update password using access tokens
    const {error} = await supabase.auth.updateUser({
      password: trimmedNewPassword,
    })

    if (error) {
      setWarn(error.message)
    } else {
      setSuccess(true)
      setWarn('')
      setTimeout(() => navigate('/login'), 1500)
    }
  }

  return (
    <AuthLayout>
      <h1 className="text-2xl font-semibold tracking-tight text-text-primary mb-1">MoleMonitor</h1>
      <h3 className="text-lg font-medium text-text-primary mb-6">Forgot your password?</h3>
      {step === 'email' ? (
        <form className="max-w-[260px] w-full mx-auto" onSubmit={handleSendEmail}>
          <Label>Email Address</Label>
          <Input type="email" placeholder="user@example.com" value={email} onChange={(e) => setEmail(e.target.value)} className="mb-4" />
          {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
          <div className="flex flex-col gap-2 mt-3">
            <Button type="submit">Send Reset Email</Button>
          </div>
        </form>
      ) : (
        <form className="max-w-[260px] w-full mx-auto" onSubmit={handleResetPassword}>
          <p className="text-sm text-text-muted mb-4">Please reset your password below.</p>
          <Label>New password</Label>
          <Input type="password" placeholder="********" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className="mb-4" />
          <Label>Confirm password</Label>
          <Input type="password" placeholder="********" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="mb-4" />
          {warn && <p className="text-semantic-warning font-medium mb-2">{warn}</p>}
          {success && <p className="text-semantic-success font-medium mb-2">Password reset.</p>}
          <div className="flex flex-col gap-2 mt-3">
            <Button type="submit">Reset password</Button>
            <Button variant="secondary" type="button" onClick={() => {navigate('/login') }}>Back to Log in</Button>
          </div>
        </form>
      )}
    </AuthLayout>
  )
}
