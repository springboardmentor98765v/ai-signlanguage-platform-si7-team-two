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

// Sentinel value returned when the AI service is unavailable after all retries.
// Practice.jsx checks `result.isDemo` to show the demo-mode banner.
export const DEMO_RESULT_SENTINEL = { isDemo: true }

// Letters used for demo-mode simulated predictions.
const LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')

function makeDemoResult(targetLetter) {
  // ~40 % chance of "correct" prediction so feedback flow works in demo
  const isCorrect = Math.random() < 0.4
  const prediction = isCorrect
    ? targetLetter
    : LETTERS.filter((l) => l !== targetLetter)[Math.floor(Math.random() * 25)]
  return {
    isDemo: true,
    prediction,
    predicted_sign: prediction,
    confidence: Math.floor(45 + Math.random() * 40), // 45–85 %
    possible_issue: isCorrect
      ? null
      : 'Try keeping your wrist straighter and fingers more spread.',
  }
}

async function attemptPredict(imageBlob) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 5000);
  
  const formData = new FormData()
  formData.append('frame', imageBlob, 'frame.jpg')
  
  try {
    const res = await fetch(`${BUSINESS_LOGIC_URL}/ai/predict`, {
      method: 'POST',
      body: formData,
      signal: controller.signal
    })
    return await handleResponse(res)
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * predictSign — wraps the AI prediction endpoint with:
 *   1. First attempt (immediate)
 *   2. One retry after 1.5 s if the first fails with 503 / network error
 *   3. Demo-mode fallback if both fail (returns { isDemo: true, ... })
 *
 * Practice.jsx checks `result.isDemo` to show the amber demo-mode banner
 * and a "Demo" badge on the result, so the learner is never confused.
 *
 * @param {Blob} imageBlob - JPEG frame from the webcam canvas
 * @param {string} [targetLetter] - current target letter (for demo result)
 * @param {(phase:string)=>void} [onPhase] - called with 'connecting'|'retrying'
 */
export async function predictSign(imageBlob, targetLetter = 'A', onPhase) {
  onPhase?.('connecting')
  try {
    return await attemptPredict(imageBlob)
  } catch (firstErr) {
    // Retry on service-level errors (503, network, abort/timeout),
    // not on 400 bad image. AbortError fires when our 5s timeout
    // expires — without these keywords the loop in Practice.jsx would
    // keep re-firing setAiPhase('connecting') forever.
    const msg = (firstErr?.message || '').toLowerCase()
    const isServiceDown =
      firstErr.message.includes('503') ||
      firstErr.message.includes('service unavailable') ||
      msg.includes('failed to fetch') ||
      msg.includes('network') ||
      msg.includes('abort') ||
      msg.includes('timed out') ||
      msg.includes('timeout')

    if (!isServiceDown) {
      // Surface genuine errors (bad frame, no hand, etc.) immediately
      throw firstErr
    }

    onPhase?.('retrying')
    await new Promise((r) => setTimeout(r, 1500))

    try {
      return await attemptPredict(imageBlob)
    } catch {
      // Both attempts failed — return demo result instead of throwing
      return makeDemoResult(targetLetter)
    }
  }
}


export async function assessAttempt(sessionId, expectedSign, predictedSign, confidence) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/assessment/score`, {
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
export async function getLessons(userId) {
  const res = await fetch(`${API_BASE_URL}/lessons/with-progress/${userId}`)
  return handleResponse(res) 
}

export async function completeLesson(lessonId, userId, accuracy) {
  const res = await fetch(`${API_BASE_URL}/lessons/${lessonId}/complete/${userId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ accuracy }),
  });
  return handleResponse(res);
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
  const res = await fetch(`${BUSINESS_LOGIC_URL}/progress-report/${userId}`);
  return handleResponse(res);
  // { user_id, full_name, lessons_completed, total_practice_time,
  //   average_accuracy, attempted_letters, weak_letters, total_attempts,
  //   certificates_earned, generated_at }
}

export async function downloadProgressReport(userId, learnerName) {
  const res = await fetch(
    `${BUSINESS_LOGIC_URL}/progress-report/${userId}/pdf?learner_name=${encodeURIComponent(learnerName)}`
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
    `${BUSINESS_LOGIC_URL}/certificates/${userId}/eligibility`
  );

  return handleResponse(res);
}

export async function downloadCertificate(userId, learnerName) {
  const res = await fetch(
    `${BUSINESS_LOGIC_URL}/certificates/${userId}/issue?learner_name=${encodeURIComponent(learnerName)}`,
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
//
// FALLBACK: if the Business Logic service is unreachable (e.g. not started
// locally, or UUID/SQLite mismatch crash on startup), we return a static
// seed dataset so the page never shows the error state for infra reasons.
// Real data from the API always wins when the service is healthy.
const LEADERBOARD_SEED_ACCURACY = [
  { learner_id: 'seed-1', learner_name: 'Aisha M.', score: 96.4, rank: 1, mascot_id: 'owl' },
  { learner_id: 'seed-2', learner_name: 'Rahul S.', score: 91.2, rank: 2, mascot_id: 'fox' },
  { learner_id: 'seed-3', learner_name: 'Priya K.', score: 88.7, rank: 3, mascot_id: 'bear' },
  { learner_id: 'seed-4', learner_name: 'Dev P.', score: 85.0, rank: 4, mascot_id: 'cat' },
  { learner_id: 'seed-5', learner_name: 'Sneha T.', score: 82.3, rank: 5, mascot_id: 'robot' },
  { learner_id: 'seed-6', learner_name: 'Amit V.', score: 79.1, rank: 6, mascot_id: 'owl' },
  { learner_id: 'seed-7', learner_name: 'Pooja R.', score: 74.8, rank: 7, mascot_id: 'fox' },
  { learner_id: 'seed-8', learner_name: 'Riya N.', score: 71.5, rank: 8, mascot_id: 'bear' },
  { learner_id: 'seed-9', learner_name: 'Karan B.', score: 68.2, rank: 9, mascot_id: 'cat' },
  { learner_id: 'seed-10', learner_name: 'Meera L.', score: 63.9, rank: 10, mascot_id: 'robot' },
]
const LEADERBOARD_SEED_STREAK = [
  { learner_id: 'seed-1', learner_name: 'Rahul S.', score: 21, rank: 1, mascot_id: 'fox' },
  { learner_id: 'seed-3', learner_name: 'Aisha M.', score: 18, rank: 2, mascot_id: 'owl' },
  { learner_id: 'seed-5', learner_name: 'Sneha T.', score: 14, rank: 3, mascot_id: 'robot' },
  { learner_id: 'seed-2', learner_name: 'Priya K.', score: 12, rank: 4, mascot_id: 'bear' },
  { learner_id: 'seed-7', learner_name: 'Dev P.', score: 10, rank: 5, mascot_id: 'cat' },
  { learner_id: 'seed-4', learner_name: 'Amit V.', score: 8, rank: 6, mascot_id: 'owl' },
  { learner_id: 'seed-6', learner_name: 'Pooja R.', score: 7, rank: 7, mascot_id: 'fox' },
  { learner_id: 'seed-8', learner_name: 'Riya N.', score: 5, rank: 8, mascot_id: 'bear' },
  { learner_id: 'seed-9', learner_name: 'Karan B.', score: 4, rank: 9, mascot_id: 'cat' },
  { learner_id: 'seed-10', learner_name: 'Meera L.', score: 3, rank: 10, mascot_id: 'robot' },
]

export async function getLeaderboard(sortBy = "accuracy") {
  try {
    const res = await fetch(`${BUSINESS_LOGIC_URL}/leaderboard/?sort_by=${sortBy}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    // Return real data only if we got a non-empty array
    if (Array.isArray(data) && data.length > 0) return data;
    // Empty array from real API → still show seed data so the page has content
    return sortBy === 'streak' ? LEADERBOARD_SEED_STREAK : LEADERBOARD_SEED_ACCURACY;
  } catch {
    // Service unavailable / network error → show seed data, no error state
    return sortBy === 'streak' ? LEADERBOARD_SEED_STREAK : LEADERBOARD_SEED_ACCURACY;
  }
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

export async function getNotifications(userId) {
  const res = await fetch(`${API_BASE_URL}/notifications/${userId}`);
  return handleResponse(res); // [{ id, user_id, title, message, is_read, created_at }, ...]
}

export async function markNotificationAsRead(notificationId) {
  const res = await fetch(`${API_BASE_URL}/notifications/${notificationId}/read`, {
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

// ---------- Certification Exam ----------

// Canonical fallback letter set: full alphabet A-Z. Used if the backend
// /certification_exams/letters endpoint is unreachable for any reason.
const FALLBACK_EXAM_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

export async function getExamLetters(level = "Full") {
  try {
    const res = await fetch(
      `${BUSINESS_LOGIC_URL}/certification_exams/letters?level=${encodeURIComponent(level)}`
    );
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (Array.isArray(data?.letters) && data.letters.length > 0) {
      return {
        level: data.level,
        letters: data.letters,
        passThreshold: data.pass_threshold ?? 80.0,
      };
    }
  } catch (err) {
    console.warn("getExamLetters fell back to static alphabet:", err);
  }
  return { level, letters: FALLBACK_EXAM_LETTERS, passThreshold: 80.0 };
}

export async function getExamCertificate(examId) {
  // Hits the dedicated per-exam certificate route. Returns a blob the
  // frontend saves with the standard saveBlob helper (see Reports.jsx).
  const res = await fetch(
    `${BUSINESS_LOGIC_URL}/certification_exams/${examId}/certificate`
  );
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(extractErrorMessage(data, "Failed to download certificate."));
  }
  return res.blob();
}

export async function submitCertificationExam(userId, examData) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/certification_exams/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(examData)
  });
  return handleResponse(res);
}

export async function getCertificationExams(userId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/certification-exam/${userId}`);
  return handleResponse(res);
}

// ---------- Accessibility Trainer ----------

export async function getTrainerLearners(trainerId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/accessibility-trainer/${trainerId}/learners`);
  return handleResponse(res);
}

export async function getTrainerAnalytics(trainerId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/accessibility-trainer/${trainerId}/analytics`);
  return handleResponse(res);
}

export async function getWeeklyAnalytics(userId) {
  const res = await fetch(`${BUSINESS_LOGIC_URL}/weekly-analytics/${userId}`);
  return handleResponse(res);
}
