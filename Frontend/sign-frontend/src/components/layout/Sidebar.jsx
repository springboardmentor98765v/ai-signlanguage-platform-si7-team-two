import { NavLink } from 'react-router-dom'
import { getUserRole } from '../../utils/auth.js'

const links = [
  { to: '/dashboard', label: 'Dashboard', roles: ['learner'] },
  { to: '/lessons', label: 'Lessons', roles: ['learner'] },

  // Default Practice page opens Letter A
  { to: '/practice/A', label: 'Practice', roles: ['learner'] },

  { to: '/reports', label: 'Reports', roles: ['learner'] },
  { to: '/instructor', label: 'Instructor', roles: ['instructor'] },
  { to: '/admin', label: 'Admin', roles: ['admin'] },
  { to: '/profile', label: 'Profile', roles: ['learner', 'instructor', 'admin'] },
]

export default function Sidebar({ open = false, onClose }) {
  const role = getUserRole()
  const visibleLinks = links.filter((link) => link.roles.includes(role))

  return (
    <aside
      id="app-sidebar"
      className={`sidebar ${open ? 'open' : ''}`}
      aria-label="Main navigation"
    >
      <div className="brand">
        <div className="mark" aria-hidden="true">SL</div>
        SignLearn
      </div>

      <nav aria-label="Primary">
        {visibleLinks.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => (isActive ? 'active' : '')}
            onClick={onClose}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}