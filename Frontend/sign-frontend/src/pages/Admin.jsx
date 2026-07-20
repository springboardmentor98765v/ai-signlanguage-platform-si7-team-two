import { useState } from 'react'
import { adminUsers, lessons } from '../data/mockData.js'

export default function Admin() {
  const [users, setUsers] = useState(adminUsers)

  function toggleUser(id) {
    setUsers((prev) =>
      prev.map((u) => (u.id === id ? { ...u, active: !u.active } : u))
    )
  }

  return (
    <div>
      <div className="reports-header">
        <h2>Admin Dashboard</h2>
        <p className="sub">Manage users and see every lesson on the platform.</p>
      </div>

      <div className="reports-grid">
        <div className="report-panel">
          <p className="panel-title">All users ({users.length})</p>

          <table className="attempts-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>
                    <p className="user-name">{u.name}</p>
                    <p className="user-email">{u.email}</p>
                  </td>
                  <td>
                    <span className={`badge ${u.role === 'Instructor' ? 'badge-intermediate' : 'badge-beginner'}`}>
                      {u.role}
                    </span>
                  </td>
                  <td>
                    <span className={`status-pill ${u.active ? 'active' : 'inactive'}`}>
                      {u.active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <button
                      type="button"
                      className="btn-secondary btn-inline btn-toggle"
                      onClick={() => toggleUser(u.id)}
                    >
                      {u.active ? 'Deactivate' : 'Activate'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="report-panel">
          <p className="panel-title">Lessons ({lessons.length})</p>

          <div className="admin-lesson-list">
            {lessons.map((lesson) => (
              <div key={lesson.id} className="admin-lesson-row">
                <div>
                  <p className="admin-lesson-title">{lesson.title}</p>
                  <span className={`badge badge-${lesson.difficulty.toLowerCase()}`}>
                    {lesson.difficulty}
                  </span>
                </div>
                <p className="admin-lesson-learners">{lesson.learnersUsing} learners</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
