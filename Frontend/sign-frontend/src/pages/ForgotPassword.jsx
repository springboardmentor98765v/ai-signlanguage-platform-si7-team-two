import { useState } from 'react'
import { Link } from 'react-router-dom'
import { forgotPassword } from '../services/api.js'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [resetLink, setResetLink] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setResetLink('')
    setIsLoading(true)
    try {
      const response = await forgotPassword(email)
      // DEV ONLY: the backend returns the reset link directly when no real
      // email service is configured, so we can show it here for testing.
      setResetLink(response.reset_link || '')
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="auth-shell">
      <div className="auth-card">
        <div className="auth-brand">
          <div className="mark">SL</div>
          <div className="name">SignLearn</div>
        </div>

        <h1>Forgot password?</h1>
        <p className="sub">Enter your email and we'll send you a reset link.</p>

        {error && <div className="form-error" role="alert">{error}</div>}

        {resetLink ? (
          <div className="form-success">
            A reset link has been generated.{' '}
            <a href={resetLink}>Click here to reset your password</a>.
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>

            <button type="submit" className="btn-primary" disabled={isLoading}>
              {isLoading ? 'Sending...' : 'Send reset link'}
            </button>
          </form>
        )}

        <div className="auth-switch">
          Remembered your password? <Link to="/">Log in</Link>
        </div>
      </div>
    </div>
  )
}
