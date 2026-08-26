import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../services/api.js";
import { saveSession, getRoleHomePath } from "../utils/auth.js";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  // Live validation state
  const [emailError, setEmailError] = useState("");

  function validateEmail(val) {
    if (!val) {
      setEmailError("");
      return true;
    }
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
    setEmailError(isValid ? "" : "Please enter a valid email address");
    return isValid;
  }

  function handleEmailChange(e) {
    const val = e.target.value;
    setEmail(val);
    validateEmail(val);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    
    if (!validateEmail(email)) {
      return;
    }

    setIsLoading(true);

    try {
      const response = await login(email, password);
      saveSession(response.user, response.access_token);
      navigate(getRoleHomePath(response.user.role));
    } catch (err) {
      setError(err.message || "Login failed. Please check your credentials.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="auth-shell">
      <main className="auth-card">
        <div className="auth-brand">
          <div className="mark" style={{ background: 'transparent' }}><img src="/app-logo-master.png" alt="" style={{ width: '100%', height: '100%', objectFit: 'contain' }} /></div>
          <div className="name">SignLearn</div>
        </div>

        <h1>Welcome back</h1>
        <p className="sub">Log in to continue your lessons.</p>

        {error && (
          <div className="form-error" role="alert">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={handleEmailChange}
              required
              disabled={isLoading}
              style={{ borderColor: emailError ? "var(--clay)" : "" }}
            />
            {emailError && <div style={{ color: "var(--clay)", fontSize: "12px", marginTop: "4px" }}>{emailError}</div>}
          </div>

          <div className="field" style={{ position: 'relative' }}>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              style={{ paddingRight: '60px' }}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? "Hide password" : "Show password"}
              style={{
                position: 'absolute',
                right: '12px',
                top: '35px',
                background: 'none',
                border: 'none',
                color: 'var(--ink)',
                cursor: 'pointer',
                fontSize: '13px',
                fontWeight: '600'
              }}
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>

          <div className="forgot-password-row">
            <Link to="/forgot-password" className="forgot-password-link">
              Forgot password?
            </Link>
          </div>

          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? "Logging in..." : "Log in"}
          </button>
        </form>

        <div className="auth-switch">
          Don't have an account? <Link to="/register">Register</Link>
        </div>
      </main>
    </div>
  );
}
