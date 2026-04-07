import { Route, Routes } from 'react-router-dom'

import ProtectedRoute from '../components/ProtectedRoute'
import AdminRoute from '../components/AdminRoute'

import Home from '../pages/Home'
import Menu from '../pages/Menu'
import Cart from '../pages/Cart'
import Checkout from '../pages/Checkout'
import Orders from '../pages/Orders'
import Login from '../pages/Login'
import Register from '../pages/Register'

import AdminLayout from '../pages/admin/AdminLayout'
import AdminDashboard from '../pages/admin/AdminDashboard'
import ManageMenu from '../pages/admin/ManageMenu'
import ManageOrders from '../pages/admin/ManageOrders'
import ManageCoupons from '../pages/admin/ManageCoupons'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/menu" element={<Menu />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        path="/cart"
        element={(
          <ProtectedRoute>
            <Cart />
          </ProtectedRoute>
        )}
      />
      <Route
        path="/checkout"
        element={(
          <ProtectedRoute>
            <Checkout />
          </ProtectedRoute>
        )}
      />
      <Route
        path="/orders"
        element={(
          <ProtectedRoute>
            <Orders />
          </ProtectedRoute>
        )}
      />

      <Route
        path="/admin"
        element={(
          <AdminRoute>
            <AdminLayout />
          </AdminRoute>
        )}
      >
        <Route index element={<AdminDashboard />} />
        <Route path="menu" element={<ManageMenu />} />
        <Route path="orders" element={<ManageOrders />} />
        <Route path="coupons" element={<ManageCoupons />} />
      </Route>

      <Route
        path="*"
        element={(
          <div className="min-h-screen flex flex-col items-center justify-center gap-4 text-center px-4">
            <span className="text-6xl">🔥</span>
            <h1 className="text-4xl font-bold text-white">404</h1>
            <p className="text-gray-500">This page went up in flames.</p>
            <a href="/" className="btn-primary px-6 py-3">Back to Home</a>
          </div>
        )}
      />
    </Routes>
  )
}

