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
    body: JSON.stringify({ full_name: name, email, password,}),
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


export async function assessAttempt(expectedSign, predictedSign, confidence) {
  const res = await fetch(`${API_BASE_URL}/assessment/score`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ expected_sign: expectedSign, predicted_sign: predictedSign, confidence }),
  })
  return handleResponse(res)
}

// --- Lessons (Intern 2 — Course Service) ---
export async function getLessons() {
  const res = await fetch(`${API_BASE_URL}/lessons`)
  return handleResponse(res) // [{ id, title, level, description }, ...]
}

export async function updateProfile(userId, profile) {
  const res = await fetch(`${API_BASE_URL}/auth/profile/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(profile),
  });

  return handleResponse(res);
}

export async function changePassword(userId, passwordData) {
  const res = await fetch(`${API_BASE_URL}/auth/change-password/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(passwordData),
  });

  return handleResponse(res);
}