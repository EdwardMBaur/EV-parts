<script setup>
import { CheckCircle2, AlertCircle, Info, X } from '@lucide/vue'
import { useToast } from '@/composables/useToast'

const { toasts, dismiss } = useToast()

const config = {
  success: { icon: CheckCircle2, ring: 'border-emerald-accent/30', tint: 'text-emerald-accent' },
  error: { icon: AlertCircle, ring: 'border-rose-300', tint: 'text-rose-500' },
  info: { icon: Info, ring: 'border-electric-300', tint: 'text-electric-500' },
}
</script>

<template>
  <div class="pointer-events-none fixed inset-x-0 top-4 z-[100] flex flex-col items-center gap-2 px-4">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="pointer-events-auto flex w-full max-w-sm items-start gap-3 rounded-xl border bg-white px-4 py-3 shadow-lg"
        :class="config[toast.type].ring"
      >
        <component :is="config[toast.type].icon" class="mt-0.5 size-5 shrink-0" :class="config[toast.type].tint" />
        <p class="flex-1 text-sm text-ink-700">{{ toast.message }}</p>
        <button class="text-ink-400 hover:text-ink-700" @click="dismiss(toast.id)">
          <X class="size-4" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
