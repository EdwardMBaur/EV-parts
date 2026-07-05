<script setup>
import { Check } from '@lucide/vue'

defineProps({
  label: { type: String, default: 'Compatível' },
})
</script>

<template>
  <span
    class="inline-flex items-center gap-1 rounded-full border border-emerald-accent/30 bg-emerald-accent/10 px-2.5 py-1 text-xs font-semibold text-emerald-accent-dark"
  >
    <Check class="size-3.5" />
    {{ label }}
  </span>
</template>
