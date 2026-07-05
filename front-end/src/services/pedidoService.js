import http from './http'

export const pedidoService = {
  criar(payload) {
    return http.post('/pedidos/', payload).then((r) => r.data)
  },
  listar() {
    return http.get('/pedidos/').then((r) => r.data)
  },
  detalhe(id) {
    return http.get(`/pedidos/${id}`).then((r) => r.data)
  },
}

export const pagamentoService = {
  iniciar(payload) {
    return http.post('/pagamentos/', payload).then((r) => r.data)
  },
  detalhe(idPedido) {
    return http.get(`/pagamentos/${idPedido}`).then((r) => r.data)
  },
}
