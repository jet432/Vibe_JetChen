import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from './components/AppLayout.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import AccountDetailsPage from './pages/AccountDetailsPage.jsx'
import CreateAccountPage from './pages/CreateAccountPage.jsx'
import DepositPage from './pages/DepositPage.jsx'
import HomePage from './pages/HomePage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import TransactionHistoryPage from './pages/TransactionHistoryPage.jsx'
import WithdrawPage from './pages/WithdrawPage.jsx'

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/create-account" element={<CreateAccountPage />} />
        <Route
          path="/account"
          element={
            <ProtectedRoute>
              <AccountDetailsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/:accountId/deposit"
          element={
            <ProtectedRoute>
              <DepositPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/:accountId/withdraw"
          element={
            <ProtectedRoute>
              <WithdrawPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/:accountId/transactions"
          element={
            <ProtectedRoute>
              <TransactionHistoryPage />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}

export default App
