import { useMemo, useState } from 'react'
import { Star, X } from 'lucide-react'

export default function ReviewModal({ open, onClose, orderId, item, onSubmit, submitting }) {
  const [rating, setRating] = useState(5)
  const [title, setTitle] = useState('')
  const [comment, setComment] = useState('')

  const itemName = useMemo(() => item?.menu_item?.name || item?.name || 'Item', [item])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4">
      <div className="w-full max-w-lg bg-coal-900 border border-white/10 rounded-2xl p-6 animate-slide-up">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h2 className="text-white font-bold text-xl">Rate your item</h2>
            <p className="text-gray-500 text-sm mt-1">
              Order #{String(orderId).padStart(4, '0')} • {itemName}
            </p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="mb-5">
          <p className="text-gray-400 text-sm mb-2">Your rating</p>
          <div className="flex items-center gap-2">
            {Array.from({ length: 5 }).map((_, i) => {
              const value = i + 1
              const active = value <= rating
              return (
                <button
                  key={value}
                  onClick={() => setRating(value)}
                  className={`w-10 h-10 rounded-xl flex items-center justify-center border transition-colors ${
                    active ? 'bg-ember-500/15 border-ember-500 text-ember-500' : 'bg-ash-100 border-white/10 text-gray-600'
                  }`}
                >
                  <Star className="w-5 h-5" fill={active ? 'currentColor' : 'none'} />
                </button>
              )
            })}
          </div>
        </div>

        <div className="space-y-3">
          <div>
            <label className="text-gray-400 text-sm mb-1 block">Title (optional)</label>
            <input value={title} onChange={(e) => setTitle(e.target.value)} className="input-field" placeholder="e.g. Super tasty" />
          </div>
          <div>
            <label className="text-gray-400 text-sm mb-1 block">Review (optional)</label>
            <textarea value={comment} onChange={(e) => setComment(e.target.value)} rows={4} className="input-field resize-none" placeholder="Tell us what you liked…" />
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button type="button" onClick={onClose} className="btn-ghost flex-1">Cancel</button>
          <button
            type="button"
            disabled={submitting}
            onClick={() => onSubmit?.({ order_id: orderId, menu_item_id: item?.menu_item_id ?? item?.menu_item?.id, rating, title: title || null, comment: comment || null })}
            className="btn-primary flex-1"
          >
            {submitting ? 'Submitting…' : 'Submit Review'}
          </button>
        </div>
      </div>
    </div>
  )
}

