import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../services/api.js";
import { saveSession } from "../utils/auth.js";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  // DEV ONLY
  function handleSkipLoginAs(roleId) {
    saveSession({
      id: "dev-user",
      full_name: "Developer",
      email: "developer@example.com",
      role_id: roleId,
    });

    if (roleId === "instructor") navigate("/instructor");
    else if (roleId === "admin") navigate("/admin");
    else navigate("/dashboard");
  }

  async function handleSubmit(e) {
    e.preventDefault();

    setError("");
    setIsLoading(true);

    try {
      const response = await login(email, password);

      // Save complete user object
      saveSession(response.user);

      navigate("/dashboard");
    } catch (err) {
      setError(err.message || "Login failed. Please check your credentials.");
    } finally {
      setIsLoading(false);
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

        <p className="sub">
          Log in to continue your lessons.
        </p>

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
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
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
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            className="btn-primary"
            disabled={isLoading}
          >
            {isLoading ? "Logging in..." : "Log in"}
          </button>
        </form>

        <div className="auth-switch">
          Don't have an account?{" "}
          <Link to="/register">
            Register
          </Link>
        </div>

        <div className="dev-skip">
          <button
            type="button"
            className="btn-dev-skip"
            onClick={() => handleSkipLoginAs("learner")}
          >
            Skip Login as Learner
          </button>

          <button
            type="button"
            className="btn-dev-skip"
            onClick={() => handleSkipLoginAs("instructor")}
          >
            Skip Login as Instructor
          </button>

          <button
            type="button"
            className="btn-dev-skip"
            onClick={() => handleSkipLoginAs("admin")}
          >
            Skip Login as Admin
          </button>

          <p className="dev-note">
            For previewing pages before the real Auth API is connected.
          </p>
        </div>
      </div>
    </div>
  );
}