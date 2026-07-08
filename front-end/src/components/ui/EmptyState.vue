<script setup>
import { PackageOpen } from 'lucide-vue-next'

defineProps({
  title: { type: String, default: 'Nada por aqui' },
  description: { type: String, default: '' },
  // Usamos uma factory (() => PackageOpen) em vez de passar o ícone direto.
  // Ícones do lucide são componentes funcionais (funções); como o `type` inclui
  // Function, o Vue trataria um default-função como factory e o INVOCARIA
  // (PackageOpen()), quebrando com "Cannot destructure property 'slots'".
  // A factory devolve o componente sem executá-lo.
  icon: { type: [Object, Function], default: () => PackageOpen },
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
