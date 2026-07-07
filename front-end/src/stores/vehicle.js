import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const STORAGE_KEY = 'evparts_vehicle'

export const useVehicleStore = defineStore('vehicle', () => {
  const context = ref(JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'))

  const label = computed(() => {
    if (!context.value) return ''
    const { montadora, modelo, ano, vin, versao_software } = context.value
    const base = [montadora, modelo, ano].filter(Boolean).join(' ') || vin || ''
    if (!base) return ''
    return versao_software ? `${base} (SW v${versao_software})` : base
  })
  const hasContext = computed(() => Boolean(label.value))

  function setContext(payload) {
    context.value = payload
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
  }

  function clear() {
    context.value = null
    localStorage.removeItem(STORAGE_KEY)
  }

  return { context, hasContext, label, setContext, clear }
})
