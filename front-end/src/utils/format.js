const brl = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

export function formatCurrency(value) {
  const number = Number(value)
  if (Number.isNaN(number)) return 'R$ 0,00'
  return brl.format(number)
}

export function formatCurrencyShort(value) {
  const number = Number(value)
  if (Number.isNaN(number)) return 'R$ 0'
  return `R$ ${new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 0 }).format(number)}`
}

export function formatInstallments(value, times = 12) {
  const parcela = Number(value) / times
  return `ou ${times}× de ${formatCurrency(parcela)} sem juros`
}

export function formatCep(cep) {
  const digits = String(cep || '').replace(/\D/g, '')
  if (digits.length !== 8) return cep
  return `${digits.slice(0, 5)}-${digits.slice(5)}`
}

export function formatDate(value) {
  if (!value) return '—'
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'medium' }).format(new Date(value))
}
