import React from 'react';
import { Link } from 'react-router-dom';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="auth-shell auth-gamified-shell" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <main className="auth-card auth-card-gamified" style={{ textAlign: 'center' }}>
            <div className="auth-brand" style={{ justifyContent: 'center' }}>
              <img src="/app-logo-master.png" alt="SignLearn Logo" className="mark-img" />
              <div className="name">SignLearn</div>
            </div>
            <h1>Something went wrong.</h1>
            <p className="sub" style={{ marginBottom: '20px' }}>
              An unexpected error occurred. Don't worry, your progress is safe!
            </p>
            <div className="form-error" role="alert" style={{ marginBottom: '20px', wordBreak: 'break-all' }}>
              {this.state.error && this.state.error.toString()}
            </div>
            <button 
              className="btn-primary btn-primary-gamified" 
              onClick={() => {
                this.setState({ hasError: false });
                window.location.href = '/';
              }}
            >
              Go to Home
            </button>
          </main>
        </div>
      );
    }

    return this.props.children; 
  }
}

export default ErrorBoundary;
