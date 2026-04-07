import { useEffect } from 'react'
import QRCode from 'react-qr-code'

export default function UpiModal({ open, onClose, upiId = 'demo@upi', amount = 0, onSuccess, autoConfirmMs = 0 }) {
  useEffect(() => {
    if (!open) return
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open])

  useEffect(() => {
    if (!open || !autoConfirmMs) return
    const t = setTimeout(() => {
      onSuccess && onSuccess()
    }, autoConfirmMs)
    return () => clearTimeout(t)
  }, [open, autoConfirmMs])

  if (!open) return null

  const qrValue = `upi://pay?pa=${encodeURIComponent(upiId)}&pn=Coolspark&am=${amount}`

  return (
    <div className="fixed inset-0 z-60 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="relative w-full max-w-md bg-coal-800 rounded-xl p-6 z-70">
        <h3 className="text-white font-bold text-lg mb-2">Pay with UPI</h3>
        <p className="text-gray-400 text-sm mb-4">Scan this QR or use the UPI ID below</p>

        <div className="flex flex-col items-center gap-3">
          <div className="bg-white p-4 rounded-lg">
            <QRCode value={qrValue} size={160} />
          </div>
          <div className="text-center">
            <div className="text-gray-300 font-medium">UPI ID</div>
            <div className="text-white font-semibold">{upiId}</div>
            <div className="text-gray-400 text-sm">Amount: ₹{amount}</div>
          </div>
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
