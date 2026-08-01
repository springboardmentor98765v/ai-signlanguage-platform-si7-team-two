const TOKEN_KEY = 'signlearn_token'
const USER_KEY = 'signlearn_user'

// TEMPORARY WORKAROUND: the backend's /auth/login response only returns
// role_id (a UUID), not a readable role name, and doesn't return an
// access_token at all. These UUIDs are specific to this database's seed
// data — if the DB is ever reseeded, this map must be updated too.
// Ideally this whole map goes away once the backend returns `role` and
// `access_token` directly in the login response.
const ROLE_ID_MAP = {
  '6b5dd979-0102-490f-841d-12e07a9d3dd3': 'learner',
  'e9186e06-6d41-4fa0-80b7-9f1ce4a5ad3c': 'instructor',
  'ae0e4eed-7e29-43ad-875d-2a83a1cbfd41': 'admin',
}

export function resolveRoleName(user) {
  if (!user) return ''
  if (user.role) return user.role
  if (user.role_id && ROLE_ID_MAP[user.role_id]) return ROLE_ID_MAP[user.role_id]
  return ''
}

export function saveSession(token, user) {
  // Avoid ever storing the literal string "undefined" — treat a missing
  // token as "no token" so getToken()/isAuthenticated() behave correctly.
  if (token) {
    localStorage.setItem(TOKEN_KEY, token)
  } else {
    localStorage.removeItem(TOKEN_KEY)
  }
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getUser() {
  const user = localStorage.getItem(USER_KEY)
  if (!user) return null
  return JSON.parse(user)
}

export function getUserId() {
  return getUser()?.id
}

export function getUserRole() {
  return getUser()?.role
}

export function getRoleHomePath(role) {
  const normalized = (role || '').toLowerCase()
  if (normalized === 'instructor') return '/instructor'
  if (normalized === 'admin') return '/admin'
  return '/dashboard'
}

export function isAuthenticated() {
  return Boolean(getUser())
}

export function clearSession() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}