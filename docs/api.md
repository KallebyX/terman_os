# 🔌 API — Terman OS

Este documento descreve as principais rotas da aplicação Terman OS, com seus métodos, parâmetros esperados e comportamentos. A API é protegida por autenticação de sessão (Flask-Login), e pode futuramente evoluir para REST/Token.

---

## 📦 Categorias de Rotas

- 👤 **Autenticação e Usuário**
- 🛍️ **Marketplace e Produtos**
- 🧾 **Pedidos e Carrinho**
- 🧑‍💼 **Administração**
- 📊 **Dashboard (futuro)**

---

## 👤 Autenticação

| Método | Rota           | Descrição               | Autenticado |
|--------|----------------|--------------------------|-------------|
| GET    | `/login`       | Página de login          | ❌          |
| POST   | `/login`       | Realiza login            | ❌          |
| GET    | `/cadastro`    | Página de cadastro       | ❌          |
| POST   | `/cadastro`    | Registra novo usuário    | ❌          |
| GET    | `/logout`      | Encerra a sessão         | ✅          |

---

## 🛍️ Marketplace

| Método | Rota                 | Descrição                           | Autenticado |
|--------|----------------------|--------------------------------------|-------------|
| GET    | `/`                  | Página inicial                       | ❌          |
| GET    | `/loja`              | Lista de produtos                    | ❌          |
| GET    | `/produto/<id>`      | Detalhes de produto                  | ❌          |
| POST   | `/carrinho/adicionar`| Adiciona produto ao carrinho         | ✅ Cliente   |
| GET    | `/carrinho`          | Visualiza carrinho                   | ✅ Cliente   |
| POST   | `/carrinho/finalizar`| Finaliza o pedido                    | ✅ Cliente   |

---

## 🧾 Pedidos

| Método | Rota                     | Descrição                           | Autenticado |
|--------|--------------------------|--------------------------------------|-------------|
| GET    | `/cliente/pedidos`       | Lista pedidos do cliente            | ✅ Cliente   |
| GET    | `/cliente/pedido/<id>`   | Visualiza detalhes de um pedido     | ✅ Cliente   |
| GET    | `/admin/pedidos`         | Lista pedidos para admin            | ✅ Admin     |
| GET    | `/admin/pedido/<id>`     | Detalhes do pedido (admin)          | ✅ Admin     |

---

## 🧑‍💼 Administração

| Método | Rota                        | Descrição                            | Autenticado |
|--------|-----------------------------|---------------------------------------|-------------|
| GET    | `/admin/produtos`           | Listar produtos                       | ✅ Admin     |
| GET    | `/admin/novo-produto`       | Página de novo produto                | ✅ Admin     |
| POST   | `/admin/novo-produto`       | Criação de produto                    | ✅ Admin     |
| GET    | `/admin/editar/<id>`        | Editar produto                        | ✅ Admin     |
| POST   | `/admin/editar/<id>`        | Atualizar produto                     | ✅ Admin     |
| POST   | `/admin/excluir/<id>`       | Remover produto                       | ✅ Admin     |
| GET    | `/admin/categorias`         | Gerenciar categorias                  | ✅ Admin     |

---

## 📊 Dashboard (previsto)

- GET `/admin/dashboard`
- Painéis com vendas, clientes, produtos mais vendidos etc.

---

## ⚠️ Observações

- Todas as rotas protegidas devem ser acessadas com sessão ativa
- No futuro, pode-se gerar token com JWT ou criar versão da API em formato RESTful

---

## 📌 Versão

- API interna 1.0 — atualizada em `{{ now() }}`

---