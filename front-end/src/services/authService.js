import http from './http'

export const authService = {
  cadastro(payload) {
    return http.post('/auth/cadastro', payload).then((r) => r.data)
  },
  login(payload) {
    return http.post('/auth/login', payload).then((r) => r.data)
  },
  me() {
    return http.get('/usuarios/me').then((r) => r.data)
  },
  updateMe(payload) {
    return http.put('/usuarios/me', payload).then((r) => r.data)
  },
}
