import { useNavigate } from 'react-router-dom'
import { clearSession } from '../../utils/auth.js'

export default function Navbar({ onMenuClick, sidebarOpen }) {
  const navigate = useNavigate()
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
        <div className="user-chip">Signed in as Guest</div>
        <button className="btn-logout" onClick={handleLogout}>Log out</button>
      </div>
    </header>
  )
}
