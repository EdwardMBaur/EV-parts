<script setup>
import { RouterLink } from 'vue-router'
import { ShieldCheck, Truck, FileText } from '@lucide/vue'

const props = defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  topAction: { type: Object, default: null },
  features: {
    type: Array,
    default: () => [
      { icon: ShieldCheck, label: 'Transações seguras com gateway integrado' },
      { icon: Truck, label: 'Rastreamento em tempo real da entrega' },
      { icon: FileText, label: 'Laudos técnicos verificados' },
    ],
  },
})
</script>

<template>
  <div class="flex min-h-screen flex-col bg-navy-900">
    <header class="flex h-16 items-center justify-between px-4 sm:px-8">
      <RouterLink to="/" class="text-xl font-extrabold tracking-tight text-white">
        EV<span class="text-slate-300">.parts</span>
      </RouterLink>
      <RouterLink v-if="topAction" :to="topAction.to">
        <span
          :class="[
            'inline-flex h-10 items-center rounded-lg px-4 text-sm font-semibold transition-colors',
            topAction.variant === 'success'
              ? 'bg-emerald-accent text-white hover:bg-emerald-accent-dark'
              : 'border border-white/30 text-white hover:bg-white/10',
          ]"
        >
          {{ topAction.label }}
        </span>
      </RouterLink>
    </header>

    <div class="flex flex-1 flex-col lg:flex-row">
      <aside class="flex flex-col justify-center px-6 py-8 text-white lg:w-[45%] lg:px-12 lg:py-16">
        <h1 class="max-w-md text-2xl font-bold leading-tight sm:text-3xl">{{ title }}</h1>
        <p v-if="subtitle" class="mt-4 max-w-md text-sm text-slate-300 sm:text-base">
          {{ subtitle }}
        </p>
        <ul class="mt-8 space-y-3">
          <li v-for="feature in props.features" :key="feature.label" class="flex items-center gap-3">
            <component :is="feature.icon" class="size-5 text-emerald-accent" />
            <span class="text-sm text-slate-200">{{ feature.label }}</span>
          </li>
        </ul>
      </aside>

      <section class="flex flex-1 items-start justify-center bg-white px-6 py-8 sm:px-10 lg:py-12">
        <div class="w-full max-w-md">
          <slot />
        </div>
      </section>
    </div>
  </div>
</template>
