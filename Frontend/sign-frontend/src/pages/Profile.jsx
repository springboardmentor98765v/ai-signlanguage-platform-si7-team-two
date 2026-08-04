import { useState } from "react";
import { getUser, saveSession } from "../utils/auth.js";
import { updateProfile, changePassword } from "../services/api.js";

export default function Profile() {
  const user = getUser();

  const [name, setName] = useState(user?.name || user?.full_name || "");
  const [email, setEmail] = useState(user?.email || "");
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState("");
  const [saveError, setSaveError] = useState("");

  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [isChangingPw, setIsChangingPw] = useState(false);
  const [pwStatus, setPwStatus] = useState("");
  const [pwError, setPwError] = useState("");

  if (!user) {
    return (
      <div>
        <h1 className="sr-only">Profile</h1>
        <p>You need to be signed in to view your profile.</p>
      </div>
    );
  }

  async function handleSaveProfile(e) {
    e.preventDefault();
    setSaveStatus("");
    setSaveError("");
    setIsSaving(true);

    try {
      const updated = await updateProfile(user.id, {
        full_name: name,
        email: email,
      });

      saveSession({
        ...user,
        name: updated.full_name,
        full_name: updated.full_name,
        email: updated.email,
      });

      setSaveStatus("Profile updated successfully.");
    } catch (err) {
      setSaveError(err.message || "Could not update profile.");
    } finally {
      setIsSaving(false);
    }
  }

  async function handleChangePassword(e) {
    e.preventDefault();
    setPwStatus("");
    setPwError("");
    setIsChangingPw(true);

    try {
      await changePassword(user.id, {
        old_password: oldPassword,
        new_password: newPassword,
      });

      setPwStatus("Password changed successfully.");
      setOldPassword("");
      setNewPassword("");
    } catch (err) {
      setPwError(err.message || "Could not change password.");
    } finally {
      setIsChangingPw(false);
    }
  }

  return (
    <div>
      <h1 className="sr-only">Profile</h1>

      <div className="practice-header">
        <h2>Profile</h2>
        <p className="sub">Manage your account details and password.</p>
      </div>

      <section className="reference-card" style={{ marginBottom: "24px" }}>
        <p className="label">Account details</p>

        <form onSubmit={handleSaveProfile}>
          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="profile-name">Name</label>
            <input
              id="profile-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="profile-email">Email</label>
            <input
              id="profile-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <p><strong>Role:</strong> {user.role}</p>

          {saveError && <p className="camera-error" role="alert">{saveError}</p>}
          {saveStatus && <p role="status">{saveStatus}</p>}

          <button className="btn-primary" type="submit" disabled={isSaving}>
            {isSaving ? "Saving..." : "Save changes"}
          </button>
        </form>
      </section>

      <section className="reference-card">
        <p className="label">Change password</p>

        <form onSubmit={handleChangePassword}>
          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="old-password">Current password</label>
            <input
              id="old-password"
              type="password"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              required
            />
          </div>

          <div style={{ marginBottom: "12px" }}>
            <label htmlFor="new-password">New password</label>
            <input
              id="new-password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              minLength={6}
            />
          </div>

          {pwError && <p className="camera-error" role="alert">{pwError}</p>}
          {pwStatus && <p role="status">{pwStatus}</p>}

          <button className="btn-primary" type="submit" disabled={isChangingPw}>
            {isChangingPw ? "Changing..." : "Change password"}
          </button>
        </form>
      </section>
    </div>
  );
}