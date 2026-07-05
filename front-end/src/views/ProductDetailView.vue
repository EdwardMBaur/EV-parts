<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { ChevronLeft, ChevronRight, ShoppingCart, Heart, ShieldCheck, FileText } from '@lucide/vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import CompatBadge from '@/components/ui/CompatBadge.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import PartThumb from '@/components/catalog/PartThumb.vue'
import FreightCalculator from '@/components/catalog/FreightCalculator.vue'
import { catalogService } from '@/services/catalogService'
import { useCartStore } from '@/stores/cart'
import { useVehicleStore } from '@/stores/vehicle'
import { useToast } from '@/composables/useToast'
import { extractError } from '@/services/http'
import { formatCurrency, formatInstallments, formatDate } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const cart = useCartStore()
const vehicle = useVehicleStore()
const toast = useToast()

const peca = ref(null)
const loading = ref(true)
const notFound = ref(false)
const activeThumb = ref(0)

const compatLabel = computed(() => {
  if (!peca.value?.veiculos_compativeis?.length) return null
  if (vehicle.hasContext) {
    const ctx = vehicle.context
    const match = peca.value.veiculos_compativeis.find(
      (v) =>
        (!ctx.modelo || v.modelo.toLowerCase().includes(String(ctx.modelo).toLowerCase())) &&
        (!ctx.ano || v.ano_fabricacao === ctx.ano),
    )
    if (match) return `Compatível com ${match.montadora} ${match.modelo} ${match.ano_fabricacao}`
  }
  const v = peca.value.veiculos_compativeis[0]
  return `Compatível com ${v.montadora} ${v.modelo} ${v.ano_fabricacao}`
})

const fichaTecnica = computed(() => {
  if (!peca.value) return []
  const p = peca.value
  const swRange = p.veiculos_compativeis?.length
    ? p.veiculos_compativeis
        .map((v) => v.versao_sw_min || v.versao_sw_max)
        .filter(Boolean)
        .join(' – ')
    : null
  return [
    { label: 'Código OEM', value: p.codigo_oem },
    { label: 'Capacidade', value: p.dimensoes },
    { label: 'Tensão nominal', value: p.voltagem },
    { label: 'Peso', value: p.peso_kg ? `${p.peso_kg} kg` : null },
    { label: 'Fabricante', value: p.fabricante },
    { label: 'Compatível com SW', value: swRange },
    {
      label: 'Estado de saúde (SoH)',
      value: p.estado_saude_soh != null ? `${p.estado_saude_soh}%` : null,
      highlight: true,
    },
  ].filter((row) => row.value)
})

async function fetchPeca() {
  loading.value = true
  notFound.value = false
  try {
    peca.value = await catalogService.detalhePeca(Number(route.params.id))
  } catch (error) {
    if (error?.response?.status === 404) notFound.value = true
    else toast.error(extractError(error))
  } finally {
    loading.value = false
  }
}

function addToCart() {
  cart.addItem(peca.value)
  toast.success('Peça adicionada ao carrinho')
}

function buyNow() {
  cart.addItem(peca.value)
  router.push('/carrinho')
}

onMounted(fetchPeca)
</script>

<template>
  <DefaultLayout show-search>
    <LoadingSpinner v-if="loading" label="Carregando peça…" />

    <EmptyState
      v-else-if="notFound || !peca"
      title="Peça não encontrada"
      description="Esta peça pode ter sido removida ou está indisponível."
    >
      <RouterLink to="/pecas">
        <BaseButton variant="primary" size="md">Voltar ao catálogo</BaseButton>
      </RouterLink>
    </EmptyState>

    <div v-else class="mx-auto max-w-6xl px-4 py-6 sm:px-6">
      <nav class="mb-5 flex flex-wrap items-center gap-1 text-sm text-ink-500">
        <RouterLink to="/" class="hover:text-electric-600">Home</RouterLink>
        <span>›</span>
        <RouterLink to="/pecas" class="hover:text-electric-600">{{ peca.nome_categoria || 'Peças' }}</RouterLink>
        <span>›</span>
        <span class="text-ink-700">{{ peca.nome_peca }}</span>
      </nav>

      <div class="grid grid-cols-1 gap-8 lg:grid-cols-[1fr_400px]">
        <div>
          <div class="relative flex h-72 items-center justify-center rounded-xl bg-surface-card sm:h-80">
            <button
              class="absolute left-3 flex size-9 items-center justify-center rounded-full bg-white/80 text-ink-600 shadow-sm hover:bg-white"
              aria-label="Anterior"
              @click="activeThumb = (activeThumb + 3) % 4"
            >
              <ChevronLeft class="size-5" />
            </button>
            <PartThumb :categoria="peca.nome_categoria" size="lg" />
            <button
              class="absolute right-3 flex size-9 items-center justify-center rounded-full bg-white/80 text-ink-600 shadow-sm hover:bg-white"
              aria-label="Próximo"
              @click="activeThumb = (activeThumb + 1) % 4"
            >
              <ChevronRight class="size-5" />
            </button>
            <div class="absolute bottom-3 flex gap-1.5">
              <span
                v-for="i in 4"
                :key="i"
                class="size-2 rounded-full"
                :class="activeThumb === i - 1 ? 'bg-electric-600' : 'bg-slate-300'"
              />
            </div>
          </div>

          <div class="mt-3 grid grid-cols-4 gap-3">
            <button
              v-for="i in 4"
              :key="i"
              class="flex h-16 items-center justify-center rounded-lg border bg-surface-card transition-colors"
              :class="activeThumb === i - 1 ? 'border-electric-500 ring-1 ring-electric-400' : 'border-slate-200'"
              @click="activeThumb = i - 1"
            >
              <PartThumb :categoria="peca.nome_categoria" />
            </button>
          </div>

          <div class="mt-8">
            <h2 class="mb-3 text-lg font-bold text-ink-900">Ficha técnica</h2>
            <dl class="divide-y divide-slate-100 border-t border-slate-100">
              <div v-for="row in fichaTecnica" :key="row.label" class="grid grid-cols-2 gap-4 py-2.5">
                <dt class="text-sm text-ink-500">{{ row.label }}</dt>
                <dd class="text-sm font-medium" :class="row.highlight ? 'text-emerald-accent' : 'text-ink-900'">
                  {{ row.value }}
                  <span v-if="row.highlight" class="ml-1 font-normal text-ink-400">
                    (laudo emitido {{ formatDate(peca.data_cadastro) }})
                  </span>
                </dd>
              </div>
            </dl>

            <a
              v-if="peca.url_laudo_tecnico"
              :href="peca.url_laudo_tecnico"
              target="_blank"
              rel="noopener"
              class="mt-4 inline-flex items-center gap-2 rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-medium text-ink-700 hover:bg-slate-50"
            >
              <FileText class="size-4" />
              Ver laudo técnico (PDF)
            </a>
          </div>
        </div>

        <aside class="space-y-4">
          <div
            v-if="compatLabel"
            class="flex items-center gap-2 rounded-lg border border-emerald-accent/30 bg-emerald-accent/5 px-4 py-3 text-sm font-semibold text-emerald-accent-dark"
          >
            <ShieldCheck class="size-5 shrink-0" />
            {{ compatLabel }}
          </div>

          <div class="rounded-xl border border-slate-200 bg-surface p-5">
            <p class="text-sm text-ink-500">Preço unitário</p>
            <p class="mt-1 text-3xl font-bold text-electric-600">{{ formatCurrency(peca.preco) }}</p>
            <p class="text-sm text-ink-500">{{ formatInstallments(peca.preco) }}</p>

            <hr class="my-4 border-slate-200" />

            <FreightCalculator :id-peca="peca.id_peca" />

            <div class="mt-5 space-y-3">
              <BaseButton variant="primary" size="lg" block @click="addToCart">
                <template #icon><ShoppingCart class="size-5" /></template>
                Adicionar ao carrinho
              </BaseButton>
              <div class="grid grid-cols-2 gap-3">
                <BaseButton variant="success" size="md" @click="buyNow">Comprar agora</BaseButton>
                <BaseButton variant="outline" size="md">
                  <template #icon><Heart class="size-4" /></template>
                  Salvar
                </BaseButton>
              </div>
            </div>
          </div>

          <div v-if="peca.veiculos_compativeis?.length" class="rounded-xl border border-slate-200 bg-white p-5">
            <h3 class="mb-2 text-sm font-bold text-ink-900">Veículos compatíveis</h3>
            <ul class="space-y-1.5">
              <li
                v-for="v in peca.veiculos_compativeis"
                :key="v.id_veiculo"
                class="flex items-center gap-2 text-sm text-ink-700"
              >
                <CompatBadge label="" class="!px-1.5" />
                {{ v.montadora }} {{ v.modelo }} · {{ v.ano_fabricacao }}
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  </DefaultLayout>
</template>
