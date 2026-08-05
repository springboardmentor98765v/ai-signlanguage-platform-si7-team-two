import { useEffect, useRef, useState } from 'react'
import { getNotifications, markNotificationAsRead } from '../../services/api.js'
import { getUserId } from '../../utils/auth.js'

function timeAgo(isoString) {
  const diffMs = Date.now() - new Date(isoString).getTime()
  const minutes = Math.floor(diffMs / 60000)
  if (minutes < 1) return 'just now'
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  return `${days}d ago`
}

export default function NotificationBell() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [open, setOpen] = useState(false)
  const wrapperRef = useRef(null)

  const unreadCount = items.filter((n) => !n.is_read).length

  useEffect(() => {
    loadNotifications()
  }, [])

  async function loadNotifications() {
    const userId = getUserId()
    if (!userId) {
      setLoading(false)
      return
    }

    setLoading(true)
    try {
      const data = await getNotifications(userId)
      setItems(data)
      setError('')
    } catch (err) {
      console.error('Failed to load notifications:', err)
      setError("Couldn't load notifications.")
    } finally {
      setLoading(false)
    }
  }

  // Close the dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  function handleKeyDown(event) {
    if (event.key === 'Escape') setOpen(false)
  }

  async function markAsRead(id) {
    // Optimistic update so the UI feels instant
    setItems((prev) => prev.map((n) => (n.id === id ? { ...n, is_read: true } : n)))
    try {
      await markNotificationAsRead(id)
    } catch (err) {
      console.error('Failed to mark notification as read:', err)
      // Revert on failure
      setItems((prev) => prev.map((n) => (n.id === id ? { ...n, is_read: false } : n)))
    }
  }

  async function markAllAsRead() {
    const unread = items.filter((n) => !n.is_read)
    setItems((prev) => prev.map((n) => ({ ...n, is_read: true })))
    try {
      await Promise.all(unread.map((n) => markNotificationAsRead(n.id)))
    } catch (err) {
      console.error('Failed to mark all as read:', err)
      loadNotifications() // re-sync with server state on failure
    }
  }

  return (
    <div className="notif-wrapper" ref={wrapperRef} onKeyDown={handleKeyDown}>
      <button
        type="button"
        className="notif-bell"
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="true"
        aria-expanded={open}
        aria-label={unreadCount > 0 ? `Notifications, ${unreadCount} unread` : 'Notifications'}
      >
        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" aria-hidden="true">
          <path
            d="M12 3a5 5 0 0 0-5 5v2.6c0 .5-.15 1-.44 1.42L5.2 14.6c-.6.85-.02 2.05 1 2.05h11.6c1.02 0 1.6-1.2 1-2.05l-1.36-1.58A2.5 2.5 0 0 1 17 11.6V8a5 5 0 0 0-5-5Z"
            stroke="currentColor"
            strokeWidth="1.6"
            strokeLinejoin="round"
          />
          <path
            d="M9.5 19a2.5 2.5 0 0 0 5 0"
            stroke="currentColor"
            strokeWidth="1.6"
            strokeLinecap="round"
          />
        </svg>
        {unreadCount > 0 && (
          <span className="notif-dot" aria-hidden="true">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="notif-dropdown" role="menu">
          <div className="notif-dropdown-header">
            <span>Notifications</span>
            {unreadCount > 0 && (
              <button type="button" className="notif-mark-all" onClick={markAllAsRead}>
                Mark all as read
              </button>
            )}
          </div>

          {loading ? (
            <p className="notif-empty">Loading...</p>
          ) : error ? (
            <div className="notif-empty" role="alert">
              <p>{error}</p>
              <button type="button" className="notif-mark-all" onClick={loadNotifications}>
                Try Again
              </button>
            </div>
          ) : items.length === 0 ? (
            <p className="notif-empty">You're all caught up — no notifications yet.</p>
          ) : (
            <ul className="notif-list">
              {items.map((n) => (
                <li key={n.id}>
                  <button
                    type="button"
                    className={`notif-item ${n.is_read ? '' : 'unread'}`}
                    onClick={() => markAsRead(n.id)}
                  >
                    {!n.is_read && <span className="notif-item-dot" aria-hidden="true" />}
                    <span className="notif-item-body">
                      <span className="notif-item-message">{n.title}: {n.message}</span>
                      <span className="notif-item-time">{timeAgo(n.created_at)}</span>
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}