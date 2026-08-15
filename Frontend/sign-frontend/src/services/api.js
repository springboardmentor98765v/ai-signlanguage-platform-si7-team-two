import { getToken } from "./../utils/auth.js";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const BUSINESS_LOGIC_URL = import.meta.env.VITE_BUSINESS_LOGIC_URL || 'http://localhost:8002'

// Turns a FastAPI error response body into a plain, readable string.
// - Simple errors: { "detail": "Invalid credentials" }              -> "Invalid credentials"
// - Validation errors (422): { "detail": [{ loc, msg, type }, ...] } -> joined msg text
// - Anything else / missing detail -> fallback message
function extractErrorMessage(data, fallback) {
  if (typeof data.detail === 'string') {
    return data.detail
  }
  if (Array.isArray(data.detail)) {
    return data.detail.map((d) => d.msg).filter(Boolean).join(' ') || fallback
  }
  return fallback
}

async function handleResponse(res) {
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(extractErrorMessage(data, 'Something went wrong. Please try again.'))
  }
  return data
}

// Builds an Authorization header from the stored JWT, if one exists.
// Used for endpoints protected by require_instructor / require_admin
// on the backend (Backend/app/core/security.py).
function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function login(email, password) {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  return handleResponse(res)
}

export async function forgotPassword(email) {
  const res = await fetch(`${API_BASE_URL}/auth/forgot-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })
  return handleResponse(res)
}

export async function register(name, email, password, role) {
  const res = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ full_name: name, email, password, role }),
  })
  return handleResponse(res)
}

export async function predictSign(imageBlob) {
  const formData = new FormData()

  formData.append(
    "file",
    imageBlob,
    "frame.jpg"
  )

  const res = await fetch(
    `${API_BASE_URL}/ai/predict`,
    {
      method: "POST",
      body: formData,
    }
  )

  return handleResponse(res)
}


export async function assessAttempt(sessionId, expectedSign, predictedSign, confidence) {
  const res = await fetch(`${API_BASE_URL}/assessment/score`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, expected_sign: expectedSign, predicted_sign: predictedSign, confidence }),
  })
  return handleResponse(res)
}

export async function startPracticeSession(userId, lessonId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/practice/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, lesson_id: lessonId }),
  })
  return handleResponse(res)
}

export async function endPracticeSession(sessionId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/practice/end`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId }),
  })
  return handleResponse(res)
}

// --- Lessons (Intern 2 — Course Service) ---
export async function getLessons() {
  const res = await fetch(`${API_BASE_URL}/lessons`)
  return handleResponse(res) // [{ id, title, level, description }, ...]
}

// ---------- Profile (Intern 2 — auth/profile endpoints) ----------
// Backend/app/schemas/user.py -> UpdateProfile { full_name, email }
export async function updateProfile(userId, profile) {
  const res = await fetch(`${API_BASE_URL}/auth/profile/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(profile), // { full_name, email }
  });

  return handleResponse(res); // { id, full_name, email, role_id }
}

// Backend/app/schemas/user.py -> ChangePassword { old_password, new_password }
export async function changePassword(userId, passwordData) {
  const res = await fetch(`${API_BASE_URL}/auth/change-password/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(passwordData), // { old_password, new_password }
  });

  return handleResponse(res); // { message: "Password changed successfully" }
}

// ---------- Instructor ----------
// These endpoints are protected by require_instructor on the backend
// (Backend/app/routers/instructor.py) — they need the Authorization
// header or every call fails with 401 Unauthorized.

export async function getStudents() {
  const res = await fetch(`${API_BASE_URL}/instructor/students`, {
    headers: { ...authHeaders() },
  });
  return handleResponse(res);
}

export async function getStudentProgress(studentId) {
  const res = await fetch(
    `${API_BASE_URL}/instructor/student/${studentId}/progress`,
    { headers: { ...authHeaders() } }
  );

  return handleResponse(res);
}

export async function getStudentAssessments(studentId) {
  const res = await fetch(
    `${API_BASE_URL}/instructor/student/${studentId}/assessments`,
    { headers: { ...authHeaders() } }
  );

  return handleResponse(res);
}

export async function createLesson(lesson) {
  const res = await fetch(`${API_BASE_URL}/lessons`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(lesson),
  });

  return handleResponse(res);
}

export async function updateLesson(id, lesson) {
  const res = await fetch(`${API_BASE_URL}/lessons/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(lesson),
  });

  return handleResponse(res);
}

export async function deleteLesson(id) {
  const res = await fetch(`${API_BASE_URL}/lessons/${id}`, {
    method: "DELETE",
  });

  return handleResponse(res);
}

// ---------- Admin ----------
// Protected by require_admin on the backend — also needs the token.

export async function getUsers() {
  const response = await fetch(`${API_BASE_URL}/admin/users`, {
    headers: { ...authHeaders() },
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(extractErrorMessage(data, "Failed to fetch users"));
  }

  return response.json();
}

export async function deleteUser(id) {
  const response = await fetch(`${API_BASE_URL}/admin/users/${id}`, {
    method: "DELETE",
    headers: { ...authHeaders() },
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(extractErrorMessage(data, "Failed to delete user"));
  }

  return response.json();
}

// ---------- Progress Report ----------

export async function getProgressReport(userId) {
  const res = await fetch(`${API_BASE_URL}/progress-report/${userId}`);
  return handleResponse(res);
  // { user_id, full_name, lessons_completed, total_practice_time,
  //   average_accuracy, attempted_letters, weak_letters, total_attempts,
  //   certificates_earned, generated_at }
}

export async function downloadProgressReport(userId, learnerName) {
  const res = await fetch(
    `${API_BASE_URL}/progress-report/${userId}/download?learner_name=${encodeURIComponent(learnerName)}`
  );

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(extractErrorMessage(data, "Failed to download progress report."));
  }

  return res.blob();
}

// Milestone 3, Day 5: CSV/Excel export (SRS FR-1 / Intern 1 Day 5).
// Hits the Bussiness_Logic service directly (Intern 4's export endpoint),
// same pattern as startPracticeSession/endPracticeSession above.
export async function downloadProgressReportExcel(userId, learnerName) {
  const res = await fetch(
    `${BUSINESS_LOGIC_URL}/progress-report/${userId}/excel?learner_name=${encodeURIComponent(learnerName)}`
  );

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(extractErrorMessage(data, "Failed to download Excel report."));
  }

  return res.blob();
}

// ---------- Certificate ----------

export async function getCertificateEligibility(userId) {
  const res = await fetch(
    `${API_BASE_URL}/certificate/eligibility/${userId}`
  );

  return handleResponse(res);
}

export async function downloadCertificate(userId, learnerName) {
  const res = await fetch(
    `${API_BASE_URL}/certificate/issue/${userId}?learner_name=${encodeURIComponent(learnerName)}`,
    {
      method: "POST",
    }
  );

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(extractErrorMessage(data, "Failed to download certificate."));
  }

  return res.blob();
}

// ---------- Leaderboard (Intern 4 — Business Logic) ----------
// Milestone 3, Day 4/7 (SRS FR-4 / Intern 1 Day 4): connects the
// Leaderboard page to Intern 4's real ranking API instead of mock data.
// sortBy must be "accuracy" or "streak" — matches the backend's
// Query(pattern="^(accuracy|streak)$") validation.
export async function getLeaderboard(sortBy = "accuracy") {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/leaderboard/?sort_by=${sortBy}`);
  return handleResponse(res); // [{ learner_id, learner_name, score, rank }, ...]
}

// ---------- Badges & Streaks (Intern 4 — Business Logic) ----------
// Wires the Dashboard's Badges & Streaks card to real data instead of
// the mockData.js placeholders. See Bussiness_Logic/routers/badge.py
// and Bussiness_Logic/routers/streak.py.
// NOTE: currently returning 500 Internal Server Error from the
// Bussiness_Logic service (port 8002) — this is a server-side crash,
// not a frontend bug. Needs the Bussiness_Logic terminal traceback to
// diagnose (see badge_service.py / streak_service.py).
export async function getBadges(learnerId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/badges/${learnerId}`);
  return handleResponse(res); // [{ id, learner_id, badge_name, earned_at }, ...]
}

export async function getStreak(learnerId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/streak/${learnerId}`);
  if (res.status === 404) return null; // no streak yet for this learner
  return handleResponse(res); // { id, learner_id, current_streak, longest_streak, last_practice_date }
}

// ---------- Notifications (Intern 2 — Backend) ----------
// Milestone 3, Day 2 (SRS FR-2 / Intern 1 Day 2): connects the
// Notification Bell to the real API instead of mockData.js.
// See Backend/app/routers/notification.py.
//
// TEMP WORKAROUND: notification.py declares its own prefix="/notifications"
// AND Backend/app/main.py adds "/notifications" again when including the
// router, doubling the path to /notifications/notifications/{user_id}.
// Pointing at the doubled path here so the bell works today. REVERT to
// the single-prefix path (remove "/notifications" once) as soon as
// Backend removes the duplicate prefix in notification.py — search this
// file for "notifications/notifications" to find both spots to fix.
export async function getNotifications(userId) {
  const res = await fetch(`${API_BASE_URL}/notifications/notifications/${userId}`);
  return handleResponse(res); // [{ id, user_id, title, message, is_read, created_at }, ...]
}

export async function markNotificationAsRead(notificationId) {
  const res = await fetch(`${API_BASE_URL}/notifications/notifications/${notificationId}/read`, {
    method: "PUT",
  });
  return handleResponse(res);
}

// ---------- Recommendations (Intern 4 — Business Logic) ----------
// Milestone 2, Day 4 (SRS FR-4): connects the Reports page's
// "Recommended Practice" section to the real recommendation engine.
// See Bussiness_Logic/routers/recommendation.py.
// NOTE: this endpoint recalculates recommendations on every call (it's
// not a pure read) and can trigger a new-recommendation notification —
// avoid calling it in a tight loop or on every render.
export async function getRecommendations(learnerId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/recommendations/${learnerId}`);
  return handleResponse(res); // { learner_id, recommendations: [{ id, letter_or_word, reason, recent_avg_accuracy, status, created_at }] }
}

// ---------- Weekly Analytics (Intern 4 — Business Logic) ----------
// Milestone 2, Day 3: powers the Dashboard's "Accuracy over time" and
// "Lessons completed" charts with real per-week data instead of mock
// arrays. See Bussiness_Logic/routers/weekly_analytics.py.
export async function getWeeklyAnalytics(userId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/weekly-analytics/${userId}`);
  return handleResponse(res);
  // { user_id, weekly_stats: [{ week_start, average_accuracy, improvement_rate, weak_letters, attempts_count }] }
}

// ---------- Accessibility Trainer (Intern 2 — Backend) ----------
// Milestone 4, Day 3 (SRS FR-1): connects the Trainer Dashboard to the
// real Trainer APIs instead of Trainer.jsx's mockLearners. See
// Backend/app/routers/trainer.py — all 5 endpoints are protected by
// require_trainer, so every call here needs the Authorization header.

export async function getTrainerLearners() {
  const res = await fetch(`${API_BASE_URL}/trainer/learners`, {
    headers: { ...authHeaders() },
  });
  return handleResponse(res); // [{ id, full_name, email, relationship }, ...]
}

export async function getLearnerEngagement(learnerId) {
  const res = await fetch(
    `${API_BASE_URL}/trainer/learner/${learnerId}/engagement`,
    { headers: { ...authHeaders() } }
  );
  return handleResponse(res);
  // { total_practice_sessions, completed_sessions, total_attempts,
  //   total_practice_time, current_streak, longest_streak }
}

export async function getLearnerSkillDevelopment(learnerId) {
  const res = await fetch(
    `${API_BASE_URL}/trainer/learner/${learnerId}/skill-development`,
    { headers: { ...authHeaders() } }
  );
  return handleResponse(res);
  // { overall_average_accuracy, recent_average_accuracy,
  //   previous_average_accuracy, weak_letters, improvement }
}

export async function getLearnerAssessmentAnalytics(learnerId) {
  const res = await fetch(
    `${API_BASE_URL}/trainer/learner/${learnerId}/assessment-analytics`,
    { headers: { ...authHeaders() } }
  );
  return handleResponse(res);
  // { total_assessments, average_assessment_score, highest_score,
  //   lowest_score, attempted_letters, weak_letters }
}

export async function getLearnerCertificationStatus(learnerId) {
  const res = await fetch(
    `${API_BASE_URL}/trainer/learner/${learnerId}/certification-status`,
    { headers: { ...authHeaders() } }
  );
  return handleResponse(res);
  // { certification_status, average_score, attempted_letters,
  //   completed_letters, missing_letters, certificate_earned,
  //   certificate_details: { certificate_code, issued_at, file_path, is_valid } | null }
}

// ---------- Admin: Activate/Deactivate user ----------
// Milestone 2, Day 5 (SRS FR-1): persists the Admin Dashboard's
// Activate/Deactivate toggle. Needs a matching backend endpoint —
// PATCH /admin/users/{id}/status — which does not exist yet as of
// this writing. This call will fail with a 404 until Backend adds it;
// once it does, this frontend code needs no changes.
export async function updateUserStatus(id, isActive) {
  const response = await fetch(`${API_BASE_URL}/admin/users/${id}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify({ is_active: isActive }),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(extractErrorMessage(data, "Failed to update user status"));
  }

  return response.json();
}