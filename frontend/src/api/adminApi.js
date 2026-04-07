/**
 * src/api/adminApi.js
 * Admin-specific API calls: dashboard, orders management, users.
 */
import axiosInstance from './axiosInstance'

export const getDashboardStats = () =>
  axiosInstance.get('/admin/dashboard')

export const getAllOrders = () =>
  axiosInstance.get('/admin/orders')

export const updateOrderStatus = (id, status) =>
  axiosInstance.patch(`/admin/orders/${id}/status`, { status })

export const getAllUsers = () =>
  axiosInstance.get('/admin/users')

export const toggleUserActive = (id) =>
  axiosInstance.patch(`/admin/users/${id}/toggle`)

export const getRestaurant = () =>
  axiosInstance.get('/restaurant/')

export const updateRestaurant = (data) =>
  axiosInstance.put('/restaurant/', data)