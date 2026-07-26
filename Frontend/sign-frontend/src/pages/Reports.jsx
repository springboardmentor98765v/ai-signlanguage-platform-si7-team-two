import { useEffect, useState } from "react";
import { getUser } from "../utils/auth";
import {
  getProgressReport,
  getCertificateEligibility,
  downloadCertificate,
  downloadProgressReport,
} from "../services/api";

// DEV ONLY: real eligibility rule comes from Intern 4's Certificate API (due Day 6/9)
const CERTIFICATE_THRESHOLD = 80;
const today = new Date().toLocaleDateString("en-GB", {
  day: "numeric",
  month: "long",
  year: "numeric",
});

export default function Reports() {
  const [report, setReport] = useState(null);
  const [eligibility, setEligibility] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const currentUser = getUser();
  const isEligible = reportSummary.overallAccuracy >= CERTIFICATE_THRESHOLD;
  useEffect(() => {
    async function loadReport() {
      try {
        const progress = await getProgressReport(currentUser.id);
        const certificate = await getCertificateEligibility(currentUser.id);

        setReport(progress);
        setEligibility(certificate);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    if (currentUser?.id) {
      loadReport();
    }
  }, []);
  function handleDownload() {
    // TODO: replace with real certificate PDF from Intern 4's API (Day 7)
    window.print();
  }
  if (loading) {
    return <p>Loading progress report...</p>;
  }
  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <div className="reports-header">
        <h2>Your Progress Report</h2>
        <p className="sub">
          A summary of your accuracy, activity, and areas to improve.
        </p>
      </div>

      {/* Top summary stats — reuses the same stat-card style as Dashboard */}
      <div className="stats-grid">
        <div className="stat-card">
          <p className="label">Overall Accuracy</p>
          <p className="value">{reportSummary.overallAccuracy}%</p>
        </div>
        <div className="stat-card">
          <p className="label">Lessons Completed</p>
          <p className="value">{reportSummary.lessonsCompleted}</p>
        </div>
        <div className="stat-card">
          <p className="label">Practice Hours</p>
          <p className="value">{reportSummary.practiceHours}h</p>
        </div>
        <div className="stat-card">
          <p className="label">Improvement Rate</p>
          <p className="value">+{reportSummary.improvementRate}%</p>
        </div>
      </div>

      <div className="reports-grid">
        {/* Attempt history table */}
        <div className="report-panel">
          <p className="panel-title" id="attempts-table-caption">
            Recent Attempts
          </p>
          <div
            className="table-scroll"
            role="region"
            aria-labelledby="attempts-table-caption"
            tabIndex={0}
          >
            <table className="attempts-table">
              <thead>
                <tr>
                  <th>Letter</th>
                  <th>Date</th>
                  <th>Accuracy</th>
                </tr>
              </thead>
              <tbody>
                {attemptHistory.map((a) => (
                  <tr key={a.id}>
                    <td className="letter-cell">{a.letter}</td>
                    <td>{a.date}</td>
                    <td>
                      <div className="accuracy-bar-wrap">
                        <div
                          className={`accuracy-bar ${a.accuracy < 70 ? "low" : ""}`}
                          style={{ width: `${a.accuracy}%` }}
                        />
                        <span>{a.accuracy}%</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Weak letters / recommendations */}
        <div className="report-panel">
          <p className="panel-title">Recommended Practice</p>
          <div className="weak-letter-list">
            {weakLetters.map((w) => (
              <div className="weak-letter-item" key={w.letter}>
                <div className="weak-letter-badge">{w.letter}</div>
                <div className="weak-letter-info">
                  <p className="weak-letter-accuracy">
                    {w.averageAccuracy}% avg accuracy
                  </p>
                  <p className="weak-letter-hint">
                    {w.sessionsRecommended} practice sessions recommended
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Certificate */}
      <div className="report-panel certificate-panel">
        <p className="panel-title">Certificate</p>

        {isEligible ? (
          <div className="certificate-row">
            <div id="certificate-preview" className="certificate-card">
              <p className="certificate-kicker">Certificate of Completion</p>
              <p className="certificate-name">{currentUser.name}</p>
              <p className="certificate-detail">
                has achieved {reportSummary.overallAccuracy}% overall accuracy
                across {reportSummary.lessonsCompleted} lessons on SignLearn.
              </p>
              <p className="certificate-date">{today}</p>
            </div>
            <div className="certificate-actions">
              <p className="certificate-note">
                You&rsquo;ve qualified for a certificate. Nice work!
              </p>
              <button
                className="btn-primary btn-inline"
                onClick={handleDownload}
              >
                Download Certificate
              </button>
            </div>
          </div>
        ) : (
          <p className="certificate-locked">
            Reach {CERTIFICATE_THRESHOLD}% overall accuracy to unlock your
            certificate. You&rsquo;re currently at{" "}
            {reportSummary.overallAccuracy}%.
          </p>
        )}
      </div>
    </div>
  );
}
