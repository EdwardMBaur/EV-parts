import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const STORAGE_KEY = 'evparts_cart'

export const useCartStore = defineStore('cart', () => {
  const items = ref(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'))

  const count = computed(() => items.value.reduce((sum, i) => sum + i.quantidade, 0))
  const subtotal = computed(() =>
    items.value.reduce((sum, i) => sum + Number(i.preco) * i.quantidade, 0),
  )
  const isEmpty = computed(() => items.value.length === 0)

  function persist() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items.value))
  }

  function quantidadeNoCarrinho(idPeca) {
    return items.value.find((i) => i.id_peca === idPeca)?.quantidade || 0
  }

  function addItem(peca, quantidade = 1) {
    const estoque = peca.estoque ?? 99
    const existing = items.value.find((i) => i.id_peca === peca.id_peca)
    const atual = existing?.quantidade || 0

    if (atual + quantidade > estoque) {
      return { ok: false, reason: 'estoque' }
    }

    if (existing) {
      existing.quantidade += quantidade
      existing.estoque = estoque
    } else {
      items.value.push({
        id_peca: peca.id_peca,
        nome_peca: peca.nome_peca,
        preco: Number(peca.preco),
        url_imagem: peca.url_imagem || null,
        nome_categoria: peca.nome_categoria || null,
        estoque,
        quantidade,
      })
    }
    persist()
    return { ok: true }
  }

  function updateQuantity(idPeca, quantidade) {
    const item = items.value.find((i) => i.id_peca === idPeca)
    if (!item) return
    item.quantidade = Math.min(Math.max(1, quantidade), item.estoque ?? 99)
    persist()
  }

  function removeItem(idPeca) {
    items.value = items.value.filter((i) => i.id_peca !== idPeca)
    persist()
  }

  function clear() {
    items.value = []
    persist()
  }

  return {
    items,
    count,
    subtotal,
    isEmpty,
    addItem,
    updateQuantity,
    removeItem,
    clear,
    quantidadeNoCarrinho,
  }
})
