/**
 * src/App.jsx
 * Root application component.
 * Sets up React Router, Context providers, Toaster, Navbar, CartSidebar,
 * and all page routes including protected and admin routes.
 */
import { useState } from 'react'
import { BrowserRouter, useNavigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import ErrorBoundary from './components/ErrorBoundary'

// Providers
import { AuthProvider } from './context/AuthContext'
import { CartProvider } from './context/CartContext'

// Layout components
import Navbar from './components/Navbar'
import CartSidebar from './components/CartSidebar'
import AppRoutes from './routes'


function AppContent() {
  const [cartOpen, setCartOpen] = useState(false)
  const navigate = useNavigate()

  return (
    <div className="bg-coal-900 min-h-screen">
      <Navbar onCartOpen={() => setCartOpen(true)} />
      <CartSidebar
        isOpen={cartOpen}
        onClose={() => setCartOpen(false)}
        onCheckout={() => navigate('/checkout')}
      />

      <AppRoutes />

      {/* Global toast notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          className: 'toast-dark',
          duration: 3500,
          style: {
            background: '#1e1e1e',
            color: '#f5f5f5',
            border: '1px solid rgba(255,107,0,0.2)',
            fontFamily: 'Poppins, sans-serif',
            fontSize: '14px',
          },
          success: {
            iconTheme: { primary: '#ff6b00', secondary: '#fff' },
          },
        }}
      />
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <ErrorBoundary>
            <AppContent />
          </ErrorBoundary>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}