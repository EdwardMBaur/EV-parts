const map = {
  aguardando_pagamento: { label: 'Aguardando pagamento', tint: 'bg-amber-100 text-amber-700' },
  pago: { label: 'Pago', tint: 'bg-emerald-accent/10 text-emerald-accent-dark' },
  em_separacao: { label: 'Em separação', tint: 'bg-electric-500/10 text-electric-700' },
  enviado: { label: 'Enviado', tint: 'bg-electric-500/10 text-electric-700' },
  entregue: { label: 'Entregue', tint: 'bg-emerald-accent/10 text-emerald-accent-dark' },
  cancelado: { label: 'Cancelado', tint: 'bg-rose-100 text-rose-600' },
  devolvido: { label: 'Devolvido', tint: 'bg-slate-100 text-ink-600' },
}

export function orderStatus(status) {
  return map[status] || { label: status, tint: 'bg-slate-100 text-ink-600' }
}
