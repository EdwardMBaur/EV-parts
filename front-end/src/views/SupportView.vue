<script setup>
import { ref, reactive } from 'vue'
import { Headphones, Mail, MessageCircle } from 'lucide-vue-next'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useToast } from '@/composables/useToast'
import { isValidEmail } from '@/utils/validators'

const toast = useToast()

const form = reactive({ nome: '', email: '', mensagem: '' })
const errors = reactive({})
const sending = ref(false)

function validate() {
  Object.keys(errors).forEach((k) => delete errors[k])
  if (!form.nome.trim()) errors.nome = 'Informe seu nome'
  if (!isValidEmail(form.email)) errors.email = 'E-mail inválido'
  if (form.mensagem.trim().length < 10) errors.mensagem = 'Descreva com pelo menos 10 caracteres'
  return Object.keys(errors).length === 0
}

function submit() {
  if (!validate()) return
  sending.value = true
  setTimeout(() => {
    sending.value = false
    toast.success('Mensagem enviada! Nossa equipe responderá em breve.')
    form.nome = ''
    form.email = ''
    form.mensagem = ''
  }, 700)
}

const canais = [
  { icon: Mail, label: 'suporte@evparts.com.br' },
  { icon: MessageCircle, label: 'Chat disponível em dias úteis, 8h–18h' },
]
</script>

<template>
  <DefaultLayout show-search>
    <div class="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <div class="mb-8 flex items-center gap-3">
        <span class="flex size-11 items-center justify-center rounded-xl bg-electric-500/10 text-electric-600">
          <Headphones class="size-6" />
        </span>
        <div>
          <h1 class="text-2xl font-bold text-ink-900">Suporte</h1>
          <p class="text-sm text-ink-500">Fale com nossa equipe especializada em logística de EVs.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_260px]">
        <form class="space-y-4 rounded-xl border border-slate-200 bg-white p-5" @submit.prevent="submit">
          <BaseInput v-model="form.nome" label="Nome" :error="errors.nome" />
          <BaseInput v-model="form.email" label="E-mail" type="email" :error="errors.email" />
          <div>
            <label class="mb-1.5 block text-sm font-medium text-ink-700">Mensagem</label>
            <textarea
              v-model="form.mensagem"
              rows="5"
              class="w-full rounded-lg border border-slate-300 px-3.5 py-2.5 text-sm focus:border-electric-500 focus:outline-none focus:ring-2 focus:ring-electric-400/40"
              placeholder="Como podemos ajudar?"
            />
            <p v-if="errors.mensagem" class="mt-1 text-xs text-rose-500">{{ errors.mensagem }}</p>
          </div>
          <BaseButton type="submit" variant="primary" size="md" :loading="sending">Enviar mensagem</BaseButton>
        </form>

        <aside class="h-fit space-y-4 rounded-xl border border-slate-200 bg-surface p-5">
          <h2 class="text-sm font-bold text-ink-900">Outros canais</h2>
          <div v-for="canal in canais" :key="canal.label" class="flex items-start gap-2.5 text-sm text-ink-700">
            <component :is="canal.icon" class="mt-0.5 size-4 text-electric-600" />
            <span>{{ canal.label }}</span>
          </div>
        </aside>
      </div>
    </div>
  </DefaultLayout>
</template>
