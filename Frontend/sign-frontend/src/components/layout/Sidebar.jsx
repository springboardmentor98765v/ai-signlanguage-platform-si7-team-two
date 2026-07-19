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

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="mark">SL</div>
        SignLearn
      </div>

      <nav>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => (isActive ? 'active' : '')}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}