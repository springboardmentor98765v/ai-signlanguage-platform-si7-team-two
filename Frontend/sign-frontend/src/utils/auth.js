const TOKEN_KEY = 'signlearn_token'
const ROLE_KEY = 'signlearn_role'

export function saveSession(token, role) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(ROLE_KEY, role)
}
export function getToken() { return localStorage.getItem(TOKEN_KEY) }
export function getRole() { return localStorage.getItem(ROLE_KEY) }
export function isAuthenticated() { return Boolean(getToken()) }
export function clearSession() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(ROLE_KEY)
}
