/**
 * src/api/menuApi.js
 * Menu CRUD API calls. Admin write operations included.
 */
import axiosInstance from './axiosInstance'

// ── Public ────────────────────────────────────────────────────────────────
export const fetchMenuItems = (params = {}) =>
  axiosInstance.get('/menu/', { params })

export const fetchMenuItem = (id) =>
  axiosInstance.get(`/menu/${id}`)

// ── Admin ─────────────────────────────────────────────────────────────────
export const createMenuItem = (data) =>
  axiosInstance.post('/menu/', data)

export const updateMenuItem = (id, data) =>
  axiosInstance.put(`/menu/${id}`, data)

export const deleteMenuItem = (id) =>
  axiosInstance.delete(`/menu/${id}`)

export const uploadMenuImage = (id, formData) =>
  axiosInstance.post(`/menu/${id}/image`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })