import { NavLink } from 'react-router-dom'
import { getUserRole } from '../../utils/auth.js'

const links = [
  { to: '/dashboard', label: 'Dashboard', roles: ['learner'] },
  { to: '/lessons', label: 'Lessons', roles: ['learner'] },

  // Default Practice page opens Letter A
  { to: '/practice/A', label: 'Practice', roles: ['learner'] },

  { to: '/reports', label: 'Reports', roles: ['learner'] },
  { to: '/leaderboard', label: 'Leaderboard', roles: ['learner'] },
  { to: '/exam', label: 'Exam', roles: ['learner'] },
  { to: '/instructor', label: 'Instructor', roles: ['instructor'] },
  { to: '/trainer-dashboard', label: 'Trainer Dashboard', roles: ['accessibility_trainer'] },
  { to: '/admin', label: 'Admin', roles: ['admin'] },
  { to: '/profile', label: 'Profile', roles: ['learner', 'instructor', 'accessibility_trainer', 'admin'] },
]

export default function Sidebar({ open = false, onClose }) {
  const role = getUserRole()
  const normalizedRole = (role || '').toLowerCase()
  const visibleLinks = links.filter((link) => link.roles.includes(normalizedRole))

  return (
    <aside
      id="app-sidebar"
      className={`sidebar ${open ? 'open' : ''}`}
      aria-label="Main navigation"
    >
      <div className="brand">
        <div className="mark" aria-hidden="true" style={{ background: 'transparent' }}>
          <img src="/app-logo-master.png" alt="" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
        </div>
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