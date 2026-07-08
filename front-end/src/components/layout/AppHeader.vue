<script setup>
import { ref, watch } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { ShoppingCart, User, Search, LogOut, Headphones } from '@lucide/vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import BaseButton from '@/components/ui/BaseButton.vue'

const props = defineProps({
  showSearch: { type: Boolean, default: false },
})

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const cart = useCartStore()

const searchTerm = ref((route.query.q || '').toString())
const menuOpen = ref(false)

watch(
  () => route.query.q,
  (v) => {
    searchTerm.value = (v || '').toString()
  },
)

function submitSearch() {
  const q = searchTerm.value.trim()
  router.push({ name: 'pecas', query: q ? { q } : {} })
}

function logout() {
  auth.logout()
  menuOpen.value = false
  router.push({ name: 'home' })
}
</script>

<template>
  <header class="sticky top-0 z-40 bg-navy-900 text-white shadow-sm">
    <div class="mx-auto flex h-16 max-w-6xl items-center gap-3 px-4 sm:gap-5 sm:px-6">
      <RouterLink to="/" class="shrink-0 text-xl font-extrabold tracking-tight">
        EV<span class="text-slate-300">.parts</span>
      </RouterLink>

      <form
        v-if="showSearch"
        class="hidden flex-1 items-center gap-2 rounded-lg bg-white/10 px-3 py-2 ring-1 ring-white/15 focus-within:ring-white/40 sm:flex"
        @submit.prevent="submitSearch"
      >
        <Search class="size-4 text-slate-300" />
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Busque por peça, VIN ou modelo"
          class="w-full bg-transparent text-sm text-white placeholder:text-slate-300 focus:outline-none"
        />
      </form>

      <div class="flex flex-1 items-center justify-end gap-2 sm:ml-auto sm:flex-none">
        <template v-if="!auth.isAuthenticated">
          <RouterLink to="/suporte" class="hidden sm:block">
            <BaseButton variant="outlineLight" size="sm">
              <template #icon><Headphones class="size-4" /></template>
              Suporte
            </BaseButton>
          </RouterLink>
          <RouterLink to="/login">
            <BaseButton variant="outlineLight" size="sm">Entrar</BaseButton>
          </RouterLink>
          <RouterLink to="/cadastro">
            <BaseButton variant="success" size="sm">Cadastrar</BaseButton>
          </RouterLink>
        </template>

        <template v-else>
          <RouterLink
            to="/carrinho"
            class="relative flex size-10 items-center justify-center rounded-lg transition-colors hover:bg-white/10"
            aria-label="Carrinho"
          >
            <ShoppingCart class="size-5" />
            <span
              v-if="cart.count"
              class="absolute -right-0.5 -top-0.5 flex min-w-5 items-center justify-center rounded-full bg-emerald-accent px-1 text-xs font-bold text-white"
            >
              {{ cart.count }}
            </span>
          </RouterLink>

          <div class="relative">
            <button
              class="flex size-10 items-center justify-center rounded-full bg-white/10 transition-colors hover:bg-white/20"
              aria-label="Conta"
              @click="menuOpen = !menuOpen"
            >
              <User class="size-5" />
            </button>
            <div
              v-if="menuOpen"
              class="absolute right-0 mt-2 w-52 overflow-hidden rounded-xl border border-slate-200 bg-white py-1 text-ink-700 shadow-lg"
            >
              <RouterLink
                to="/painel"
                class="block px-4 py-2.5 text-sm hover:bg-slate-50"
                @click="menuOpen = false"
              >
                Meu painel
              </RouterLink>
              <RouterLink
                to="/painel/pedidos"
                class="block px-4 py-2.5 text-sm hover:bg-slate-50"
                @click="menuOpen = false"
              >
                Meus pedidos
              </RouterLink>
              <button
                class="flex w-full items-center gap-2 border-t border-slate-100 px-4 py-2.5 text-left text-sm text-rose-500 hover:bg-rose-50"
                @click="logout"
              >
                <LogOut class="size-4" />
                Sair
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>

    <form
      v-if="showSearch"
      class="flex items-center gap-2 border-t border-white/10 px-4 py-2 sm:hidden"
      @submit.prevent="submitSearch"
    >
      <div class="flex flex-1 items-center gap-2 rounded-lg bg-white/10 px-3 py-2 ring-1 ring-white/15">
        <Search class="size-4 text-slate-300" />
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Busque por peça, VIN ou modelo"
          class="w-full bg-transparent text-sm text-white placeholder:text-slate-300 focus:outline-none"
        />
      </div>
    </form>
  </header>
</template>
