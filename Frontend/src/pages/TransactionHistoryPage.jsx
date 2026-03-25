import { useEffect, useState } from 'react'
import { Navigate, useParams } from 'react-router-dom'
import { api } from '../services/api.js'

function TransactionHistoryPage() {
  const { accountId } = useParams()
  const session = api.getSession()
  const [transactions, setTransactions] = useState([])
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const allowed = session?.accounts?.some((account) => String(account.accountId) === accountId)

  useEffect(() => {
    async function fetchTransactions() {
      setError('')
      setIsLoading(true)

      try {
        const response = await api.getTransactions(accountId)
        setTransactions(response)
      } catch (err) {
        setTransactions([])
        setError(err.message || 'Failed to load transactions')
      } finally {
        setIsLoading(false)
      }
    }

    void fetchTransactions()
  }, [accountId])

  if (!allowed) {
    return <Navigate to="/account" replace />
  }

  return (
    <section className="auth-wrap">
      <article className="auth-card wide-card">
        <h1>Transaction History</h1>
        <p>Account ID: {accountId}</p>

        {error ? <p className="form-error">{error}</p> : null}
        {isLoading ? <p>Loading transactions...</p> : null}

        {!isLoading ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Transaction ID</th>
                  <th>Type</th>
                  <th>Amount</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {transactions.length === 0 ? (
                  <tr>
                    <td colSpan="4">No transactions found.</td>
                  </tr>
                ) : (
                  transactions.map((transaction, index) => (
                    <tr key={`${transaction.transactionId}-${index}`}>
                      <td>{transaction.transactionId ?? '-'}</td>
                      <td>{transaction.type}</td>
                      <td>${Number(transaction.amount).toFixed(2)}</td>
                      <td>{transaction.date}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        ) : null}
      </article>
    </section>
  )
}

export default TransactionHistoryPage
