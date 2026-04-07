/**
 * src/pages/admin/AdminLayout.jsx
 * Layout wrapper for admin pages — renders navbar + sidebar navigation.
 */
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom'
import { LayoutDashboard, ShoppingBag, ChefHat, ArrowLeft, LogOut, TicketPercent } from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'

const NAV_LINKS = [
  { to: '/admin',      label: 'Dashboard',     icon: LayoutDashboard },
  { to: '/admin/menu', label: 'Manage Menu',   icon: ChefHat },
  { to: '/admin/orders', label: 'Manage Orders', icon: ShoppingBag },
  { to: '/admin/coupons', label: 'Coupons', icon: TicketPercent },
]

export default function AdminLayout() {
  const location = useLocation()
  const navigate = useNavigate()
  const { logout, user } = useAuth()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen pt-20 pb-16 px-4">
      <div className="max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link to="/" className="btn-ghost flex items-center gap-2 text-sm">
              <ArrowLeft className="w-4 h-4" /> Back to Site
            </Link>
            <div className="h-6 w-px bg-white/10" />
            <div>
              <h1 className="text-white font-bold text-lg">Admin Panel</h1>
              <p className="text-gray-500 text-xs">Logged in as {user?.full_name}</p>
            </div>
          </div>
          <button onClick={handleLogout} className="btn-ghost flex items-center gap-2 text-sm text-red-400 hover:text-red-300">
            <LogOut className="w-4 h-4" /> Logout
          </button>
        </div>

        {/* Admin Navigation Tabs */}
        <div className="flex gap-2 mb-8 border-b border-white/5 pb-1">
          {NAV_LINKS.map(({ to, label, icon: Icon }) => {
            const isActive = location.pathname === to || 
                            (to !== '/admin' && location.pathname.startsWith(to))
            return (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-t-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-ash-100 text-ember-500 border-b-2 border-ember-500 -mb-1'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon className="w-4 h-4" />
                {label}
              </Link>
            )
          })}
        </div>

        {/* Page Content */}
        <Outlet />
      </div>
    </div>
  )
}
