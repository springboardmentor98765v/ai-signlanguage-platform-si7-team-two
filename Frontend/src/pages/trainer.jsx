import { useEffect, useState } from "react";
import {
  getTrainerLearners,
  getTrainerEngagement,
  getTrainerSkillDevelopment,
  getTrainerAssessmentAnalytics,
  getTrainerCertificationStatus,
} from "../services/api";

export default function Trainer() {
  const [learners, setLearners] = useState([]);
  const [selectedLearner, setSelectedLearner] = useState(null);
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadLearners();
  }, []);

  async function loadLearners() {
    try {
      setLoading(true);
      const data = await getTrainerLearners();
      setLearners(data);

      if (data.length > 0) {
        setSelectedLearner(data[0]);
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to load learners.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!selectedLearner) return;

    async function loadDetails() {
      try {
        setError("");

        const learnerId = selectedLearner.id;

        const [
          engagement,
          skill,
          assessment,
          certification,
        ] = await Promise.all([
          getTrainerEngagement(learnerId),
          getTrainerSkillDevelopment(learnerId),
          getTrainerAssessmentAnalytics(learnerId),
          getTrainerCertificationStatus(learnerId),
        ]);

        setDetails({
          engagement,
          skill,
          assessment,
          certification,
        });
      } catch (err) {
        console.error(err);
        setError(err.message || "Failed to load learner details.");
        setDetails(null);
      }
    }

    loadDetails();
  }, [selectedLearner]);

  if (loading) {
    return <div>Loading Trainer Dashboard...</div>;
  }

  return (
    <div>
      <div className="reports-header">
        <h2>Trainer Dashboard</h2>
        <p className="sub">
          Monitor assigned learners and their learning progress.
        </p>
      </div>

      {error && (
        <div className="empty-page" role="alert">
          <p>{error}</p>
        </div>
      )}

      <div className="reports-grid">
        <div className="report-panel">
          <p className="panel-title">
            Assigned Learners ({learners.length})
          </p>

          {learners.length === 0 ? (
            <p className="lessons-status">
              No learners assigned.
            </p>
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
                  {learners.map((learner) => (
                    <tr
                      key={learner.id}
                      className={
                        learner.id === selectedLearner?.id
                          ? "student-row selected"
                          : "student-row"
                      }
                      onClick={() => setSelectedLearner(learner)}
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

        <div className="report-panel">
          <p className="panel-title">
            Learner Details
          </p>

          {selectedLearner && (
            <>
              <h3>{selectedLearner.full_name}</h3>
              <p className="page-sub">
                {selectedLearner.email}
              </p>

              {details && (
                <>
                  <h4>Engagement</h4>

                  <div className="summary-row">
                    <span>Total Practice Sessions</span>
                    <span>
                      {details.engagement.total_practice_sessions}
                    </span>
                  </div>

                  <div className="summary-row">
                    <span>Completed Sessions</span>
                    <span>
                      {details.engagement.completed_sessions}
                    </span>
                  </div>

                  <div className="summary-row">
                    <span>Total Attempts</span>
                    <span>
                      {details.engagement.total_attempts}
                    </span>
                  </div>

                  <div className="summary-row">
                    <span>Current Streak</span>
                    <span>
                      {details.engagement.current_streak}
                    </span>
                  </div>

                  <h4>Skill Development</h4>

                  <div className="summary-row">
                    <span>Overall Accuracy</span>
                    <span>
                      {details.skill.overall_average_accuracy}%
                    </span>
                  </div>

                  <div className="summary-row">
                    <span>Recent Accuracy</span>
                    <span>
                      {details.skill.recent_average_accuracy}%
                    </span>
                  </div>

                  <div className="summary-row">
                    <span>Improvement</span>
                    <span>
                      {details.skill.improvement}%
                    </span>
                  </div>

                  <p className="label">Weak Letters</p>

                  {details.skill.weak_letters.length === 0 ? (
                    <p className="lessons-status">
                      No weak letters.
                    </p>
                  ) : (
                    <p>
                      {details.skill.weak_letters.join(", ")}
                    </p>
                  )}

                  <h4>Assessment</h4>

                  <div className="summary-row">
                    <span>Total Assessments</span>
                    <span>
                      {details.assessment.total_assessments}
                    </span>
                  </div>

                  <div className="summary-row">
                    <span>Average Score</span>
                    <span>
                      {details.assessment.average_assessment_score}%
                    </span>
                  </div>

                  <h4>Certification</h4>

                  <div className="summary-row">
                    <span>Status</span>
                    <span>
                      {details.certification.certification_status}
                    </span>
                  </div>

                  <div className="summary-row">
                    <span>Certificate Earned</span>
                    <span>
                      {details.certification.certificate_earned
                        ? "Yes"
                        : "No"}
                    </span>
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}