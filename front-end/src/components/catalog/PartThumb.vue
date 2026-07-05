<script setup>
import { computed } from 'vue'
import { categoryVisual } from '@/utils/categoryIcons'

const props = defineProps({
  categoria: { type: String, default: '' },
  size: { type: String, default: 'md' },
})

const visual = computed(() => categoryVisual(props.categoria))
const sizeClass = computed(() => (props.size === 'lg' ? 'size-16' : 'size-9'))
</script>

<template>
  <component :is="visual.icon" :class="[sizeClass, 'text-ink-400']" :stroke-width="1.5" />
</template>
