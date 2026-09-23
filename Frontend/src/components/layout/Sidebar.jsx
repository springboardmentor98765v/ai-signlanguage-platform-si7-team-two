import { NavLink } from 'react-router-dom'
import { getUserRole, getUser } from '../../utils/auth.js'

const roleIcons = {
  grid: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 3H8V8H3z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M16 3H21V8H16z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M16 16H21V21H16z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3 16H8V21H3z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  book: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M2 6C2 4.89543 2.89543 4 4 4H8C9.10457 4 10 4.89543 10 6V18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M2 12C2 10.89543 2.89543 10 4 10H8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M14 6V18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M12 6H18C19.1046 6 20 6.89543 20 8V16C20 17.1046 19.1046 18 18 18H12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  hand: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M18.921 12c.331 0 .627-.174.792-.44.167-.27.139-.61-.069-.845-.207-.232-.531-.31-.817-.215-.284.095-.418.399-.323.684.095.286.399.417.684.32.27-.092.417-.397.318-.678-.099-.279-.402-.36-.678-.272-.276.087-.468.345-.508.642-.857 1.463-2.214 2.318-3.734 2.318H12V20c0 .552.448 1 1 1h3.371c2.178 0 4.094-1.232 4.916-3.02.208-.426-.112-1.316C19.753 13.38 18.921 13 18 13h-3a1 1 0 110-2h3z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M10 11V5a4 4 0 00-3-3.912" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M7 8a3 3 0 100-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  target: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M12 2V5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M2 12H5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M19 12H22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M12 19V22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  document: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M4 4C4 2.89543 4.89543 2 6 2H12L18 8V20C18 21.1046 17.1046 22 16 22H8C6.89543 22 6 21.1046 6 20V4H6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M14 2L18 6V8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  certificate: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M6 9L12 12L18 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M6 5V19C6 20.1046 6.89543 21 8 21H16C17.1046 21 18 20.1046 18 19V5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M9 12V17H15V12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M8 9H16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  podium: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M6 15V9C6 8.44772 6.44772 8 7 8H17C17.5523 8 18 8.44772 18 9V15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M6 15L9 12L12 15L15 12L18 15V20C18 20.5523 17.5523 21 17 21H7C6.44772 21 6 20.5523 6 20V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M9 9V2C9 2 10 2 10 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M15 9V2C15 2 14 2 14 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  user: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M20 21V12C20 10.8954 19.1046 10 18 10H6C4.89543 10 4 10.8954 4 12V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M12 9C14.2091 9 16 7.20914 16 5C16 2.79086 14.2091 1 12 1C9.79086 1 8 2.79086 8 5C8 7.20914 9.79086 9 12 9Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  shield: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 22S2 18 2 12V5C2 3.89543 2.89543 3 4 3H20C21.1046 3 22 3.89543 22 5V12C22 18 12 22 12 22Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M9 12L11 14L15 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  graduation: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 14L3 9L12 4L21 9L12 14Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3 9V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M12 14V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  users: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M17 21V15C17 13.8954 16.1046 13 15 13H9C7.89543 13 7 13.8954 7 15V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M9 7C9 5.34315 10.3431 4 12 4C13.6569 4 15 5.34315 15 7C15 8.65685 13.6569 10 12 10C10.3431 10 9 8.65685 9 7Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3 21V15C3 13.6108 4.10024 12.4539 5.4375 12.1205" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
}

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: 'grid', roles: ['learner'] },
  { to: '/lessons', label: 'Lessons', icon: 'book', roles: ['learner'] },
  { to: '/word-lessons', label: 'Word Practice', icon: 'hand', roles: ['learner'] },
  { to: '/practice/A', label: 'Practice', icon: 'target', roles: ['learner'] },
  { to: '/reports', label: 'Reports', icon: 'document', roles: ['learner'] },
  { to: '/certification', label: 'Certification', icon: 'certificate', roles: ['learner'] },
  { to: '/leaderboard', label: 'Leaderboard', icon: 'podium', roles: ['learner'] },
  { to: '/instructor', label: 'Instructor', icon: 'graduation', roles: ['instructor'] },
  { to: '/admin', label: 'Admin', icon: 'shield', roles: ['admin'] },
  { to: '/trainer', label: 'Trainer Dashboard', icon: 'users', roles: ['trainer'] },
  { to: '/profile', label: 'Profile', icon: 'user', roles: ['learner', 'instructor', 'admin', 'trainer'] },
]

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

export default function Sidebar({ open = false, onClose }) {
  const role = getUserRole()
  const normalizedRole = (role || '').toLowerCase()
  const user = getUser()
  const visibleLinks = links.filter((link) => link.roles.includes(normalizedRole))

  const learnerLinks = visibleLinks.filter((l) => !['instructor', 'admin', 'trainer'].includes(l.roles[0]))
  const roleLinks = visibleLinks.filter((l) => ['instructor', 'admin', 'trainer'].includes(l.roles[0]))

  return (
    <aside
      id="app-sidebar"
      className={`sidebar ${open ? 'open' : ''}`}
      aria-label="Main navigation"
    >
      <div className="brand">
        <div className="mark" aria-hidden="true">
          <img src="/app-logo-master.png" alt="" />
        </div>
        SignLearn
      </div>

      <nav aria-label="Primary">
        {learnerLinks.length > 0 && (
          <>
            <div className="nav-label">Learn</div>
            {learnerLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) => (isActive ? 'active' : '')}
                onClick={onClose}
              >
                <span className="sidebar-nav-icon">{roleIcons[link.icon]}</span>
                {link.label}
              </NavLink>
            ))}
          </>
        )}

        {roleLinks.length > 0 && (
          <>
            <div className="nav-divider" />
            <div className="nav-label">Management</div>
            {roleLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) => (isActive ? 'active' : '')}
                onClick={onClose}
              >
                <span className="sidebar-nav-icon">{roleIcons[link.icon]}</span>
                {link.label}
              </NavLink>
            ))}
          </>
        )}

        <div className="nav-divider" />

        <div className="sidebar-user">
          <div className={`user-avatar ${getRoleBadgeClass(role)}`}>
            {getInitials(user?.full_name || user?.name || user?.email || '?')}
          </div>
          <div className="user-meta">
            <span className="user-name">
              {user?.full_name || user?.name || 'User'}
            </span>
          </div>
        </div>
      </nav>
    </aside>
  )
}
