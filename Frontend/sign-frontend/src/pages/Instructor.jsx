import { useEffect, useState } from "react";
import { getStudents, getStudentProgress } from "../services/api";

export default function Instructor() {
  const [students, setStudents] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [selectedProgress, setSelectedProgress] = useState(null);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  // Load all students
  useEffect(() => {
    async function loadStudents() {
      try {
        const data = await getStudents();
        setStudents(data);

        if (data.length > 0) {
          setSelectedId(data[0].id);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    loadStudents();
  }, []);

  // Load selected student's progress
  useEffect(() => {
    if (!selectedId) return;

    async function loadProgress() {
      try {
        const data = await getStudentProgress(selectedId);
        setSelectedProgress(data);
      } catch (err) {
        console.error(err);
        setSelectedProgress(null);
      }
    }

    loadProgress();
  }, [selectedId]);

  const filteredStudents = students.filter((student) =>
    student.full_name.toLowerCase().includes(search.toLowerCase())
  );

  const selectedStudent = students.find((s) => s.id === selectedId);

  if (loading) {
    return <div>Loading students...</div>;
  }

  return (
    <div>
      <div className="reports-header">
        <h2>Instructor Dashboard</h2>
        <p className="sub">See how each of your students is progressing.</p>
      </div>

      <div className="field search-field">
        <label htmlFor="student-search" className="sr-only">
          Search student by name
        </label>

        <input
          id="student-search"
          type="text"
          placeholder="Search student by name"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="reports-grid">
        {/* LEFT PANEL */}

        <div className="report-panel">
          <p className="panel-title">
            Students ({filteredStudents.length})
          </p>

          {filteredStudents.length === 0 ? (
            <p className="lessons-status">
              No students found.
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
                  {filteredStudents.map((student) => (
                    <tr
                      key={student.id}
                      className={
                        student.id === selectedId
                          ? "student-row selected"
                          : "student-row"
                      }
                      onClick={() => setSelectedId(student.id)}
                      style={{ cursor: "pointer" }}
                    >
                      <td>{student.full_name}</td>
                      <td>{student.email}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* RIGHT PANEL */}

        <div className="report-panel">
          <p className="panel-title">
            Student Detail
          </p>

          {selectedStudent ? (
            <>
              <p className="profile-name">
                {selectedStudent.full_name}
              </p>

              <p className="page-sub">
                {selectedStudent.email}
              </p>

              {selectedProgress ? (
                <>
                  <div className="summary-row">
                    <span>Overall Accuracy</span>
                    <span>
                      {selectedProgress.average_accuracy}%
                    </span>
                  </div>

                  <div className="summary-row">
                    <span>Lessons Completed</span>
                    <span>
                      {selectedProgress.lessons_completed}
                    </span>
                  </div>

                  <p
                    className="label"
                    style={{ marginTop: 16 }}
                  >
                    Weak Letters
                  </p>

                  {selectedProgress.weak_letters.length === 0 ? (
                    <p className="lessons-status">
                      No weak letters.
                    </p>
                  ) : (
                    <div className="weak-letter-list">
                      {selectedProgress.weak_letters.map(
                        (letter) => (
                          <div
                            key={letter}
                            className="weak-letter-item"
                          >
                            <div className="weak-letter-badge">
                              {letter}
                            </div>

                            <div>
                              <p className="weak-letter-hint">
                                Recommend extra practice
                              </p>
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  )}
                </>
              ) : (
                <p className="lessons-status">
                  No analytics available for this student.
                </p>
              )}
            </>
          ) : (
            <p>Select a student.</p>
          )}
        </div>
      </div>
    </div>
  );
}