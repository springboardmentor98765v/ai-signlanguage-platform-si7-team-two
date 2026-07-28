import { useEffect, useState } from 'react'
import { useLocation, Outlet } from 'react-router-dom'
import Sidebar from './Sidebar.jsx'
import Navbar from './Navbar.jsx'

export default function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()

  // Close the mobile drawer automatically whenever the route changes
  useEffect(() => {
    setSidebarOpen(false)
  }, [location.pathname])

  return (
    <div className="app-shell">
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Click-outside overlay, mobile only */}
      <button
        type="button"
        className={`sidebar-overlay ${sidebarOpen ? 'open' : ''}`}
        aria-hidden={!sidebarOpen}
        tabIndex={-1}
        onClick={() => setSidebarOpen(false)}
      />

      <div className="main-area">
        <Navbar onMenuClick={() => setSidebarOpen((v) => !v)} sidebarOpen={sidebarOpen} />
        <main id="main-content" className="page-body" tabIndex={-1}>
          <Outlet />
        </main>
      </div>
    </div>
  )
}
