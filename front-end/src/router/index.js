import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue'), meta: { guestOnly: true } },
  {
    path: '/cadastro',
    name: 'cadastro',
    component: () => import('@/views/RegisterView.vue'),
    meta: { guestOnly: true },
  },
  { path: '/pecas', name: 'pecas', component: () => import('@/views/CatalogView.vue') },
  {
    path: '/pecas/:id',
    name: 'peca-detalhe',
    component: () => import('@/views/ProductDetailView.vue'),
  },
  { path: '/carrinho', name: 'carrinho', component: () => import('@/views/CartView.vue') },
  {
    path: '/checkout',
    name: 'checkout',
    component: () => import('@/views/CheckoutView.vue'),
    meta: { requiresAuth: true },
  },
  { path: '/suporte', name: 'suporte', component: () => import('@/views/SupportView.vue') },
  {
    path: '/painel',
    name: 'painel',
    component: () => import('@/views/account/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/painel/pedidos',
    name: 'pedidos',
    component: () => import('@/views/account/OrdersView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/painel/pedidos/:id',
    name: 'pedido-detalhe',
    component: () => import('@/views/account/OrderDetailView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/painel/enderecos',
    name: 'enderecos',
    component: () => import('@/views/account/AddressesView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/painel/perfil',
    name: 'perfil',
    component: () => import('@/views/account/ProfileView.vue'),
    meta: { requiresAuth: true },
  },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/NotFoundView.vue') },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: 'painel' }
  }
  return true
})

export default router
