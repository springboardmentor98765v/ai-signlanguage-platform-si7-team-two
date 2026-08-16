import { useState } from "react";

// Milestone 4, Day 2 (SRS FR-1): Accessibility Trainer Dashboard.
// Built from the same structure as Instructor.jsx per the SRS's own
// guidance ("fastest way is to copy the Instructor Dashboard").
// Running on mock data today — real APIs (Intern 2's Trainer endpoints,
// Intern 4's engagement/skill/analytics calculations) wire in on Day 3.

const mockLearners = [
  {
    id: "mock-1",
    full_name: "Aarav Sharma",
    email: "aarav@example.com",
    engagement: "High (5 sessions this week)",
    skillDevelopment: "+12% over last 4 weeks",
    assessmentAvg: 82,
    certificationStatus: "Certified — Beginner",
  },
  {
    id: "mock-2",
    full_name: "Meera Iyer",
    email: "meera@example.com",
    engagement: "Moderate (2 sessions this week)",
    skillDevelopment: "+4% over last 4 weeks",
    assessmentAvg: 68,
    certificationStatus: "Not yet certified",
  },
  {
    id: "mock-3",
    full_name: "Kabir Nair",
    email: "kabir@example.com",
    engagement: "Low (0 sessions this week)",
    skillDevelopment: "No change",
    assessmentAvg: 54,
    certificationStatus: "Not yet certified",
  },
];

export default function Trainer() {
  const [learners] = useState(mockLearners);
  const [selectedId, setSelectedId] = useState(mockLearners[0]?.id ?? null);
  const [search, setSearch] = useState("");

  const filteredLearners = learners.filter((l) =>
    l.full_name.toLowerCase().includes(search.toLowerCase())
  );

  const selectedLearner = learners.find((l) => l.id === selectedId);

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

          {filteredLearners.length === 0 ? (
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

              <div className="summary-row">
                <span>Engagement</span>
                <span>{selectedLearner.engagement}</span>
              </div>

              <div className="summary-row">
                <span>Skill Development</span>
                <span>{selectedLearner.skillDevelopment}</span>
              </div>

              <div className="summary-row">
                <span>Assessment Average</span>
                <span>{selectedLearner.assessmentAvg}%</span>
              </div>

              <div className="summary-row">
                <span>Certification Status</span>
                <span>{selectedLearner.certificationStatus}</span>
              </div>
            </>
          ) : (
            <p>Select a learner.</p>
          )}
        </div>
      </div>
    </div>
  );
}