import { useState, useEffect } from "react";
import { adminUsers } from "../data/mockData.js";
import {
  getLessons,
  createLesson,
  updateLesson,
  deleteLesson,
} from "../services/api.js";

export default function Admin() {
  const [users, setUsers] = useState(adminUsers);
  const [lessons, setLessons] = useState([]);
  const [loadingLessons, setLoadingLessons] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingLessonId, setEditingLessonId] = useState(null);

const [newLesson, setNewLesson] = useState({
  course_id: "",
  letter: "",
  title: "",
  description: "",
  reference_image_url: "",
  order_index: "",
});

  function toggleUser(id) {
    setUsers((prev) =>
      prev.map((u) => (u.id === id ? { ...u, active: !u.active } : u))
    );
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
      course_id: updated[0].course_id,
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
      course_id: updated[0].course_id,
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
    `Are you sure you want to delete "${title}"?`
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
  useEffect(() => {
    async function loadLessons() {
      try {
        const data = await getLessons();
        console.log("Lessons loaded:", data);
        setLessons(data);

if (data.length > 0) {
  setNewLesson((prev) => ({
    ...prev,
    course_id: data[0].course_id,
  }));
}
      } catch (err) {
        console.error("Failed to load lessons:", err);
      } finally {
        setLoadingLessons(false);
      }
    }

    loadLessons();
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
                {users.map((u) => (
                  <tr key={u.id}>
                    <td>
                      <p className="user-name">{u.name}</p>
                      <p className="user-email">{u.email}</p>
                    </td>

                    <td>
                      <span
                        className={`badge ${
                          u.role === "Instructor"
                            ? "badge-intermediate"
                            : "badge-beginner"
                        }`}
                      >
                        {u.role}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`status-pill ${
                          u.active ? "active" : "inactive"
                        }`}
                      >
                        {u.active ? "Active" : "Inactive"}
                      </span>
                    </td>

                    <td>
                      <button
                        type="button"
                        className="btn-secondary btn-inline btn-toggle"
                        onClick={() => toggleUser(u.id)}
                        aria-label={`${
                          u.active ? "Deactivate" : "Activate"
                        } ${u.name}`}
                      >
                        {u.active ? "Deactivate" : "Activate"}
                      </button>
                    </td>
                  </tr>
                ))}
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
            <p className="panel-title">
              Lessons ({lessons.length})
            </p>

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
  onClick={
    editingLessonId
      ? handleUpdateLesson
      : handleAddLesson
  }
>
  {editingLessonId ? "Update" : "Save"}
</button>
      <button
        className="btn-secondary"
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
          ) : (
            <div className="admin-lesson-list">
              {lessons.map((lesson) => (
                <div
                  key={lesson.id}
                  className="admin-lesson-row"
                >
                  <div>
                    <p className="admin-lesson-title">
                      {lesson.title}
                    </p>

                    <span
                      className="badge badge-beginner"
                    >
                      {lesson.letter}
                    </span>
                  </div>

                  <div
                    style={{
                      display: "flex",
                      gap: "8px",
                    }}
                  >
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
  onClick={() => handleDeleteLesson(lesson.id, lesson.title)}
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