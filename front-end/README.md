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
| Ícones | Lucide (`lucide-vue-next`) |

## Pré-requisitos

- **Node.js 20.19+** ou **22.12+** (exigência do Vite 8)
- **npm** 10+
- Back-end da API em execução (veja `../back-end/README.md`). Por padrão o front espera a API em `http://localhost:8000`.

## Configuração

O front-end consome a API do back-end. Crie um arquivo `.env` na raiz do `front-end`
(há um `.env.example` de referência) e defina a URL base:

```env
VITE_API_URL=http://localhost:8000
```

## Como rodar

```sh
# 1. Instalar dependências
npm install

# 2. Subir o servidor de desenvolvimento (http://localhost:5173)
npm run dev

# 3. Gerar o build de produção
npm run build

# 4. Pré-visualizar o build gerado
npm run preview

# Qualidade de código (oxlint + eslint)
npm run lint
```

> **Ordem de subida:** inicie o back-end primeiro (`../back-end`), depois o front-end.
> Sem a API no ar, as telas carregam mas as listagens/ações ficam vazias ou exibem erro.

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
- **Catálogo (RF04)** — filtros laterais (categoria, faixa de preço, SoH, localização, código OEM), selo de compatibilidade, ordenação e busca textual.
- **Detalhe da peça (RF05)** — carrossel, ficha técnica, laudo em PDF, calculadora de frete e indicador de estoque.
- **Carrinho e Checkout (RF05)** — fluxo em 3 etapas (Carrinho → Entrega → Pagamento) com Cartão/Pix/Boleto B2B.
- **Painel do cliente** — visão geral, pedidos, rastreamento, endereços e perfil.
- **Suporte** — formulário de contato/atendimento.

Layout responsivo Mobile-First seguindo a paleta do projeto (azul elétrico, verde esmeralda, cinza chumbo).

## Observações de integração

Alguns comportamentos são tratados no front-end porque a API atual não os cobre,
sem inventar regras de negócio:

- **Busca textual do catálogo** — filtragem por nome/OEM/fabricante/categoria é feita no cliente sobre os resultados retornados.
- **Filtro de Localização** — mapeia região (Sul/Sudeste/Centro-Oeste) para faixas de CEP no cliente.
- **Valor do frete no pedido** — a API grava `valor_frete = 0` na criação; o valor escolhido é persistido localmente e reexibido nas telas de pedido.
- **Pagamento** — o endpoint de pagamento é simulado (não há gateway real).
