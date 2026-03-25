import { Link, Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { api } from '../services/api.js'

function AccountDetailsPage() {
  const session = api.getSession()
  const [account, setAccount] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const selectedAccountId = session?.accounts?.[0]?.accountId

  useEffect(() => {
    async function fetchAccountDetails() {
      if (!selectedAccountId) {
        setAccount(null)
        return
      }

      setError('')
      setIsLoading(true)

      try {
        const response = await api.getAccount(selectedAccountId)
        setAccount(response)
      } catch (err) {
        setAccount(null)
        setError(err.message || 'Failed to load account')
      } finally {
        setIsLoading(false)
      }
    }

    void fetchAccountDetails()
  }, [selectedAccountId])

  if (!session?.user) {
    return <Navigate to="/login" replace />
  }

  return (
    <section className="auth-wrap">
      <article className="auth-card wide-card">
        <h1>My Account</h1>
        <p>Signed in as {session.user.name}.</p>

        {error ? <p className="form-error">{error}</p> : null}

        {isLoading ? <p>Loading account...</p> : null}

        {!isLoading && !selectedAccountId ? (
          <p>No account was found for this user. Please create an account first.</p>
        ) : null}

        {account ? (
          <section className="account-summary">
            <div>
              <span>Account ID</span>
              <strong>{account.accountId}</strong>
            </div>
            <div>
              <span>User Name</span>
              <strong>{account.userName || '-'}</strong>
            </div>
            <div>
              <span>Balance</span>
              <strong>${Number(account.balance).toFixed(2)}</strong>
            </div>
            <div className="button-row">
              <Link className="btn secondary" to={`/account/${account.accountId}/deposit`}>
                Deposit
              </Link>
              <Link className="btn secondary" to={`/account/${account.accountId}/withdraw`}>
                Withdraw
              </Link>
              <Link className="btn primary" to={`/account/${account.accountId}/transactions`}>
                View Transactions
              </Link>
            </div>
          </section>
        ) : null}
      </article>
    </section>
  )
}

export default AccountDetailsPage