const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:5000'
const SESSION_KEY = 'bank_session'

async function request(path, options = {}) {
  const session = JSON.parse(sessionStorage.getItem(SESSION_KEY) || 'null')
  const token = session?.token
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers ?? {}),
    },
    ...options,
  })

  const payload = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(payload.error || 'Request failed')
  }

  return payload
}

export const api = {
  async createUserAndAccount({ name, email, password, accountType }) {
    const registerPayload = await request('/api/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    })

    return request('/api/accounts', {
      method: 'POST',
      body: JSON.stringify({
        userId: registerPayload.user.userId,
        accountType,
      }),
    })
  },

  getAccount(accountId) {
    return request(`/api/accounts/${accountId}`)
  },

  deposit(accountId, amount) {
    return request(`/api/accounts/${accountId}/deposit`, {
      method: 'POST',
      body: JSON.stringify({ amount: Number(amount) }),
    })
  },

  withdraw(accountId, amount) {
    return request(`/api/accounts/${accountId}/withdraw`, {
      method: 'POST',
      body: JSON.stringify({ amount: Number(amount) }),
    })
  },

  getTransactions(accountId) {
    return request(`/api/accounts/${accountId}/transactions`)
  },

  login(credentials) {
    return request('/api/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    })
  },

  setSession(sessionPayload) {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(sessionPayload))
  },

  getSession() {
    return JSON.parse(sessionStorage.getItem(SESSION_KEY) || 'null')
  },

  clearSession() {
    sessionStorage.removeItem(SESSION_KEY)
  },
}
