import { useState, useEffect } from 'react'
import { getUser } from '../utils/auth.js'
import {
  getProgressReport,
  getStudentAssessments,
  getRecommendations,
  getCertificateEligibility,
  issueCertificate,
} from '../services/api.js'

const today = new Date().toLocaleDateString('en-GB', {
  day: 'numeric', month: 'long', year: 'numeric',
})

export default function Reports() {
  const user = getUser()

  const [report, setReport] = useState(null)
  const [recentAttempts, setRecentAttempts] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [eligibility, setEligibility] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [loadError, setLoadError] = useState('')

  const [isIssuing, setIsIssuing] = useState(false)
  const [issuedCertificate, setIssuedCertificate] = useState(null)
  const [issueError, setIssueError] = useState('')

  useEffect(() => {
    if (!user) {
      setIsLoading(false)
      return
    }
    let isMounted = true

    async function loadReport() {
      setIsLoading(true)
      setLoadError('')
      try {
        const [progressReport, assessments, recs, eligible] = await Promise.all([
          getProgressReport(user.id),
          getStudentAssessments(user.id).catch(() => []),
          getRecommendations(user.id).catch(() => ({ recommendations: [] })),
          getCertificateEligibility(user.id).catch(() => null),
        ])

        if (!isMounted) return
        setReport(progressReport)
        setRecentAttempts(
          [...assessments]
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            .slice(0, 8)
        )
        setRecommendations(recs.recommendations || [])
        setEligibility(eligible)

        if (progressReport.certificates_earned?.length > 0) {
          setIssuedCertificate(progressReport.certificates_earned[0])
        }
      } catch (err) {
        if (isMounted) setLoadError(err.message || 'No progress recorded yet.')
      } finally {
        if (isMounted) setIsLoading(false)
      }
    }

    loadReport()
    return () => { isMounted = false }
  }, [user?.id])

  async function handleIssueCertificate() {
    if (!user) return
    setIsIssuing(true)
    setIssueError('')
    try {
      const cert = await issueCertificate(user.id, user.full_name)
      setIssuedCertificate(cert)
    } catch (err) {
      setIssueError(err.message || 'Could not issue your certificate.')
    } finally {
      setIsIssuing(false)
    }
  }

  function handlePrint() {
    window.print()
  }

  if (!user) {
    return <p className="lessons-status error">You need to be logged in to view your progress report.</p>
  }

  if (isLoading) {
    return <p className="lessons-status">Loading your progress report...</p>
  }

  if (loadError || !report) {
    return (
      <div>
        <div className="reports-header">
          <h2>Your Progress Report</h2>
          <p className="sub">A summary of your accuracy, activity, and areas to improve.</p>
        </div>
        <p className="lessons-status">
          No practice history yet. Head to Practice and try a letter to start building your report.
        </p>
      </div>
    )
  }

  return (
    <div>
      <div className="reports-header">
        <h2>Your Progress Report</h2>
        <p className="sub">A summary of your accuracy, activity, and areas to improve.</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <p className="label">Overall Accuracy</p>
          <p className="value">{Math.round(report.average_accuracy)}%</p>
        </div>
        <div className="stat-card">
          <p className="label">Lessons Completed</p>
          <p className="value">{report.lessons_completed}</p>
        </div>
        <div className="stat-card">
          <p className="label">Practice Hours</p>
          <p className="value">{(report.total_practice_time / 3600).toFixed(1)}h</p>
        </div>
        <div className="stat-card">
          <p className="label">Total Attempts</p>
          <p className="value">{report.total_attempts}</p>
        </div>
      </div>

      <div className="reports-grid">
        <div className="report-panel">
          <p className="panel-title" id="attempts-table-caption">Recent Attempts</p>
          {recentAttempts.length === 0 ? (
            <p className="lessons-status">No attempts recorded yet.</p>
          ) : (
            <div className="table-scroll" role="region" aria-labelledby="attempts-table-caption" tabIndex={0}>
              <table className="attempts-table">
                <thead>
                  <tr>
                    <th>Letter</th>
                    <th>Date</th>
                    <th>Accuracy</th>
                  </tr>
                </thead>
                <tbody>
                  {recentAttempts.map((a) => (
                    <tr key={a.id}>
                      <td className="letter-cell">{a.predicted_sign}</td>
                      <td>{new Date(a.created_at).toLocaleDateString('en-GB')}</td>
                      <td>
                        <div className="accuracy-bar-wrap">
                          <div
                            className={`accuracy-bar ${a.overall_score < 70 ? 'low' : ''}`}
                            style={{ width: `${a.overall_score}%` }}
                          />
                          <span>{Math.round(a.overall_score)}%</span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="report-panel">
          <p className="panel-title">Recommended Practice</p>
          {recommendations.length === 0 ? (
            <p className="lessons-status">No active recommendations — keep practicing!</p>
          ) : (
            <div className="weak-letter-list">
              {recommendations.map((r) => (
                <div className="weak-letter-item" key={r.id}>
                  <div className="weak-letter-badge">{r.letter_or_word}</div>
                  <div className="weak-letter-info">
                    {r.recent_avg_accuracy != null && (
                      <p className="weak-letter-accuracy">{Math.round(r.recent_avg_accuracy)}% avg accuracy</p>
                    )}
                    <p className="weak-letter-hint">{r.reason}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="report-panel certificate-panel">
        <p className="panel-title">Certificate</p>

        {issuedCertificate ? (
          <div className="certificate-row">
            <div id="certificate-preview" className="certificate-card">
              <p className="certificate-kicker">Certificate of Completion</p>
              <p className="certificate-name">{user.full_name}</p>
              <p className="certificate-detail">
                has achieved {Math.round(issuedCertificate.average_score)}% overall accuracy on SignLearn.
              </p>
              <p className="certificate-detail">Certificate code: {issuedCertificate.certificate_code}</p>
              <p className="certificate-date">{today}</p>
            </div>
            <div className="certificate-actions">
              <p className="certificate-note">You&rsquo;ve earned a certificate. Nice work!</p>
              <button className="btn-primary btn-inline" onClick={handlePrint}>
                Print / Save as PDF
              </button>
            </div>
          </div>
        ) : eligibility?.eligible ? (
          <div className="certificate-row">
            <div className="certificate-actions">
              <p className="certificate-note">
                You&rsquo;re eligible for a certificate at {Math.round(eligibility.average_score)}% average accuracy.
              </p>
              {issueError && <p className="form-error" role="alert">{issueError}</p>}
              <button className="btn-primary btn-inline" onClick={handleIssueCertificate} disabled={isIssuing}>
                {isIssuing ? 'Issuing...' : 'Issue Certificate'}
              </button>
            </div>
          </div>
        ) : eligibility ? (
          <p className="certificate-locked">
            You&rsquo;re at {Math.round(eligibility.average_score)}% average accuracy across{' '}
            {eligibility.attempts_count} attempts.
            {eligibility.missing_letters?.length > 0 && (
              <> Still need practice on: {eligibility.missing_letters.join(', ')}.</>
            )}
          </p>
        ) : (
          <p className="certificate-locked">Certificate eligibility isn&rsquo;t available right now.</p>
        )}
      </div>
    </div>
  )
}