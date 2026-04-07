/**
 * src/context/AuthContext.jsx
 * Global authentication state — user, token, login, logout.
 * Persists to localStorage and rehydrates on page load.
 */
import { createContext, useState, useEffect, useCallback } from 'react'
import { loginUser, registerUser } from '../api/authApi'

export const AuthContext = createContext(null)

const TOKEN_KEY = 'cs_token'
const USER_KEY  = 'cs_user'

export function AuthProvider({ children }) {
  const [user, setUser]   = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)

  // ── Rehydrate from localStorage on mount ─────────────────────────────────
  useEffect(() => {
    const savedToken = localStorage.getItem(TOKEN_KEY)
    const savedUser  = localStorage.getItem(USER_KEY)
    if (savedToken && savedUser) {
      try {
        setToken(savedToken)
        setUser(JSON.parse(savedUser))
      } catch {
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(USER_KEY)
      }
    }
    setLoading(false)
  }, [])

  // ── Persist to localStorage whenever token/user changes ──────────────────
  const persistSession = useCallback((tokenVal, userVal) => {
    localStorage.setItem(TOKEN_KEY, tokenVal)
    localStorage.setItem(USER_KEY, JSON.stringify(userVal))
    setToken(tokenVal)
    setUser(userVal)
  }, [])

  // ── Login ─────────────────────────────────────────────────────────────────
  const login = useCallback(async (email, password) => {
    const res = await loginUser({ email, password })
    persistSession(res.data.access_token, res.data.user)
    return res.data.user
  }, [persistSession])

  // ── Register ──────────────────────────────────────────────────────────────
  const register = useCallback(async (formData) => {
    const res = await registerUser(formData)
    persistSession(res.data.access_token, res.data.user)
    return res.data.user
  }, [persistSession])

  // ── Logout ────────────────────────────────────────────────────────────────
  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    setToken(null)
    setUser(null)
  }, [])

  const isAdmin = user?.role === 'admin'
  const isAuthenticated = !!token && !!user

  return (
    <AuthContext.Provider value={{
      user,
      token,
      loading,
      isAuthenticated,
      isAdmin,
      login,
      register,
      logout,
    }}>
      {children}
    </AuthContext.Provider>
  )
}