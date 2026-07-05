<script setup>
import { PackageOpen } from '@lucide/vue'

defineProps({
  title: { type: String, default: 'Nada por aqui' },
  description: { type: String, default: '' },
  icon: { type: [Object, Function], default: PackageOpen },
})
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3 px-6 py-16 text-center">
    <div class="flex size-14 items-center justify-center rounded-full bg-slate-100">
      <component :is="icon" class="size-7 text-ink-400" />
    </div>
    <h3 class="text-base font-semibold text-ink-900">{{ title }}</h3>
    <p v-if="description" class="max-w-sm text-sm text-ink-500">{{ description }}</p>
    <slot />
  </div>
</template>
