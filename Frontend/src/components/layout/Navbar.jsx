import { useNavigate, useLocation } from 'react-router-dom'
import { clearSession, getUser, getUserRole } from '../../utils/auth.js'
import NotificationBell from './NotificationBell.jsx'

function getInitials(name) {
  if (!name) return '?'
  const parts = name.trim().split(/\s+/)
  if (parts.length === 1) return parts[0].charAt(0).toUpperCase()
  return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase()
}

function getRoleBadgeClass(role) {
  const normalized = (role || '').toLowerCase()
  if (normalized === 'learner') return ''
  if (normalized === 'instructor') return 'instructor'
  if (normalized === 'admin') return 'admin'
  if (normalized === 'trainer') return 'trainer'
  return ''
}

function getPageTitle(pathname) {
  const segments = pathname.split('/').filter(Boolean)
  if (segments.length === 0) return 'Overview'

  const labels = {
    dashboard: 'Dashboard',
    lessons: 'Lessons',
    'word-lessons': 'Word Practice',
    practice: 'Practice',
    reports: 'Reports',
    certification: 'Certification',
    leaderboard: 'Leaderboard',
    profile: 'Profile',
    admin: 'Admin',
    instructor: 'Instructor',
    trainer: 'Trainer Dashboard',
  }

  if (segments[0] === 'practice' && segments.length > 1) return 'Practice'
  return labels[segments[0]] || segments[0]
}

export default function Navbar({ onMenuClick, sidebarOpen }) {
  const navigate = useNavigate()
  const location = useLocation()
  const user = getUser()
  const role = getUserRole()
  const pageTitle = getPageTitle(location.pathname)

  function handleLogout() {
    clearSession()
    navigate('/')
  }

  const avatarClass = getRoleBadgeClass(role)

  return (
    <header className="navbar">
      <div className="navbar-left">
        <button
          type="button"
          className="menu-toggle"
          onClick={onMenuClick}
          aria-label={sidebarOpen ? 'Close navigation menu' : 'Open navigation menu'}
          aria-expanded={sidebarOpen}
          aria-controls="app-sidebar"
        >
          <span className="bar" />
        </button>

        <div className="title">{pageTitle}</div>
      </div>

      <div className="navbar-right">
        <NotificationBell />
        <div className="user-chip">
          <span className={`user-avatar ${avatarClass}`}>
            {getInitials(user?.full_name || user?.name || user?.email || '?')}
          </span>
          <span style={{ color: 'var(--muted-dim)' }}>Signed in as</span>
          <span style={{ color: 'var(--ink)', fontWeight: 600 }}>
            {user ? (user.full_name || user.name || user.email) : 'Guest'}
          </span>
        </div>
        <button className="btn-logout" onClick={handleLogout}>Log out</button>
      </div>
    </header>
  )
}
