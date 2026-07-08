<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { ClipboardList } from 'lucide-vue-next'
import AccountLayout from '@/layouts/AccountLayout.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { orderStatus } from '@/utils/orderStatus'
import { formatCurrency, formatDate } from '@/utils/format'
import { pedidoService } from '@/services/pedidoService'
import { useToast } from '@/composables/useToast'
import { extractError } from '@/services/http'

const toast = useToast()
const pedidos = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    pedidos.value = await pedidoService.listar()
  } catch (error) {
    toast.error(extractError(error))
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <AccountLayout title="Meus pedidos">
    <LoadingSpinner v-if="loading" />
    <EmptyState
      v-else-if="!pedidos.length"
      :icon="ClipboardList"
      title="Nenhum pedido ainda"
      description="Quando você concluir uma compra, ela aparecerá aqui."
    >
      <RouterLink to="/pecas">
        <BaseButton variant="primary" size="md">Buscar peças</BaseButton>
      </RouterLink>
    </EmptyState>

    <div v-else class="space-y-3">
      <RouterLink
        v-for="pedido in pedidos"
        :key="pedido.id_pedido"
        :to="{ name: 'pedido-detalhe', params: { id: pedido.id_pedido } }"
        class="block rounded-xl border border-slate-200 bg-white p-4 transition-shadow hover:shadow-md"
      >
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p class="text-sm font-semibold text-ink-900">Pedido #{{ pedido.id_pedido }}</p>
            <p class="text-xs text-ink-500">
              {{ formatDate(pedido.data_pedido) }} · {{ pedido.itens.length }} item(ns)
            </p>
          </div>
          <span class="rounded-full px-2.5 py-1 text-xs font-medium" :class="orderStatus(pedido.status_pedido).tint">
            {{ orderStatus(pedido.status_pedido).label }}
          </span>
          <p class="text-base font-bold text-electric-600">{{ formatCurrency(pedido.valor_total) }}</p>
        </div>
      </RouterLink>
    </div>
  </AccountLayout>
</template>
