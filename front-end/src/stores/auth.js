import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/authService'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('evparts_token') || '')
  const perfil = ref(localStorage.getItem('evparts_perfil') || '')
  const user = ref(null)

  const isAuthenticated = computed(() => Boolean(token.value))

  function setSession(accessToken, tipoPerfil) {
    token.value = accessToken
    perfil.value = tipoPerfil || ''
    localStorage.setItem('evparts_token', accessToken)
    localStorage.setItem('evparts_perfil', perfil.value)
  }

  async function login(credentials) {
    const data = await authService.login(credentials)
    setSession(data.access_token, data.tipo_perfil)
    await fetchUser()
    return data
  }

  async function fetchUser() {
    if (!token.value) return null
    try {
      user.value = await authService.me()
    } catch {
      logout()
    }
    return user.value
  }

  function logout() {
    token.value = ''
    perfil.value = ''
    user.value = null
    localStorage.removeItem('evparts_token')
    localStorage.removeItem('evparts_perfil')
  }

  return { token, perfil, user, isAuthenticated, login, fetchUser, logout, setSession }
})
