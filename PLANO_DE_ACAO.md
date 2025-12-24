# 🎯 PLANO DE AÇÃO EXECUTIVO - TERMAN OS

> **Data:** 24 de Dezembro de 2025
> **Status Atual:** ~45% completo
> **Objetivo:** Elevar o sistema para produção com qualidade

---

## 📊 DIAGNÓSTICO ATUAL

| Área | Status | Risco |
|------|--------|-------|
| Segurança | 🟡 85% | MÉDIO |
| Funcionalidades Core | 🔴 45% | ALTO |
| Testes | 🔴 0% | CRÍTICO |
| Integrações | 🔴 0% | ALTO |
| CRM/ERP | 🔴 20% | ALTO |
| DevOps | 🔴 10% | MÉDIO |

---

## 🚨 FASE 1: CORREÇÕES CRÍTICAS (1-2 Semanas)

### 1.1 Segurança Imediata

| ID | Tarefa | Arquivo(s) | Esforço | Status |
|----|--------|-----------|---------|--------|
| SEC-01 | Remover SECRET_KEY padrão | `config.py:22` | 1h | ⬜ |
| SEC-02 | Remover endpoints de debug | `app/routes/auth.py:162` | 2h | ⬜ |
| SEC-03 | Adicionar CSRF em todos forms POST | Templates diversos | 4h | ⬜ |
| SEC-04 | Sanitização de inputs XSS | `app/utils.py` + rotas | 4h | ⬜ |
| SEC-05 | Rate limiting em operações financeiras | `app/routes/erp.py` | 2h | ⬜ |

### 1.2 Estabilidade do Sistema

| ID | Tarefa | Arquivo(s) | Esforço | Status |
|----|--------|-----------|---------|--------|
| STB-01 | Corrigir handlers `pass` vazios | `app/routes/site.py:134,159` | 1h | ⬜ |
| STB-02 | Adicionar try/except + rollback | Rotas de admin/CRM/ERP | 4h | ⬜ |
| STB-03 | Implementar logging em operações críticas | Todas as rotas | 3h | ⬜ |
| STB-04 | Corrigir scraping externo (Correios) | `app/routes/cliente.py:50-67` | 2h | ⬜ |

### 1.3 Validação de Forms

| ID | Tarefa | Arquivo(s) | Esforço | Status |
|----|--------|-----------|---------|--------|
| VAL-01 | Implementar CadastroProdutoForm | `app/forms/cadastro_produto.py` | 3h | ⬜ |
| VAL-02 | Validação completa em rotas CRM | `app/routes/crm.py` | 4h | ⬜ |
| VAL-03 | Validação em rotas de produtos | `app/routes/admin/produtos.py` | 3h | ⬜ |
| VAL-04 | Validação em checkout/carrinho | `app/routes/marketplace.py` | 3h | ⬜ |

**Entregáveis Fase 1:**
- [ ] Sistema seguro contra ataques comuns (XSS, CSRF)
- [ ] Logs estruturados de todas operações críticas
- [ ] Tratamento de erros adequado
- [ ] Validação de entrada em todos os formulários

---

## 🔧 FASE 2: FUNCIONALIDADES CORE (3-4 Semanas)

### 2.1 E-commerce Completo

| ID | Tarefa | Descrição | Esforço | Status |
|----|--------|-----------|---------|--------|
| ECOM-01 | Sistema de Reviews | CRUD + moderação + rating médio | 3d | ⬜ |
| ECOM-02 | Wishlist/Favoritos | Adicionar/remover + persistência | 2d | ⬜ |
| ECOM-03 | Cupons de Desconto | CRUD + validação + tipos | 2d | ⬜ |
| ECOM-04 | Rastreamento de Pedidos | Timeline visual + notificações | 2d | ⬜ |
| ECOM-05 | Carrinho Persistente | Migrar sessão → banco (usuário logado) | 1d | ⬜ |

### 2.2 Gestão de Usuários

| ID | Tarefa | Descrição | Esforço | Status |
|----|--------|-----------|---------|--------|
| USER-01 | Recuperação de Senha | Token via email + reset seguro | 1d | ⬜ |
| USER-02 | Perfil Completo | Edição + avatar + histórico | 2d | ⬜ |
| USER-03 | Confirmação de Email | Token + verificação | 1d | ⬜ |

### 2.3 Conteúdo

| ID | Tarefa | Descrição | Esforço | Status |
|----|--------|-----------|---------|--------|
| CONT-01 | Blog Funcional | CRUD + categorias + SEO | 3d | ⬜ |
| CONT-02 | FAQ Sistema | CRUD + busca + votação útil | 2d | ⬜ |
| CONT-03 | Contato Funcional | Salvar mensagens + notificação | 1d | ⬜ |

**Entregáveis Fase 2:**
- [ ] E-commerce com funcionalidades competitivas
- [ ] Fluxo completo de usuário
- [ ] Gestão de conteúdo funcional

---

## 📦 FASE 3: MÓDULOS CRM/ERP (4-6 Semanas)

### 3.1 CRM - Customer Relationship Management

| ID | Tarefa | Descrição | Esforço | Status |
|----|--------|-----------|---------|--------|
| CRM-01 | Blueprint CRM | Estrutura de rotas completa | 1d | ⬜ |
| CRM-02 | CRUD Leads | Listagem + filtros + formulários | 2d | ⬜ |
| CRM-03 | CRUD Oportunidades | Listagem + pipeline + formulários | 2d | ⬜ |
| CRM-04 | Pipeline Kanban | Interface drag-and-drop | 3d | ⬜ |
| CRM-05 | Atividades/Tarefas | Calendário + lembretes | 2d | ⬜ |
| CRM-06 | Propostas | Geração + envio + tracking | 2d | ⬜ |
| CRM-07 | Dashboard CRM | Métricas + gráficos | 2d | ⬜ |
| CRM-08 | RFM Calculation | Algoritmo + segmentação | 1d | ⬜ |

### 3.2 ERP - Suprimentos

| ID | Tarefa | Descrição | Esforço | Status |
|----|--------|-----------|---------|--------|
| SUP-01 | CRUD Fornecedores | Listagem + ficha + histórico | 2d | ⬜ |
| SUP-02 | Pedidos de Compra | Criação + aprovação workflow | 3d | ⬜ |
| SUP-03 | Recebimento | Entrada de mercadorias + conferência | 2d | ⬜ |
| SUP-04 | Estoque Avançado | Movimentações + alertas + inventário | 3d | ⬜ |

### 3.3 ERP - Financeiro

| ID | Tarefa | Descrição | Esforço | Status |
|----|--------|-----------|---------|--------|
| FIN-01 | Contas a Pagar | CRUD + parcelas + vencimentos | 2d | ⬜ |
| FIN-02 | Contas a Receber | CRUD + baixas + inadimplência | 2d | ⬜ |
| FIN-03 | Fluxo de Caixa | Dashboard + projeções | 2d | ⬜ |
| FIN-04 | Conciliação | Bancária + pagamentos | 2d | ⬜ |
| FIN-05 | Relatórios PDF/Excel | Vendas + estoque + financeiro | 2d | ⬜ |

### 3.4 Manufatura

| ID | Tarefa | Descrição | Esforço | Status |
|----|--------|-----------|---------|--------|
| MAN-01 | Ordens de Serviço | CRUD + anexos + histórico | 3d | ⬜ |
| MAN-02 | Ordens de Produção | Planejamento + execução | 2d | ⬜ |
| MAN-03 | Qualidade | Inspeções + checklists | 2d | ⬜ |

**Entregáveis Fase 3:**
- [ ] CRM operacional com pipeline visual
- [ ] ERP Suprimentos com workflow de compras
- [ ] ERP Financeiro com fluxo de caixa
- [ ] Manufatura com OS e qualidade

---

## 💳 FASE 4: INTEGRAÇÕES (3-4 Semanas)

### 4.1 Pagamentos

| ID | Tarefa | Gateway | Esforço | Status |
|----|--------|---------|---------|--------|
| PAY-01 | Integração Pix | Mercado Pago/PagSeguro | 5d | ⬜ |
| PAY-02 | QR Code Dinâmico | Geração + expiração | 2d | ⬜ |
| PAY-03 | Webhooks Pagamento | Confirmação automática | 2d | ⬜ |
| PAY-04 | Cartão de Crédito | Tokenização + parcelamento | 5d | ⬜ |
| PAY-05 | Conciliação Gateway | Status + taxas + estornos | 2d | ⬜ |

### 4.2 Comunicação

| ID | Tarefa | Serviço | Esforço | Status |
|----|--------|---------|---------|--------|
| COM-01 | Email Transacional | SendGrid/Mailgun | 3d | ⬜ |
| COM-02 | Templates Email | Pedido + status + senha | 2d | ⬜ |
| COM-03 | WhatsApp Business | Twilio/Evolution API | 5d | ⬜ |
| COM-04 | Notificações In-App | Sistema interno | 2d | ⬜ |

### 4.3 Logística

| ID | Tarefa | Serviço | Esforço | Status |
|----|--------|---------|---------|--------|
| LOG-01 | Cálculo de Frete | Correios + transportadoras | 3d | ⬜ |
| LOG-02 | Rastreamento | Webhooks + atualização | 2d | ⬜ |
| LOG-03 | Etiquetas | Geração automática | 1d | ⬜ |

### 4.4 Fiscal

| ID | Tarefa | Serviço | Esforço | Status |
|----|--------|---------|---------|--------|
| NFE-01 | Emissão NFe | NFe.io/Bling/Tiny | 5d | ⬜ |
| NFE-02 | DANFE PDF | Geração automática | 2d | ⬜ |
| NFE-03 | Cancelamento | Fluxo completo | 1d | ⬜ |

**Entregáveis Fase 4:**
- [ ] Checkout com Pix e cartão funcionais
- [ ] Emails automáticos em todos eventos
- [ ] WhatsApp para notificações
- [ ] NFe emitida automaticamente

---

## 🧪 FASE 5: QUALIDADE E DEVOPS (2-3 Semanas)

### 5.1 Testes

| ID | Tarefa | Cobertura | Esforço | Status |
|----|--------|-----------|---------|--------|
| TST-01 | Setup Pytest + Fixtures | Base | 1d | ⬜ |
| TST-02 | Testes de Models | 80% | 2d | ⬜ |
| TST-03 | Testes de Rotas | 70% | 3d | ⬜ |
| TST-04 | Testes de Auth | 100% | 1d | ⬜ |
| TST-05 | Testes de Pagamento | 100% | 2d | ⬜ |
| TST-06 | Testes E2E (Playwright) | Fluxos críticos | 3d | ⬜ |

### 5.2 DevOps

| ID | Tarefa | Descrição | Esforço | Status |
|----|--------|-----------|---------|--------|
| DEV-01 | Dockerfile | Multi-stage otimizado | 1d | ⬜ |
| DEV-02 | docker-compose | Dev + prod configs | 1d | ⬜ |
| DEV-03 | GitHub Actions CI | Testes + lint | 1d | ⬜ |
| DEV-04 | GitHub Actions CD | Deploy Render/Railway | 1d | ⬜ |
| DEV-05 | Backup Automático | DB + uploads | 1d | ⬜ |

### 5.3 Qualidade de Código

| ID | Tarefa | Ferramenta | Esforço | Status |
|----|--------|------------|---------|--------|
| QUA-01 | Formatação | Black + isort | 2h | ⬜ |
| QUA-02 | Linting | Flake8 + pylint | 2h | ⬜ |
| QUA-03 | Type Checking | mypy | 4h | ⬜ |
| QUA-04 | Pre-commit Hooks | Configurar | 2h | ⬜ |
| QUA-05 | Security Scan | Bandit + Safety | 2h | ⬜ |

**Entregáveis Fase 5:**
- [ ] Cobertura de testes > 80%
- [ ] Pipeline CI/CD automatizado
- [ ] Deploy automatizado
- [ ] Código padronizado e type-safe

---

## 📈 FASE 6: API E DOCUMENTAÇÃO (1-2 Semanas)

### 6.1 API REST

| ID | Tarefa | Descrição | Esforço | Status |
|----|--------|-----------|---------|--------|
| API-01 | Auth JWT | Login + refresh tokens | 2d | ⬜ |
| API-02 | CRUD Produtos | Endpoints completos | 1d | ⬜ |
| API-03 | CRUD Pedidos | Endpoints + webhooks | 2d | ⬜ |
| API-04 | CRUD Clientes | Endpoints completos | 1d | ⬜ |
| API-05 | Swagger/OpenAPI | Documentação interativa | 1d | ⬜ |
| API-06 | Rate Limiting API | Por API key | 1d | ⬜ |

### 6.2 Documentação

| ID | Tarefa | Tipo | Esforço | Status |
|----|--------|------|---------|--------|
| DOC-01 | API Docs | Swagger completo | 2d | ⬜ |
| DOC-02 | Deploy Guide | Render/Railway/VPS | 1d | ⬜ |
| DOC-03 | Manual Admin | Operação do sistema | 2d | ⬜ |
| DOC-04 | Manual Cliente | Uso da loja | 1d | ⬜ |

**Entregáveis Fase 6:**
- [ ] API REST documentada e funcional
- [ ] Documentação completa para deploy
- [ ] Manuais de usuário

---

## 📅 CRONOGRAMA RESUMIDO

| Fase | Duração | Início | Fim | Dependências |
|------|---------|--------|-----|--------------|
| **Fase 1** - Correções Críticas | 2 sem | Semana 1 | Semana 2 | - |
| **Fase 2** - Funcionalidades Core | 4 sem | Semana 3 | Semana 6 | Fase 1 |
| **Fase 3** - CRM/ERP | 6 sem | Semana 7 | Semana 12 | Fase 1 |
| **Fase 4** - Integrações | 4 sem | Semana 13 | Semana 16 | Fase 2 |
| **Fase 5** - Qualidade/DevOps | 3 sem | Semana 17 | Semana 19 | Fases 2,3,4 |
| **Fase 6** - API/Docs | 2 sem | Semana 20 | Semana 21 | Todas |

**Total Estimado: ~21 semanas (5 meses)**

---

## 🎯 MÉTRICAS DE SUCESSO

### Técnicas
| Métrica | Atual | Meta |
|---------|-------|------|
| Cobertura de Testes | 0% | 80% |
| Vulnerabilidades Críticas | 5+ | 0 |
| Uptime | - | 99.9% |
| TTFB | - | <200ms |
| Lighthouse Score | - | >90 |

### Negócio
| Métrica | Meta |
|---------|------|
| Conversão E-commerce | Medir baseline |
| Taxa Abandono Carrinho | <30% |
| Tempo Resposta Suporte | <2h |
| NPS | >50 |

---

## 🚀 PRÓXIMOS PASSOS IMEDIATOS

### Esta Semana
1. [ ] **SEC-01**: Corrigir SECRET_KEY em `config.py`
2. [ ] **SEC-02**: Remover endpoints debug em `auth.py`
3. [ ] **STB-01**: Corrigir handlers vazios em `site.py`
4. [ ] **VAL-01**: Implementar `CadastroProdutoForm`

### Próxima Semana
1. [ ] **SEC-03/04**: CSRF + Sanitização XSS
2. [ ] **STB-02/03**: Try/except + logging em rotas críticas
3. [ ] **VAL-02/03/04**: Validação completa em CRM/produtos/checkout
4. [ ] **TST-01**: Setup inicial Pytest

---

## 📝 REGISTRO DE PROGRESSO

### Atualizações
| Data | Fase | Itens Concluídos | Observações |
|------|------|------------------|-------------|
| 24/12/2025 | - | Plano criado | Análise completa de gaps |

---

## 🔗 REFERÊNCIAS

- [TODO.md](./TODO.md) - Lista detalhada de todos os gaps
- [ROADMAP.md](./ROADMAP.md) - Visão de longo prazo
- [CHANGELOG.md](./CHANGELOG.md) - Histórico de versões

---

**Responsável:** Equipe de Desenvolvimento
**Aprovado por:** [Pendente]
**Última Revisão:** 24 de Dezembro de 2025
