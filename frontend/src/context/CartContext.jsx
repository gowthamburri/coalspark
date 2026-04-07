/**
 * src/context/CartContext.jsx
 * Global cart state — items, quantities, add/remove/clear, total calculation.
 * Persists to localStorage so cart survives browser restarts.
 */
import { createContext, useState, useEffect, useCallback } from 'react'

export const CartContext = createContext(null)

const CART_KEY = 'cs_cart'
const MAX_ITEM_QTY = 20

function normalizeCart(rawItems) {
  if (!Array.isArray(rawItems)) return []
  return rawItems
    .filter((item) => item && Number.isFinite(Number(item.id)) && Number.isFinite(Number(item.price)))
    .map((item) => ({
      ...item,
      id: Number(item.id),
      price: Number(item.price),
      quantity: Math.min(MAX_ITEM_QTY, Math.max(1, Number(item.quantity) || 1)),
    }))
}

export function CartProvider({ children }) {
  const [items, setItems] = useState([])

  // ── Rehydrate cart from localStorage ───────────────────────────────────
  useEffect(() => {
    try {
      const saved = localStorage.getItem(CART_KEY)
      if (saved) setItems(normalizeCart(JSON.parse(saved)))
    } catch {
      localStorage.removeItem(CART_KEY)
    }
  }, [])

  // ── Sync cart to localStorage on every change ──────────────────────────
  useEffect(() => {
    localStorage.setItem(CART_KEY, JSON.stringify(items))
  }, [items])

  // ── Add item (or increment quantity) ─────────────────────────────────────
  const addItem = useCallback((menuItem) => {
    setItems((prev) => {
      const existing = prev.find((i) => i.id === menuItem.id)
      if (existing) {
        return prev.map((i) =>
          i.id === menuItem.id ? { ...i, quantity: Math.min(MAX_ITEM_QTY, i.quantity + 1) } : i
        )
      }
      return [...prev, { ...menuItem, quantity: 1, price: Number(menuItem.price) }]
    })
  }, [])

  // ── Remove item (or decrement quantity) ──────────────────────────────────
  const removeItem = useCallback((menuItemId) => {
    setItems((prev) => {
      const existing = prev.find((i) => i.id === menuItemId)
      if (!existing) return prev
      if (existing.quantity === 1) {
        return prev.filter((i) => i.id !== menuItemId)
      }
      return prev.map((i) =>
        i.id === menuItemId ? { ...i, quantity: i.quantity - 1 } : i
      )
    })
  }, [])

  // ── Delete item entirely ──────────────────────────────────────────────────
  const deleteItem = useCallback((menuItemId) => {
    setItems((prev) => prev.filter((i) => i.id !== menuItemId))
  }, [])

  // ── Clear entire cart ─────────────────────────────────────────────────────
  const clearCart = useCallback(() => {
    setItems([])
    localStorage.removeItem(CART_KEY)
  }, [])

  // ── Set quantity explicitly (clamped 1..MAX_ITEM_QTY) ────────────────────
  const setItemQuantity = useCallback((menuItemId, quantity) => {
    const nextQty = Math.min(MAX_ITEM_QTY, Math.max(1, Number(quantity) || 1))
    setItems((prev) => prev.map((item) => (
      item.id === menuItemId ? { ...item, quantity: nextQty } : item
    )))
  }, [])

  // ── Get quantity of a specific item ──────────────────────────────────────
  const getQuantity = useCallback(
    (menuItemId) => items.find((i) => i.id === menuItemId)?.quantity ?? 0,
    [items]
  )

  // ── Computed values ───────────────────────────────────────────────────────
  const totalItems = items.reduce((sum, i) => sum + i.quantity, 0)
  const totalPrice = items.reduce((sum, i) => sum + i.price * i.quantity, 0)

  return (
    <CartContext.Provider value={{
      items,
      totalItems,
      totalPrice,
      addItem,
      removeItem,
      deleteItem,
      clearCart,
      setItemQuantity,
      getQuantity,
      MAX_ITEM_QTY,
    }}>
      {children}
    </CartContext.Provider>
  )
}