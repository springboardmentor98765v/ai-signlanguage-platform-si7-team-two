import { useState } from 'react'
import { instructorStudents } from '../data/mockData.js'

export default function Instructor() {
  const [search, setSearch] = useState('')
  const [selectedId, setSelectedId] = useState(instructorStudents[0]?.id ?? null)

  const filteredStudents = instructorStudents.filter((s) =>
    s.name.toLowerCase().includes(search.toLowerCase())
  )

  const selectedStudent = instructorStudents.find((s) => s.id === selectedId)

  return (
    <div>
      <div className="reports-header">
        <h2>Instructor Dashboard</h2>
        <p className="sub">See how each of your students is progressing.</p>
      </div>

      <div className="field search-field">
        <label htmlFor="student-search" className="sr-only">Search student by name</label>
        <input
          id="student-search"
          type="text"
          placeholder="Search student by name"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="reports-grid">
        <div className="report-panel">
          <p className="panel-title" id="students-table-caption">Students ({filteredStudents.length})</p>

          {filteredStudents.length === 0 ? (
            <p className="lessons-status">No students match that search.</p>
          ) : (
            <div className="table-scroll" role="region" aria-labelledby="students-table-caption" tabIndex={0}>
              <table className="attempts-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Accuracy</th>
                    <th>Lessons</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredStudents.map((s) => (
                    <tr
                      key={s.id}
                      className={`student-row ${s.id === selectedId ? 'selected' : ''}`}
                      onClick={() => setSelectedId(s.id)}
                      tabIndex={0}
                      role="button"
                      aria-pressed={s.id === selectedId}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                          e.preventDefault()
                          setSelectedId(s.id)
                        }
                      }}
                    >
                      <td className="letter-cell student-name">{s.name}</td>
                      <td>
                        <div className="accuracy-bar-wrap">
                          <div
                            className={`accuracy-bar ${s.accuracy < 70 ? 'low' : ''}`}
                            style={{ width: `${s.accuracy}%` }}
                          />
                          <span>{s.accuracy}%</span>
                        </div>
                      </td>
                      <td>{s.lessonsCompleted}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="report-panel">
          <p className="panel-title">Student Detail</p>

          {selectedStudent ? (
            <div>
              <p className="profile-name">{selectedStudent.name}</p>
              <p className="page-sub" style={{ marginBottom: 16 }}>
                Last active {selectedStudent.lastActive}
              </p>

              <div className="summary-row">
                <span>Overall accuracy</span>
                <span>{selectedStudent.accuracy}%</span>
              </div>
              <div className="summary-row">
                <span>Lessons completed</span>
                <span>{selectedStudent.lessonsCompleted}</span>
              </div>

              <p className="label" style={{ marginTop: 16 }}>Weak letters</p>
              {selectedStudent.weakLetters.length === 0 ? (
                <p className="lessons-status">No weak letters — great progress.</p>
              ) : (
                <div className="weak-letter-list">
                  {selectedStudent.weakLetters.map((letter) => (
                    <div className="weak-letter-item" key={letter}>
                      <div className="weak-letter-badge">{letter}</div>
                      <div>
                        <p className="weak-letter-hint">Recommend extra practice</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <p className="lessons-status">Select a student to view their progress.</p>
          )}
        </div>
      </div>
    </div>
  )
}
