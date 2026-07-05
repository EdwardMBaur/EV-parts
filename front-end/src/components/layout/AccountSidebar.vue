<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { LayoutDashboard, ClipboardList, MapPinned, User } from '@lucide/vue'

const route = useRoute()

const links = [
  { to: '/painel', label: 'Visão geral', icon: LayoutDashboard, exact: true },
  { to: '/painel/pedidos', label: 'Meus pedidos', icon: ClipboardList },
  { to: '/painel/enderecos', label: 'Endereços', icon: MapPinned },
  { to: '/painel/perfil', label: 'Perfil', icon: User },
]

function isActive(link) {
  return link.exact ? route.path === link.to : route.path.startsWith(link.to)
}
</script>

<template>
  <nav class="flex gap-1 overflow-x-auto rounded-xl border border-slate-200 bg-white p-2 lg:flex-col lg:overflow-visible">
    <RouterLink
      v-for="link in links"
      :key="link.to"
      :to="link.to"
      :class="[
        'flex shrink-0 items-center gap-2.5 rounded-lg px-3.5 py-2.5 text-sm font-medium transition-colors',
        isActive(link) ? 'bg-electric-500/10 text-electric-700' : 'text-ink-600 hover:bg-slate-50',
      ]"
    >
      <component :is="link.icon" class="size-4" />
      {{ link.label }}
    </RouterLink>
  </nav>
</template>
