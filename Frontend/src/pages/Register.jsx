import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register } from '../services/api.js'
import { saveSession } from '../utils/auth.js'

export default function Register() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [role, setRole] = useState('learner')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [showPassword, setShowPassword] = useState(false)

  // Live validation state
  const [emailError, setEmailError] = useState("")
  const [passwordError, setPasswordError] = useState("")

  function validateEmail(val) {
    if (!val) {
      setEmailError("")
      return true
    }
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)
    setEmailError(isValid ? "" : "Please enter a valid email address")
    return isValid
  }

  function handleEmailChange(e) {
    const val = e.target.value
    setEmail(val)
    validateEmail(val)
  }

  function validatePasswords(pass, confirm) {
    if (!pass || !confirm) {
      setPasswordError("")
      return true
    }
    const isValid = pass === confirm
    setPasswordError(isValid ? "" : "Passwords do not match")
    return isValid
  }

  function handlePasswordChange(e) {
    const val = e.target.value
    setPassword(val)
    validatePasswords(val, confirmPassword)
  }

  function handleConfirmPasswordChange(e) {
    const val = e.target.value
    setConfirmPassword(val)
    validatePasswords(password, val)
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    
    if (!validateEmail(email)) {
      return
    }
    if (!validatePasswords(password, confirmPassword)) {
      return
    }

    setIsLoading(true)
    try {
      const response = await register(name, email, password, role)

      // NOTE: the backend's /auth/register currently always creates a
      // Learner account regardless of the role sent here (see
      // AuthService.register — it hardcodes role_id to the Learner
      // role). Saving the selected role locally so the UI reflects
      // what was picked, but it will not match reality until the
      // backend is updated to actually honor this field.
      saveSession({ ...(response.user ?? response), role })

      navigate('/dashboard')
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="auth-shell">
      <main className="auth-card">
        <div className="auth-brand">
          <div className="mark" style={{ background: 'transparent' }}><img src="/app-logo-master.png" alt="" style={{ width: '100%', height: '100%', objectFit: 'contain' }} /></div>
          <div className="name">SignLearn</div>
        </div>
        <h1>Create your account</h1>
        <p className="sub">Start learning sign language today.</p>

        {error && <div className="form-error" role="alert">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="name">Full name</label>
            <input id="name" type="text" placeholder="Jane Doe"
              value={name} onChange={(e) => setName(e.target.value)} required disabled={isLoading} />
          </div>
          <div className="field">
            <label htmlFor="email">Email</label>
            <input id="email" type="email" placeholder="you@example.com"
              value={email} onChange={handleEmailChange} required disabled={isLoading} 
              style={{ borderColor: emailError ? "var(--clay)" : "" }} />
            {emailError && <div style={{ color: "var(--clay)", fontSize: "12px", marginTop: "4px" }}>{emailError}</div>}
          </div>
          <div className="field" style={{ position: 'relative' }}>
            <label htmlFor="password">Password</label>
            <input id="password" type={showPassword ? "text" : "password"} placeholder="••••••••"
              value={password} onChange={handlePasswordChange} required disabled={isLoading} 
              style={{ paddingRight: '60px', borderColor: passwordError ? "var(--clay)" : "" }} />
            <button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? "Hide password" : "Show password"}
              style={{ position: 'absolute', right: '12px', top: '35px', background: 'none', border: 'none', color: 'var(--ink)', cursor: 'pointer', fontSize: '13px', fontWeight: '600' }}>
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
          <div className="field" style={{ position: 'relative' }}>
            <label htmlFor="confirmPassword">Confirm password</label>
            <input id="confirmPassword" type={showPassword ? "text" : "password"} placeholder="••••••••"
              value={confirmPassword} onChange={handleConfirmPasswordChange} required disabled={isLoading} 
              style={{ paddingRight: '60px', borderColor: passwordError ? "var(--clay)" : "" }} />
            {passwordError && <div style={{ color: "var(--clay)", fontSize: "12px", marginTop: "4px" }}>{passwordError}</div>}
            <button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? "Hide password" : "Show password"}
              style={{ position: 'absolute', right: '12px', top: '35px', background: 'none', border: 'none', color: 'var(--ink)', cursor: 'pointer', fontSize: '13px', fontWeight: '600' }}>
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
          <div className="field">
            <label htmlFor="role">Role</label>
            <select id="role" value={role} onChange={(e) => setRole(e.target.value)} disabled={isLoading}>
              <option value="learner">Learner</option>
              <option value="instructor">Instructor</option>
              <option value="trainer">Accessibility Trainer</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        <div className="auth-switch">
          Already have an account? <Link to="/">Log in</Link>
        </div>
      </main>
    </div>
  )
}