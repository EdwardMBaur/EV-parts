import { ref } from 'vue'

const toasts = ref([])
let seq = 0

export function useToast() {
  function push(message, type = 'info', timeout = 4000) {
    const id = ++seq
    toasts.value.push({ id, message, type })
    if (timeout) {
      setTimeout(() => dismiss(id), timeout)
    }
    return id
  }

  function dismiss(id) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  return {
    toasts,
    dismiss,
    success: (msg, t) => push(msg, 'success', t),
    error: (msg, t) => push(msg, 'error', t),
    info: (msg, t) => push(msg, 'info', t),
  }
}
