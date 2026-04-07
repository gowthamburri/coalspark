import axiosInstance from './axiosInstance'

export const createPayment = (data) =>
  axiosInstance.post('/payments/create-order', data)

export const verifyPayment = (data) =>
  axiosInstance.post('/payments/verify', data)
