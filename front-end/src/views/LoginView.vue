<script setup>
import { ref, reactive } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { Eye, EyeOff } from 'lucide-vue-next'
import AuthLayout from '@/layouts/AuthLayout.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import { extractError } from '@/services/http'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const toast = useToast()

const form = reactive({ login: '', senha: '', manter: true })
const errors = reactive({ login: '', senha: '' })
const showPassword = ref(false)
const loading = ref(false)

function validate() {
  errors.login = form.login.trim() ? '' : 'Informe e-mail ou CPF/CNPJ'
  errors.senha = form.senha ? '' : 'Informe sua senha'
  return !errors.login && !errors.senha
}

async function submit() {
  if (!validate()) return
  loading.value = true
  try {
    await auth.login({ login: form.login.trim(), senha: form.senha })
    toast.success('Bem-vindo de volta!')
    const redirect = route.query.redirect || '/painel'
    router.push(redirect)
  } catch (error) {
    toast.error(extractError(error, 'Credenciais inválidas'))
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <AuthLayout
    title="Seu marketplace especializado em peças para veículos elétricos"
    subtitle="Acesse sua conta para buscar peças com compatibilidade garantida, acompanhar pedidos e muito mais."
    :top-action="{ label: 'Criar conta', to: '/cadastro', variant: 'success' }"
  >
    <h2 class="text-xl font-bold text-ink-900">Entrar na conta</h2>

    <form class="mt-6 space-y-4" @submit.prevent="submit">
      <BaseInput
        v-model="form.login"
        label="E-mail ou CPF/CNPJ"
        placeholder="seu@email.com ou 000.000.000-00"
        autocomplete="username"
        :error="errors.login"
      />

      <BaseInput
        v-model="form.senha"
        label="Senha"
        :type="showPassword ? 'text' : 'password'"
        placeholder="••••••••"
        autocomplete="current-password"
        :error="errors.senha"
      >
        <template #suffix>
          <button type="button" class="text-ink-400 hover:text-ink-700" @click="showPassword = !showPassword">
            <component :is="showPassword ? EyeOff : Eye" class="size-5" />
          </button>
        </template>
      </BaseInput>

      <div class="flex items-center justify-between">
        <label class="flex items-center gap-2 text-sm text-ink-700">
          <input v-model="form.manter" type="checkbox" class="size-4 rounded border-slate-300 text-electric-600 focus:ring-electric-400" />
          Manter sessão ativa
        </label>
        <RouterLink to="/login" class="text-sm font-medium text-electric-600 hover:underline">
          Esqueci minha senha
        </RouterLink>
      </div>

      <BaseButton type="submit" variant="primary" size="lg" block :loading="loading">Entrar</BaseButton>
    </form>

    <p class="mt-6 text-center text-sm text-ink-500">
      Não tem conta?
      <RouterLink to="/cadastro" class="font-semibold text-electric-600 hover:underline">
        Cadastre-se grátis
      </RouterLink>
    </p>
  </AuthLayout>
</template>
