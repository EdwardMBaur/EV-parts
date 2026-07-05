# EV.parts — Front-end

Interface web do marketplace de peças para veículos elétricos.
Construído com **Vue 3 (Composition API)**, **Vite**, **Tailwind CSS**, **Vue Router**, **Pinia** e **Axios**.

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Framework | Vue 3 (`<script setup>`) |
| Build | Vite |
| Estilos | Tailwind CSS |
| Rotas | Vue Router |
| Estado | Pinia |
| HTTP | Axios |
| Ícones | Lucide (`@lucide/vue`) |

## Configuração

O front-end consome a API do back-end. Configure a URL base em `.env`:

```env
VITE_API_URL=http://localhost:8000
```

## Como rodar

```sh
npm install
npm run dev      # servidor de desenvolvimento (http://localhost:5173)
npm run build    # build de produção
npm run preview  # pré-visualiza o build
npm run lint     # oxlint + eslint
```

## Estrutura

```
src/
├── components/
│   ├── ui/            # botões, inputs, badges, toasts, estados vazios
│   ├── layout/        # header, footer, sidebar da conta
│   ├── catalog/       # card de peça, filtros, thumb, calculadora de frete
│   └── checkout/      # stepper do checkout
├── layouts/           # DefaultLayout, AuthLayout, AccountLayout
├── views/             # telas (home, login, cadastro, catálogo, detalhe, carrinho, checkout, painel…)
│   └── account/       # painel do cliente (pedidos, endereços, perfil)
├── services/          # camada HTTP por domínio (auth, catálogo, logística, pedidos…)
├── stores/            # Pinia (auth, cart, vehicle)
├── composables/       # useToast
├── utils/             # formatação, máscaras, validadores, mapeamentos
└── router/            # rotas + guards de autenticação
```

## Telas implementadas (RF01–RF05)

- **Home** — busca inteligente por compatibilidade (VIN/montadora/modelo/ano), categorias em destaque, seção "Como funciona".
- **Login** — e-mail ou CPF/CNPJ + senha.
- **Cadastro** — perfil B2C/B2B/Fornecedor, validações, auto-preenchimento de CEP via ViaCEP.
- **Catálogo** — filtros laterais (categoria, preço, SoH, código OEM), selo de compatibilidade, ordenação.
- **Detalhe da peça** — ficha técnica, laudo em PDF, calculadora de frete, checkout.
- **Carrinho e Checkout** — fluxo em 3 etapas (Carrinho → Entrega → Pagamento) com Cartão/Pix/Boleto B2B.
- **Painel do cliente** — visão geral, pedidos, rastreamento, endereços e perfil.

Layout responsivo Mobile-First seguindo a paleta do projeto (azul elétrico, verde esmeralda, cinza chumbo).
