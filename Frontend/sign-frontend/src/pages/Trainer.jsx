import { useEffect, useState } from "react";
import {
  getTrainerLearners,
  getLearnerEngagement,
  getLearnerSkillDevelopment,
  getLearnerAssessmentAnalytics,
  getLearnerCertificationStatus,
} from "../services/api";

// Milestone 4, Day 3 (SRS FR-1): Accessibility Trainer Dashboard, now
// wired to the real Trainer APIs (Backend/app/routers/trainer.py)
// instead of the Day 2 mockLearners placeholder.

export default function Trainer() {
  const [learners, setLearners] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [learnersError, setLearnersError] = useState("");

  const [detail, setDetail] = useState(null);
  const [detailError, setDetailError] = useState("");
  const [detailLoading, setDetailLoading] = useState(false);

  // Load assigned learners
  useEffect(() => {
    loadLearners();
  }, []);

  async function loadLearners() {
    setLoading(true);
    try {
      const data = await getTrainerLearners();
      setLearners(data);
      setLearnersError("");

      if (data.length > 0) {
        setSelectedId(data[0].id);
      }
    } catch (err) {
      console.error(err);
      setLearnersError(
        "We couldn't load your assigned learners. Please check your connection and try again."
      );
    } finally {
      setLoading(false);
    }
  }

  // Load selected learner's engagement + skill + assessment + certification
  useEffect(() => {
    if (!selectedId) return;

    async function loadDetail() {
      setDetailLoading(true);
      setDetailError("");
      try {
        const [engagement, skill, assessment, certification] =
          await Promise.all([
            getLearnerEngagement(selectedId),
            getLearnerSkillDevelopment(selectedId),
            getLearnerAssessmentAnalytics(selectedId),
            getLearnerCertificationStatus(selectedId),
          ]);
        setDetail({ engagement, skill, assessment, certification });
      } catch (err) {
        console.error(err);
        setDetail(null);
        setDetailError(
          "We couldn't load this learner's analytics. Please try again."
        );
      } finally {
        setDetailLoading(false);
      }
    }

    loadDetail();
  }, [selectedId]);

  const filteredLearners = learners.filter((l) =>
    l.full_name.toLowerCase().includes(search.toLowerCase())
  );

  const selectedLearner = learners.find((l) => l.id === selectedId);

  if (loading) {
    return <div>Loading learners...</div>;
  }

  return (
    <div>
      <h1 className="sr-only">Accessibility Trainer Dashboard</h1>
      <div className="reports-header">
        <h2>Accessibility Trainer Dashboard</h2>
        <p className="sub">
          Learner engagement, skill development, assessment analytics, and
          certification status for your assigned learners.
        </p>
      </div>

      <div className="field search-field">
        <label htmlFor="learner-search" className="sr-only">
          Search learner by name
        </label>
        <input
          id="learner-search"
          type="text"
          placeholder="Search learner by name"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="reports-grid">
        {/* LEFT PANEL */}
        <div className="report-panel">
          <p className="panel-title">
            Assigned Learners ({filteredLearners.length})
          </p>

          {learnersError ? (
            <div className="empty-page" role="alert">
              <p>{learnersError}</p>
              <button
                type="button"
                className="btn-secondary btn-inline"
                onClick={loadLearners}
              >
                Try Again
              </button>
            </div>
          ) : filteredLearners.length === 0 ? (
            <p className="lessons-status">No learners found.</p>
          ) : (
            <div className="table-scroll">
              <table className="attempts-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredLearners.map((learner) => (
                    <tr
                      key={learner.id}
                      className={
                        learner.id === selectedId
                          ? "student-row selected"
                          : "student-row"
                      }
                      onClick={() => setSelectedId(learner.id)}
                      style={{ cursor: "pointer" }}
                    >
                      <td>{learner.full_name}</td>
                      <td>{learner.email}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* RIGHT PANEL */}
        <div className="report-panel">
          <p className="panel-title">Learner Detail</p>

          {selectedLearner ? (
            <>
              <p className="profile-name">{selectedLearner.full_name}</p>
              <p className="page-sub">{selectedLearner.email}</p>

              {detailError ? (
                <p className="lessons-status" role="alert">
                  {detailError}
                </p>
              ) : detailLoading ? (
                <p className="lessons-status">Loading analytics...</p>
              ) : detail ? (
                <>
                  <p className="section-heading" style={{ marginTop: 20 }}>
                    Engagement
                  </p>
                  <div className="summary-row">
                    <span>Practice Sessions</span>
                    <span>{detail.engagement.total_practice_sessions}</span>
                  </div>
                  <div className="summary-row">
                    <span>Completed Sessions</span>
                    <span>{detail.engagement.completed_sessions}</span>
                  </div>
                  <div className="summary-row">
                    <span>Current Streak</span>
                    <span>{detail.engagement.current_streak} days</span>
                  </div>
                  <div className="summary-row">
                    <span>Longest Streak</span>
                    <span>{detail.engagement.longest_streak} days</span>
                  </div>

                  <p className="section-heading" style={{ marginTop: 20 }}>
                    Skill Development
                  </p>
                  <div className="summary-row">
                    <span>Overall Accuracy</span>
                    <span>{detail.skill.overall_average_accuracy}%</span>
                  </div>
                  <div className="summary-row">
                    <span>Recent Accuracy</span>
                    <span>{detail.skill.recent_average_accuracy}%</span>
                  </div>
                  <div className="summary-row">
                    <span>Improvement</span>
                    <span>{detail.skill.improvement}%</span>
                  </div>

                  <p className="section-heading" style={{ marginTop: 20 }}>
                    Assessment Analytics
                  </p>
                  <div className="summary-row">
                    <span>Total Assessments</span>
                    <span>{detail.assessment.total_assessments}</span>
                  </div>
                  <div className="summary-row">
                    <span>Average Score</span>
                    <span>{detail.assessment.average_assessment_score}%</span>
                  </div>

                  <p className="section-heading" style={{ marginTop: 20 }}>
                    Certification Status
                  </p>
                  <div className="summary-row">
                    <span>Status</span>
                    <span>{detail.certification.certification_status}</span>
                  </div>
                  <div className="summary-row">
                    <span>Certificate Earned</span>
                    <span>
                      {detail.certification.certificate_earned ? "Yes" : "No"}
                    </span>
                  </div>

                  {detail.skill.weak_letters.length > 0 && (
                    <>
                      <p className="label" style={{ marginTop: 16 }}>
                        Weak Letters
                      </p>
                      <div className="weak-letter-list">
                        {detail.skill.weak_letters.map((letter) => (
                          <div key={letter} className="weak-letter-item">
                            <div className="weak-letter-badge">{letter}</div>
                          </div>
                        ))}
                      </div>
                    </>
                  )}
                </>
              ) : (
                <p className="lessons-status">
                  No analytics available for this learner.
                </p>
              )}
            </>
          ) : (
            <p>Select a learner.</p>
          )}
        </div>
      </div>
    </div>
  );
}