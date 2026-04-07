/**
 * src/pages/Orders.jsx
 * Authenticated user's order history page.
 */
import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { Package } from 'lucide-react'
import toast from 'react-hot-toast'
import { getMyOrders } from '../api/orderApi'
import OrderSummary from '../components/OrderSummary'
import ReviewModal from '../components/ReviewModal'
import { createReview, getMyReviews } from '../api/reviewApi'

export default function Orders() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [myReviews, setMyReviews] = useState([])
  const [reviewOpen, setReviewOpen] = useState(false)
  const [reviewOrderId, setReviewOrderId] = useState(null)
  const [reviewItem, setReviewItem] = useState(null)
  const [submittingReview, setSubmittingReview] = useState(false)

  useEffect(() => {
    const loadOrders = async (silent = false) => {
      if (!silent) setLoading(true)
      try {
        const res = await getMyOrders()
        setOrders(res.data)
        const rev = await getMyReviews()
        setMyReviews(rev.data)
      } catch (err) {
        if (!silent) toast.error('Failed to load orders')
      } finally {
        if (!silent) setLoading(false)
      }
    }

    loadOrders()
    const iv = setInterval(() => loadOrders(true), 8000)
    return () => clearInterval(iv)
  }, [])

  const reviewedKeys = useMemo(() => new Set(myReviews.map((r) => `${r.order_id}:${r.menu_item_id}`)), [myReviews])

  const openReview = (orderId, item) => {
    setReviewOrderId(orderId)
    setReviewItem(item)
    setReviewOpen(true)
  }

  const handleSubmitReview = async (payload) => {
    setSubmittingReview(true)
    try {
      await createReview(payload)
      toast.success('Thanks for your review!')
      const rev = await getMyReviews()
      setMyReviews(rev.data)
      setReviewOpen(false)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to submit review')
    } finally {
      setSubmittingReview(false)
    }
  }

  return (
    <div className="min-h-screen pt-24 pb-16 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="mb-8">
          <h1 className="section-title">My Orders</h1>
          <p className="section-subtitle">Track your past and current orders</p>
        </div>

        {loading ? (
          <div className="space-y-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="skeleton h-48 rounded-2xl" />
            ))}
          </div>
        ) : orders.length === 0 ? (
          <div className="text-center py-24 space-y-4">
            <div className="w-20 h-20 bg-ash-100 rounded-full flex items-center justify-center mx-auto">
              <Package className="w-10 h-10 text-gray-600" />
            </div>
            <h3 className="text-white font-semibold text-xl">No orders yet</h3>
            <p className="text-gray-500">Your order history will appear here.</p>
            <Link to="/menu" className="btn-primary inline-block px-8 py-3">
              Start Ordering
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {orders.map((order) => {
              const canReview = order.status === 'delivered'
              return (
                <div key={order.id} className="space-y-3">
                  <OrderSummary order={order} />

                  {canReview && (
                    <div className="card p-4">
                      <p className="text-sm text-gray-300 font-medium mb-3">Rate items from this order</p>
                      <div className="flex flex-col gap-2">
                        {(order.order_items || []).map((it) => {
                          const key = `${order.id}:${it.menu_item_id}`
                          const already = reviewedKeys.has(key)
                          return (
                            <div key={key} className="flex items-center justify-between gap-3 bg-ash-200 border border-white/5 rounded-xl p-3">
                              <div className="min-w-0">
                                <p className="text-white text-sm font-medium truncate">{it.menu_item?.name || 'Item'}</p>
                                <p className="text-gray-500 text-xs">Qty {it.quantity}</p>
                              </div>
                              <button
                                disabled={already}
                                onClick={() => openReview(order.id, it)}
                                className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
                                  already ? 'bg-white/5 text-gray-600 cursor-not-allowed' : 'bg-ember-500/20 text-ember-500 hover:bg-ember-500/30'
                                }`}
                              >
                                {already ? 'Reviewed' : 'Write Review'}
                              </button>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>

      <ReviewModal
        open={reviewOpen}
        onClose={() => setReviewOpen(false)}
        orderId={reviewOrderId}
        item={reviewItem}
        onSubmit={handleSubmitReview}
        submitting={submittingReview}
      />
    </div>
  )
}