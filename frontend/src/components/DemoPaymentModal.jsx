import { useEffect } from 'react'

export default function DemoPaymentModal({ open, onClose, amount = 0, onSuccess }) {
  useEffect(() => {
    if (!open) return
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-60 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="relative w-full max-w-md bg-coal-800 rounded-xl p-6 z-70">
        <h3 className="text-white font-bold text-lg mb-2">Card Payment (Demo)</h3>
        <p className="text-gray-400 text-sm mb-4">Use test card details below or click simulate to succeed.</p>

        <div className="space-y-3 mb-4">
          <div className="text-sm text-gray-300">
            <div>Card: <span className="text-white font-semibold">4111 1111 1111 1111</span></div>
            <div>Expiry: <span className="text-white font-semibold">12/30</span></div>
            <div>CVV: <span className="text-white font-semibold">123</span></div>
            <div className="mt-2">OTP: <span className="text-white font-semibold">1234</span></div>
          </div>
          <div className="text-gray-400 text-sm">Amount: <span className="text-white">₹{amount}</span></div>
        </div>

        <div className="mt-6 flex gap-3">
          <button
            onClick={onSuccess}
            className="btn-primary flex-1 py-3"
          >
            Simulate Payment Success
          </button>
          <button
            onClick={onClose}
            className="border border-white/10 text-gray-300 px-4 py-3 rounded-lg flex-1"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}
