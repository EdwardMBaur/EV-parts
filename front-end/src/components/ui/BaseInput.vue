<script setup>
import { computed, useSlots } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  label: { type: String, default: '' },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  error: { type: String, default: '' },
  hint: { type: String, default: '' },
  id: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  maxlength: { type: [String, Number], default: undefined },
  inputmode: { type: String, default: undefined },
  autocomplete: { type: String, default: undefined },
})

const emit = defineEmits(['update:modelValue', 'blur'])
const slots = useSlots()

const fieldId = computed(() => props.id || `field-${Math.random().toString(36).slice(2, 9)}`)

const inputClasses = computed(() => [
  'w-full rounded-lg border bg-white px-3.5 text-sm text-ink-900 placeholder:text-ink-400',
  'transition-colors focus:outline-none focus:ring-2 focus:ring-electric-400/40',
  'disabled:bg-slate-50 disabled:text-ink-400',
  props.error
    ? 'border-rose-400 focus:border-rose-400'
    : 'border-slate-300 focus:border-electric-500',
  slots.suffix ? 'h-11 pr-10 pl-3.5' : 'h-11',
])
</script>

<template>
  <div class="w-full">
    <label v-if="label" :for="fieldId" class="mb-1.5 block text-sm font-medium text-ink-700">
      {{ label }}
    </label>
    <div class="relative">
      <input
        :id="fieldId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :maxlength="maxlength"
        :inputmode="inputmode"
        :autocomplete="autocomplete"
        :class="inputClasses"
        @input="emit('update:modelValue', $event.target.value)"
        @blur="emit('blur', $event)"
      />
      <div v-if="$slots.suffix" class="absolute inset-y-0 right-0 flex items-center pr-3">
        <slot name="suffix" />
      </div>
    </div>
    <p v-if="error" class="mt-1 text-xs text-rose-500">{{ error }}</p>
    <p v-else-if="hint" class="mt-1 text-xs text-ink-400">{{ hint }}</p>
  </div>
</template>
