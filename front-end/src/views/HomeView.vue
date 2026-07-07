<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, ScanLine, ShieldCheck, Leaf } from '@lucide/vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { categoryVisual } from '@/utils/categoryIcons'
import { catalogService } from '@/services/catalogService'
import { useVehicleStore } from '@/stores/vehicle'

const router = useRouter()
const vehicle = useVehicleStore()

const form = ref({ chassi: '', modelo: '', ano: '' })
const categorias = ref([])
const loadingCategorias = ref(true)

const destaque = ['Baterias', 'Inversores', 'Módulos Eletrônicos', 'Motores Elétricos']

const comoFunciona = [
  {
    icon: ScanLine,
    title: 'Busque pelo seu veículo',
    text: 'Informe o VIN ou modelo e o sistema filtra peças 100% compatíveis.',
  },
  {
    icon: ShieldCheck,
    title: 'Garantia de compatibilidade',
    text: 'Cada peça possui laudo técnico e índice de saúde (SoH) verificado.',
  },
  {
    icon: Leaf,
    title: 'Sustentabilidade',
    text: 'Prolongamos a vida útil de componentes e reduzimos o descarte eletrônico.',
  },
]

function submitSearch() {
  const chassi = form.value.chassi.trim()
  const modelo = form.value.modelo.trim()
  const ano = form.value.ano.trim()

  if (!chassi && !modelo && !ano) {
    vehicle.clear()
    router.push({ name: 'pecas' })
    return
  }

  const query = {}
  if (chassi) query.chassi = chassi
  if (modelo) query.modelo = modelo
  if (ano) query.ano = ano

  const isVin = chassi.replace(/\s/g, '').length >= 11
  vehicle.setContext({
    montadora: isVin ? null : chassi || null,
    modelo: modelo || null,
    ano: ano ? Number(ano) : null,
    vin: isVin ? chassi : null,
  })
  router.push({ name: 'pecas', query })
}

function goToCategory(cat) {
  router.push({ name: 'pecas', query: { id_categoria: cat.id_categoria } })
}

onMounted(async () => {
  try {
    const data = await catalogService.listarCategorias()
    categorias.value = data.filter((c) => destaque.includes(c.nome_categoria))
    if (categorias.value.length < 4) {
      categorias.value = data.slice(0, 4)
    }
  } finally {
    loadingCategorias.value = false
  }
})
</script>

<template>
  <DefaultLayout>
    <section class="bg-navy-900 text-white">
      <div class="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-14">
        <h1 class="text-2xl font-bold sm:text-3xl">Peças originais para veículos elétricos</h1>
        <p class="mt-2 text-sm text-slate-300 sm:text-base">
          Busca por compatibilidade técnica exata — chassi, modelo e versão de software
        </p>

        <form
          class="mt-6 rounded-xl bg-white/5 p-4 ring-1 ring-white/10 sm:p-5"
          @submit.prevent="submitSearch"
        >
          <p class="mb-3 text-xs font-bold uppercase tracking-wide text-slate-300">
            Busca inteligente por compatibilidade
          </p>
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-[1fr_1fr_1fr_auto]">
            <input
              v-model="form.chassi"
              type="text"
              placeholder="Chassi (VIN) ou Montadora"
              class="h-11 rounded-lg border border-white/15 bg-white/10 px-3.5 text-sm text-white placeholder:text-slate-300 focus:border-white/40 focus:outline-none sm:col-span-1"
            />
            <input
              v-model="form.modelo"
              type="text"
              placeholder="Modelo"
              class="h-11 rounded-lg border border-white/15 bg-white/10 px-3.5 text-sm text-white placeholder:text-slate-300 focus:border-white/40 focus:outline-none"
            />
            <input
              v-model="form.ano"
              type="text"
              inputmode="numeric"
              maxlength="4"
              placeholder="Ano"
              class="h-11 rounded-lg border border-white/15 bg-white/10 px-3.5 text-sm text-white placeholder:text-slate-300 focus:border-white/40 focus:outline-none"
            />
            <BaseButton variant="success" size="md" type="submit">
              <template #icon><Search class="size-4" /></template>
              Buscar
            </BaseButton>
          </div>
        </form>
      </div>
    </section>

    <section class="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <h2 class="mb-5 text-lg font-bold text-ink-900">Categorias em destaque</h2>
      <LoadingSpinner v-if="loadingCategorias" label="Carregando categorias…" />
      <div v-else class="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <button
          v-for="cat in categorias"
          :key="cat.id_categoria"
          class="flex cursor-pointer flex-col items-center gap-2 rounded-xl border border-slate-200 bg-white p-5 text-center transition-shadow hover:shadow-md"
          @click="goToCategory(cat)"
        >
          <span
            class="flex size-12 items-center justify-center rounded-xl"
            :class="categoryVisual(cat.nome_categoria).tint"
          >
            <component :is="categoryVisual(cat.nome_categoria).icon" class="size-6" />
          </span>
          <span class="text-sm font-semibold text-ink-900">{{ cat.nome_categoria }}</span>
          <span class="text-xs text-ink-500">{{ cat.total_pecas }} peças</span>
        </button>
      </div>
    </section>

    <section class="bg-surface">
      <div class="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <h2 class="mb-5 text-lg font-bold text-ink-900">Como funciona</h2>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
          <div v-for="item in comoFunciona" :key="item.title" class="flex gap-3">
            <span class="flex size-10 shrink-0 items-center justify-center rounded-lg bg-white shadow-sm">
              <component :is="item.icon" class="size-5 text-emerald-accent" />
            </span>
            <div>
              <h3 class="text-sm font-bold text-ink-900">{{ item.title }}</h3>
              <p class="mt-1 text-sm text-ink-500">{{ item.text }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>
