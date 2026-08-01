const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
// Analytics, weekly-analytics, and recommendations live on the separate
// Business Logic microservice (port 8002) and are not proxied through the
// Backend (port 8000), so they're called here directly.
const BUSINESS_LOGIC_URL = import.meta.env.VITE_BUSINESS_LOGIC_URL || 'http://localhost:8002'

function getToken() {
  return localStorage.getItem('signlearn_token')
}

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function handleResponse(res) {
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(data.detail || 'Something went wrong. Please try again.')
  }
  return data
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
    body: JSON.stringify({ full_name: name, email, password }),
  })
  return handleResponse(res)
}

export async function predictSign(imageBlob) {
  const formData = new FormData()
  formData.append("file", imageBlob, "frame.jpg")

  const res = await fetch(`${API_BASE_URL}/ai/predict`, {
    method: "POST",
    body: formData,
    headers: { ...authHeaders() },
  })

  return handleResponse(res)
}

export async function assessAttempt(expectedSign, predictedSign, confidence) {
  const res = await fetch(`${API_BASE_URL}/assessment/score`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ expected_sign: expectedSign, predicted_sign: predictedSign, confidence }),
  })
  return handleResponse(res)
}

// --- Lessons ---
export async function getLessons() {
  const res = await fetch(`${API_BASE_URL}/lessons`, { headers: { ...authHeaders() } })
  return handleResponse(res)
}

export async function createLesson(lesson) {
  const res = await fetch(`${API_BASE_URL}/lessons`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(lesson),
  })
  return handleResponse(res)
}

export async function updateLesson(id, lesson) {
  const res = await fetch(`${API_BASE_URL}/lessons/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(lesson),
  })
  return handleResponse(res)
}

export async function deleteLesson(id) {
  const res = await fetch(`${API_BASE_URL}/lessons/${id}`, {
    method: "DELETE",
    headers: { ...authHeaders() },
  })
  return handleResponse(res)
}

// --- Profile ---
export async function updateProfile(userId, profile) {
  const res = await fetch(`${API_BASE_URL}/auth/profile/${userId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(profile),
  })
  return handleResponse(res)
}

export async function changePassword(userId, passwordData) {
  const res = await fetch(`${API_BASE_URL}/auth/change-password/${userId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(passwordData),
  })
  return handleResponse(res)
}

// ---------- Instructor ----------
export async function getStudents() {
  const res = await fetch(`${API_BASE_URL}/instructor/students`, { headers: { ...authHeaders() } })
  return handleResponse(res)
}
// Alias to match the name used in Instructor.jsx
export const getInstructorStudents = getStudents

export async function getStudentProgress(studentId) {
  const res = await fetch(`${API_BASE_URL}/instructor/student/${studentId}/progress`, {
    headers: { ...authHeaders() },
  })
  return handleResponse(res)
}

export async function getStudentAssessments(studentId) {
  const res = await fetch(`${API_BASE_URL}/instructor/student/${studentId}/assessments`, {
    headers: { ...authHeaders() },
  })
  return handleResponse(res)
}

// ---------- Admin ----------
export async function getUsers() {
  const res = await fetch(`${API_BASE_URL}/admin/users`, { headers: { ...authHeaders() } })
  return handleResponse(res)
}

export async function deleteUser(id) {
  const res = await fetch(`${API_BASE_URL}/admin/users/${id}`, {
    method: "DELETE",
    headers: { ...authHeaders() },
  })
  return handleResponse(res)
}

// ---------- Progress Report (Backend proxies to Business Logic) ----------
export async function getProgressReport(userId) {
  const res = await fetch(`${API_BASE_URL}/progress-report/${userId}`, { headers: { ...authHeaders() } })
  return handleResponse(res)
}

export async function downloadProgressReport(userId, learnerName) {
  const res = await fetch(
    `${API_BASE_URL}/progress-report/${userId}/download?learner_name=${encodeURIComponent(learnerName)}`,
    { headers: { ...authHeaders() } }
  )
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    throw new Error(data.detail || "Failed to download progress report.")
  }
  return res.blob()
}

// ---------- Certificate (Backend proxies to Business Logic; always returns a PDF) ----------
export async function getCertificateEligibility(userId) {
  const res = await fetch(`${API_BASE_URL}/certificate/eligibility/${userId}`, { headers: { ...authHeaders() } })
  return handleResponse(res)
}

// Returns a PDF blob — there is no JSON "issue" endpoint on the backend.
export async function issueCertificate(userId, learnerName) {
  const res = await fetch(
    `${API_BASE_URL}/certificate/issue/${userId}?learner_name=${encodeURIComponent(learnerName)}`,
    { method: "POST", headers: { ...authHeaders() } }
  )
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    throw new Error(data.detail?.message || data.detail || "Failed to issue certificate.")
  }
  return res.blob()
}

// ---------- Analytics / Recommendations (direct to Business Logic service — not proxied) ----------
export async function getLearnerAnalytics(userId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/analytics/${userId}`, { headers: { ...authHeaders() } })
  return handleResponse(res)
}

export async function getWeeklyAnalytics(userId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/weekly-analytics/${userId}`, { headers: { ...authHeaders() } })
  return handleResponse(res)
}

export async function getRecommendations(userId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/recommendations/${userId}`, { headers: { ...authHeaders() } })
  return handleResponse(res)
}