import { NavLink, useNavigate } from 'react-router-dom'
import { api } from '../services/api.js'

function Navbar() {
  const navigate = useNavigate()
  const session = api.getSession()

  function handleLogout() {
    api.clearSession()
    navigate('/login')
  }

  return (
    <header className="top-nav">
      <div className="brand">
        <span className="brand-dot" />
        <p>Simple Bank</p>
      </div>
      <nav>
        <NavLink to="/">Home</NavLink>
        {!session ? <NavLink to="/login">Login</NavLink> : null}
        {!session ? <NavLink to="/create-account">Create Account</NavLink> : null}
        {session ? <NavLink to="/account">My Account</NavLink> : null}
        {session ? (
          <button className="btn secondary nav-button" onClick={handleLogout} type="button">
            Logout
          </button>
        ) : null}
      </nav>
    </header>
  )
}

export default Navbar
