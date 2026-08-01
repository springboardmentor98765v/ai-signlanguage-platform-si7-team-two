import { useNavigate } from 'react-router-dom'
import { clearSession, getUser } from '../../utils/auth.js'
import NotificationBell from './NotificationBell.jsx'

export default function Navbar({ onMenuClick, sidebarOpen }) {
  const navigate = useNavigate()
  const user = getUser()

  function handleLogout() {
    clearSession()
    navigate('/')
  }
  return (
    <header className="navbar">
      <div className="navbar-left" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
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
        <div className="title">Overview</div>
      </div>
      <div className="navbar-right">
        <NotificationBell />
        <div className="user-chip">
          {user ? `Signed in as ${user.full_name}` : 'Signed in as Guest'}
        </div>
        <button className="btn-logout" onClick={handleLogout}>Log out</button>
      </div>
    </header>
  )
}