import { useState } from 'react'
import { Navigate, useNavigate, useParams } from 'react-router-dom'
import { api } from '../services/api.js'

function WithdrawPage() {
  const { accountId } = useParams()
  const navigate = useNavigate()
  const session = api.getSession()
  const [amount, setAmount] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const allowed = session?.accounts?.some((account) => String(account.accountId) === accountId)

  if (!allowed) {
    return <Navigate to="/account" replace />
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await api.withdraw(accountId, amount)
      navigate('/account')
    } catch (err) {
      setError(err.message || 'Withdraw failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="dashboard-shell">
      <article className="auth-card wide-card dashboard-main dashboard-page">
        <header className="dashboard-head">
          <div>
            <p className="eyebrow">Overview</p>
            <h1>Withdraw Money</h1>
          </div>
          <div className="dashboard-user">
            <strong>Account #{accountId}</strong>
            <span>Withdraw</span>
          </div>
        </header>
        <p>Account ID: {accountId}</p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="withdrawAmount">
            Amount
            <input
              id="withdrawAmount"
              min="0.01"
              onChange={(event) => setAmount(event.target.value)}
              required
              step="0.01"
              type="number"
              value={amount}
            />
          </label>

          {error ? <p className="form-error">{error}</p> : null}

          <button className="btn primary" disabled={isLoading} type="submit">
            {isLoading ? 'Submitting...' : 'Submit'}
          </button>
        </form>
      </article>
    </section>
  )
}

export default WithdrawPage
