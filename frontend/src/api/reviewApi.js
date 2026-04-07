import axiosInstance from './axiosInstance'

export const createReview = (payload) => axiosInstance.post('/reviews', payload)
export const getMyReviews = () => axiosInstance.get('/reviews/me')
export const getMenuItemReviews = (menuItemId) => axiosInstance.get(`/reviews/menu-item/${menuItemId}`)

