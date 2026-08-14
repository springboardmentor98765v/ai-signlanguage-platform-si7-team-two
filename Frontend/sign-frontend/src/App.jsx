import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import ForgotPassword from './pages/ForgotPassword.jsx'
import AppLayout from './components/layout/AppLayout.jsx'
import ProtectedRoute from './components/auth/ProtectedRoute.jsx'
import RoleRoute from './components/auth/RoleRoute.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Lessons from './pages/Lessons.jsx'
import Practice from './pages/Practice.jsx'
import Reports from './pages/Reports.jsx'
import Profile from './pages/Profile.jsx'
import Instructor from './pages/Instructor.jsx'
import Admin from './pages/Admin.jsx'
import Leaderboard from './pages/Leaderboard.jsx'
import Trainer from './pages/Trainer.jsx'
import Certification from './pages/Certification.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        {/* Learner-only pages */}
        <Route
          path="/dashboard"
          element={
            <RoleRoute allowedRoles={["learner"]}>
              <Dashboard />
            </RoleRoute>
          }
        />
        <Route
          path="/lessons"
          element={
            <RoleRoute allowedRoles={["learner"]}>
              <Lessons />
            </RoleRoute>
          }
        />
        <Route
          path="/practice/:letter"
          element={
            <RoleRoute allowedRoles={["learner"]}>
              <Practice />
            </RoleRoute>
          }
        />
        <Route
          path="/reports"
          element={
            <RoleRoute allowedRoles={["learner"]}>
              <Reports />
            </RoleRoute>
          }
        />
        <Route
          path="/certification"
          element={
            <RoleRoute allowedRoles={["learner"]}>
              <Certification />
            </RoleRoute>
          }
        />
        <Route
          path="/leaderboard"
          element={
            <RoleRoute allowedRoles={["learner"]}>
              <Leaderboard />
            </RoleRoute>
          }
        />

        {/* Any logged-in role can manage their own profile */}
        <Route path="/profile" element={<Profile />} />

        {/* Instructor-only */}
        <Route
          path="/instructor"
          element={
            <RoleRoute allowedRoles={["instructor"]}>
              <Instructor />
            </RoleRoute>
          }
        />

        {/* Admin-only */}
        <Route
          path="/admin"
          element={
            <RoleRoute allowedRoles={["admin"]}>
              <Admin />
            </RoleRoute>
          }
        />

        {/* Accessibility Trainer-only */}
        <Route
          path="/trainer"
          element={
            <RoleRoute allowedRoles={["trainer"]}>
              <Trainer />
            </RoleRoute>
          }
        />
      </Route>
    </Routes>
  )
}