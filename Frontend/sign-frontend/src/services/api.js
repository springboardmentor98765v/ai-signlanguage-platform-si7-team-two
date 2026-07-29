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
// ---------- Instructor ----------

export async function getStudents() {
  const res = await fetch(`${API_BASE_URL}/instructor/students`);
  return handleResponse(res);
}

export async function getStudentProgress(studentId) {
  const res = await fetch(
    `${API_BASE_URL}/instructor/student/${studentId}/progress`
  );

  return handleResponse(res);
}

export async function getStudentAssessments(studentId) {
  const res = await fetch(
    `${API_BASE_URL}/instructor/student/${studentId}/assessments`
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
export async function getUsers() {
  const response = await fetch(`${API_BASE_URL}/admin/users`);

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  return response.json();
}

export async function deleteUser(id) {
  const response = await fetch(`${API_BASE_URL}/admin/users/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Failed to delete user");
  }

  return response.json();
}
// ---------- Progress Report ----------

export async function getProgressReport(userId) {
  const res = await fetch(`${API_BASE_URL}/progress-report/${userId}`);
  return handleResponse(res);
}

export async function downloadProgressReport(userId, learnerName) {
  const res = await fetch(
    `${API_BASE_URL}/progress-report/${userId}/download?learner_name=${encodeURIComponent(learnerName)}`
  );

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "Failed to download progress report.");
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
    throw new Error(data.detail || "Failed to download certificate.");
  }

  return res.blob();
}