import { NavLink } from 'react-router-dom'

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/lessons', label: 'Lessons' },
  { to: '/practice', label: 'Practice' },
  { to: '/reports', label: 'Reports' },
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
