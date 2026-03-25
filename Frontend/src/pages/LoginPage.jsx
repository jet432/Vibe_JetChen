import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api.js'

function LoginPage() {
  const navigate = useNavigate()
  const [formState, setFormState] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      const payload = await api.login(formState)
      api.setSession(payload)
      navigate('/account')
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="auth-wrap">
      <article className="auth-card">
        <h1>Login</h1>
        <p>Sign in to access your account details and transactions.</p>

        <form className="auth-form" onSubmit={handleSubmit}>
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

          {error ? <p className="form-error">{error}</p> : null}

          <button className="btn primary" disabled={isLoading} type="submit">
            {isLoading ? 'Signing in...' : 'Login'}
          </button>
        </form>
      </article>
    </section>
  )
}

export default LoginPage
