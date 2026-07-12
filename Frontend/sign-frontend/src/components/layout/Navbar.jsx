import { useNavigate } from 'react-router-dom'
import { clearSession } from '../../utils/auth.js'

export default function Navbar() {
  const navigate = useNavigate()
  function handleLogout() {
    clearSession()
    navigate('/')
  }
  return (
    <header className="navbar">
      <div className="title">Overview</div>
      <div className="navbar-right">
        <div className="user-chip">Signed in as Guest</div>
        <button className="btn-logout" onClick={handleLogout}>Log out</button>
      </div>
    </header>
  )
}
