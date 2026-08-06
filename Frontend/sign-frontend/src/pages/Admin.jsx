import { useState, useEffect } from "react";
import {
  getLessons,
  createLesson,
  updateLesson,
  deleteLesson,
  getUsers,
  deleteUser,
} from "../services/api.js";

export default function Admin() {
  const [users, setUsers] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(true);
  const [usersError, setUsersError] = useState("");
  const [lessons, setLessons] = useState([]);
  const [loadingLessons, setLoadingLessons] = useState(true);
  const [lessonsError, setLessonsError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingLessonId, setEditingLessonId] = useState(null);

  // Frontend-only note shown next to the toggle button, since there is
  // currently no backend endpoint to persist activate/deactivate — see
  // the TODO on toggleUser() below. Keeps the UI honest instead of
  // silently reverting the status on refresh.
  const [toggleNotice, setToggleNotice] = useState("");

  const [newLesson, setNewLesson] = useState({
    course_id: "",
    letter: "",
    title: "",
    description: "",
    reference_image_url: "",
    order_index: "",
  });

  // TODO (Backend/Intern 2): there is no PATCH/PUT endpoint yet to
  // persist a user's active/inactive status — AdminService currently
  // only supports get_all_users() and a hard delete_user(). Per the
  // Milestone 2 SRS (Intern 1, Day 5) this should be a real
  // Activate/Deactivate action, not just local UI state. Once a
  // backend endpoint exists (e.g. PATCH /admin/users/{id}/status),
  // swap this function to call it and re-run loadUsers() on success,
  // the same pattern as handleDeleteUser below.
  function toggleUser(id) {
    setUsers((prev) =>
      prev.map((user) => {
        if (user.id !== id) return user;

        const isActive = user.is_active !== false;

        return {
          ...user,
          is_active: !isActive,
          active: !isActive,
        };
      }),
    );

    setToggleNotice(
      "Status updated in this view only — this isn't saved yet (backend support pending). It will reset on refresh.",
    );
  }

  async function loadUsers() {
    setLoadingUsers(true);
    try {
      const data = await getUsers();
      setUsers(data);
      setUsersError("");
    } catch (err) {
      console.error(err);
      // Milestone 3, Day 7: previously this only logged to the console —
      // an admin whose user list failed to load saw an empty table with
      // no way to tell "no users" apart from "failed to load".
      setUsersError(
        "We couldn't load the user list. Please check your connection and try again.",
      );
    } finally {
      setLoadingUsers(false);
    }
  }

  async function handleDeleteUser(id, name) {
    const confirmed = window.confirm(`Delete ${name}?`);

    if (!confirmed) return;

    try {
      await deleteUser(id);
      await loadUsers();
      alert("User deleted successfully.");
    } catch (err) {
      alert(err.message);
    }
  }

  async function handleAddLesson() {
    try {
      await createLesson({
        ...newLesson,
        order_index: Number(newLesson.order_index),
      });

      const updated = await getLessons();
      setLessons(updated);
      setShowForm(false);

      setNewLesson({
        course_id: updated[0]?.course_id || "",
        letter: "",
        title: "",
        description: "",
        reference_image_url: "",
        order_index: "",
      });
    } catch (err) {
      alert(err.message);
    }
  }

  async function handleEditClick(lesson) {
    setEditingLessonId(lesson.id);

    setNewLesson({
      course_id: lesson.course_id,
      letter: lesson.letter,
      title: lesson.title,
      description: lesson.description || "",
      reference_image_url: lesson.reference_image_url || "",
      order_index: lesson.order_index,
    });

    setShowForm(true);
  }

  async function handleUpdateLesson() {
    try {
      await updateLesson(editingLessonId, {
        ...newLesson,
        order_index: Number(newLesson.order_index),
      });

      const updated = await getLessons();
      setLessons(updated);
      setEditingLessonId(null);
      setShowForm(false);

      setNewLesson({
        course_id: updated[0]?.course_id || "",
        letter: "",
        title: "",
        description: "",
        reference_image_url: "",
        order_index: "",
      });
    } catch (err) {
      alert(err.message);
    }
  }

  async function handleDeleteLesson(id, title) {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${title}"?`,
    );

    if (!confirmed) return;

    try {
      await deleteLesson(id);

      const updated = await getLessons();
      setLessons(updated);

      alert("Lesson deleted successfully.");
    } catch (err) {
      alert(err.message);
    }
  }

  async function loadLessons() {
    setLoadingLessons(true);
    try {
      const data = await getLessons();
      setLessons(data);
      setLessonsError("");

      if (data.length > 0) {
        setNewLesson((prev) => ({
          ...prev,
          course_id: data[0].course_id,
        }));
      }
    } catch (err) {
      console.error("Failed to load lessons:", err);
      // Milestone 3, Day 7: same fix as loadUsers — show a real error
      // instead of silently rendering an empty lesson list.
      setLessonsError(
        "We couldn't load the lesson list. Please check your connection and try again.",
      );
    } finally {
      setLoadingLessons(false);
    }
  }

  useEffect(() => {
    loadLessons();
    loadUsers();
  }, []);

  return (
    <div>
      <div className="reports-header">
        <h2>Admin Dashboard</h2>
        <p className="sub">
          Manage users and see every lesson on the platform.
        </p>
      </div>

      <div className="reports-grid">
        {/* USERS PANEL */}
        <div className="report-panel">
          <p className="panel-title" id="users-table-caption">
            All users ({users.length})
          </p>

          {toggleNotice && (
            <p className="lessons-status" role="status">
              {toggleNotice}
            </p>
          )}

          <div
            className="table-scroll"
            role="region"
            aria-labelledby="users-table-caption"
            tabIndex={0}
          >
            <table className="attempts-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>
                    <span className="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>

              <tbody>
                {loadingUsers ? (
                  <tr>
                    <td colSpan={4}>Loading users...</td>
                  </tr>
                ) : usersError ? (
                  <tr>
                    <td colSpan={4} role="alert">
                      {usersError}{" "}
                      <button
                        type="button"
                        className="btn-secondary btn-inline"
                        onClick={loadUsers}
                      >
                        Try Again
                      </button>
                    </td>
                  </tr>
                ) : users.length === 0 ? (
                  <tr>
                    <td colSpan={4}>No users found.</td>
                  </tr>
                ) : (
                  users.map((u) => {
                    const isActive = u.is_active !== false;

                    return (
                      <tr key={u.id}>
                        <td>
                          <p className="user-name">{u.full_name}</p>
                          <p className="user-email">{u.email}</p>
                        </td>

                        <td>
                          {/* Note: backend currently returns role_id (a
                              UUID), not a resolved role name. Displaying
                              the raw ID here until Backend adds a `role`
                              name field to UserResponse — see the note
                              sent to the Backend owner. */}
                          <span
                            className="badge badge-beginner"
                            title="Backend doesn't return a role name yet — showing role_id"
                          >
                            {u.role_id}
                          </span>
                        </td>

                        <td>
                          <span
                            className={`status-pill ${isActive ? "active" : "inactive"}`}
                          >
                            {isActive ? "Active" : "Inactive"}
                          </span>
                        </td>

                        <td>
                          <button
                            type="button"
                            className="btn-secondary btn-inline btn-toggle"
                            onClick={() => toggleUser(u.id)}
                          >
                            {isActive ? "Deactivate" : "Activate"}
                          </button>

                          <button
                            type="button"
                            className="btn-secondary btn-inline"
                            onClick={() => handleDeleteUser(u.id, u.full_name)}
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* LESSONS PANEL */}
        <div className="report-panel">
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "15px",
            }}
          >
            <p className="panel-title">Lessons ({lessons.length})</p>

            <button
              className="btn-secondary"
              type="button"
              onClick={() => setShowForm(true)}
            >
              + Add Lesson
            </button>

            {showForm && (
              <div
                style={{
                  marginBottom: "20px",
                  display: "flex",
                  flexDirection: "column",
                  gap: "10px",
                }}
              >
                <input
                  placeholder="Letter"
                  value={newLesson.letter}
                  onChange={(e) =>
                    setNewLesson({
                      ...newLesson,
                      letter: e.target.value.toUpperCase(),
                    })
                  }
                />

                <input
                  placeholder="Title"
                  value={newLesson.title}
                  onChange={(e) =>
                    setNewLesson({
                      ...newLesson,
                      title: e.target.value,
                    })
                  }
                />

                <textarea
                  placeholder="Description"
                  value={newLesson.description}
                  onChange={(e) =>
                    setNewLesson({
                      ...newLesson,
                      description: e.target.value,
                    })
                  }
                />

                <input
                  type="number"
                  placeholder="Order Index"
                  value={newLesson.order_index}
                  onChange={(e) =>
                    setNewLesson({
                      ...newLesson,
                      order_index: e.target.value,
                    })
                  }
                />

                <div
                  style={{
                    display: "flex",
                    gap: "10px",
                  }}
                >
                  <button
                    className="btn-secondary"
                    type="button"
                    onClick={
                      editingLessonId ? handleUpdateLesson : handleAddLesson
                    }
                  >
                    {editingLessonId ? "Update" : "Save"}
                  </button>

                  <button
                    className="btn-secondary"
                    type="button"
                    onClick={() => {
                      setShowForm(false);
                      setEditingLessonId(null);
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>

          {loadingLessons ? (
            <p>Loading lessons...</p>
          ) : lessonsError ? (
            <div className="empty-page" role="alert">
              <p>{lessonsError}</p>
              <button
                type="button"
                className="btn-secondary btn-inline"
                onClick={loadLessons}
              >
                Try Again
              </button>
            </div>
          ) : (
            <div className="admin-lesson-list">
              {lessons.map((lesson) => (
                <div key={lesson.id} className="admin-lesson-row">
                  <div>
                    <p className="admin-lesson-title">{lesson.title}</p>

                    <span className="badge badge-beginner">
                      {lesson.letter}
                    </span>
                  </div>

                  <div style={{ display: "flex", gap: "8px" }}>
                    <button
                      className="btn-secondary btn-inline"
                      type="button"
                      onClick={() => handleEditClick(lesson)}
                    >
                      Edit
                    </button>

                    <button
                      className="btn-secondary btn-inline"
                      type="button"
                      onClick={() =>
                        handleDeleteLesson(lesson.id, lesson.title)
                      }
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}