import { Navigate } from "react-router-dom";
import { getUserRole, getRoleHomePath } from "../../utils/auth.js";

// Wraps a single page and blocks it unless the logged-in user's role is
// in allowedRoles. A mismatched role is sent to their OWN home page
// (not the login screen) — e.g. a Learner hitting /admin lands back on
// /dashboard instead of being logged out.
export default function RoleRoute({ children, allowedRoles }) {
  const role = getUserRole();

  if (allowedRoles && allowedRoles.length > 0 && !allowedRoles.includes(role)) {
    return <Navigate to={getRoleHomePath(role)} replace />;
  }

  return children;
}
