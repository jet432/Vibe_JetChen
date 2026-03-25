import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api.js'

function CreateAccountPage() {
  const navigate = useNavigate()
  const [formState, setFormState] = useState({
    name: '',
    email: '',
    password: '',
    accountType: 'SAVINGS',
  })
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await api.createUserAndAccount(formState)
      navigate('/login')
    } catch (err) {
      setError(err.message || 'Failed to create account')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="auth-wrap">
      <article className="auth-card">
        <h1>Create Account</h1>
        <p>Register a user and open a bank account.</p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="name">
            Name
            <input
              id="name"
              name="name"
              onChange={(event) =>
                setFormState((previous) => ({ ...previous, name: event.target.value }))
              }
              required
              type="text"
              value={formState.name}
            />
          </label>

          <label htmlFor="email">
            Email
            <input
              id="email"
              name="email"
              onChange={(event) =>
                setFormState((previous) => ({ ...previous, email: event.target.value }))
              }
              required
              type="email"
              value={formState.email}
            />
          </label>

          <label htmlFor="password">
            Password
            <input
              id="password"
              name="password"
              onChange={(event) =>
                setFormState((previous) => ({ ...previous, password: event.target.value }))
              }
              required
              type="password"
              value={formState.password}
            />
          </label>

          <label htmlFor="accountType">
            Account Type
            <select
              id="accountType"
              name="accountType"
              onChange={(event) =>
                setFormState((previous) => ({ ...previous, accountType: event.target.value }))
              }
              value={formState.accountType}
            >
              <option value="SAVINGS">SAVINGS</option>
              <option value="CHECKING">CHECKING</option>
            </select>
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

export default CreateAccountPage
