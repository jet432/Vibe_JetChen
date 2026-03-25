import { Link } from 'react-router-dom'

function HomePage() {
  return (
    <section className="home-grid">
      <article className="hero-card">
        <p className="eyebrow">Simple Banking System</p>
        <h1>Manage deposits, withdrawals, and account history.</h1>
        <p>
          Use the pages below to create an account, check balances, and track
          transactions with a clean beginner-friendly workflow.
        </p>
        <div className="button-row">
          <Link className="btn secondary" to="/login">
            Login
          </Link>
          <Link className="btn primary" to="/create-account">
            Create Account
          </Link>
        </div>
      </article>

      <article className="stats-card">
        <h2>Getting Started</h2>
        <p>1. Create your account.</p>
        <p>2. Login with email and password.</p>
        <p>3. Access your account dashboard.</p>
      </article>
    </section>
  )
}

export default HomePage
