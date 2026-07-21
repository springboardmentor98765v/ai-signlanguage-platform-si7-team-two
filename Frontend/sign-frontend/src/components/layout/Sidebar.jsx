import { NavLink } from 'react-router-dom'

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/lessons', label: 'Lessons' },

  // Default Practice page opens Letter A
  { to: '/practice/A', label: 'Practice' },

  { to: '/reports', label: 'Reports' },
  { to: '/instructor', label: 'Instructor' },
  { to: '/admin', label: 'Admin' },
  { to: '/profile', label: 'Profile' },
]

export default function Sidebar({ open = false, onClose }) {
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
        {links.map((link) => (
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