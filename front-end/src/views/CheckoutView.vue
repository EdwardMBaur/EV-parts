<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { CreditCard, QrCode, FileText, MapPin, Check } from '@lucide/vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import CheckoutStepper from '@/components/checkout/CheckoutStepper.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { useCartStore } from '@/stores/cart'
import { useToast } from '@/composables/useToast'
import { extractError } from '@/services/http'
import { enderecoService } from '@/services/enderecoService'
import { logisticaService } from '@/services/logisticaService'
import { pedidoService, pagamentoService } from '@/services/pedidoService'
import { formatCurrency } from '@/utils/format'
import { maskCep, onlyDigits } from '@/utils/masks'
import { isValidCep } from '@/utils/validators'

const router = useRouter()
const cart = useCartStore()
const toast = useToast()

const step = ref(2)
const loadingEnderecos = ref(true)
const enderecos = ref([])
const selectedEndereco = ref(null)
const showNewForm = ref(false)
const savingEndereco = ref(false)

const novoEndereco = reactive({
  cep: '',
  logradouro: '',
  numero: '',
  complemento: '',
  bairro: '',
  cidade: '',
  estado: '',
})
const enderecoErrors = reactive({})

const freteModalidades = ref([])
const selectedFrete = ref(null)
const loadingFrete = ref(false)

const metodos = [
  { value: 'cartao_credito', label: 'Cartão', icon: CreditCard },
  { value: 'pix', label: 'Pix', icon: QrCode },
  { value: 'boleto_b2b', label: 'Boleto B2B', icon: FileText },
]
const metodoPagamento = ref('cartao_credito')
const finalizando = ref(false)

const valorFrete = computed(() => (selectedFrete.value ? Number(selectedFrete.value.valor) : 0))
const total = computed(() => cart.subtotal + valorFrete.value)

async function loadEnderecos() {
  loadingEnderecos.value = true
  try {
    enderecos.value = await enderecoService.listar()
    if (enderecos.value.length) {
      const principal = enderecos.value.find((e) => e.principal === 'S')
      selectEndereco(principal || enderecos.value[0])
    } else {
      showNewForm.value = true
    }
  } catch (error) {
    toast.error(extractError(error))
  } finally {
    loadingEnderecos.value = false
  }
}

async function selectEndereco(endereco) {
  selectedEndereco.value = endereco
  await calcularFrete(endereco.cep)
}

async function onCepInput(value) {
  novoEndereco.cep = maskCep(value)
  if (onlyDigits(novoEndereco.cep).length === 8) {
    try {
      const data = await logisticaService.consultarCep(onlyDigits(novoEndereco.cep))
      novoEndereco.logradouro = data.logradouro
      novoEndereco.bairro = data.bairro
      novoEndereco.cidade = data.cidade
      novoEndereco.estado = data.estado
    } catch {
      toast.error('CEP não encontrado')
    }
  }
}

function validateEndereco() {
  Object.keys(enderecoErrors).forEach((k) => delete enderecoErrors[k])
  if (!isValidCep(novoEndereco.cep)) enderecoErrors.cep = 'CEP inválido'
  if (!novoEndereco.logradouro) enderecoErrors.logradouro = 'Obrigatório'
  if (!novoEndereco.numero) enderecoErrors.numero = 'Obrigatório'
  if (!novoEndereco.bairro) enderecoErrors.bairro = 'Obrigatório'
  if (!novoEndereco.cidade) enderecoErrors.cidade = 'Obrigatório'
  if (!novoEndereco.estado) enderecoErrors.estado = 'Obrigatório'
  return Object.keys(enderecoErrors).length === 0
}

async function saveEndereco() {
  if (!validateEndereco()) return
  savingEndereco.value = true
  try {
    const created = await enderecoService.criar({
      cep: onlyDigits(novoEndereco.cep),
      logradouro: novoEndereco.logradouro,
      numero: novoEndereco.numero,
      complemento: novoEndereco.complemento || null,
      bairro: novoEndereco.bairro,
      cidade: novoEndereco.cidade,
      estado: novoEndereco.estado.toUpperCase(),
      principal: enderecos.value.length ? 'N' : 'S',
    })
    enderecos.value.push(created)
    showNewForm.value = false
    await selectEndereco(created)
    toast.success('Endereço adicionado')
  } catch (error) {
    toast.error(extractError(error))
  } finally {
    savingEndereco.value = false
  }
}

async function calcularFrete(cep) {
  loadingFrete.value = true
  selectedFrete.value = null
  try {
    const firstItem = cart.items[0]
    const data = await logisticaService.fretePorPeca(firstItem.id_peca, onlyDigits(cep))
    freteModalidades.value = data.modalidades
    selectedFrete.value = data.modalidades[0]
  } catch (error) {
    freteModalidades.value = []
    toast.error(extractError(error, 'Não foi possível calcular o frete'))
  } finally {
    loadingFrete.value = false
  }
}

function goToPayment() {
  if (!selectedEndereco.value) {
    toast.error('Selecione um endereço de entrega')
    return
  }
  if (!selectedFrete.value) {
    toast.error('Selecione uma modalidade de frete')
    return
  }
  step.value = 3
}

async function finalizar() {
  finalizando.value = true
  try {
    const pedido = await pedidoService.criar({
      id_endereco_entrega: selectedEndereco.value.id_endereco,
      itens: cart.items.map((i) => ({ id_peca: i.id_peca, quantidade: i.quantidade })),
      modal_frete: selectedFrete.value.codigo,
    })
    await pagamentoService.iniciar({
      id_pedido: pedido.id_pedido,
      metodo_pagamento: metodoPagamento.value,
    })
    cart.clear()
    toast.success('Pedido realizado com sucesso!')
    router.push({ name: 'pedido-detalhe', params: { id: pedido.id_pedido } })
  } catch (error) {
    toast.error(extractError(error, 'Não foi possível finalizar o pedido'))
  } finally {
    finalizando.value = false
  }
}

onMounted(() => {
  if (cart.isEmpty) {
    router.replace('/carrinho')
    return
  }
  loadEnderecos()
})
</script>

<template>
  <DefaultLayout show-search>
    <div class="mx-auto max-w-4xl px-4 py-8 sm:px-6">
      <h1 class="mb-6 text-2xl font-bold text-ink-900">Finalizar compra</h1>
      <div class="mb-8 overflow-x-auto">
        <CheckoutStepper :current="step" />
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_320px]">
        <div class="space-y-5">
          <template v-if="step === 2">
            <section class="rounded-xl border border-slate-200 bg-white p-5">
              <h2 class="mb-4 text-base font-bold text-ink-900">Endereço de entrega</h2>

              <LoadingSpinner v-if="loadingEnderecos" label="Carregando endereços…" />

              <div v-else class="space-y-3">
                <button
                  v-for="endereco in enderecos"
                  :key="endereco.id_endereco"
                  class="flex w-full items-start gap-3 rounded-lg border p-3 text-left transition-colors"
                  :class="
                    selectedEndereco?.id_endereco === endereco.id_endereco
                      ? 'border-electric-500 ring-1 ring-electric-400 bg-electric-500/5'
                      : 'border-slate-200 hover:border-slate-300'
                  "
                  @click="selectEndereco(endereco)"
                >
                  <MapPin class="mt-0.5 size-5 text-ink-400" />
                  <span class="text-sm text-ink-700">
                    {{ endereco.logradouro }}, {{ endereco.numero }}
                    <span v-if="endereco.complemento">— {{ endereco.complemento }}</span>
                    <br />
                    {{ endereco.bairro }} · {{ endereco.cidade }}/{{ endereco.estado }} · {{ endereco.cep }}
                  </span>
                </button>

                <button
                  v-if="!showNewForm"
                  class="text-sm font-medium text-electric-600 hover:underline"
                  @click="showNewForm = true"
                >
                  + Adicionar novo endereço
                </button>

                <div v-if="showNewForm" class="space-y-3 rounded-lg border border-slate-200 p-4">
                  <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    <BaseInput
                      :model-value="novoEndereco.cep"
                      label="CEP"
                      placeholder="00000-000"
                      inputmode="numeric"
                      :error="enderecoErrors.cep"
                      @update:model-value="onCepInput"
                    />
                    <BaseInput v-model="novoEndereco.numero" label="Número" :error="enderecoErrors.numero" />
                  </div>
                  <BaseInput v-model="novoEndereco.logradouro" label="Logradouro" :error="enderecoErrors.logradouro" />
                  <BaseInput v-model="novoEndereco.complemento" label="Complemento (opcional)" />
                  <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
                    <BaseInput v-model="novoEndereco.bairro" label="Bairro" :error="enderecoErrors.bairro" />
                    <BaseInput v-model="novoEndereco.cidade" label="Cidade" :error="enderecoErrors.cidade" />
                    <BaseInput v-model="novoEndereco.estado" label="UF" :maxlength="2" :error="enderecoErrors.estado" />
                  </div>
                  <div class="flex gap-2">
                    <BaseButton variant="primary" size="sm" :loading="savingEndereco" @click="saveEndereco">
                      Salvar endereço
                    </BaseButton>
                    <BaseButton v-if="enderecos.length" variant="ghost" size="sm" @click="showNewForm = false">
                      Cancelar
                    </BaseButton>
                  </div>
                </div>
              </div>
            </section>

            <section v-if="selectedEndereco" class="rounded-xl border border-slate-200 bg-white p-5">
              <h2 class="mb-4 text-base font-bold text-ink-900">Modalidade de frete</h2>
              <LoadingSpinner v-if="loadingFrete" label="Calculando frete…" />
              <div v-else class="space-y-3">
                <button
                  v-for="modal in freteModalidades"
                  :key="modal.codigo"
                  class="flex w-full items-center justify-between rounded-lg border p-3 text-left transition-colors"
                  :class="
                    selectedFrete?.codigo === modal.codigo
                      ? 'border-electric-500 ring-1 ring-electric-400 bg-electric-500/5'
                      : 'border-slate-200 hover:border-slate-300'
                  "
                  @click="selectedFrete = modal"
                >
                  <span>
                    <span class="block text-sm font-semibold text-ink-900">{{ modal.nome }}</span>
                    <span class="text-xs text-ink-500">{{ modal.prazo_dias }} dias úteis · {{ modal.descricao }}</span>
                  </span>
                  <span class="ml-3 shrink-0 text-sm font-bold text-ink-900">{{ formatCurrency(modal.valor) }}</span>
                </button>
              </div>
            </section>
          </template>

          <template v-else>
            <section class="rounded-xl border border-slate-200 bg-white p-5">
              <h2 class="mb-4 text-base font-bold text-ink-900">Forma de pagamento</h2>
              <div class="grid grid-cols-3 gap-3">
                <button
                  v-for="metodo in metodos"
                  :key="metodo.value"
                  class="flex flex-col items-center gap-2 rounded-lg border p-4 transition-colors"
                  :class="
                    metodoPagamento === metodo.value
                      ? 'border-electric-500 ring-1 ring-electric-400 bg-electric-500/5 text-electric-600'
                      : 'border-slate-200 text-ink-600 hover:border-slate-300'
                  "
                  @click="metodoPagamento = metodo.value"
                >
                  <component :is="metodo.icon" class="size-5" />
                  <span class="text-sm font-medium">{{ metodo.label }}</span>
                </button>
              </div>
              <p class="mt-4 flex items-center gap-2 rounded-lg bg-slate-50 px-3 py-2.5 text-xs text-ink-500">
                <Check class="size-4 text-emerald-accent" />
                Transação processada com segurança pelo gateway integrado.
              </p>
            </section>

            <button class="text-sm font-medium text-electric-600 hover:underline" @click="step = 2">
              ← Voltar para entrega
            </button>
          </template>
        </div>

        <aside class="h-fit rounded-xl border border-slate-200 bg-surface p-5">
          <h2 class="mb-4 text-base font-bold text-ink-900">
            Etapa {{ step }} — {{ step === 2 ? 'Endereço e frete' : 'Pagamento' }}
          </h2>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between text-ink-700">
              <span>Subtotal</span>
              <span>{{ formatCurrency(cart.subtotal) }}</span>
            </div>
            <div class="flex justify-between text-ink-700">
              <span>Frete {{ selectedFrete ? `(${selectedFrete.nome})` : '' }}</span>
              <span>{{ selectedFrete ? formatCurrency(valorFrete) : '—' }}</span>
            </div>
            <hr class="border-slate-200" />
            <div class="flex justify-between text-base font-bold">
              <span class="text-ink-900">Total</span>
              <span class="text-electric-600">{{ formatCurrency(total) }}</span>
            </div>
          </div>

          <BaseButton
            v-if="step === 2"
            variant="primary"
            size="lg"
            block
            class="mt-5"
            :disabled="!selectedEndereco || !selectedFrete"
            @click="goToPayment"
          >
            Ir para pagamento
          </BaseButton>
          <BaseButton
            v-else
            variant="success"
            size="lg"
            block
            class="mt-5"
            :loading="finalizando"
            @click="finalizar"
          >
            Confirmar e pagar
          </BaseButton>

          <RouterLink to="/carrinho" class="mt-3 block text-center text-sm text-ink-500 hover:text-ink-700">
            Voltar ao carrinho
          </RouterLink>
        </aside>
      </div>
    </div>
  </DefaultLayout>
</template>
