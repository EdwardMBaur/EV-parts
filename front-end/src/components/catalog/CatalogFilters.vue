<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { formatCurrencyShort } from '@/utils/format'
import { catalogService } from '@/services/catalogService'

const props = defineProps({
  modelValue: { type: Object, required: true },
})
const emit = defineEmits(['update:modelValue', 'apply'])

const categorias = ref([])
const local = reactive({ ...props.modelValue })

const sohOptions = [
  { label: 'Acima de 90%', value: 90 },
  { label: '80% – 90%', value: 80 },
  { label: 'Abaixo de 80%', value: 0 },
]

const regioes = [
  { label: 'Sul', value: 'sul' },
  { label: 'Sudeste', value: 'sudeste' },
  { label: 'Centro-Oeste', value: 'centro-oeste' },
]

const PRECO_MIN = 800
const PRECO_MAX = 18000

watch(
  () => props.modelValue,
  (v) => Object.assign(local, v),
  { deep: true },
)

function toggleCategoria(id) {
  local.categorias = local.categorias.includes(id)
    ? local.categorias.filter((c) => c !== id)
    : [...local.categorias, id]
  commit()
}

function selectSoh(value) {
  local.soh_min = local.soh_min === value ? null : value
  commit()
}

function toggleRegiao(value) {
  local.regioes = local.regioes.includes(value)
    ? local.regioes.filter((r) => r !== value)
    : [...local.regioes, value]
  commit()
}

function commit() {
  emit('update:modelValue', { ...local })
}

function apply() {
  commit()
  emit('apply')
}

function clear() {
  local.categorias = []
  local.soh_min = null
  local.preco_max = PRECO_MAX
  local.codigo_oem = ''
  local.regioes = []
  commit()
  emit('apply')
}

onMounted(async () => {
  categorias.value = await catalogService.listarCategorias()
})
</script>

<template>
  <div class="space-y-6 rounded-xl border border-slate-200 bg-white p-5">
    <div>
      <h3 class="mb-3 text-sm font-bold text-ink-900">Categoria</h3>
      <div class="space-y-2">
        <label
          v-for="cat in categorias"
          :key="cat.id_categoria"
          class="flex items-center gap-2 text-sm text-ink-700"
        >
          <input
            type="checkbox"
            :checked="local.categorias.includes(cat.id_categoria)"
            class="size-4 rounded border-slate-300 text-electric-600 focus:ring-electric-400"
            @change="toggleCategoria(cat.id_categoria)"
          />
          {{ cat.nome_categoria }}
        </label>
      </div>
    </div>

    <div>
      <h3 class="mb-3 text-sm font-bold text-ink-900">Faixa de preço</h3>
      <input
        v-model.number="local.preco_max"
        type="range"
        :min="PRECO_MIN"
        :max="PRECO_MAX"
        step="100"
        class="w-full accent-electric-600"
        @change="commit"
      />
      <div class="mt-1 flex justify-between text-xs text-ink-500">
        <span>{{ formatCurrencyShort(PRECO_MIN) }}</span>
        <span>{{ formatCurrencyShort(local.preco_max) }}</span>
      </div>
    </div>

    <div>
      <h3 class="mb-3 text-sm font-bold text-ink-900">SoH da bateria</h3>
      <div class="space-y-2">
        <label v-for="opt in sohOptions" :key="opt.label" class="flex items-center gap-2 text-sm text-ink-700">
          <input
            type="checkbox"
            :checked="local.soh_min === opt.value"
            class="size-4 rounded border-slate-300 text-electric-600 focus:ring-electric-400"
            @change="selectSoh(opt.value)"
          />
          {{ opt.label }}
        </label>
      </div>
    </div>

    <div>
      <h3 class="mb-3 text-sm font-bold text-ink-900">Localização</h3>
      <div class="space-y-2">
        <label v-for="reg in regioes" :key="reg.value" class="flex items-center gap-2 text-sm text-ink-700">
          <input
            type="checkbox"
            :checked="local.regioes.includes(reg.value)"
            class="size-4 rounded border-slate-300 text-electric-600 focus:ring-electric-400"
            @change="toggleRegiao(reg.value)"
          />
          {{ reg.label }}
        </label>
      </div>
    </div>

    <div>
      <h3 class="mb-2 text-sm font-bold text-ink-900">Código OEM</h3>
      <input
        v-model="local.codigo_oem"
        type="text"
        placeholder="Ex: 1EA-915-105"
        class="h-10 w-full rounded-lg border border-slate-300 px-3 text-sm focus:border-electric-500 focus:outline-none focus:ring-2 focus:ring-electric-400/40"
        @keyup.enter="apply"
      />
    </div>

    <div class="flex gap-2 pt-1">
      <BaseButton variant="primary" size="sm" block @click="apply">Aplicar filtros</BaseButton>
      <BaseButton variant="ghost" size="sm" @click="clear">Limpar</BaseButton>
    </div>
  </div>
</template>
