const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

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

export async function register(name, email, password, role) {
  const res = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password, role }),
  })
  return handleResponse(res)
}

export async function predictSign(imageBlob) {
  const formData = new FormData()
  formData.append('frame', imageBlob)
  const res = await fetch(`${API_BASE_URL}/ai/predict`, {
    method: 'POST',
    body: formData,
  })
  return handleResponse(res)
}

export async function assessAttempt(expectedSign, predictedSign, confidence, attemptDuration = 0) {
  const res = await fetch(`${API_BASE_URL}/assessment/score`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      expected_sign: expectedSign,
      predicted_sign: predictedSign,
      confidence,
      attempt_duration: attemptDuration,
    }),
  })
  return handleResponse(res)
}

// --- Lessons (Intern 2 — Course Service) ---
export async function getLessons() {
  const res = await fetch(`${API_BASE_URL}/lessons`)
  return handleResponse(res) // [{ id, title, level, description }, ...]
}
