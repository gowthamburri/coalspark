/**
 * src/components/Navbar.jsx
 * Top navigation bar with CoalSpark branding, links, cart badge, auth menu.
 * Collapses to mobile hamburger on small screens.
 */
import { useState } from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { ShoppingCart, Menu, X, Flame, LogOut, User, LayoutDashboard } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { useCart } from '../hooks/useCart'

export default function Navbar({ onCartOpen }) {
  const { isAuthenticated, isAdmin, user, logout } = useAuth()
  const { totalItems } = useCart()
  const navigate = useNavigate()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    setUserMenuOpen(false)
    navigate('/')
  }

  const navLinks = [
    { to: '/',      label: 'Home'   },
    { to: '/menu',  label: 'Menu'   },
    { to: '/orders', label: 'Orders' },
  ]

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-coal-900/95 backdrop-blur-md border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">

          {/* ── Logo ──────────────────────────────────────────────────── */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 bg-ember-500 rounded-lg flex items-center justify-center
                            group-hover:shadow-ember transition-shadow duration-300">
              <Flame className="w-5 h-5 text-white" strokeWidth={2.5} />
            </div>
            <div className="leading-tight">
              <span className="text-white font-bold text-lg tracking-tight">CoalSpark</span>
              <span className="hidden sm:block text-ember-500 text-[10px] font-medium -mt-1 tracking-widest uppercase">
                Where Fire Meets Flavour
              </span>
            </div>
          </Link>

          {/* ── Desktop nav links ──────────────────────────────────────── */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.to === '/'}
                className={({ isActive }) =>
                  `px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'text-ember-500 bg-ember-500/10'
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </div>

          {/* ── Right side actions ────────────────────────────────────── */}
          <div className="flex items-center gap-3">
            {/* Cart button */}
            <button
              onClick={onCartOpen}
              className="relative p-2 rounded-lg text-gray-400 hover:text-white
                         hover:bg-white/5 transition-all duration-200"
              aria-label="Open cart"
            >
              <ShoppingCart className="w-5 h-5" />
              {totalItems > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-ember-500 text-white
                                 text-[10px] font-bold rounded-full flex items-center justify-center
                                 animate-pulse-ember">
                  {totalItems > 99 ? '99+' : totalItems}
                </span>
              )}
            </button>

            {/* Auth section */}
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setUserMenuOpen((p) => !p)}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg
                             bg-ash-100 hover:bg-ash-200 transition-colors duration-200"
                >
                  <div className="w-7 h-7 bg-ember-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-xs font-bold">
                      {user?.full_name?.[0]?.toUpperCase() ?? 'U'}
                    </span>
                  </div>
                  <span className="hidden sm:block text-sm text-gray-300 max-w-[100px] truncate">
                    {user?.full_name?.split(' ')[0]}
                  </span>
                </button>

                {/* User dropdown */}
                {userMenuOpen && (
                  <div className="absolute right-0 mt-2 w-52 bg-ash-100 border border-white/10
                                  rounded-xl shadow-card overflow-hidden animate-fade-in z-50">
                    <div className="px-4 py-3 border-b border-white/5">
                      <p className="text-white text-sm font-medium truncate">{user?.full_name}</p>
                      <p className="text-gray-500 text-xs truncate">{user?.email}</p>
                    </div>
                    {isAdmin && (
                      <Link
                        to="/admin"
                        onClick={() => setUserMenuOpen(false)}
                        className="flex items-center gap-3 px-4 py-3 text-sm text-gray-300
                                   hover:text-white hover:bg-white/5 transition-colors"
                      >
                        <LayoutDashboard className="w-4 h-4 text-ember-500" />
                        Admin Dashboard
                      </Link>
                    )}
                    <Link
                      to="/orders"
                      onClick={() => setUserMenuOpen(false)}
                      className="flex items-center gap-3 px-4 py-3 text-sm text-gray-300
                                 hover:text-white hover:bg-white/5 transition-colors"
                    >
                      <User className="w-4 h-4" />
                      My Orders
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-4 py-3 text-sm
                                 text-red-400 hover:text-red-300 hover:bg-red-500/10
                                 transition-colors border-t border-white/5"
                    >
                      <LogOut className="w-4 h-4" />
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="hidden md:flex items-center gap-2">
                <Link to="/login" className="btn-ghost text-sm py-2">Sign In</Link>
                <Link to="/register" className="btn-primary text-sm py-2 px-4">Join Now</Link>
              </div>
            )}

            {/* Mobile hamburger */}
            <button
              onClick={() => setMobileOpen((p) => !p)}
              className="md:hidden p-2 rounded-lg text-gray-400 hover:text-white
                         hover:bg-white/5 transition-colors"
            >
              {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* ── Mobile menu ───────────────────────────────────────────────── */}
        {mobileOpen && (
          <div className="md:hidden border-t border-white/5 py-4 animate-fade-in">
            {navLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.to === '/'}
                onClick={() => setMobileOpen(false)}
                className={({ isActive }) =>
                  `block px-4 py-3 rounded-lg text-sm font-medium mb-1 transition-colors ${
                    isActive
                      ? 'text-ember-500 bg-ember-500/10'
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
            {!isAuthenticated && (
              <div className="flex gap-2 mt-4 pt-4 border-t border-white/5">
                <Link to="/login" onClick={() => setMobileOpen(false)}
                      className="flex-1 btn-outline text-center text-sm py-2">
                  Sign In
                </Link>
                <Link to="/register" onClick={() => setMobileOpen(false)}
                      className="flex-1 btn-primary text-center text-sm py-2">
                  Join Now
                </Link>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Click-outside overlay for user menu */}
      {userMenuOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setUserMenuOpen(false)}
        />
      )}
    </nav>
  )
}