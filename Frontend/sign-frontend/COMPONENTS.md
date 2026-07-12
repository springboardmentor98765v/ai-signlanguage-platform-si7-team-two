# SignLearn Frontend — Component Documentation

Milestone 1 · Intern 1 (Frontend / UI-UX Developer)

## Pages (`src/pages/`)

### Login.jsx
Login form (email, password). Calls `login()` from `services/api.js`,
saves the JWT token via `utils/auth.js`, then navigates to `/dashboard`.
Shows a loading state ("Logging in...") and an error banner on failure.
Includes a **dev-only "Skip Login" button** to bypass auth while the
real backend isn't reachable — remove before final submission.

### Register.jsx
Registration form (name, email, password, confirm password, role).
Validates that passwords match client-side before calling `register()`.
Same loading/error pattern as Login.

### Dashboard.jsx
Learner overview — accuracy, lessons completed, practice hours.
Currently rendering `mockData.dashboardStats` (real data comes from
Intern 4's Analytics endpoint in a later milestone).

### Lessons.jsx
Fetches lesson list from `getLessons()` (Intern 2's Course API) on
mount. Shows a loading state, and falls back to local mock lessons
with an error message if the API call fails, so the page is never
empty during development/demo.

### Practice.jsx
The core Day 5–7 screen:
- Requests webcam access (`getUserMedia`), shows live video feed
- Start/Stop Practice buttons
- "Check My Sign" — captures the current frame, sends it to
  `predictSign()` (Intern 3's AI service), then sends that result to
  `assessAttempt()` (Intern 4's Assessment/Feedback service)
- Displays predicted sign, confidence, accuracy score, and the
  feedback message list returned by the Assessment service

### Reports.jsx
Progress report screen — overall stats, a recent-attempts table with
accuracy bars, and a weak-letter recommendation panel. Currently uses
mock data from `data/mockData.js` (real data comes from Intern 4's
Analytics endpoint in a later milestone).

## Shared layout (`src/components/layout/`)

### AppLayout.jsx
Wraps Sidebar + Navbar + `<Outlet />` so every protected page shares
the same shell without repeating layout code.

### Sidebar.jsx
Left navigation — links to Dashboard, Lessons, Practice, Reports.

### Navbar.jsx
Top bar — page title + user chip + Log out button (clears the saved
session and redirects to Login).

## Auth (`src/components/auth/`, `src/utils/`)

### ProtectedRoute.jsx
Wraps any route that requires login. Redirects to `/` if no valid
token is found via `isAuthenticated()`.

### utils/auth.js
Small helpers for saving/reading/clearing the JWT token and role in
`localStorage`.

## API layer (`src/services/api.js`)

Real `fetch()`-based calls to the backend, using `VITE_API_BASE_URL`
(defaults to `http://localhost:8000`):
- `login(email, password)` → Intern 2 Auth
- `register(name, email, password, role)` → Intern 2 Auth
- `getLessons()` → Intern 2 Course Service
- `predictSign(imageBlob)` → Intern 3 AI/CV service
- `assessAttempt(expectedSign, predictedSign, confidence)` → Intern 4
  Assessment/Feedback service

All calls throw on non-2xx responses so callers can catch and display
an error message; this is the "Failed to fetch" behavior seen while
the real backend isn't running yet.

## Known limitations (Milestone 1)

- Dashboard and Reports still use mock data (per SRS scope: "mock data
  acceptable" for Dashboard in FR-1).
- Login/Register/Lessons/Practice will show error states until Interns
  2, 3, and 4's real endpoints are live and `VITE_API_BASE_URL` is set.
- "Skip Login (Dev Mode)" button on the Login page is temporary and
  should be removed before final submission.
