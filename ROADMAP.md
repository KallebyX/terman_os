# 🛣️ Roadmap — Terman OS (Mangueiras Terman)

Este roadmap apresenta as funcionalidades e melhorias previstas para o sistema, separadas por estágio de desenvolvimento.

---

## ✅ Concluído

- [x] Estrutura inicial com Flask e SQLAlchemy
- [x] Autenticação de usuários (cliente e admin)
- [x] CRUD de produtos e categorias
- [x] Carrinho de compras com sessão
- [x] Painel administrativo funcional
- [x] Upload de imagens para produtos
- [x] Visualização de pedidos (cliente e admin)
- [x] Geração de relatórios em PDF
- [x] Geração de relatórios em Excel
- [x] Deploy via Render com banco PostgreSQL
- [x] Worker + CronJob para tarefas automáticas

---

## 🛠️ Em Desenvolvimento

- [ ] Dashboard com KPIs e gráficos
- [ ] Página de confirmação de pedido (pós-finalização)
- [ ] Página de perfil do usuário com edição e histórico
- [ ] Página de administração de usuários
- [ ] Documentação técnica (`README`, `.env.example`, `render.yaml`)

---

## 🎯 Próximos Passos

- [ ] Geração de relatórios por intervalo de datas
- [ ] Filtros de pedidos por cliente, data e valor
- [ ] Integração com Pix (via PagSeguro ou Gerencianet)
- [ ] Integração com envio de mensagens por WhatsApp (Twilio ou Z-API)
- [ ] Logs administrativos e auditoria
- [ ] Toasts e feedbacks visuais nas ações
- [ ] Sistema de recuperação de senha
- [ ] Gamificação para fidelização de clientes

---

## 🧪 Testes & Qualidade

- [ ] Testes unitários com `pytest`
- [ ] Testes de integração de rotas protegidas
- [ ] Monitoramento de erros e logs em produção
- [ ] Código limpo com `black` + `flake8`

---

## 📘 Documentação

- [ ] `README.md` completo (✔️ em andamento)
- [x] `ROADMAP.md` (✔️ este arquivo)
- [x] `CONTRIBUTING.md`
- [x] `CODE_OF_CONDUCT.md`
- [x] `docs/` para API futura (se aplicável)

---

## 🧩 Ideias Futuras

- [ ] API REST para integração com app mobile
- [ ] Interface pública de catálogo em QR Code
- [ ] Sistema de fidelidade e cupons
- [ ] Integração com logística para entrega local
- [ ] Dashboard para relatórios agroindustriais