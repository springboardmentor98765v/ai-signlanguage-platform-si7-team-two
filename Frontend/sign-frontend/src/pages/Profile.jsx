import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { updateProfile, changePassword } from "../services/api";

import { getUser, clearSession } from "../utils/auth";

export default function ProfilePage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  const [draft, setDraft] = useState({
    full_name: "",
    email: "",
  });
  useEffect(() => {
    const loggedUser = getUser();

    if (loggedUser) {
      setUser(loggedUser);

      setDraft({
        full_name: loggedUser.full_name,
        email: loggedUser.email,
      });
    }
  }, []);

  const [editing, setEditing] = useState(false);

  const [passwords, setPasswords] = useState({
    oldPassword: "",
    newPassword: "",
  });
  const [passwordError, setPasswordError] = useState("");
  const [passwordSuccess, setPasswordSuccess] = useState(false);
  if (!user) {
    return <div>Loading...</div>;
  }

  async function saveProfile() {
    try {
      const updatedUser = await updateProfile(user.id, {
        full_name: draft.full_name,
        email: draft.email,
      });

      setUser(updatedUser);

      localStorage.setItem("signlearn_user", JSON.stringify(updatedUser));

      setEditing(false);

      alert("Profile updated successfully!");
    } catch (err) {
      console.error(err);
      alert("Failed to update profile.");
    }
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
  function startEditing() {
    setDraft({
      full_name: user.full_name,
      email: user.email,
    });

    setEditing(true);
  }

  async function submitPasswordChange(e) {
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

  try {
    await changePassword(user.id, {
      old_password: oldPassword,
      new_password: newPassword,
    });

    setPasswordSuccess(true);
    setPasswordError("");
    setPasswords({
      oldPassword: "",
      newPassword: "",
    });

    // Password changed successfully — force logout so the old session
    // can't keep being used, then send the user back to the login page.
    setTimeout(() => {
      clearSession();
      navigate("/");
    }, 1500);

  } catch (err) {
    setPasswordSuccess(false);
    setPasswordError(err.message || "Failed to change password.");
  }
}

  const initials = user?.full_name
    ?.split(" ")
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
            <p className="profile-name">{user.full_name}</p>
            <span className="badge badge-beginner">Learner</span>
          </div>
        </div>

        <div className="field">
          <label>Name</label>
          {editing ? (
            <input
              type="text"
              value={draft.full_name}
              onChange={(e) =>
                setDraft({ ...draft, full_name: e.target.value })
              }
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
          <p className="field-static field-static-muted">
            Learner (set by admin)
          </p>
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
        <p className="page-sub">
          Use at least 6 characters, different from your current password.
        </p>

        <form onSubmit={submitPasswordChange}>
          <div className="field">
            <label>Old password</label>
            <input
              type="password"
              value={passwords.oldPassword}
              onChange={(e) =>
                handlePasswordChange("oldPassword", e.target.value)
              }
            />
          </div>

          <div className="field">
            <label>New password</label>
            <input
              type="password"
              value={passwords.newPassword}
              onChange={(e) =>
                handlePasswordChange("newPassword", e.target.value)
              }
            />
          </div>

          {passwordError && (
            <p className="form-error" role="alert">
              {passwordError}
            </p>
          )}
          {passwordSuccess && (
            <p className="form-success" role="status">
              Password updated. Logging you out...
            </p>
          )}

          <button type="submit" className="btn-primary btn-inline">
            Update password
          </button>
        </form>
      </div>
    </div>
  );
}
