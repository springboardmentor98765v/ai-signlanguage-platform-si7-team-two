import { login } from "../services/api";
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  async function handleSubmit(e) {
  e.preventDefault();

  try {
    const data = await login(email, password);

    console.log(data);

    alert(data.message);

    navigate("/dashboard");
  } catch (err) {
    console.error(err);
    alert("Login failed");
  }
}

  return (
    <div className="auth-shell">
      <div className="auth-card">
        <div className="auth-brand">
          <div className="mark">SL</div>
          <div className="name">SignLearn</div>
        </div>
        <h1>Welcome back</h1>
        <p className="sub">Log in to continue your lessons.</p>

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
            />
          </div>
          <div className="field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn-primary">Log in</button>
        </form>

        <div className="auth-switch">
          Don't have an account? <Link to="/register">Register</Link>
        </div>
      </div>
    </div>
  )
}
