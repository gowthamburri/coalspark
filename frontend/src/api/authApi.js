/**
 * src/api/authApi.js
 * Authentication API calls: register, login, get current user.
 */
import axiosInstance from './axiosInstance'

export const registerUser = (data) =>
  axiosInstance.post('/auth/register', data)

export const loginUser = (data) =>
  axiosInstance.post('/auth/login', data)

export const getMe = () =>
  axiosInstance.get('/auth/me')