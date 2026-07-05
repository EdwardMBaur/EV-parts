<script setup>
import { ref, reactive, onMounted } from 'vue'
import AccountLayout from '@/layouts/AccountLayout.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useAuthStore } from '@/stores/auth'
import { authService } from '@/services/authService'
import { useToast } from '@/composables/useToast'
import { extractError } from '@/services/http'
import { maskCpfCnpj, maskPhone } from '@/utils/masks'

const auth = useAuthStore()
const toast = useToast()

const loading = ref(true)
const saving = ref(false)
const form = reactive({ nome_razao_social: '', email: '', telefone: '', cpf_cnpj: '', tipo_perfil: '' })

const perfilLabels = {
  comprador: 'Comprador (B2C)',
  oficina: 'Oficina (B2B)',
  fornecedor: 'Fornecedor',
  admin: 'Administrador',
}

async function save() {
  saving.value = true
  try {
    await authService.updateMe({
      nome_razao_social: form.nome_razao_social,
      telefone: form.telefone ? form.telefone.replace(/\D/g, '') : null,
      email: form.email,
    })
    await auth.fetchUser()
    toast.success('Perfil atualizado')
  } catch (error) {
    toast.error(extractError(error))
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  const user = await auth.fetchUser()
  if (user) {
    form.nome_razao_social = user.nome_razao_social
    form.email = user.email
    form.telefone = user.telefone ? maskPhone(user.telefone) : ''
    form.cpf_cnpj = maskCpfCnpj(user.cpf_cnpj)
    form.tipo_perfil = user.tipo_perfil
  }
  loading.value = false
})
</script>

<template>
  <AccountLayout title="Perfil">
    <LoadingSpinner v-if="loading" />
    <form v-else class="max-w-lg space-y-4 rounded-xl border border-slate-200 bg-white p-5" @submit.prevent="save">
      <div class="inline-flex rounded-full bg-electric-500/10 px-3 py-1 text-xs font-medium text-electric-700">
        {{ perfilLabels[form.tipo_perfil] || form.tipo_perfil }}
      </div>
      <BaseInput v-model="form.nome_razao_social" label="Nome / Razão social" :maxlength="60" />
      <BaseInput v-model="form.email" label="E-mail" type="email" />
      <BaseInput
        :model-value="form.telefone"
        label="Telefone"
        inputmode="numeric"
        @update:model-value="form.telefone = maskPhone($event)"
      />
      <BaseInput :model-value="form.cpf_cnpj" label="CPF / CNPJ" disabled />
      <BaseButton type="submit" variant="primary" size="md" :loading="saving">Salvar alterações</BaseButton>
    </form>
  </AccountLayout>
</template>
