<script setup>
import { Check } from 'lucide-vue-next'

defineProps({
  current: { type: Number, required: true },
})

const steps = [
  { id: 1, label: 'Carrinho' },
  { id: 2, label: 'Entrega' },
  { id: 3, label: 'Pagamento' },
]
</script>

<template>
  <div class="flex items-center">
    <template v-for="(step, index) in steps" :key="step.id">
      <div class="flex items-center gap-2">
        <span
          class="flex size-7 items-center justify-center rounded-full text-xs font-bold transition-colors"
          :class="[
            step.id < current
              ? 'bg-emerald-accent text-white'
              : step.id === current
                ? 'bg-electric-600 text-white'
                : 'border border-slate-300 text-ink-400',
          ]"
        >
          <Check v-if="step.id < current" class="size-4" />
          <template v-else>{{ step.id }}</template>
        </span>
        <span
          class="text-sm font-medium"
          :class="step.id <= current ? 'text-ink-900' : 'text-ink-400'"
        >
          {{ step.label }}
        </span>
      </div>
      <span
        v-if="index < steps.length - 1"
        class="mx-3 h-px flex-1 min-w-6"
        :class="step.id < current ? 'bg-emerald-accent' : 'bg-slate-200'"
      />
    </template>
  </div>
</template>
