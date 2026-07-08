<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { ClipboardList, Truck, PackageCheck } from 'lucide-vue-next'
import AccountLayout from '@/layouts/AccountLayout.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { orderStatus } from '@/utils/orderStatus'
import { formatCurrency, formatDate } from '@/utils/format'
import { pedidoService } from '@/services/pedidoService'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const pedidos = ref([])
const loading = ref(true)

const stats = computed(() => {
  const total = pedidos.value.length
  const emTransito = pedidos.value.filter((p) => ['enviado', 'em_separacao'].includes(p.status_pedido)).length
  const entregues = pedidos.value.filter((p) => p.status_pedido === 'entregue').length
  return [
    { label: 'Pedidos', value: total, icon: ClipboardList },
    { label: 'Em trânsito', value: emTransito, icon: Truck },
    { label: 'Entregues', value: entregues, icon: PackageCheck },
  ]
})

const recentes = computed(() => pedidos.value.slice(0, 3))

onMounted(async () => {
  await auth.fetchUser()
  try {
    pedidos.value = await pedidoService.listar()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <AccountLayout :title="`Olá, ${auth.user?.nome_razao_social?.split(' ')[0] || 'cliente'}`">
    <LoadingSpinner v-if="loading" />
    <div v-else class="space-y-6">
      <div class="grid grid-cols-3 gap-4">
        <div v-for="stat in stats" :key="stat.label" class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="flex items-center gap-2 text-ink-500">
            <component :is="stat.icon" class="size-4" />
            <span class="text-xs">{{ stat.label }}</span>
          </div>
          <p class="mt-2 text-2xl font-bold text-ink-900">{{ stat.value }}</p>
        </div>
      </div>

      <section class="rounded-xl border border-slate-200 bg-white p-5">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-base font-bold text-ink-900">Pedidos recentes</h2>
          <RouterLink to="/painel/pedidos" class="text-sm font-medium text-electric-600 hover:underline">
            Ver todos
          </RouterLink>
        </div>
        <p v-if="!recentes.length" class="py-6 text-center text-sm text-ink-500">
          Você ainda não fez nenhum pedido.
        </p>
        <ul v-else class="divide-y divide-slate-100">
          <li v-for="pedido in recentes" :key="pedido.id_pedido">
            <RouterLink
              :to="{ name: 'pedido-detalhe', params: { id: pedido.id_pedido } }"
              class="flex items-center justify-between py-3 hover:opacity-80"
            >
              <div>
                <p class="text-sm font-semibold text-ink-900">Pedido #{{ pedido.id_pedido }}</p>
                <p class="text-xs text-ink-500">{{ formatDate(pedido.data_pedido) }}</p>
              </div>
              <div class="flex items-center gap-3">
                <span class="rounded-full px-2.5 py-1 text-xs font-medium" :class="orderStatus(pedido.status_pedido).tint">
                  {{ orderStatus(pedido.status_pedido).label }}
                </span>
                <span class="text-sm font-bold text-ink-900">{{ formatCurrency(pedido.valor_total) }}</span>
              </div>
            </RouterLink>
          </li>
        </ul>
      </section>
    </div>
  </AccountLayout>
</template>
