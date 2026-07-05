<script setup>
import { ref } from 'vue'
import { Info, Truck, Zap } from '@lucide/vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { logisticaService } from '@/services/logisticaService'
import { formatCurrencyShort, formatCep } from '@/utils/format'
import { maskCep, onlyDigits } from '@/utils/masks'
import { extractError } from '@/services/http'

const props = defineProps({
  idPeca: { type: Number, required: true },
})

const cep = ref('')
const loading = ref(false)
const error = ref('')
const result = ref(null)

function onInput(value) {
  cep.value = maskCep(value)
}

async function calcular() {
  error.value = ''
  if (onlyDigits(cep.value).length !== 8) {
    error.value = 'Informe um CEP válido'
    return
  }
  loading.value = true
  try {
    result.value = await logisticaService.fretePorPeca(props.idPeca, onlyDigits(cep.value))
  } catch (e) {
    error.value = extractError(e, 'Não foi possível calcular o frete')
    result.value = null
  } finally {
    loading.value = false
  }
}

const modalIcon = (codigo) => (codigo === 'expresso' ? Zap : Truck)
</script>

<template>
  <div>
    <h3 class="mb-2 text-sm font-bold text-ink-900">Calcular frete</h3>
    <form class="flex gap-2" @submit.prevent="calcular">
      <input
        :value="cep"
        type="text"
        inputmode="numeric"
        placeholder="CEP de destino"
        class="h-11 flex-1 rounded-lg border border-slate-300 px-3.5 text-sm focus:border-electric-500 focus:outline-none focus:ring-2 focus:ring-electric-400/40"
        @input="onInput($event.target.value)"
      />
      <BaseButton type="submit" variant="primary" size="md" :loading="loading">Calcular</BaseButton>
    </form>
    <p v-if="error" class="mt-1.5 text-xs text-rose-500">{{ error }}</p>

    <div v-if="result" class="mt-3 space-y-2 rounded-lg bg-white p-3 ring-1 ring-slate-200">
      <p class="flex items-start gap-1.5 text-xs text-ink-500">
        <Info class="mt-0.5 size-3.5 shrink-0" />
        Roteamento inteligente para {{ result.aviso_carga_especial ? 'carga pesada / classe 9' : 'carga geral' }}
      </p>
      <div
        v-for="modal in result.modalidades"
        :key="modal.codigo"
        class="flex items-center justify-between text-sm"
      >
        <span class="flex items-center gap-2 text-ink-700">
          <component :is="modalIcon(modal.codigo)" class="size-4 text-ink-500" />
          {{ modal.nome }} ({{ modal.prazo_dias }} dias)
        </span>
        <span class="font-semibold text-ink-900">{{ formatCurrencyShort(modal.valor) }}</span>
      </div>
      <p v-if="result.aviso_carga_especial" class="pt-1 text-xs text-amber-600">
        {{ result.aviso_carga_especial }}
      </p>
    </div>
  </div>
</template>
