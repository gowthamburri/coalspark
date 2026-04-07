import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { useCart } from '../hooks/useCart'
import { useAuth } from '../hooks/useAuth'
import { placeOrder } from '../api/orderApi'
import { createPayment, verifyPayment } from '../api/paymentApi'
import loadRazorpay from '../utils/razorpay'
import { formatCurrency } from '../utils/formatCurrency'
import UpiModal from '../components/UpiModal'
import DemoPaymentModal from '../components/DemoPaymentModal'
import { getErrorMessage } from '../utils/error'

function Checkout() {
  const { items, totalPrice, clearCart } = useCart()
  const { isAuthenticated, user } = useAuth()
  const navigate = useNavigate()

  const [paymentMethod, setPaymentMethod] = useState('upi')
  const [processing, setProcessing] = useState(false)
  const [upiOpen, setUpiOpen] = useState(false)
  const [cardDemoOpen, setCardDemoOpen] = useState(false)

  const taxes = totalPrice * 0.05
  const grandTotal = Math.round((totalPrice + taxes) * 100) / 100

  if (items.length === 0) return (
    <div className="min-h-screen pt-20 flex flex-col items-center justify-center gap-6 px-4">
      <h2 className="text-white font-semibold">Your cart is empty</h2>
      <button className="btn-primary" onClick={() => navigate('/menu')}>Browse Menu</button>
    </div>
  )
  const handlePayment = async () => {
    if (processing) return
    if (!isAuthenticated) {
      toast.error('Please login to continue')
      navigate('/login')
      return
    }

    setProcessing(true)

    const payload = {
      items: items.map((i) => ({ menu_item_id: i.id, quantity: i.quantity })),
      delivery_address: null,
      special_instructions: null,
      payment_method: paymentMethod,
    }

    try {
      if (paymentMethod === 'cod') {
        await placeOrder(payload)
        clearCart()
        toast.success('Order placed — Cash on Delivery')
        navigate('/orders')
        return
      }

      // Online payment flow (card or upi) using Razorpay
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
              razorpay_signature: response.razorpay_signature,
            })
            if (verifyRes.data.success) {
              clearCart()
              toast.success('Payment successful — order placed!')
              navigate('/orders')
            } else {
              toast.error(verifyRes.data.message || 'Payment verification failed')
            }
            } catch (err) {
              toast.error(getErrorMessage(err) || 'Verification failed')
            } finally {
            setProcessing(false)
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
        setProcessing(false)
        toast.error('Payment failed. Please try again.')
      })
      rzp.open()
    } catch (err) {
      console.error(err)
      toast.error(getErrorMessage(err) || 'Payment failed')
    } finally {
      setProcessing(false)
    }
  }

  // UPI and Card demo modals are kept as fallbacks but real Razorpay flow is used above.

  const handleUpiSuccess = async (response) => {
    setUpiOpen(false)
    setProcessing(true)
    try {
      // If modal returns a Razorpay-like response, verify it; otherwise place order directly
      if (response?.razorpay_order_id && response?.razorpay_payment_id && response?.razorpay_signature) {
        const verifyRes = await verifyPayment({
          razorpay_order_id: response.razorpay_order_id,
          razorpay_payment_id: response.razorpay_payment_id,
          razorpay_signature: response.razorpay_signature,
        })
        if (!verifyRes.data.success) throw new Error(verifyRes.data.message || 'Verification failed')
      } else {
        // Fallback: create order as paid (demo UPI flow)
        await placeOrder({
          items: items.map((i) => ({ menu_item_id: i.id, quantity: i.quantity })),
          delivery_address: null,
          special_instructions: null,
          payment_method: 'upi',
        })
      }

      clearCart()
      toast.success('Payment confirmed — Order placed')
      navigate('/orders')
    } finally {
      setProcessing(false)
    }
  }

  const handleCardDemoSuccess = async (response) => {
    setCardDemoOpen(false)
    setProcessing(true)
    try {
      if (response?.razorpay_order_id && response?.razorpay_payment_id && response?.razorpay_signature) {
        const verifyRes = await verifyPayment({
          razorpay_order_id: response.razorpay_order_id,
          razorpay_payment_id: response.razorpay_payment_id,
          razorpay_signature: response.razorpay_signature,
        })
        if (!verifyRes.data.success) throw new Error(verifyRes.data.message || 'Verification failed')
      } else {
        await placeOrder({
          items: items.map((i) => ({ menu_item_id: i.id, quantity: i.quantity })),
          delivery_address: null,
          special_instructions: null,
          payment_method: 'card',
        })
      }

      clearCart()
      toast.success('Card payment confirmed — Order placed')
      navigate('/orders')
    } catch (err) {
      console.error(err)
      toast.error(getErrorMessage(err) || err.message || 'Failed to place order after payment')
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="min-h-screen pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="section-title">Checkout</h1>

        <div className="grid lg:grid-cols-[1fr_360px] gap-8">
          <div className="card p-6">
            <h2 className="text-white font-bold mb-4">Select Payment Method</h2>
            <div className="grid grid-cols-3 gap-3">
              {['upi', 'card', 'cod'].map((m) => (
                <button
                  key={m}
                  onClick={() => setPaymentMethod(m)}
                  className={`py-3 rounded-xl text-sm font-semibold capitalize border transition-all ${
                    paymentMethod === m
                      ? 'bg-ember-500/20 border-ember-500 text-ember-500'
                      : 'bg-ash-100 border-white/10 text-gray-400 hover:border-white/20'
                  }`}
                >
                  {m === 'cod' ? 'Cash on Delivery' : m === 'card' ? 'Card' : 'UPI'}
                </button>
              ))}
            </div>

            <div className="mt-6">
              <h3 className="text-gray-400 text-sm">Order Summary</h3>
              <div className="mt-3 space-y-2">
                {items.map((item) => (
                  <div key={item.id} className="flex justify-between text-sm">
                    <span className="text-gray-400">{item.name} ×{item.quantity}</span>
                    <span className="text-gray-300">{formatCurrency(item.price * item.quantity)}</span>
                  </div>
                ))}
              </div>
              <div className="ember-divider my-4" />
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Subtotal</span>
                <span className="text-gray-300">{formatCurrency(totalPrice)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Taxes (5%)</span>
                <span className="text-gray-300">{formatCurrency(taxes)}</span>
              </div>
              <div className="flex justify-between font-bold text-base mt-3">
                <span className="text-white">Total</span>
                <span className="text-ember-500 text-lg">{formatCurrency(grandTotal)}</span>
              </div>
            </div>

            <button
              onClick={handlePayment}
              disabled={processing}
              className="btn-primary mt-6 w-full py-4"
            >
              {processing ? 'Processing…' : paymentMethod === 'cod' ? 'Place Order (COD)' : 'Pay Now'}
            </button>
          </div>

          <div className="card p-6">
            <h2 className="text-white font-bold mb-4">Delivery & Notes</h2>
            <p className="text-gray-400 text-sm">Delivery details are collected at checkout on the app. For this demo, we use a minimal flow.</p>
          </div>
        </div>
      </div>
      <UpiModal
        open={upiOpen}
        onClose={() => setUpiOpen(false)}
        upiId={import.meta.env.VITE_DEMO_UPI || 'demo@upi'}
        amount={grandTotal}
        onSuccess={handleUpiSuccess}
        autoConfirmMs={8000}
      />
      <DemoPaymentModal
        open={cardDemoOpen}
        onClose={() => setCardDemoOpen(false)}
        amount={grandTotal}
        onSuccess={handleCardDemoSuccess}
      />
    </div>
  )
}

export default Checkout
