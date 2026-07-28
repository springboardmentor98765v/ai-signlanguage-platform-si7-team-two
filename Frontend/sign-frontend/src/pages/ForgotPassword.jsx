import { useState } from "react";
import { Link } from "react-router-dom";
import { forgotPassword } from "../services/api.js";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    setError("");
    setIsLoading(true);

    try {
      await forgotPassword(email);
      setSubmitted(true);
    } catch (err) {
      // Don't reveal whether the email exists — show the same
      // confirmation either way, unless the request itself failed.
      setSubmitted(true);
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

        <h1>Reset your password</h1>

        <p className="sub">
          {submitted
            ? "Check your inbox for next steps."
            : "Enter your email and we'll send you a link to reset your password."}
        </p>

        {error && (
          <div className="form-error" role="alert">
            {error}
          </div>
        )}

        {submitted ? (
          <div className="form-success" role="status">
            If an account exists for <strong>{email}</strong>, a password
            reset link is on its way.
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

            <button
              type="submit"
              className="btn-primary"
              disabled={isLoading}
            >
              {isLoading ? "Sending..." : "Send reset link"}
            </button>
          </form>
        )}

        <div className="auth-switch">
          Remembered your password?{" "}
          <Link to="/">Log in</Link>
        </div>
      </div>
    </div>
  );
}
