<script setup>
import { computed } from 'vue'
import { Loader2 } from 'lucide-vue-next'

const props = defineProps({
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'md' },
  type: { type: String, default: 'button' },
  loading: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  block: { type: Boolean, default: false },
})

const variants = {
  primary: 'bg-electric-600 text-white hover:bg-electric-700 focus-visible:ring-electric-400',
  success:
    'bg-emerald-accent text-white hover:bg-emerald-accent-dark focus-visible:ring-emerald-accent',
  outline:
    'border border-slate-300 bg-white text-ink-700 hover:bg-slate-50 focus-visible:ring-electric-400',
  outlineLight:
    'border border-white/40 bg-transparent text-white hover:bg-white/15 focus-visible:ring-white/50',
  ghost: 'text-ink-700 hover:bg-slate-100 focus-visible:ring-electric-400',
  navy: 'bg-navy-900 text-white hover:bg-navy-800 focus-visible:ring-navy-700',
}

const sizes = {
  sm: 'h-9 px-3 text-sm',
  md: 'h-11 px-5 text-sm',
  lg: 'h-12 px-6 text-base',
}

const classes = computed(() => [
  'inline-flex cursor-pointer items-center justify-center gap-2 rounded-lg font-semibold transition-colors',
  'focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
  'disabled:cursor-not-allowed disabled:opacity-50',
  variants[props.variant],
  sizes[props.size],
  props.block ? 'w-full' : '',
])
</script>

<template>
  <button :type="type" :class="classes" :disabled="disabled || loading">
    <Loader2 v-if="loading" class="size-4 animate-spin" />
    <slot v-else name="icon" />
    <slot />
  </button>
</template>
