/**
 * src/components/OrderSummary.jsx
 * Displays a single order's details — items, status badge, total, date.
 * Used on the Orders page and potentially in other contexts.
 */
import { Package, Clock, CheckCircle, XCircle, ChefHat, MapPin } from 'lucide-react'
import { formatCurrency } from '../utils/formatCurrency'
import { formatDate } from '../utils/formatCurrency'
import OrderTracker from './OrderTracker'

const STATUS_CONFIG = {
  pending:   { label: 'Pending',    icon: Clock,        color: 'text-yellow-400', bg: 'bg-yellow-400/10', border: 'border-yellow-400/20' },
  confirmed: { label: 'Confirmed',  icon: CheckCircle,  color: 'text-blue-400',   bg: 'bg-blue-400/10',   border: 'border-blue-400/20' },
  preparing: { label: 'Preparing',  icon: ChefHat,      color: 'text-orange-400', bg: 'bg-orange-400/10', border: 'border-orange-400/20' },
  ready:     { label: 'Ready',      icon: CheckCircle,  color: 'text-green-400',  bg: 'bg-green-400/10',  border: 'border-green-400/20' },
  delivered: { label: 'Delivered',  icon: CheckCircle,  color: 'text-emerald-400',bg: 'bg-emerald-400/10',border: 'border-emerald-400/20' },
  cancelled: { label: 'Cancelled',  icon: XCircle,      color: 'text-red-400',    bg: 'bg-red-400/10',    border: 'border-red-400/20' },
}

const PLACEHOLDER = 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=100&q=60'

export default function OrderSummary({ order }) {
  const statusConfig = STATUS_CONFIG[order.status] || STATUS_CONFIG.pending
  const StatusIcon = statusConfig.icon

  const items = order.order_items || order.items || []
  const subtotal = items.reduce((sum, item) => sum + Number(item.subtotal || 0), 0)

  return (
    <div className="card p-5 animate-slide-up">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 ${statusConfig.bg} rounded-xl flex items-center justify-center`}>
            <StatusIcon className={`w-5 h-5 ${statusConfig.color}`} />
          </div>
          <div>
            <h3 className="text-white font-bold text-base">
              Order #{order.id.toString().padStart(4, '0')}
            </h3>
            <p className="text-gray-500 text-xs">{formatDate(order.created_at)}</p>
          </div>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${statusConfig.border} ${statusConfig.color} bg-opacity-10`}>
          {statusConfig.label}
        </span>
      </div>
      <OrderTracker status={order.status} />

      {/* Order items */}
      <div className="space-y-3 mb-4">
        {items.map((item) => (
          <div key={item.id} className="flex gap-3">
            <div className="w-14 h-14 rounded-lg overflow-hidden bg-ash-200 flex-shrink-0">
              <img
                src={item.menu_item?.image_url || PLACEHOLDER}
                alt={item.menu_item?.name || 'Item'}
                className="w-full h-full object-cover"
                onError={(e) => { e.target.src = PLACEHOLDER }}
              />
            </div>
            <div className="flex-1 min-w-0">
              <h4 className="text-white font-medium text-sm truncate">
                {item.menu_item?.name || 'Unknown Item'}
              </h4>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-gray-500 text-xs">Qty: {item.quantity}</span>
                <span className="text-ember-500 font-semibold text-sm">
                  {formatCurrency(item.subtotal ?? (item.menu_item?.price || 0) * item.quantity)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Delivery info */}
      {order.delivery_address && (
        <div className="flex items-start gap-2 p-3 bg-ash-200 rounded-lg border border-white/5 mb-4">
          <MapPin className="w-4 h-4 text-ember-500 flex-shrink-0 mt-0.5" />
          <p className="text-gray-400 text-sm">{order.delivery_address}</p>
        </div>
      )}

      {/* Totals */}
      <div className="space-y-2 pt-4 border-t border-white/5">
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Subtotal</span>
          <span className="text-gray-300">{formatCurrency(subtotal)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Delivery</span>
          <span className="text-green-400 text-xs font-medium">Free</span>
        </div>
        <div className="ember-divider my-2" />
        <div className="flex justify-between font-bold text-base">
          <span className="text-white">Total</span>
          <span className="text-ember-500 text-lg">{formatCurrency(order.total_amount)}</span>
        </div>
      </div>

      {/* Special instructions */}
      {order.special_instructions && (
        <div className="mt-4 p-3 bg-ash-200 rounded-lg border border-white/5">
          <p className="text-gray-500 text-xs mb-1">Special Instructions:</p>
          <p className="text-gray-400 text-sm">{order.special_instructions}</p>
        </div>
      )}

      {/* Payment method */}
      <div className="mt-4 flex items-center gap-2">
        <Package className="w-4 h-4 text-gray-500" />
        <span className="text-gray-500 text-xs capitalize">
          Payment: {order.payment_method === 'upi' ? 'UPI' : order.payment_method}
        </span>
      </div>
    </div>
  )
}