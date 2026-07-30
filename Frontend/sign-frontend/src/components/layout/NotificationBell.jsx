import { useEffect, useRef, useState } from 'react'
import { notifications as initialNotifications } from '../../data/mockData.js'

// DEV ONLY (Milestone 3, Day 2): notifications are read from local mock data.
// Real data will come from Intern 2's Notification API (due Day 4) — see
// FR-2 / dependency matrix: Notifications table -> Notification API ->
// Notification triggers -> this component.

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
  const [items, setItems] = useState(initialNotifications)
  const [open, setOpen] = useState(false)
  const wrapperRef = useRef(null)

  const unreadCount = items.filter((n) => !n.read).length

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

  // Close on Escape for keyboard users
  function handleKeyDown(event) {
    if (event.key === 'Escape') setOpen(false)
  }

  function markAsRead(id) {
    setItems((prev) => prev.map((n) => (n.id === id ? { ...n, read: true } : n)))
  }

  function markAllAsRead() {
    setItems((prev) => prev.map((n) => ({ ...n, read: true })))
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

          {items.length === 0 ? (
            <p className="notif-empty">You're all caught up — no notifications yet.</p>
          ) : (
            <ul className="notif-list">
              {items.map((n) => (
                <li key={n.id}>
                  <button
                    type="button"
                    className={`notif-item ${n.read ? '' : 'unread'}`}
                    onClick={() => markAsRead(n.id)}
                  >
                    {!n.read && <span className="notif-item-dot" aria-hidden="true" />}
                    <span className="notif-item-body">
                      <span className="notif-item-message">{n.message}</span>
                      <span className="notif-item-time">{timeAgo(n.createdAt)}</span>
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
