import { Navigate } from 'react-router-dom'
import { api } from '../services/api.js'

function ProtectedRoute({ children }) {
  const session = api.getSession()

  if (!session?.user) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute
