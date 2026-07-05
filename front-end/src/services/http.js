import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('evparts_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('evparts_token')
      localStorage.removeItem('evparts_perfil')
    }
    return Promise.reject(error)
  },
)

export function extractError(error, fallback = 'Ocorreu um erro inesperado. Tente novamente.') {
  const detail = error?.response?.data?.detail
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg || d).join(' · ')
  }
  return detail || error?.message || fallback
}

export default http
