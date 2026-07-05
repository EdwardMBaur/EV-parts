<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AccountSidebar from '@/components/layout/AccountSidebar.vue'

defineProps({
  title: { type: String, default: '' },
})
</script>

<template>
  <DefaultLayout show-search>
    <div class="mx-auto max-w-6xl px-4 py-8 sm:px-6">
      <h1 v-if="title" class="mb-6 text-2xl font-bold text-ink-900">{{ title }}</h1>
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-[220px_1fr]">
        <AccountSidebar />
        <div>
          <slot />
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>
