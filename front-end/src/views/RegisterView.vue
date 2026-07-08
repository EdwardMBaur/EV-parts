<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { Eye, EyeOff, Check, ShieldCheck, FileText, Truck } from 'lucide-vue-next'
import AuthLayout from '@/layouts/AuthLayout.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { authService } from '@/services/authService'
import { logisticaService } from '@/services/logisticaService'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import { extractError } from '@/services/http'
import { maskCpfCnpj, maskPhone, maskCep, onlyDigits } from '@/utils/masks'
import { isValidEmail, isValidCpfCnpj, isValidCep, passwordRules, isValidPassword } from '@/utils/validators'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const perfis = [
  { value: 'comprador', label: 'Comprador (B2C)' },
  { value: 'oficina', label: 'Oficina (B2B)' },
  { value: 'fornecedor', label: 'Fornecedor' },
]

const form = reactive({
  tipo_perfil: 'comprador',
  email: '',
  nome_razao_social: '',
  cpf_cnpj: '',
  telefone: '',
  cep: '',
  cidade_uf: '',
  senha: '',
  confirmar: '',
  aceite: false,
})

const errors = reactive({})
const showPassword = ref(false)
const loadingCep = ref(false)
const submitting = ref(false)

const authFeatures = [
  { icon: ShieldCheck, label: 'Busca por compatibilidade técnica exata' },
  { icon: FileText, label: 'Laudos técnicos e SoH de baterias' },
  { icon: Truck, label: 'Logística especializada em cargas pesadas' },
]

const senhaChecks = computed(() => passwordRules.map((rule) => ({ ...rule, ok: rule.test(form.senha) })))
const senhaConfere = computed(() => form.confirmar.length > 0 && form.senha === form.confirmar)

watch(
  () => form.cpf_cnpj,
  (v) => {
    form.cpf_cnpj = maskCpfCnpj(v)
  },
)
watch(
  () => form.telefone,
  (v) => {
    form.telefone = maskPhone(v)
  },
)

async function handleCep() {
  const digits = onlyDigits(form.cep)
  if (digits.length !== 8) return
  loadingCep.value = true
  try {
    const data = await logisticaService.consultarCep(digits)
    form.cidade_uf = `${data.cidade} / ${data.estado}`
    errors.cep = ''
  } catch {
    form.cidade_uf = ''
    errors.cep = 'CEP não encontrado'
  } finally {
    loadingCep.value = false
  }
}

function onCepInput(value) {
  form.cep = maskCep(value)
  if (onlyDigits(form.cep).length === 8) handleCep()
}

function validate() {
  Object.keys(errors).forEach((k) => delete errors[k])
  if (!isValidEmail(form.email)) errors.email = 'E-mail inválido'
  if (form.nome_razao_social.trim().length < 2) errors.nome_razao_social = 'Informe o nome completo'
  if (!isValidCpfCnpj(form.cpf_cnpj)) errors.cpf_cnpj = 'CPF (11 dígitos) ou CNPJ (14 dígitos)'
  if (form.cep && !isValidCep(form.cep)) errors.cep = 'CEP inválido'
  if (!isValidPassword(form.senha)) errors.senha = 'A senha não atende aos requisitos'
  if (!senhaConfere.value) errors.confirmar = 'As senhas não coincidem'
  if (!form.aceite) errors.aceite = 'Você deve aceitar os termos'
  return Object.keys(errors).length === 0
}

async function submit() {
  if (!validate()) return
  submitting.value = true
  try {
    await authService.cadastro({
      tipo_perfil: form.tipo_perfil,
      email: form.email.trim(),
      nome_razao_social: form.nome_razao_social.trim(),
      cpf_cnpj: onlyDigits(form.cpf_cnpj),
      telefone: form.telefone ? onlyDigits(form.telefone) : null,
      senha: form.senha,
    })
    await auth.login({ login: form.email.trim(), senha: form.senha })
    toast.success('Conta criada com sucesso!')
    router.push('/painel')
  } catch (error) {
    toast.error(extractError(error, 'Não foi possível concluir o cadastro'))
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <AuthLayout
    title="Crie sua conta no marketplace especializado em EVs"
    subtitle="Acesse centenas de peças verificadas com compatibilidade garantida para o seu veículo elétrico."
    :features="authFeatures"
    :top-action="{ label: 'Já tenho conta', to: '/login' }"
  >
    <h2 class="text-xl font-bold text-ink-900">Criar conta</h2>

    <form class="mt-5 space-y-4" @submit.prevent="submit">
      <div>
        <p class="mb-2 text-sm font-medium text-ink-700">Tipo de perfil</p>
        <div class="flex flex-wrap gap-x-5 gap-y-2">
          <label v-for="p in perfis" :key="p.value" class="flex items-center gap-2 text-sm text-ink-700">
            <input v-model="form.tipo_perfil" type="radio" :value="p.value" class="size-4 text-electric-600 focus:ring-electric-400" />
            {{ p.label }}
          </label>
        </div>
      </div>

      <BaseInput v-model="form.email" label="E-mail" type="email" placeholder="seu@email.com" :error="errors.email" />
      <BaseInput
        v-model="form.nome_razao_social"
        label="Nome completo"
        placeholder="máx. 60 caracteres"
        :maxlength="60"
        :error="errors.nome_razao_social"
      />

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <BaseInput v-model="form.cpf_cnpj" label="CPF / CNPJ" placeholder="000.000.000-00" :error="errors.cpf_cnpj" inputmode="numeric" />
        <BaseInput v-model="form.telefone" label="Telefone" placeholder="(00) 00000-0000" inputmode="numeric" />
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <BaseInput
          :model-value="form.cep"
          label="CEP"
          placeholder="00000-000"
          inputmode="numeric"
          :error="errors.cep"
          :hint="loadingCep ? 'Buscando…' : undefined"
          @update:model-value="onCepInput"
        />
        <BaseInput :model-value="form.cidade_uf" label="Cidade / UF" placeholder="Preenchido via API" disabled />
      </div>

      <div>
        <BaseInput
          v-model="form.senha"
          label="Senha"
          :type="showPassword ? 'text' : 'password'"
          placeholder="••••••••"
          :error="errors.senha"
        >
          <template #suffix>
            <button type="button" class="text-ink-400 hover:text-ink-700" @click="showPassword = !showPassword">
              <component :is="showPassword ? EyeOff : Eye" class="size-5" />
            </button>
          </template>
        </BaseInput>
        <div class="mt-1.5 flex flex-wrap gap-x-3 gap-y-1 text-xs">
          <span
            v-for="check in senhaChecks"
            :key="check.key"
            class="inline-flex items-center gap-1"
            :class="check.ok ? 'text-emerald-accent' : 'text-ink-400'"
          >
            <Check class="size-3" />{{ check.label }}
          </span>
        </div>
      </div>

      <BaseInput
        v-model="form.confirmar"
        label="Confirmar senha"
        :type="showPassword ? 'text' : 'password'"
        placeholder="••••••••"
        :error="errors.confirmar"
      >
        <template #suffix>
          <Check v-if="senhaConfere" class="size-5 text-emerald-accent" />
        </template>
      </BaseInput>

      <div>
        <label class="flex items-start gap-2 text-sm text-ink-700">
          <input v-model="form.aceite" type="checkbox" class="mt-0.5 size-4 rounded border-slate-300 text-electric-600 focus:ring-electric-400" />
          <span>
            Concordo com os
            <a href="#" class="font-medium text-electric-600 hover:underline">Termos de Uso</a>
            e
            <a href="#" class="font-medium text-electric-600 hover:underline">Política de Privacidade</a>
          </span>
        </label>
        <p v-if="errors.aceite" class="mt-1 text-xs text-rose-500">{{ errors.aceite }}</p>
      </div>

      <BaseButton type="submit" variant="primary" size="lg" block :loading="submitting">Criar conta</BaseButton>
    </form>

    <p class="mt-5 text-center text-sm text-ink-500">
      Já tem conta?
      <RouterLink to="/login" class="font-semibold text-electric-600 hover:underline">Entrar</RouterLink>
    </p>
  </AuthLayout>
</template>
