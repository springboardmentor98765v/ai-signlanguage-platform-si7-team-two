import { useEffect, useState, useCallback } from "react";
import { getUser } from "../utils/auth";
import {
  getProgressReport,
  getCertificateEligibility,
  downloadCertificate,
  downloadProgressReport,
  downloadProgressReportExcel,
} from "../services/api";

export default function Reports() {
  const user = getUser();
  const [report, setReport] = useState(null);
  const [eligibility, setEligibility] = useState(null);
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

  useEffect(() => {
    fetchReport();
  }, [fetchReport]);

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

  return (
    <div style={{ padding: 30 }}>
      <h1>Progress Report</h1>

      <p><b>Overall Accuracy:</b> {report.average_accuracy}%</p>
      <p><b>Lessons Completed:</b> {report.lessons_completed}</p>
      <p><b>Total Attempts:</b> {report.total_attempts}</p>
      <p><b>Practice Time:</b> {(report.total_practice_time / 3600).toFixed(2)} hours</p>

      <h2>Attempted Letters</h2>
      {report.attempted_letters.length === 0 ? (
        <p>No letters attempted yet.</p>
      ) : (
        <ul>
          {report.attempted_letters.map((l) => (
            <li key={l}>{l}</li>
          ))}
        </ul>
      )}

      <h2>Weak Letters</h2>
      {report.weak_letters.length === 0 ? (
        <p>None 🎉</p>
      ) : (
        <ul>
          {report.weak_letters.map((l) => (
            <li key={l}>{l}</li>
          ))}
        </ul>
      )}

      <h2>Certificate</h2>
      {eligibility?.eligible ? (
        <>
          <p>Eligible ✅</p>
          <button
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
          <p>Not Eligible ❌</p>
          <p>Missing: {eligibility?.missing_letters?.join(", ")}</p>
        </>
      )}

      <br />
      <br />

      <button
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

      <br />
      <br />

      <button
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
  );
}