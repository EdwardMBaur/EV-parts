<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { ShieldCheck, SlidersHorizontal, X } from 'lucide-vue-next'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import CatalogFilters from '@/components/catalog/CatalogFilters.vue'
import PartCard from '@/components/catalog/PartCard.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { catalogService } from '@/services/catalogService'
import { useVehicleStore } from '@/stores/vehicle'
import { useCartStore } from '@/stores/cart'
import { useToast } from '@/composables/useToast'
import { extractError } from '@/services/http'

const route = useRoute()
const vehicle = useVehicleStore()
const cart = useCartStore()
const toast = useToast()

const pecas = ref([])
const loading = ref(true)
const ordenar = ref('relevancia')
const showFiltersMobile = ref(false)
const termo = ref((route.query.q || '').toString())

const filters = reactive({
  categorias: route.query.id_categoria ? [Number(route.query.id_categoria)] : [],
  soh_min: null,
  preco_max: 18000,
  codigo_oem: '',
})

const pecasFiltradas = computed(() => {
  const q = termo.value.trim().toLowerCase()
  if (!q) return pecas.value
  return pecas.value.filter((p) =>
    [p.nome_peca, p.codigo_oem, p.fabricante, p.nome_categoria]
      .filter(Boolean)
      .some((campo) => campo.toLowerCase().includes(q)),
  )
})

const pecasOrdenadas = computed(() => {
  const list = [...pecasFiltradas.value]
  if (ordenar.value === 'menor') list.sort((a, b) => Number(a.preco) - Number(b.preco))
  if (ordenar.value === 'maior') list.sort((a, b) => Number(b.preco) - Number(a.preco))
  return list
})

const totalLabel = computed(() => {
  const n = pecasOrdenadas.value.length
  const suffix = vehicle.hasContext ? ' compatíveis' : ''
  return `${n} ${n === 1 ? 'peça encontrada' : 'peças' + suffix + ' encontradas'}`
})

async function fetchPecas() {
  loading.value = true
  try {
    const params = {}
    const ctx = vehicle.context
    if (ctx?.vin) params.vin = ctx.vin
    else if (ctx?.montadora && ctx?.modelo && ctx?.ano) {
      params.montadora = ctx.montadora
      params.modelo = ctx.modelo
      params.ano = ctx.ano
    }
    if (filters.categorias.length) params.id_categoria = filters.categorias[0]
    if (filters.soh_min) params.soh_min = filters.soh_min
    if (filters.preco_max && filters.preco_max < 18000) params.preco_max = filters.preco_max
    if (filters.codigo_oem) params.codigo_oem = filters.codigo_oem

    pecas.value = await catalogService.listarPecas(params)
  } catch (error) {
    toast.error(extractError(error, 'Não foi possível carregar o catálogo'))
    pecas.value = []
  } finally {
    loading.value = false
  }
}

function addToCart(peca) {
  const result = cart.addItem(peca)
  if (!result.ok) {
    toast.error(`Estoque insuficiente para "${peca.nome_peca}"`)
    return
  }
  toast.success(`${peca.nome_peca} adicionado ao carrinho`)
}

function clearVehicle() {
  vehicle.clear()
  fetchPecas()
}

watch(
  () => route.query.id_categoria,
  (v) => {
    filters.categorias = v ? [Number(v)] : []
    fetchPecas()
  },
)

watch(
  () => route.query.q,
  (v) => {
    termo.value = (v || '').toString()
  },
)

onMounted(fetchPecas)
</script>

<template>
  <DefaultLayout show-search>
    <div class="mx-auto max-w-6xl px-4 py-6 sm:px-6">
      <nav class="mb-4 flex items-center gap-1 text-sm text-ink-500">
        <RouterLink to="/" class="hover:text-electric-600">Home</RouterLink>
        <span>›</span>
        <span class="text-ink-700">Resultados</span>
      </nav>

      <div
        v-if="vehicle.hasContext"
        class="mb-5 flex flex-wrap items-center justify-between gap-3 rounded-lg border border-emerald-accent/30 bg-emerald-accent/5 px-4 py-3"
      >
        <div class="flex items-center gap-2 text-sm font-medium text-emerald-accent-dark">
          <ShieldCheck class="size-5 shrink-0" />
          <span>Filtrando apenas peças 100% compatíveis com {{ vehicle.label }}</span>
        </div>
        <button class="text-sm font-medium text-ink-500 hover:text-ink-700" @click="clearVehicle">
          Alterar veículo
        </button>
      </div>

      <div class="flex items-center justify-between gap-3">
        <span
          v-if="termo.trim()"
          class="inline-flex items-center gap-2 rounded-full bg-electric-500/10 px-3 py-1 text-sm text-electric-700"
        >
          Busca: “{{ termo.trim() }}”
          <button class="text-electric-700/70 hover:text-electric-700" aria-label="Limpar busca" @click="termo = ''">
            <X class="size-3.5" />
          </button>
        </span>
        <span v-else />
        <BaseButton variant="outline" size="sm" class="lg:hidden" @click="showFiltersMobile = true">
          <template #icon><SlidersHorizontal class="size-4" /></template>
          Filtros
        </BaseButton>
      </div>

      <div class="mt-4 grid grid-cols-1 gap-6 lg:grid-cols-[260px_1fr]">
        <aside class="hidden lg:block">
          <CatalogFilters v-model="filters" @apply="fetchPecas" />
        </aside>

        <div>
          <div class="mb-4 flex items-center justify-between gap-3">
            <p class="text-sm text-ink-700">{{ totalLabel }}</p>
            <label class="flex items-center gap-2 text-sm text-ink-500">
              Ordenar:
              <select
                v-model="ordenar"
                class="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium text-ink-900 focus:border-electric-500 focus:outline-none"
              >
                <option value="relevancia">Relevância</option>
                <option value="menor">Menor preço</option>
                <option value="maior">Maior preço</option>
              </select>
            </label>
          </div>

          <LoadingSpinner v-if="loading" label="Buscando peças…" />
          <EmptyState
            v-else-if="!pecasOrdenadas.length"
            title="Nenhuma peça encontrada"
            :description="
              termo.trim()
                ? `Nada corresponde a “${termo.trim()}”. Tente outro termo ou ajuste os filtros.`
                : 'Tente ajustar os filtros ou alterar o veículo pesquisado.'
            "
          />
          <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
            <PartCard v-for="peca in pecasOrdenadas" :key="peca.id_peca" :peca="peca" @add="addToCart" />
          </div>
        </div>
      </div>
    </div>

    <div v-if="showFiltersMobile" class="fixed inset-0 z-50 lg:hidden">
      <div class="absolute inset-0 bg-black/40" @click="showFiltersMobile = false" />
      <div class="absolute inset-y-0 left-0 w-[85%] max-w-sm overflow-y-auto bg-surface p-4">
        <div class="mb-3 flex items-center justify-between">
          <h2 class="text-base font-bold text-ink-900">Filtros</h2>
          <button class="text-ink-500" @click="showFiltersMobile = false"><X class="size-5" /></button>
        </div>
        <CatalogFilters
          v-model="filters"
          @apply="() => { fetchPecas(); showFiltersMobile = false }"
        />
      </div>
    </div>
  </DefaultLayout>
</template>
