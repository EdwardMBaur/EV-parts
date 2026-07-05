import http from './http'

export const catalogService = {
  listarCategorias() {
    return http.get('/categorias/').then((r) => r.data)
  },
  listarPecas(params = {}) {
    return http.get('/pecas/', { params }).then((r) => r.data)
  },
  detalhePeca(id) {
    return http.get(`/pecas/${id}`).then((r) => r.data)
  },
  verificarCompatibilidade(payload) {
    return http.post('/pecas/compatibilidade/verificar', payload).then((r) => r.data)
  },
  listarVeiculos(params = {}) {
    return http.get('/veiculos/', { params }).then((r) => r.data)
  },
  listarMontadoras() {
    return http.get('/veiculos/montadoras').then((r) => r.data)
  },
}
