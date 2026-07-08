<script setup>
import { Loader2 } from 'lucide-vue-next'

defineProps({
  label: { type: String, default: 'Carregando…' },
})
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3 py-16 text-ink-500">
    <Loader2 class="size-8 animate-spin text-electric-500" />
    <p class="text-sm">{{ label }}</p>
  </div>
</template>
