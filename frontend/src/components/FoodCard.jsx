/**
 * src/components/FoodCard.jsx
 * Premium food item card with image, details, spice level, veg/non-veg badge,
 * and add/remove cart controls.
 */
import { Plus, Minus, Leaf, Flame } from 'lucide-react'
import { useCart } from '../hooks/useCart'
import { formatCurrency } from '../utils/formatCurrency'

const PLACEHOLDER = 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&q=80'

export default function FoodCard({ item }) {
  const { addItem, removeItem, getQuantity } = useCart()
  const qty = getQuantity(item.id)

  const spiceLevel = Math.min(5, Math.max(1, item.spice_level ?? 1))
  const rating = Number(item.avg_rating ?? item.rating ?? 0)

  return (
    <div className="card glow-on-hover flex flex-col overflow-hidden group animate-slide-up">
      {/* ── Image ──────────────────────────────────────────────────────── */}
      <div className="relative h-48 overflow-hidden bg-ash-200">
        <img
          src={item.image_url ? item.image_url : PLACEHOLDER}
          alt={item.name}
          className="w-full h-full object-cover transition-transform duration-500
                     group-hover:scale-110"
          onError={(e) => { e.target.src = PLACEHOLDER }}
        />
        {/* Veg / Non-veg badge */}
        <div className={`absolute top-3 left-3 flex items-center gap-1 px-2 py-1 rounded-md text-xs font-semibold
          ${item.is_vegetarian
            ? 'bg-green-900/80 text-green-400 border border-green-600/40'
            : 'bg-red-900/80 text-red-400 border border-red-600/40'
          }`}>
          <Leaf className="w-3 h-3" />
          {item.is_vegetarian ? 'Veg' : 'Non-Veg'}
        </div>

        {/* Featured badge */}
        {item.is_featured && (
          <div className="absolute top-3 right-3 bg-ember-500 text-white
                          text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
            Chef's Pick
          </div>
        )}
        {item.is_best_seller && (
          <div className="absolute top-10 right-3 bg-yellow-500/90 text-black
                          text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
            Best Seller
          </div>
        )}

        {/* Prep time */}
        <div className="absolute bottom-3 right-3 bg-black/70 backdrop-blur-sm
                        text-gray-300 text-xs px-2 py-0.5 rounded-full">
          ~{item.preparation_time} min
        </div>
      </div>

      {/* ── Content ────────────────────────────────────────────────────── */}
      <div className="flex flex-col flex-1 p-4">
        {/* Category tag */}
        <span className="text-ember-500 text-[11px] font-semibold uppercase tracking-wider mb-1">
          {item.category}
        </span>

        <h3 className="text-white font-semibold text-base leading-tight mb-1 line-clamp-1">
          {item.name}
        </h3>
        <div className="text-xs text-yellow-400 mb-2">{rating > 0 ? `★ ${rating.toFixed(1)}` : '★ New'}</div>

        {item.description && (
          <p className="text-gray-500 text-xs leading-relaxed mb-3 line-clamp-2">
            {item.description}
          </p>
        )}

        {/* Spice level */}
        <div className="flex items-center gap-1.5 mb-3">
          <Flame className="w-3.5 h-3.5 text-gray-600" />
          <div className="flex gap-0.5">
            {Array.from({ length: 5 }).map((_, i) => (
              <div
                key={i}
                className={`spice-dot ${
                  i < spiceLevel ? 'bg-ember-500' : 'bg-gray-700'
                }`}
              />
            ))}
          </div>
          <span className="text-gray-600 text-[10px]">Spice</span>
        </div>

        {/* ── Price + Cart controls ─────────────────────────────────── */}
        <div className="flex items-center justify-between mt-auto pt-3 border-t border-white/5">
          <span className="text-ember-500 font-bold text-lg">
            {formatCurrency(item.price)}
          </span>

          {qty === 0 ? (
            <button
              onClick={() => addItem(item)}
              className="flex items-center gap-1.5 bg-ember-500 hover:bg-ember-600
                         text-white text-sm font-semibold px-3 py-1.5 rounded-lg
                         transition-all duration-200 hover:shadow-ember active:scale-95"
            >
              <Plus className="w-4 h-4" />
              Add
            </button>
          ) : (
            <div className="flex items-center gap-2">
              <button
                onClick={() => removeItem(item.id)}
                className="w-7 h-7 flex items-center justify-center rounded-lg
                           bg-ash-200 hover:bg-ash-100 text-white transition-colors"
              >
                <Minus className="w-3.5 h-3.5" />
              </button>
              <span className="text-white font-bold text-sm w-5 text-center">{qty}</span>
              <button
                onClick={() => addItem(item)}
                className="w-7 h-7 flex items-center justify-center rounded-lg
                           bg-ember-500 hover:bg-ember-600 text-white transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}