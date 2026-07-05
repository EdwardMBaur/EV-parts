import http from './http'

export const enderecoService = {
  listar() {
    return http.get('/enderecos/').then((r) => r.data)
  },
  criar(payload) {
    return http.post('/enderecos/', payload).then((r) => r.data)
  },
  atualizar(id, payload) {
    return http.put(`/enderecos/${id}`, payload).then((r) => r.data)
  },
  remover(id) {
    return http.delete(`/enderecos/${id}`).then((r) => r.data)
  },
}
