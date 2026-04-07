/**
 * src/components/CartSidebar.jsx
 * Slide-out cart sidebar — shows items, subtotal, and checkout button.
 * Used on mobile/tablet or as an alternative to the full cart page.
 */
import { X, Minus, Plus, Trash2, ShoppingBag } from 'lucide-react'
import { useCart } from '../hooks/useCart'
import { formatCurrency } from '../utils/formatCurrency'

const PLACEHOLDER = 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=100&q=60'

export default function CartSidebar({ isOpen, onClose, onCheckout }) {
  const { items, totalItems, totalPrice, addItem, removeItem, deleteItem } = useCart()

  if (!isOpen) return null

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 animate-fade-in"
        onClick={onClose}
      />

      {/* Sidebar */}
      <div className="fixed top-0 right-0 h-full w-full max-w-md bg-ash-100 border-l border-white/10 shadow-2xl z-50 animate-slide-left">
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-5 border-b border-white/5">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 bg-ember-500 rounded-lg flex items-center justify-center">
                <ShoppingBag className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="text-white font-bold text-lg">Your Cart</h2>
                <p className="text-gray-500 text-xs">{totalItems} items</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Cart items */}
          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            {items.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center space-y-4">
                <div className="w-20 h-20 bg-ash-200 rounded-full flex items-center justify-center">
                  <ShoppingBag className="w-10 h-10 text-gray-600" />
                </div>
                <div>
                  <p className="text-white font-semibold text-lg">Your cart is empty</p>
                  <p className="text-gray-500 text-sm mt-1">Add some delicious items!</p>
                </div>
              </div>
            ) : (
              items.map((item) => (
                <div
                  key={item.id}
                  className="flex gap-3 p-3 bg-ash-200 rounded-xl border border-white/5"
                >
                  <div className="w-16 h-16 rounded-lg overflow-hidden bg-ash-200 flex-shrink-0">
                    <img
                      src={item.image_url || PLACEHOLDER}
                      alt={item.name}
                      className="w-full h-full object-cover"
                      onError={(e) => { e.target.src = PLACEHOLDER }}
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="text-white font-medium text-sm truncate pr-2">
                        {item.name}
                      </h4>
                      <button
                        onClick={() => deleteItem(item.id)}
                        className="text-red-500 hover:text-red-400 transition-colors flex-shrink-0"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => removeItem(item.id)}
                          className="w-6 h-6 rounded bg-ash-100 hover:bg-ash-200 text-white
                                     flex items-center justify-center transition-colors"
                        >
                          <Minus className="w-3 h-3" />
                        </button>
                        <span className="text-white font-bold text-xs w-4 text-center">
                          {item.quantity}
                        </span>
                        <button
                          onClick={() => addItem(item)}
                          className="w-6 h-6 rounded bg-ember-500 hover:bg-ember-600 text-white
                                     flex items-center justify-center transition-colors"
                        >
                          <Plus className="w-3 h-3" />
                        </button>
                      </div>
                      <span className="text-ember-500 font-bold text-sm">
                        {formatCurrency(item.price * item.quantity)}
                      </span>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          {items.length > 0 && (
            <div className="border-t border-white/5 p-5 space-y-4 bg-ash-100">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Subtotal</span>
                  <span className="text-gray-300">{formatCurrency(totalPrice)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Taxes (5%)</span>
                  <span className="text-gray-300">{formatCurrency(totalPrice * 0.05)}</span>
                </div>
                <div className="ember-divider my-2" />
                <div className="flex justify-between font-bold text-base">
                  <span className="text-white">Total</span>
                  <span className="text-ember-500 text-lg">
                    {formatCurrency(totalPrice * 1.05)}
                  </span>
                </div>
              </div>
              <button
                onClick={() => {
                  onClose()
                  onCheckout?.()
                }}
                className="btn-primary w-full py-3 text-base"
              >
                Proceed to Checkout
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  )
}