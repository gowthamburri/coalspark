import axiosInstance from './axiosInstance'

export const validateCoupon = (payload) => axiosInstance.post('/coupons/validate', payload)
export const getCoupons = () => axiosInstance.get('/coupons')
export const createCoupon = (payload) => axiosInstance.post('/coupons', payload)
export const updateCoupon = (couponId, payload) => axiosInstance.patch(`/coupons/${couponId}`, payload)
export const deleteCoupon = (couponId) => axiosInstance.delete(`/coupons/${couponId}`)

