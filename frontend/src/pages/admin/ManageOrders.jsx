/**
 * src/pages/admin/ManageOrders.jsx
 * Admin orders management — list all orders, update status.
 */
import { useEffect, useState } from 'react'
import { RefreshCw } from 'lucide-react'
import toast from 'react-hot-toast'
import { getAllOrders, updateOrderStatus } from '../../api/adminApi'
import { formatCurrency, formatDate } from '../../utils/formatCurrency'

const STATUSES = ['pending','confirmed','preparing','ready','delivered','cancelled']
const STATUS_COLORS = {
  pending:   'text-yellow-400 bg-yellow-400/10',
  confirmed: 'text-blue-400 bg-blue-400/10',
  preparing: 'text-orange-400 bg-orange-400/10',
  ready:     'text-green-400 bg-green-400/10',
  delivered: 'text-emerald-400 bg-emerald-400/10',
  cancelled: 'text-red-400 bg-red-400/10',
}

export default function ManageOrders() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [updating, setUpdating] = useState(null)

  const load = async () => {
    setLoading(true)
    try {
      const res = await getAllOrders()
      setOrders(res.data)
    } catch { toast.error('Failed to load orders') }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  const handleStatusChange = async (orderId, status) => {
    setUpdating(orderId)
    try {
      await updateOrderStatus(orderId, status)
      setOrders((prev) => prev.map((o) => o.id === orderId ? { ...o, status } : o))
      toast.success(`Order #${orderId} → ${status}`)
    } catch { toast.error('Status update failed') }
    finally { setUpdating(null) }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Manage Orders</h1>
          <p className="text-gray-500 text-sm mt-1">{orders.length} orders total</p>
        </div>
        <button onClick={load} disabled={loading}
                className="btn-ghost flex items-center gap-2 text-sm">
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => <div key={i} className="skeleton h-20 rounded-xl" />)}
        </div>
      ) : orders.length === 0 ? (
        <div className="text-center py-24 text-gray-500">No orders yet.</div>
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="border-b border-white/5">
                <tr className="text-gray-500 text-left">
                  <th className="px-5 py-3 font-medium">Order</th>
                  <th className="px-5 py-3 font-medium">Customer</th>
                  <th className="px-5 py-3 font-medium">Items</th>
                  <th className="px-5 py-3 font-medium">Total</th>
                  <th className="px-5 py-3 font-medium">Date</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id} className="border-b border-white/5 hover:bg-white/2 transition-colors">
                    <td className="px-5 py-4 text-ember-500 font-bold">#{order.id}</td>
                    <td className="px-5 py-4 text-gray-300">User #{order.user_id}</td>
                    <td className="px-5 py-4 text-gray-400">
                      {order.order_items?.length ?? 0} item(s)
                    </td>
                    <td className="px-5 py-4 text-white font-semibold">
                      {formatCurrency(order.total_amount)}
                    </td>
                    <td className="px-5 py-4 text-gray-500 text-xs">
                      {formatDate(order.created_at)}
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-2">
                        <span className={`badge ${STATUS_COLORS[order.status]}`}>
                          {order.status}
                        </span>
                        {updating === order.id ? (
                          <div className="w-4 h-4 border-2 border-ember-500 border-t-transparent rounded-full animate-spin" />
                        ) : (
                          <select
                            value={order.status}
                            onChange={(e) => handleStatusChange(order.id, e.target.value)}
                            className="bg-ash-100 border border-white/10 text-gray-400 text-xs
                                       rounded-lg px-2 py-1 outline-none focus:border-ember-500"
                          >
                            {STATUSES.map((s) => (
                              <option key={s} value={s}>{s}</option>
                            ))}
                          </select>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}