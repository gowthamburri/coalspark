/**
 * src/pages/Cart.jsx
 * Full cart / checkout page — shows items, delivery address form, order summary,
 * and handles order placement via the API.
 */
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ShoppingBag, Minus, Plus, Trash2, MapPin, FileText, ArrowRight } from 'lucide-react'
import toast from 'react-hot-toast'
import { getErrorMessage } from '../utils/error'
import { useCart } from '../hooks/useCart'
import { useAuth } from '../hooks/useAuth'
import { placeOrder } from '../api/orderApi'
import { createPayment, verifyPayment } from '../api/paymentApi'
import loadRazorpay from '../utils/razorpay'
import { validateCoupon } from '../api/couponApi'
import { formatCurrency } from '../utils/formatCurrency'
import CouponInput from '../components/CouponInput'

const PLACEHOLDER = 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=100&q=60'

export default function Cart() {
  const { items, totalItems, totalPrice, addItem, removeItem, deleteItem, clearCart, MAX_ITEM_QTY } = useCart()
  const { isAuthenticated, user } = useAuth()
  const navigate = useNavigate()

  const [address, setAddress] = useState('')
  const [instructions, setInstructions] = useState('')
  const [paymentMethod, setPaymentMethod] = useState('cash')
  const [placing, setPlacing] = useState(false)
  const [couponCode, setCouponCode] = useState('')
  const [discountAmount, setDiscountAmount] = useState(0)
  const [validatingCoupon, setValidatingCoupon] = useState(false)

  const taxes = totalPrice * 0.05
  const grandTotal = totalPrice + taxes - discountAmount

  const handleApplyCoupon = async (code) => {
    if (!code?.trim()) return
    setValidatingCoupon(true)
    try {
      const res = await validateCoupon({ code, subtotal: totalPrice + taxes })
      if (!res.data.is_valid) {
        toast.error(res.data.message || 'Invalid coupon')
        return
      }
      setCouponCode(code)
      setDiscountAmount(res.data.amount || 0)
      toast.success(res.data.message || 'Coupon applied')
    } catch (err) {
      const msg = getErrorMessage(err) || 'Failed to validate coupon'
      toast.error(msg)
    } finally {
      setValidatingCoupon(false)
    }
  }

  const handlePlaceOrder = async () => {
    if (items.length === 0) return

    setPlacing(true)
    try {
      const itemsPayload = items.map((i) => ({ menu_item_id: i.id, quantity: i.quantity }))

      // Cash flow: existing API creates order immediately
      if (paymentMethod === 'cash') {
        const payload = {
          items: itemsPayload,
          delivery_address: address || null,
          special_instructions: instructions || null,
          payment_method: paymentMethod,
          coupon_code: couponCode || null,
        }
        await placeOrder(payload)
        clearCart()
        toast.success('🔥 Order placed successfully!')
        navigate('/orders')
        return
      }

      // Online payment flow using Razorpay
      const amount = Number((grandTotal).toFixed(2))
      const createRes = await createPayment({ amount })
      const { order_id, amount: amountPaise, currency, key_id } = createRes.data

      const ok = await loadRazorpay()
      if (!ok) throw new Error('Failed to load Razorpay SDK')

      const options = {
        key: key_id,
        amount: amountPaise,
        currency,
        name: 'CoalSpark',
        description: 'Order Payment',
        order_id,
        handler: async function (response) {
          try {
            const verifyRes = await verifyPayment({
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
              amount,
            })
            if (verifyRes.data.success) {
              clearCart()
              toast.success('Payment successful — order placed!')
              navigate('/orders')
            } else {
              toast.error(verifyRes.data.message || 'Payment verification failed')
            }
          } catch (err) {
            toast.error(getErrorMessage(err) || err.message || 'Verification failed')
          } finally {
            setPlacing(false)
          }
        },
        prefill: {
          name: (isAuthenticated && user?.full_name) || undefined,
          email: (isAuthenticated && user?.email) || undefined,
        },
        theme: { color: '#ff4500' },
      }

      const rzp = new window.Razorpay(options)
      rzp.on('payment.failed', function (resp) {
        setPlacing(false)
        toast.error('Payment failed. Please try again.')
      })
      rzp.open()
    } catch (err) {
      const msg = getErrorMessage(err) || err.message || 'Failed to place order. Please try again.'
      toast.error(msg)
      setPlacing(false)
    }
  }

  if (items.length === 0) {
    return (
      <div className="min-h-screen pt-20 flex flex-col items-center justify-center gap-6 px-4">
        <div className="w-24 h-24 bg-ash-100 rounded-full flex items-center justify-center">
          <ShoppingBag className="w-12 h-12 text-gray-600" />
        </div>
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-2">Your cart is empty</h2>
          <p className="text-gray-500">Looks like you haven't added anything yet.</p>
        </div>
        <Link to="/menu" className="btn-primary px-8 py-3">
          Browse Menu
        </Link>
      </div>
    )
  }

  return (
    <div className="min-h-screen pt-24 pb-16 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="section-title mb-8">Checkout</h1>

        <div className="grid lg:grid-cols-[1fr_400px] gap-8">
          {/* ── Left: Cart items + delivery form ─────────────────────── */}
          <div className="space-y-6">

            {/* Cart items */}
            <div className="card p-6">
              <div className="flex items-center justify-between mb-5">
                <h2 className="text-white font-bold text-lg">
                  Order Items ({totalItems})
                </h2>
                <button
                  onClick={clearCart}
                  className="text-red-400 hover:text-red-300 text-xs flex items-center gap-1 transition-colors"
                >
                  <Trash2 className="w-3.5 h-3.5" /> Clear all
                </button>
              </div>

              <div className="space-y-4">
                {items.map((item) => (
                  <div key={item.id} className="flex gap-4 pb-4 border-b border-white/5 last:border-0 last:pb-0">
                    <div className="w-16 h-16 rounded-xl overflow-hidden bg-ash-200 flex-shrink-0">
                      <img
                        src={item.image_url || PLACEHOLDER}
                        alt={item.name}
                        className="w-full h-full object-cover"
                        onError={(e) => { e.target.src = PLACEHOLDER }}
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between items-start">
                        <div>
                          <h4 className="text-white font-medium text-sm truncate max-w-[200px]">
                            {item.name}
                          </h4>
                          <p className="text-ember-500 font-semibold text-sm mt-0.5">
                            {formatCurrency(item.price)}
                          </p>
                        </div>
                        <button
                          onClick={() => deleteItem(item.id)}
                          className="text-red-500 hover:text-red-400 transition-colors p-1 ml-2"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                      <div className="flex items-center justify-between mt-3">
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => removeItem(item.id)}
                            className="w-7 h-7 rounded-lg bg-ash-200 hover:bg-ash-100 text-white
                                       flex items-center justify-center transition-colors"
                          >
                            <Minus className="w-3.5 h-3.5" />
                          </button>
                          <span className="text-white font-bold text-sm w-5 text-center">
                            {item.quantity}
                          </span>
                          <button
                          onClick={() => {
                            if (item.quantity >= MAX_ITEM_QTY) {
                              toast.error(`Maximum ${MAX_ITEM_QTY} quantity per item`)
                              return
                            }
                            addItem(item)
                          }}
                            className="w-7 h-7 rounded-lg bg-ember-500 hover:bg-ember-600 text-white
                                       flex items-center justify-center transition-colors"
                          >
                            <Plus className="w-3.5 h-3.5" />
                          </button>
                        </div>
                        <span className="text-gray-300 font-semibold text-sm">
                          {formatCurrency(item.price * item.quantity)}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Delivery details */}
            <div className="card p-6 space-y-4">
              <h2 className="text-white font-bold text-lg flex items-center gap-2">
                <MapPin className="w-5 h-5 text-ember-500" />
                Delivery Details
              </h2>
              <div>
                <label className="text-gray-400 text-sm mb-2 block">Delivery Address</label>
                <textarea
                  rows={3}
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Enter your full delivery address…"
                  className="input-field resize-none"
                />
              </div>
              <div>
                <label className="text-gray-400 text-sm mb-2 block flex items-center gap-1">
                  <FileText className="w-3.5 h-3.5" /> Special Instructions (optional)
                </label>
                <textarea
                  rows={2}
                  value={instructions}
                  onChange={(e) => setInstructions(e.target.value)}
                  placeholder="Allergies, preferences, extra spice…"
                  className="input-field resize-none"
                />
              </div>
            </div>

            {/* Payment method */}
            <div className="card p-6">
              <h2 className="text-white font-bold text-lg mb-4">Payment Method</h2>
              <div className="grid grid-cols-3 gap-3">
                {['cash', 'card', 'upi'].map((method) => (
                  <button
                    key={method}
                    onClick={() => setPaymentMethod(method)}
                    className={`py-3 rounded-xl text-sm font-semibold capitalize border transition-all ${
                      paymentMethod === method
                        ? 'bg-ember-500/20 border-ember-500 text-ember-500'
                        : 'bg-ash-100 border-white/10 text-gray-400 hover:border-white/20'
                    }`}
                  >
                    {method === 'upi' ? 'UPI' : method.charAt(0).toUpperCase() + method.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            <CouponInput
              onApply={handleApplyCoupon}
              appliedCoupon={couponCode}
              discountAmount={discountAmount}
              loading={validatingCoupon}
            />
          </div>

          {/* ── Right: Order summary ──────────────────────────────────── */}
          <div className="lg:sticky lg:top-24 h-fit">
            <div className="card p-6">
              <h2 className="text-white font-bold text-lg mb-5">Order Summary</h2>

              <div className="space-y-3 mb-5">
                {items.map((item) => (
                  <div key={item.id} className="flex justify-between text-sm">
                    <span className="text-gray-400 truncate max-w-[200px]">
                      {item.name} <span className="text-gray-600">×{item.quantity}</span>
                    </span>
                    <span className="text-gray-300 ml-2 flex-shrink-0">
                      {formatCurrency(item.price * item.quantity)}
                    </span>
                  </div>
                ))}
              </div>

              <div className="ember-divider mb-4" />

              <div className="space-y-2 mb-5">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Subtotal</span>
                  <span className="text-gray-300">{formatCurrency(totalPrice)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Taxes (5%)</span>
                  <span className="text-gray-300">{formatCurrency(taxes)}</span>
                </div>
                {discountAmount > 0 && (
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Coupon ({couponCode})</span>
                    <span className="text-green-400">- {formatCurrency(discountAmount)}</span>
                  </div>
                )}
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Delivery</span>
                  <span className="text-green-400 text-xs font-medium">Free</span>
                </div>
              </div>

              <div className="ember-divider mb-5" />

              <div className="flex justify-between font-bold text-base mb-6">
                <span className="text-white">Grand Total</span>
                <span className="text-ember-500 text-xl">{formatCurrency(grandTotal)}</span>
              </div>

              {!isAuthenticated ? (
                <div className="space-y-3">
                  <p className="text-gray-400 text-sm text-center">
                    Please sign in to place your order
                  </p>
                  <Link to="/login" className="btn-primary w-full text-center block py-3">
                    Sign In to Order
                  </Link>
                </div>
              ) : (
                <button
                  onClick={handlePlaceOrder}
                  disabled={placing || validatingCoupon}
                  className="btn-primary w-full py-4 flex items-center justify-center gap-2 text-base"
                >
                  {placing ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Placing Order…
                    </>
                  ) : (
                    <>
                      Place Order <ArrowRight className="w-5 h-5" />
                    </>
                  )}
                </button>
              )}

              <Link to="/menu" className="block text-center text-gray-500 hover:text-gray-300
                                          text-sm mt-4 transition-colors">
                ← Continue Shopping
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}