<script setup>
import { RouterLink } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
  <DefaultLayout>
    <div class="mx-auto flex max-w-lg flex-col items-center px-4 py-24 text-center">
      <p class="text-6xl font-extrabold text-electric-600">404</p>
      <h1 class="mt-4 text-xl font-bold text-ink-900">Página não encontrada</h1>
      <p class="mt-2 text-sm text-ink-500">A página que você procura não existe ou foi movida.</p>
      <RouterLink to="/" class="mt-6">
        <BaseButton variant="primary" size="md">Voltar para a home</BaseButton>
      </RouterLink>
    </div>
  </DefaultLayout>
</template>
