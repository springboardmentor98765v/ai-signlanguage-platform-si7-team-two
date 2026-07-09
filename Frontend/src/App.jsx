import { Routes, Route } from 'react-router-dom'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'
import AppLayout from './components/layout/AppLayout.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Lessons from './pages/Lessons.jsx'
import Practice from './pages/Practice.jsx'
import Reports from './pages/Reports.jsx'

export default function App() {
  return (
    <Routes>
      {/* Auth screens: no sidebar/navbar */}
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* App screens: share sidebar + navbar via AppLayout */}
      <Route element={<AppLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/lessons" element={<Lessons />} />
        <Route path="/practice" element={<Practice />} />
        <Route path="/reports" element={<Reports />} />
      </Route>
    </Routes>
  )
}
