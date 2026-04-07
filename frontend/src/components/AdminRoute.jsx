/**
 * src/components/AdminRoute.jsx
 * Route guard for admin-only pages.
 * Redirects to home if user is not authenticated or not an admin.
 */
import { Navigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function AdminRoute({ children }) {
  const { isAuthenticated, isAdmin, loading } = useAuth()

  // Show nothing while checking auth status
  if (loading) {
    return (
      <div className="min-h-screen pt-20 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-ember-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-gray-500 text-sm">Loading...</p>
        </div>
      </div>
    )
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  // Redirect to home if not an admin
  if (!isAdmin) {
    return <Navigate to="/" replace />
  }

  // Render admin content
  return children
}