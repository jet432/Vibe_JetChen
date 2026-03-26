import { Link } from 'react-router-dom'
import { api } from '../services/api.js'

function HomePage() {
  const session = api.getSession()
  const isLoggedIn = Boolean(session?.user)

  return (
    <section className="home-grid">
      <article className="hero-card">
        <p className="eyebrow">Simple Banking System</p>
        <h1>
          {isLoggedIn
            ? 'Welcome back. Manage your account activity from one place.'
            : 'Manage deposits, withdrawals, and account history.'}
        </h1>
        <p>
          {isLoggedIn
            ? 'Go to your account dashboard to deposit, withdraw, and review your transaction history.'
            : 'Use the pages below to create an account, check balances, and track transactions with a clean beginner-friendly workflow.'}
        </p>
        {!isLoggedIn ? (
          <div className="button-row">
            <Link className="btn secondary" to="/login">
              Login
            </Link>
            <Link className="btn primary" to="/create-account">
              Create Account
            </Link>
          </div>
        ) : (
          <div className="button-row">
            <Link className="btn primary" to="/account">
              Go to My Account
            </Link>
          </div>
        )}
      </article>

      <article className="stats-card">
        <h2>{isLoggedIn ? 'Quick Actions' : 'Getting Started'}</h2>
        {isLoggedIn ? (
          <>
            <p>1. Open My Account.</p>
            <p>2. Deposit or withdraw funds.</p>
            <p>3. Review transaction history.</p>
          </>
        ) : (
          <>
            <p>1. Create your account.</p>
            <p>2. Login with email and password.</p>
            <p>3. Access your account dashboard.</p>
          </>
        )}
      </article>
    </section>
  )
}

export default HomePage
