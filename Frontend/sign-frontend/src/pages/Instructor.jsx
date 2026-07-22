import { useState, useEffect } from 'react'
import { getInstructorStudents, getStudentProgress } from '../services/api.js'

// NOTE: GET /instructor/students currently returns EVERY user with the "Learner" role,
// not students actually assigned to the logged-in instructor (InstructorService.
// get_assigned_students has no instructor_id filter yet) — that's a backend gap for
// Intern 2 to close, not something fixable from this page.
export default function Instructor() {
  const [students, setStudents] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')

  const [selectedId, setSelectedId] = useState(null)
  const [selectedProgress, setSelectedProgress] = useState(null)
  const [isLoadingProgress, setIsLoadingProgress] = useState(false)
  const [progressError, setProgressError] = useState('')

  // Day 4 fix: table needs overall accuracy % per row, not just in the detail panel.
  // getInstructorStudents() doesn't return accuracy itself, so we fetch each student's
  // progress in parallel once the list loads and keep it in a lookup map.
  // Value is: undefined = still loading, null = no progress yet (404 / new learner), number = accuracy.
  const [accuracyById, setAccuracyById] = useState({})

  useEffect(() => {
    let isMounted = true

    async function loadStudents() {
      setIsLoading(true)
      setError('')
      try {
        const data = await getInstructorStudents()
        if (isMounted) {
          setStudents(data)
          if (data.length > 0) setSelectedId(data[0].id)
        }

        // Fire off accuracy lookups in parallel; each resolves independently so one
        // student's missing data doesn't block the rest of the table from showing up.
        data.forEach((s) => {
          getStudentProgress(s.id)
            .then((progress) => {
              if (isMounted) {
                setAccuracyById((prev) => ({ ...prev, [s.id]: progress.average_accuracy }))
              }
            })
            .catch(() => {
              if (isMounted) {
                setAccuracyById((prev) => ({ ...prev, [s.id]: null }))
              }
            })
        })
      } catch (err) {
        if (isMounted) setError(err.message || 'Could not load your students.')
      } finally {
        if (isMounted) setIsLoading(false)
      }
    }

    loadStudents()
    return () => { isMounted = false }
  }, [])

  useEffect(() => {
    if (!selectedId) return
    let isMounted = true

    async function loadProgress() {
      setIsLoadingProgress(true)
      setProgressError('')
      setSelectedProgress(null)
      try {
        const data = await getStudentProgress(selectedId)
        if (isMounted) setSelectedProgress(data)
      } catch (err) {
        // 404 here means this student has no analytics row yet (no practice history) —
        // that's a normal state for a brand-new learner, not an integration failure.
        if (isMounted) setProgressError(err.message || 'No progress recorded for this student yet.')
      } finally {
        if (isMounted) setIsLoadingProgress(false)
      }
    }

    loadProgress()
    return () => { isMounted = false }
  }, [selectedId])

  const filteredStudents = students.filter((s) =>
    (s.full_name || '').toLowerCase().includes(search.toLowerCase())
  )

  const selectedStudent = students.find((s) => s.id === selectedId)

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

      {isLoading && <p className="lessons-status">Loading students...</p>}
      {!isLoading && error && <p className="lessons-status error" role="alert">{error}</p>}

      {!isLoading && !error && (
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
                      <th>Email</th>
                      <th>Accuracy</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredStudents.map((s) => {
                      const accuracy = accuracyById[s.id]
                      return (
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
                          <td className="letter-cell student-name">{s.full_name}</td>
                          <td>{s.email}</td>
                          <td>
                            {accuracy === undefined ? (
                              <span className="lessons-status">Loading...</span>
                            ) : accuracy === null ? (
                              <span className="lessons-status">No data yet</span>
                            ) : (
                              <div className="accuracy-bar-wrap">
                                <div
                                  className={`accuracy-bar ${accuracy < 70 ? 'low' : ''}`}
                                  style={{ width: `${accuracy}%` }}
                                />
                                <span>{Math.round(accuracy)}%</span>
                              </div>
                            )}
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          <div className="report-panel">
            <p className="panel-title">Student Detail</p>

            {!selectedStudent && <p className="lessons-status">Select a student to view their progress.</p>}

            {selectedStudent && (
              <div>
                <p className="profile-name">{selectedStudent.full_name}</p>
                <p className="page-sub" style={{ marginBottom: 16 }}>{selectedStudent.email}</p>

                {isLoadingProgress && <p className="lessons-status">Loading progress...</p>}

                {!isLoadingProgress && progressError && (
                  <p className="lessons-status">{progressError}</p>
                )}

                {!isLoadingProgress && selectedProgress && (
                  <>
                    <div className="summary-row">
                      <span>Overall accuracy</span>
                      <span>{Math.round(selectedProgress.average_accuracy)}%</span>
                    </div>
                    <div className="summary-row">
                      <span>Lessons completed</span>
                      <span>{selectedProgress.lessons_completed}</span>
                    </div>

                    <p className="label" style={{ marginTop: 16 }}>Weak letters</p>
                    {!selectedProgress.weak_letters || selectedProgress.weak_letters.length === 0 ? (
                      <p className="lessons-status">No weak letters — great progress.</p>
                    ) : (
                      <div className="weak-letter-list">
                        {selectedProgress.weak_letters.map((letter) => (
                          <div className="weak-letter-item" key={letter}>
                            <div className="weak-letter-badge">{letter}</div>
                            <div>
                              <p className="weak-letter-hint">Recommend extra practice</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}