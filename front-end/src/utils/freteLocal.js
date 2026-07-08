const STORAGE_KEY = 'evparts_fretes'

function readAll() {
  return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')
}

export function saveFreteLocal(idPedido, frete) {
  const all = readAll()
  all[idPedido] = { valor: Number(frete.valor), nome: frete.nome, codigo: frete.codigo }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(all))
}

export function getFreteLocal(idPedido) {
  return readAll()[idPedido] || null
}

export function freteEfetivo(pedido) {
  const doBackend = Number(pedido.valor_frete) || 0
  if (doBackend > 0) return doBackend
  return getFreteLocal(pedido.id_pedido)?.valor || 0
}

export function totalEfetivo(pedido) {
  return Number(pedido.valor_total) + freteEfetivo(pedido)
}
