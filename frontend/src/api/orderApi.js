/**
 * src/api/orderApi.js
 * Order placement and retrieval API calls.
 */
import axiosInstance from './axiosInstance'

export const placeOrder = (data) =>
  axiosInstance.post('/orders/', data)

export const getMyOrders = () =>
  axiosInstance.get('/orders/me')

export const getOrderById = (id) =>
  axiosInstance.get(`/orders/${id}`)