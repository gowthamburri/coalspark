/**
 * src/pages/admin/AdminDashboard.jsx
 * Admin home — stats cards, recent orders panel, quick links.
 */
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Users, ShoppingBag, IndianRupee, Clock, ChefHat, TrendingUp } from 'lucide-react'
import { getDashboardStats } from '../../api/adminApi'
import { formatCurrency } from '../../utils/formatCurrency'

const STAT_CARDS = [
  { key: 'total_users',      label: 'Total Customers', icon: Users,        color: 'text-blue-400',   bg: 'bg-blue-400/10'   },
  { key: 'total_orders',     label: 'Total Orders',    icon: ShoppingBag,  color: 'text-ember-500',  bg: 'bg-ember-500/10'  },
  { key: 'total_revenue',    label: 'Revenue',         icon: IndianRupee,  color: 'text-green-400',  bg: 'bg-green-400/10', currency: true },
  { key: 'pending_orders',   label: 'Pending Orders',  icon: Clock,        color: 'text-yellow-400', bg: 'bg-yellow-400/10' },
  { key: 'total_menu_items', label: 'Menu Items',      icon: ChefHat,      color: 'text-purple-400', bg: 'bg-purple-400/10' },
]

const STATUS_COLORS = {
  pending:   'text-yellow-400', confirmed: 'text-blue-400',
  preparing: 'text-orange-400', ready:     'text-green-400',
  delivered: 'text-emerald-400', cancelled: 'text-red-400',
}

export default function AdminDashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getDashboardStats()
      .then((res) => setStats(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-gray-500 text-sm mt-1">CoalSpark Restaurant — Admin Panel</p>
      </div>

      {/* ── Stat cards ──────────────────────────────────────────────── */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        {STAT_CARDS.map(({ key, label, icon: Icon, color, bg, currency }) => (
          <div key={key} className="card p-5">
            <div className={`w-10 h-10 ${bg} rounded-xl flex items-center justify-center mb-4`}>
              <Icon className={`w-5 h-5 ${color}`} />
            </div>
            {loading ? (
              <div className="skeleton h-7 w-20 rounded mb-1" />
            ) : (
              <p className={`text-2xl font-bold ${color}`}>
                {currency ? formatCurrency(stats?.[key] ?? 0) : (stats?.[key] ?? 0)}
              </p>
            )}
            <p className="text-gray-500 text-xs mt-1">{label}</p>
          </div>
        ))}
      </div>

      {/* ── Orders by status ─────────────────────────────────────────── */}
      {stats?.orders_by_status && (
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-5">
            <TrendingUp className="w-5 h-5 text-ember-500" />
            <h2 className="text-white font-bold">Orders by Status</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {Object.entries(stats.orders_by_status).map(([status, count]) => (
              <div key={status} className="text-center">
                <p className={`text-2xl font-bold ${STATUS_COLORS[status] || 'text-gray-400'}`}>
                  {count}
                </p>
                <p className="text-gray-500 text-xs capitalize mt-1">{status}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Quick actions ─────────────────────────────────────────────── */}
      <div className="grid sm:grid-cols-2 gap-4">
        <Link to="/admin/menu" className="card p-6 hover:border-ember-500/30 transition-all group">
          <ChefHat className="w-8 h-8 text-ember-500 mb-3" />
          <h3 className="text-white font-semibold mb-1">Manage Menu</h3>
          <p className="text-gray-500 text-sm">Add, edit, or remove menu items and upload food images.</p>
        </Link>
        <Link to="/admin/orders" className="card p-6 hover:border-ember-500/30 transition-all group">
          <ShoppingBag className="w-8 h-8 text-ember-500 mb-3" />
          <h3 className="text-white font-semibold mb-1">Manage Orders</h3>
          <p className="text-gray-500 text-sm">View all orders and update their status in real time.</p>
        </Link>
      </div>
    </div>
  )
}