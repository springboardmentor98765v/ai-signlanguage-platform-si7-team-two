import { useEffect, useState, useCallback } from "react";
import { getUser } from "../utils/auth";
import {
  getProgressReport,
  getCertificateEligibility,
  downloadCertificate,
  downloadProgressReport,
  downloadProgressReportExcel,
  getRecommendations,
} from "../services/api";

export default function Reports() {
  const user = getUser();
  const [report, setReport] = useState(null);
  const [eligibility, setEligibility] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [recommendationsError, setRecommendationsError] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Milestone 3, Day 6/7: one shared status per download button, instead
  // of alert()/silent-failure. Each entry is "" (idle), "loading", or an
  // error message string.
  const [downloadStatus, setDownloadStatus] = useState({
    pdf: "",
    excel: "",
    certificate: "",
  });

  const fetchReport = useCallback(async () => {
    if (!user?.id) return;

    setLoading(true);
    setError("");

    try {
      const [reportData, eligibilityData] = await Promise.all([
        getProgressReport(user.id),
        getCertificateEligibility(user.id),
      ]);
      setReport(reportData);
      setEligibility(eligibilityData);
    } catch (e) {
      // Milestone 3, Day 7: friendly, non-technical error message instead
      // of showing the raw fetch/network error text.
      setError(
        "We couldn't load your report right now. Please check your connection and try again."
      );
    } finally {
      setLoading(false);
    }
  }, [user?.id]);

  const fetchRecommendations = useCallback(async () => {
    if (!user?.id) return;

    try {
      const data = await getRecommendations(user.id);
      setRecommendations(data.recommendations || []);
      setRecommendationsError("");
    } catch (e) {
      console.error("Failed to load recommendations:", e);
      setRecommendationsError("Couldn't load recommendations.");
    }
  }, [user?.id]);

  useEffect(() => {
    fetchReport();
    fetchRecommendations();
  }, [fetchReport, fetchRecommendations]);

  async function saveBlob(blob, name) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    a.click();
    URL.revokeObjectURL(url);
  }

  // Milestone 3, Day 6/7: shared handler for all three downloads so every
  // button gets the same loading + visible-error treatment (previously
  // the PDF and Certificate buttons had no error handling at all, and
  // Excel used a blocking alert()).
  async function handleDownload(kind, downloadFn, filename) {
    setDownloadStatus((prev) => ({ ...prev, [kind]: "loading" }));
    try {
      const blob = await downloadFn(
        user.id,
        user.name || user.full_name || "Learner"
      );
      await saveBlob(blob, filename);
      setDownloadStatus((prev) => ({ ...prev, [kind]: "" }));
    } catch (e) {
      setDownloadStatus((prev) => ({
        ...prev,
        [kind]: e.message || "Download failed. Please try again.",
      }));
    }
  }

  if (loading) {
    return (
      <p className="lessons-status" role="status">
        Loading your report...
      </p>
    );
  }

  if (error) {
    return (
      <div className="empty-page" role="alert">
        <h2>Something went wrong</h2>
        <p>{error}</p>
        <button className="btn-secondary btn-inline" onClick={fetchReport}>
          Try Again
        </button>
      </div>
    );
  }

  const learnerName = user?.name || user?.full_name || "Learner";

  return (
    <div style={{ padding: 30 }}>
      <h1>Progress Report</h1>

      <div className="stats-grid" style={{ marginTop: 20, marginBottom: 28 }}>
        <div className="stat-card fade-up">
          <p className="label">Overall Accuracy</p>
          <p className="value">{report.average_accuracy}%</p>
        </div>
        <div className="stat-card fade-up">
          <p className="label">Lessons Completed</p>
          <p className="value">{report.lessons_completed}</p>
        </div>
        <div className="stat-card fade-up">
          <p className="label">Total Attempts</p>
          <p className="value">{report.total_attempts}</p>
        </div>
        <div className="stat-card fade-up">
          <p className="label">Practice Time</p>
          <p className="value">{(report.total_practice_time / 3600).toFixed(2)}h</p>
        </div>
      </div>

      <h2 className="section-heading">
        <span className="icon" aria-hidden="true">✍️</span>
        Attempted Letters
      </h2>
      {report.attempted_letters.length === 0 ? (
        <p className="empty-note">No letters attempted yet.</p>
      ) : (
        <ul className="letter-chip-list">
          {report.attempted_letters.map((l) => (
            <li key={l} className="letter-chip">{l}</li>
          ))}
        </ul>
      )}

      <h2 className="section-heading">
        <span className="icon" aria-hidden="true">⚠️</span>
        Weak Letters
      </h2>
      {report.weak_letters.length === 0 ? (
        <p className="empty-note">None 🎉</p>
      ) : (
        <ul className="letter-chip-list">
          {report.weak_letters.map((l) => (
            <li key={l} className="letter-chip weak">{l}</li>
          ))}
        </ul>
      )}

      <h2 className="section-heading">
        <span className="icon" aria-hidden="true">💡</span>
        Recommended Practice
      </h2>
      {recommendationsError ? (
        <p className="form-error" role="alert">{recommendationsError}</p>
      ) : recommendations.length === 0 ? (
        <p className="empty-note">No recommendations right now — keep practicing! 🎉</p>
      ) : (
        <ul className="recommendation-list">
          {recommendations.map((rec) => (
            <li key={rec.id} className="recommendation-item">
              <div className="weak-letter-badge">{rec.letter_or_word}</div>
              <div>
                <p>{rec.reason}</p>
                {rec.recent_avg_accuracy != null && (
                  <p className="page-sub">
                    Recent average: {rec.recent_avg_accuracy.toFixed(1)}%
                  </p>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}

      <h2 className="section-heading">
        <span className="icon" aria-hidden="true">🏅</span>
        Certificate
        {eligibility?.eligible && (
          <span className="sparkle-dot gold" aria-hidden="true"></span>
        )}
      </h2>

      <div className="certificate-row">
        {/* Certificate preview — always visible, styled as locked/grayscale until eligible */}
        <div
          className={`certificate-card${eligibility?.eligible ? "" : " locked"}`}
          id="certificate-preview"
        >
          {!eligibility?.eligible && (
            <span className="certificate-lock-icon" aria-hidden="true">🔒</span>
          )}
          <p className="certificate-seal" aria-hidden="true">🏅</p>
          <p className="certificate-kicker">Certificate of Completion</p>
          <p className="certificate-name">{learnerName}</p>
          <p className="certificate-detail">
            has successfully completed the AI-Powered Sign Language
            Learning &amp; Assessment Program
          </p>
          <p className="certificate-date">
            {eligibility?.eligible
              ? new Date().toLocaleDateString()
              : "Not yet issued"}
          </p>
        </div>

        <div className="certificate-actions">
          {eligibility?.eligible ? (
            <>
              <p className="certificate-note">You're eligible ✅</p>
              <button
                className="btn-primary"
                disabled={downloadStatus.certificate === "loading"}
                onClick={() =>
                  handleDownload(
                    "certificate",
                    downloadCertificate,
                    "Certificate.pdf"
                  )
                }
              >
                {downloadStatus.certificate === "loading"
                  ? "Preparing your certificate..."
                  : "Download Certificate"}
              </button>
              {downloadStatus.certificate &&
                downloadStatus.certificate !== "loading" && (
                  <p className="form-error" role="alert">
                    {downloadStatus.certificate}
                  </p>
                )}
            </>
          ) : (
            <>
              <p className="certificate-locked">Not eligible yet ❌</p>
              {eligibility?.missing_letters?.length > 0 && (
                <div className="missing-letters-row">
                  {eligibility.missing_letters.map((l) => (
                    <span key={l} className="missing-letter-chip">
                      {l}
                    </span>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>

      <div style={{ marginTop: 28, display: "flex", gap: 12, flexWrap: "wrap" }}>
        <div>
          <button
            className="btn-secondary btn-inline"
            disabled={downloadStatus.pdf === "loading"}
            onClick={() =>
              handleDownload(
                "pdf",
                downloadProgressReport,
                "Progress_Report.pdf"
              )
            }
          >
            {downloadStatus.pdf === "loading"
              ? "Preparing your file..."
              : "Download Progress Report (PDF)"}
          </button>
          {downloadStatus.pdf && downloadStatus.pdf !== "loading" && (
            <p className="form-error" role="alert">
              {downloadStatus.pdf}
            </p>
          )}
        </div>

        <div>
          <button
            className="btn-secondary btn-inline"
            disabled={downloadStatus.excel === "loading"}
            onClick={() =>
              handleDownload(
                "excel",
                downloadProgressReportExcel,
                "Progress_Report.xlsx"
              )
            }
          >
            {downloadStatus.excel === "loading"
              ? "Preparing your file..."
              : "Export Report (Excel)"}
          </button>
          {downloadStatus.excel && downloadStatus.excel !== "loading" && (
            <p className="form-error" role="alert">
              {downloadStatus.excel}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}