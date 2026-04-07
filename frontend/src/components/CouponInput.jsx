import { useState } from 'react'
import { Tag } from 'lucide-react'

export default function CouponInput({ onApply, appliedCoupon, discountAmount, loading }) {
  const [code, setCode] = useState('')

  return (
    <div className="card p-4">
      <p className="text-sm text-gray-300 mb-3 font-medium">Have a coupon?</p>
      <div className="flex gap-2">
        <div className="relative flex-1">
          <Tag className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            value={code}
            onChange={(e) => setCode(e.target.value.toUpperCase())}
            placeholder="Enter code (e.g. BBQ20)"
            className="input-field pl-9 py-2.5"
          />
        </div>
        <button
          onClick={() => onApply?.(code)}
          disabled={loading || !code.trim()}
          className="btn-outline px-4 py-2.5 text-sm"
        >
          {loading ? '...' : 'Apply'}
        </button>
      </div>

      {appliedCoupon && (
        <div className="mt-3 text-xs text-green-400">
          {appliedCoupon} applied. You saved Rs. {discountAmount.toFixed(2)}
        </div>
      )}
    </div>
  )
}

