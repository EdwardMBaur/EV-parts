<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { ArrowLeft, Truck } from 'lucide-vue-next'
import AccountLayout from '@/layouts/AccountLayout.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import PartThumb from '@/components/catalog/PartThumb.vue'
import { orderStatus } from '@/utils/orderStatus'
import { formatCurrency, formatDate } from '@/utils/format'
import { pedidoService } from '@/services/pedidoService'
import { useToast } from '@/composables/useToast'
import { extractError } from '@/services/http'

const route = useRoute()
const toast = useToast()
const pedido = ref(null)
const loading = ref(true)
const notFound = ref(false)

onMounted(async () => {
  try {
    pedido.value = await pedidoService.detalhe(Number(route.params.id))
  } catch (error) {
    if (error?.response?.status === 404) notFound.value = true
    else toast.error(extractError(error))
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <AccountLayout>
    <LoadingSpinner v-if="loading" />
    <EmptyState v-else-if="notFound || !pedido" title="Pedido não encontrado" />

    <div v-else class="space-y-5">
      <RouterLink to="/painel/pedidos" class="inline-flex items-center gap-1.5 text-sm font-medium text-ink-500 hover:text-ink-700">
        <ArrowLeft class="size-4" /> Voltar aos pedidos
      </RouterLink>

      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 class="text-xl font-bold text-ink-900">Pedido #{{ pedido.id_pedido }}</h1>
          <p class="text-sm text-ink-500">Realizado em {{ formatDate(pedido.data_pedido) }}</p>
        </div>
        <span class="rounded-full px-3 py-1 text-sm font-medium" :class="orderStatus(pedido.status_pedido).tint">
          {{ orderStatus(pedido.status_pedido).label }}
        </span>
      </div>

      <section
        v-if="pedido.codigo_rastreio || pedido.prazo_entrega"
        class="rounded-xl border border-slate-200 bg-white p-5"
      >
        <h2 class="mb-3 flex items-center gap-2 text-base font-bold text-ink-900">
          <Truck class="size-5 text-electric-600" /> Rastreamento
        </h2>
        <div class="space-y-1.5 text-sm text-ink-700">
          <p v-if="pedido.codigo_rastreio">
            Código de rastreio: <span class="font-semibold">{{ pedido.codigo_rastreio }}</span>
          </p>
          <p v-if="pedido.transportadora">Transportadora: {{ pedido.transportadora }}</p>
          <p v-if="pedido.modal_frete">Modalidade: {{ pedido.modal_frete }}</p>
          <p v-if="pedido.prazo_entrega">Previsão de entrega: {{ formatDate(pedido.prazo_entrega) }}</p>
        </div>
      </section>

      <section class="rounded-xl border border-slate-200 bg-white p-5">
        <h2 class="mb-4 text-base font-bold text-ink-900">Itens</h2>
        <ul class="divide-y divide-slate-100">
          <li v-for="item in pedido.itens" :key="item.id_peca" class="flex items-center gap-4 py-3">
            <div class="flex size-14 shrink-0 items-center justify-center rounded-lg bg-surface-card">
              <PartThumb />
            </div>
            <div class="flex-1">
              <p class="text-sm font-semibold text-ink-900">{{ item.nome_peca }}</p>
              <p class="text-xs text-ink-500">Quantidade: {{ item.quantidade }}</p>
            </div>
            <p class="text-sm font-bold text-ink-900">
              {{ formatCurrency(item.preco_unitario * item.quantidade) }}
            </p>
          </li>
        </ul>
      </section>

      <section class="rounded-xl border border-slate-200 bg-surface p-5">
        <div class="space-y-2 text-sm">
          <div class="flex justify-between text-ink-700">
            <span>Subtotal</span><span>{{ formatCurrency(pedido.valor_total) }}</span>
          </div>
          <div class="flex justify-between text-ink-700">
            <span>Frete</span><span>{{ formatCurrency(pedido.valor_frete) }}</span>
          </div>
          <hr class="border-slate-200" />
          <div class="flex justify-between text-base font-bold">
            <span class="text-ink-900">Total</span>
            <span class="text-electric-600">
              {{ formatCurrency(Number(pedido.valor_total) + Number(pedido.valor_frete)) }}
            </span>
          </div>
        </div>
      </section>
    </div>
  </AccountLayout>
</template>
