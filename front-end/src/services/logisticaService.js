import http from './http'

export const logisticaService = {
  calcularFrete(payload) {
    return http.post('/logistica/frete', payload).then((r) => r.data)
  },
  fretePorPeca(idPeca, cepDestino) {
    return http
      .get(`/logistica/frete/peca/${idPeca}`, { params: { cep_destino: cepDestino } })
      .then((r) => r.data)
  },
  consultarCep(cep) {
    return http.get(`/enderecos/cep/${cep}`).then((r) => r.data)
  },
}
