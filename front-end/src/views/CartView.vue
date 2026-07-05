<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { Minus, Plus, Trash2, ShoppingBag } from '@lucide/vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import PartThumb from '@/components/catalog/PartThumb.vue'
import { useCartStore } from '@/stores/cart'
import { formatCurrency } from '@/utils/format'

const router = useRouter()
const cart = useCartStore()

function goCheckout() {
  router.push('/checkout')
}
</script>

<template>
  <DefaultLayout show-search>
    <div class="mx-auto max-w-4xl px-4 py-8 sm:px-6">
      <h1 class="mb-6 text-2xl font-bold text-ink-900">Seu carrinho</h1>

      <EmptyState
        v-if="cart.isEmpty"
        :icon="ShoppingBag"
        title="Seu carrinho está vazio"
        description="Explore o catálogo e adicione peças compatíveis com seu veículo."
      >
        <RouterLink to="/pecas">
          <BaseButton variant="primary" size="md">Buscar peças</BaseButton>
        </RouterLink>
      </EmptyState>

      <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_320px]">
        <div class="space-y-3">
          <div
            v-for="item in cart.items"
            :key="item.id_peca"
            class="flex gap-4 rounded-xl border border-slate-200 bg-white p-4"
          >
            <div class="flex size-20 shrink-0 items-center justify-center rounded-lg bg-surface-card">
              <PartThumb :categoria="item.nome_categoria" />
            </div>
            <div class="flex flex-1 flex-col">
              <RouterLink
                :to="{ name: 'peca-detalhe', params: { id: item.id_peca } }"
                class="text-sm font-semibold text-ink-900 hover:text-electric-600"
              >
                {{ item.nome_peca }}
              </RouterLink>
              <p v-if="item.nome_categoria" class="text-xs text-ink-500">{{ item.nome_categoria }}</p>

              <div class="mt-auto flex items-center justify-between pt-2">
                <div class="flex items-center rounded-lg border border-slate-300">
                  <button
                    class="flex size-8 items-center justify-center text-ink-600 hover:bg-slate-50 disabled:opacity-40"
                    :disabled="item.quantidade <= 1"
                    @click="cart.updateQuantity(item.id_peca, item.quantidade - 1)"
                  >
                    <Minus class="size-4" />
                  </button>
                  <span class="w-9 text-center text-sm font-medium">{{ item.quantidade }}</span>
                  <button
                    class="flex size-8 items-center justify-center text-ink-600 hover:bg-slate-50"
                    @click="cart.updateQuantity(item.id_peca, item.quantidade + 1)"
                  >
                    <Plus class="size-4" />
                  </button>
                </div>
                <p class="text-sm font-bold text-electric-600">
                  {{ formatCurrency(item.preco * item.quantidade) }}
                </p>
              </div>
            </div>
            <button
              class="self-start text-ink-400 hover:text-rose-500"
              aria-label="Remover"
              @click="cart.removeItem(item.id_peca)"
            >
              <Trash2 class="size-5" />
            </button>
          </div>
        </div>

        <aside class="h-fit rounded-xl border border-slate-200 bg-surface p-5">
          <h2 class="mb-4 text-base font-bold text-ink-900">Resumo</h2>
          <div class="flex justify-between text-sm text-ink-700">
            <span>Subtotal ({{ cart.count }} itens)</span>
            <span class="font-semibold">{{ formatCurrency(cart.subtotal) }}</span>
          </div>
          <p class="mt-1 text-xs text-ink-400">Frete calculado na próxima etapa</p>
          <BaseButton variant="primary" size="lg" block class="mt-5" @click="goCheckout">
            Finalizar compra
          </BaseButton>
          <RouterLink to="/pecas" class="mt-3 block text-center text-sm text-electric-600 hover:underline">
            Continuar comprando
          </RouterLink>
        </aside>
      </div>
    </div>
  </DefaultLayout>
</template>
