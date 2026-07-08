<script setup>
import { ref, reactive, onMounted } from 'vue'
import { MapPinned, Trash2 } from 'lucide-vue-next'
import AccountLayout from '@/layouts/AccountLayout.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { enderecoService } from '@/services/enderecoService'
import { logisticaService } from '@/services/logisticaService'
import { useToast } from '@/composables/useToast'
import { extractError } from '@/services/http'
import { maskCep, onlyDigits } from '@/utils/masks'
import { isValidCep } from '@/utils/validators'

const toast = useToast()
const enderecos = ref([])
const loading = ref(true)
const showForm = ref(false)
const saving = ref(false)

const form = reactive({
  cep: '',
  logradouro: '',
  numero: '',
  complemento: '',
  bairro: '',
  cidade: '',
  estado: '',
})
const errors = reactive({})

async function load() {
  loading.value = true
  try {
    enderecos.value = await enderecoService.listar()
  } catch (error) {
    toast.error(extractError(error))
  } finally {
    loading.value = false
  }
}

async function onCepInput(value) {
  form.cep = maskCep(value)
  if (onlyDigits(form.cep).length === 8) {
    try {
      const data = await logisticaService.consultarCep(onlyDigits(form.cep))
      form.logradouro = data.logradouro
      form.bairro = data.bairro
      form.cidade = data.cidade
      form.estado = data.estado
    } catch {
      toast.error('CEP não encontrado')
    }
  }
}

function validate() {
  Object.keys(errors).forEach((k) => delete errors[k])
  if (!isValidCep(form.cep)) errors.cep = 'CEP inválido'
  if (!form.logradouro) errors.logradouro = 'Obrigatório'
  if (!form.numero) errors.numero = 'Obrigatório'
  if (!form.bairro) errors.bairro = 'Obrigatório'
  if (!form.cidade) errors.cidade = 'Obrigatório'
  if (!form.estado) errors.estado = 'Obrigatório'
  return Object.keys(errors).length === 0
}

async function save() {
  if (!validate()) return
  saving.value = true
  try {
    await enderecoService.criar({
      cep: onlyDigits(form.cep),
      logradouro: form.logradouro,
      numero: form.numero,
      complemento: form.complemento || null,
      bairro: form.bairro,
      cidade: form.cidade,
      estado: form.estado.toUpperCase(),
      principal: enderecos.value.length ? 'N' : 'S',
    })
    toast.success('Endereço adicionado')
    resetForm()
    showForm.value = false
    await load()
  } catch (error) {
    toast.error(extractError(error))
  } finally {
    saving.value = false
  }
}

async function remover(id) {
  try {
    await enderecoService.remover(id)
    toast.success('Endereço removido')
    await load()
  } catch (error) {
    toast.error(extractError(error))
  }
}

function resetForm() {
  Object.assign(form, {
    cep: '',
    logradouro: '',
    numero: '',
    complemento: '',
    bairro: '',
    cidade: '',
    estado: '',
  })
}

onMounted(load)
</script>

<template>
  <AccountLayout title="Endereços">
    <LoadingSpinner v-if="loading" />
    <div v-else class="space-y-4">
      <div v-if="enderecos.length" class="space-y-3">
        <div
          v-for="endereco in enderecos"
          :key="endereco.id_endereco"
          class="flex items-start justify-between gap-3 rounded-xl border border-slate-200 bg-white p-4"
        >
          <div class="flex gap-3">
            <MapPinned class="mt-0.5 size-5 text-ink-400" />
            <div class="text-sm text-ink-700">
              <p class="font-medium text-ink-900">
                {{ endereco.logradouro }}, {{ endereco.numero }}
                <span v-if="endereco.principal === 'S'" class="ml-2 rounded-full bg-electric-500/10 px-2 py-0.5 text-xs text-electric-700">
                  Principal
                </span>
              </p>
              <p>{{ endereco.bairro }} · {{ endereco.cidade }}/{{ endereco.estado }} · {{ endereco.cep }}</p>
            </div>
          </div>
          <button class="text-ink-400 hover:text-rose-500" @click="remover(endereco.id_endereco)">
            <Trash2 class="size-5" />
          </button>
        </div>
      </div>

      <EmptyState
        v-else-if="!showForm"
        :icon="MapPinned"
        title="Nenhum endereço cadastrado"
        description="Adicione um endereço para agilizar seus checkouts."
      />

      <div v-if="showForm" class="space-y-3 rounded-xl border border-slate-200 bg-white p-5">
        <h2 class="text-base font-bold text-ink-900">Novo endereço</h2>
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <BaseInput :model-value="form.cep" label="CEP" placeholder="00000-000" inputmode="numeric" :error="errors.cep" @update:model-value="onCepInput" />
          <BaseInput v-model="form.numero" label="Número" :error="errors.numero" />
        </div>
        <BaseInput v-model="form.logradouro" label="Logradouro" :error="errors.logradouro" />
        <BaseInput v-model="form.complemento" label="Complemento (opcional)" />
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <BaseInput v-model="form.bairro" label="Bairro" :error="errors.bairro" />
          <BaseInput v-model="form.cidade" label="Cidade" :error="errors.cidade" />
          <BaseInput v-model="form.estado" label="UF" :maxlength="2" :error="errors.estado" />
        </div>
        <div class="flex gap-2">
          <BaseButton variant="primary" size="sm" :loading="saving" @click="save">Salvar</BaseButton>
          <BaseButton variant="ghost" size="sm" @click="showForm = false">Cancelar</BaseButton>
        </div>
      </div>

      <BaseButton v-if="!showForm" variant="outline" size="md" @click="showForm = true">
        + Adicionar endereço
      </BaseButton>
    </div>
  </AccountLayout>
</template>
