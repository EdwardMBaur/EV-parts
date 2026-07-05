<script setup>
import { RouterLink } from 'vue-router'

const columns = [
  {
    title: 'EV.parts',
    links: [
      { label: 'Sobre nós', to: '/' },
      { label: 'Como funciona', to: '/' },
      { label: 'Sustentabilidade', to: '/' },
    ],
  },
  {
    title: 'Para compradores',
    links: [
      { label: 'Buscar peças', to: '/pecas' },
      { label: 'Garantias', to: '/' },
      { label: 'Devoluções', to: '/' },
    ],
  },
  {
    title: 'Para fornecedores',
    links: [
      { label: 'Cadastrar estoque', to: '/cadastro' },
      { label: 'Integrações', to: '/' },
      { label: 'Suporte', to: '/suporte' },
    ],
  },
]
</script>

<template>
  <footer class="bg-navy-900 text-slate-300">
    <div class="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <div class="grid grid-cols-1 gap-8 sm:grid-cols-3">
        <div v-for="col in columns" :key="col.title">
          <h4 class="mb-3 text-sm font-bold text-white">{{ col.title }}</h4>
          <ul class="space-y-2">
            <li v-for="link in col.links" :key="link.label">
              <RouterLink
                :to="link.to"
                class="text-sm text-slate-300 underline-offset-4 transition-colors hover:text-white hover:underline"
              >
                {{ link.label }}
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
      <div class="mt-10 border-t border-white/10 pt-6 text-xs text-slate-400">
        EV.parts © 2025 · Marketplace especializado em veículos elétricos
      </div>
    </div>
  </footer>
</template>
