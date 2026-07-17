import { useState } from "react";

// Mock current user — swap for real data once Intern 2's Profile API is ready (Day 9)
const mockUser = {
  name: "Aisha Khan",
  email: "aisha.khan@example.com",
  role: "Learner",
};

export default function ProfilePage() {
  const [user, setUser] = useState(mockUser);
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(mockUser);

  const [passwords, setPasswords] = useState({ oldPassword: "", newPassword: "" });
  const [passwordError, setPasswordError] = useState("");
  const [passwordSuccess, setPasswordSuccess] = useState(false);

  function startEditing() {
    setDraft(user);
    setEditing(true);
  }

  function saveProfile() {
    setUser(draft);
    setEditing(false);
  }

  function cancelEditing() {
    setDraft(user);
    setEditing(false);
  }

  function handlePasswordChange(field, value) {
    setPasswords((prev) => ({ ...prev, [field]: value }));
    setPasswordError("");
    setPasswordSuccess(false);
  }

  function submitPasswordChange(e) {
    e.preventDefault();
    const { oldPassword, newPassword } = passwords;

    if (!oldPassword) {
      setPasswordError("Enter your current password.");
      return;
    }
    if (newPassword.length < 6) {
      setPasswordError("New password must be at least 6 characters.");
      return;
    }
    if (newPassword === oldPassword) {
      setPasswordError("New password must be different from the old one.");
      return;
    }

    // TODO: replace with real Change Password API call (Intern 2, Day 2)
    setPasswordSuccess(true);
    setPasswords({ oldPassword: "", newPassword: "" });
  }

  const initials = user.name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

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
            <p className="profile-name">{user.name}</p>
            <span className="badge badge-beginner">{user.role}</span>
          </div>
        </div>

        <div className="field">
          <label>Name</label>
          {editing ? (
            <input
              type="text"
              value={draft.name}
              onChange={(e) => setDraft({ ...draft, name: e.target.value })}
            />
          ) : (
            <p className="field-static">{user.name}</p>
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
              <button onClick={saveProfile} className="btn-primary btn-inline">
                Save changes
              </button>
              <button onClick={cancelEditing} className="btn-secondary">
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
            />
          </div>

          <div className="field">
            <label>New password</label>
            <input
              type="password"
              value={passwords.newPassword}
              onChange={(e) => handlePasswordChange("newPassword", e.target.value)}
            />
          </div>

          {passwordError && <p className="form-error">{passwordError}</p>}
          {passwordSuccess && <p className="form-success">Password updated.</p>}

          <button type="submit" className="btn-primary btn-inline">
            Update password
          </button>
        </form>
      </div>
    </div>
  );
}
