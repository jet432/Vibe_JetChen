import { Link, Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { api } from '../services/api.js'

function AccountDetailsPage() {
  const session = api.getSession()
  const [account, setAccount] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showDepositForm, setShowDepositForm] = useState(false)
  const [showWithdrawForm, setShowWithdrawForm] = useState(false)
  const [depositAmount, setDepositAmount] = useState('')
  const [withdrawAmount, setWithdrawAmount] = useState('')
  const [depositError, setDepositError] = useState('')
  const [withdrawError, setWithdrawError] = useState('')
  const [isSubmittingDeposit, setIsSubmittingDeposit] = useState(false)
  const [isSubmittingWithdraw, setIsSubmittingWithdraw] = useState(false)

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

  function toggleDepositForm() {
    setShowDepositForm((prev) => !prev)
    setDepositError('')
  }

  function toggleWithdrawForm() {
    setShowWithdrawForm((prev) => !prev)
    setWithdrawError('')
  }

  async function handleDepositSubmit(event) {
    event.preventDefault()

    if (!selectedAccountId) {
      return
    }

    setDepositError('')
    setIsSubmittingDeposit(true)

    try {
      await api.deposit(selectedAccountId, depositAmount)
      const refreshedAccount = await api.getAccount(selectedAccountId)
      setAccount(refreshedAccount)
      setDepositAmount('')
      setShowDepositForm(false)
    } catch (err) {
      setDepositError(err.message || 'Deposit failed')
    } finally {
      setIsSubmittingDeposit(false)
    }
  }

  async function handleWithdrawSubmit(event) {
    event.preventDefault()

    if (!selectedAccountId) {
      return
    }

    setWithdrawError('')
    setIsSubmittingWithdraw(true)

    try {
      await api.withdraw(selectedAccountId, withdrawAmount)
      const refreshedAccount = await api.getAccount(selectedAccountId)
      setAccount(refreshedAccount)
      setWithdrawAmount('')
      setShowWithdrawForm(false)
    } catch (err) {
      setWithdrawError(err.message || 'Withdraw failed')
    } finally {
      setIsSubmittingWithdraw(false)
    }
  }

  return (
    <section className="dashboard-shell">
      <article className="auth-card wide-card dashboard-main">
        <header className="dashboard-head">
          <div>
            <p className="eyebrow">Overview</p>
            <h1>My Account</h1>
          </div>
          <div className="dashboard-user">
            <strong>{session.user.name}</strong>
            <span>Main Account</span>
          </div>
        </header>

        {error ? <p className="form-error">{error}</p> : null}

        {isLoading ? <p className="dashboard-note">Loading account...</p> : null}

        {!isLoading && !selectedAccountId ? (
          <p className="dashboard-note">No account was found for this user. Please create an account first.</p>
        ) : null}

        {account ? (
          <>
            <section className="balance-hero">
              <div>
                <p className="mini-label">Your account balance</p>
                <strong>${Number(account.balance).toFixed(2)} USD</strong>
                <p className="subtle-copy">All core account actions remain available below.</p>
              </div>
            </section>

            <section className="account-summary bank-summary">
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
              <div className="action-columns">
                <div className="action-column left">
                  <button className="btn secondary" onClick={toggleDepositForm} type="button">
                    Deposit
                  </button>
                  {showDepositForm ? (
                    <form className="inline-action-card" onSubmit={handleDepositSubmit}>
                      <label htmlFor="depositInlineAmount">
                        Deposit Amount
                        <input
                          id="depositInlineAmount"
                          min="0.01"
                          onChange={(event) => setDepositAmount(event.target.value)}
                          required
                          step="0.01"
                          type="number"
                          value={depositAmount}
                        />
                      </label>
                      {depositError ? <p className="form-error">{depositError}</p> : null}
                      <button className="btn primary" disabled={isSubmittingDeposit} type="submit">
                        {isSubmittingDeposit ? 'Submitting...' : 'Submit Deposit'}
                      </button>
                    </form>
                  ) : null}
                </div>

                <div className="action-column center">
                  <button className="btn secondary" onClick={toggleWithdrawForm} type="button">
                    Withdraw
                  </button>
                  {showWithdrawForm ? (
                    <form className="inline-action-card" onSubmit={handleWithdrawSubmit}>
                      <label htmlFor="withdrawInlineAmount">
                        Withdraw Amount
                        <input
                          id="withdrawInlineAmount"
                          min="0.01"
                          onChange={(event) => setWithdrawAmount(event.target.value)}
                          required
                          step="0.01"
                          type="number"
                          value={withdrawAmount}
                        />
                      </label>
                      {withdrawError ? <p className="form-error">{withdrawError}</p> : null}
                      <button className="btn primary" disabled={isSubmittingWithdraw} type="submit">
                        {isSubmittingWithdraw ? 'Submitting...' : 'Submit Withdraw'}
                      </button>
                    </form>
                  ) : null}
                </div>

                <div className="action-column right">
                  <Link className="btn secondary" to={`/account/${account.accountId}/transactions`}>
                    View Transactions
                  </Link>
                </div>
              </div>
            </section>
          </>
        ) : null}
      </article>
    </section>
  )
}

export default AccountDetailsPage
