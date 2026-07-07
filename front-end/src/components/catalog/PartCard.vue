<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ShoppingCart } from '@lucide/vue'
import CompatBadge from '@/components/ui/CompatBadge.vue'
import PartThumb from '@/components/catalog/PartThumb.vue'
import { formatCurrencyShort } from '@/utils/format'

const props = defineProps({
  peca: { type: Object, required: true },
})

const emit = defineEmits(['add'])
const router = useRouter()

const meta = computed(() => {
  const parts = []
  if (props.peca.fabricante) parts.push(props.peca.fabricante)
  if (props.peca.estado_saude_soh != null) parts.push(`SoH ${props.peca.estado_saude_soh}%`)
  return parts.join(' · ')
})

const semEstoque = computed(() => (props.peca.estoque ?? 0) <= 0)

function goToDetail() {
  router.push({ name: 'peca-detalhe', params: { id: props.peca.id_peca } })
}
</script>

<template>
  <article
    class="group flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white transition-shadow hover:shadow-md"
  >
    <button
      class="relative flex h-36 items-center justify-center bg-surface-card"
      @click="goToDetail"
    >
      <CompatBadge v-if="peca.compativel" class="absolute right-3 top-3" />
      <span
        v-if="semEstoque"
        class="absolute left-3 top-3 rounded-full bg-rose-100 px-2.5 py-1 text-xs font-semibold text-rose-600"
      >
        Esgotado
      </span>
      <PartThumb :categoria="peca.nome_categoria" size="lg" :class="semEstoque ? 'opacity-40' : ''" />
    </button>

    <div class="flex flex-1 flex-col gap-1 p-4">
      <button class="text-left" @click="goToDetail">
        <h3 class="line-clamp-2 text-sm font-semibold text-ink-900 hover:text-electric-600">
          {{ peca.nome_peca }}
        </h3>
      </button>
      <p v-if="meta" class="line-clamp-1 text-xs text-ink-500">{{ meta }}</p>

      <div class="mt-auto flex items-end justify-between pt-3">
        <p class="text-lg font-bold text-electric-600">{{ formatCurrencyShort(peca.preco) }}</p>
        <button
          class="flex size-9 items-center justify-center rounded-lg border border-electric-500/20 bg-electric-500/10 text-electric-600 transition-colors hover:bg-electric-500/20 disabled:cursor-not-allowed disabled:opacity-50"
          :disabled="semEstoque"
          aria-label="Adicionar ao carrinho"
          @click="emit('add', peca)"
        >
          <ShoppingCart class="size-4" />
        </button>
      </div>
    </div>
  </article>
</template>
