import { useState } from "react"
import { getUser, saveSession, getToken } from "../utils/auth.js"
import { updateProfile, changePassword } from "../services/api.js"

export default function ProfilePage() {
  const [user, setUser] = useState(getUser())
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState({ full_name: user?.full_name || "", email: user?.email || "" })
  const [profileError, setProfileError] = useState("")
  const [isSavingProfile, setIsSavingProfile] = useState(false)

  const [passwords, setPasswords] = useState({ oldPassword: "", newPassword: "" })
  const [passwordError, setPasswordError] = useState("")
  const [passwordSuccess, setPasswordSuccess] = useState(false)
  const [isChangingPassword, setIsChangingPassword] = useState(false)

  function startEditing() {
    setDraft({ full_name: user.full_name, email: user.email })
    setProfileError("")
    setEditing(true)
  }

  async function saveProfile() {
    if (!user) return
    setIsSavingProfile(true)
    setProfileError("")
    try {
      const updated = await updateProfile(user.id, {
        full_name: draft.full_name,
        email: draft.email,
      })
      // Preserve role locally since /auth/profile/{id} doesn't return it
      const mergedUser = { ...user, ...updated, role: user.role }
      setUser(mergedUser)
      saveSession(getToken(), mergedUser)
      setEditing(false)
    } catch (err) {
      setProfileError(err.message || "Could not update your profile.")
    } finally {
      setIsSavingProfile(false)
    }
  }

  function cancelEditing() {
    setDraft({ full_name: user.full_name, email: user.email })
    setProfileError("")
    setEditing(false)
  }

  function handlePasswordChange(field, value) {
    setPasswords((prev) => ({ ...prev, [field]: value }))
    setPasswordError("")
    setPasswordSuccess(false)
  }

  async function submitPasswordChange(e) {
    e.preventDefault()
    const { oldPassword, newPassword } = passwords

    if (!oldPassword) {
      setPasswordError("Enter your current password.")
      return
    }
    if (newPassword.length < 6) {
      setPasswordError("New password must be at least 6 characters.")
      return
    }
    if (newPassword === oldPassword) {
      setPasswordError("New password must be different from the old one.")
      return
    }

    setIsChangingPassword(true)
    try {
      await changePassword(user.id, {
        old_password: oldPassword,
        new_password: newPassword,
      })
      setPasswordSuccess(true)
      setPasswords({ oldPassword: "", newPassword: "" })
    } catch (err) {
      setPasswordError(err.message || "Could not update your password.")
    } finally {
      setIsChangingPassword(false)
    }
  }

  if (!user) {
    return <p className="lessons-status error">You need to be logged in to view your profile.</p>
  }

  const initials = (user.full_name || "")
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  return (
    <div className="profile-shell">
      <div>
        <h1 className="page-title">Profile</h1>
        <p className="page-sub">View and update your account details.</p>
      </div>

      {/* Identity + editable fields */}
      <div className="profile-card">
        <div className="profile-identity">
          <div className="avatar">{initials}</div>
          <div>
            <p className="profile-name">{user.full_name}</p>
            <span className="badge badge-beginner">{user.role}</span>
          </div>
        </div>

        {profileError && <p className="form-error" role="alert">{profileError}</p>}

        <div className="field">
          <label>Name</label>
          {editing ? (
            <input
              type="text"
              value={draft.full_name}
              onChange={(e) => setDraft({ ...draft, full_name: e.target.value })}
            />
          ) : (
            <p className="field-static">{user.full_name}</p>
          )}
        </div>

        <div className="field">
          <label>Email</label>
          {editing ? (
            <input
              type="email"
              value={draft.email}
              onChange={(e) => setDraft({ ...draft, email: e.target.value })}
            />
          ) : (
            <p className="field-static">{user.email}</p>
          )}
        </div>

        <div className="field">
          <label>Role</label>
          <p className="field-static field-static-muted">{user.role} (set by admin)</p>
        </div>

        <div className="profile-actions">
          {editing ? (
            <>
              <button onClick={saveProfile} className="btn-primary btn-inline" disabled={isSavingProfile}>
                {isSavingProfile ? "Saving..." : "Save changes"}
              </button>
              <button onClick={cancelEditing} className="btn-secondary" disabled={isSavingProfile}>
                Cancel
              </button>
            </>
          ) : (
            <button onClick={startEditing} className="btn-secondary">
              Edit profile
            </button>
          )}
        </div>
      </div>

      {/* Change password */}
      <div className="profile-card">
        <h2 className="label">Change password</h2>
        <p className="page-sub">Use at least 6 characters, different from your current password.</p>

        <form onSubmit={submitPasswordChange}>
          <div className="field">
            <label>Old password</label>
            <input
              type="password"
              value={passwords.oldPassword}
              onChange={(e) => handlePasswordChange("oldPassword", e.target.value)}
              disabled={isChangingPassword}
            />
          </div>

          <div className="field">
            <label>New password</label>
            <input
              type="password"
              value={passwords.newPassword}
              onChange={(e) => handlePasswordChange("newPassword", e.target.value)}
              disabled={isChangingPassword}
            />
          </div>

          {passwordError && <p className="form-error" role="alert">{passwordError}</p>}
          {passwordSuccess && <p className="form-success" role="status">Password updated.</p>}

          <button type="submit" className="btn-primary btn-inline" disabled={isChangingPassword}>
            {isChangingPassword ? "Updating..." : "Update password"}
          </button>
        </form>
      </div>
    </div>
  )
}