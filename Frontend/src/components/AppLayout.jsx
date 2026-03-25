import { Outlet } from 'react-router-dom'
import Navbar from './Navbar.jsx'

function AppLayout() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  )
}

export default AppLayout
