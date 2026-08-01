import { Navigate } from 'react-router-dom'
import { getUserRole, getRoleHomePath } from '../../utils/auth.js'

// Blocks a route unless the logged-in user's role is in allowedRoles.
// A mismatched role is redirected to their OWN home page (not logged out) —
// e.g. a Learner hitting /admin lands back on /dashboard instead.
export default function RoleRoute({ children, allowedRoles }) {
  const role = getUserRole()
  const normalizedRole = (role || '').toLowerCase()
  const normalizedAllowed = (allowedRoles || []).map((r) => r.toLowerCase())

  if (normalizedAllowed.length > 0 && !normalizedAllowed.includes(normalizedRole)) {
    return <Navigate to={getRoleHomePath(role)} replace />
  }

  return children
}