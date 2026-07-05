<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

defineProps({
  showSearch: { type: Boolean, default: false },
})
</script>

<template>
  <div class="flex min-h-screen flex-col bg-white">
    <AppHeader :show-search="showSearch" />
    <main class="flex-1">
      <slot />
    </main>
    <AppFooter />
  </div>
</template>
