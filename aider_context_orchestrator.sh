#!/bin/bash

echo "🔄 Iniciando orquestrador de contexto do Aider para o projeto Terman OS"
echo "Você pode sair a qualquer momento com CTRL+C"
echo "--------------------------------------------------------"

pause() {
  echo
  read -p "⏸️ Pressione Enter para continuar para a próxima etapa..." _
  echo "--------------------------------------------------------"
}

run_aider_command() {
  echo -e "\n🧠 Rodando: $1\n"
  echo "$1" | pbcopy
  echo "📋 Comando copiado para sua área de transferência (use CMD+V no Aider)"
}

# Etapa 1 — POS + Orders + Inventory + Products
run_aider_command "/add backend/apps/pos/models.py backend/apps/pos/views.py backend/apps/pos/serializers.py"
run_aider_command "/add backend/apps/orders/models.py backend/apps/orders/views.py backend/apps/orders/serializers.py"
run_aider_command "/add backend/apps/inventory/models.py backend/apps/inventory/views.py backend/apps/inventory/serializers.py"
run_aider_command "/add backend/apps/products/models.py backend/apps/products/views.py backend/apps/products/serializers.py"
pause
run_aider_command "/drop backend/apps/pos/ backend/apps/orders/ backend/apps/inventory/ backend/apps/products/"
pause

# Etapa 2 — JWT Auth Backend + Frontend
run_aider_command "/add backend/apps/accounts/views.py backend/apps/accounts/serializers.py backend/apps/accounts/models.py"
run_aider_command "/add backend/apps/accounts/permissions.py backend/apps/accounts/urls.py"
run_aider_command "/add frontend/src/contexts/AuthContext.tsx frontend/src/services/AuthContext.tsx frontend/src/utils/auth.ts"
pause
run_aider_command "/drop backend/apps/accounts/ frontend/src/contexts/AuthContext.tsx frontend/src/services/AuthContext.tsx frontend/src/utils/auth.ts"
pause

# Etapa 3 — Configuração de API
run_aider_command "/add frontend/src/services/api.ts frontend/vite.config.js frontend/.env"
pause
run_aider_command "/drop frontend/src/services/api.ts frontend/vite.config.js frontend/.env"
pause

# Etapa 4 — Login
run_aider_command "/add frontend/src/pages/Login.tsx"
pause
run_aider_command "/drop frontend/src/pages/Login.tsx"
pause

# Etapa 5 — Componentes dinâmicos
run_aider_command "/add frontend/src/pages/dashboard/ frontend/src/pages/PDV/ frontend/src/pages/Orders/ frontend/src/pages/inventory/"
pause
run_aider_command "/drop frontend/src/pages/dashboard/ frontend/src/pages/PDV/ frontend/src/pages/Orders/ frontend/src/pages/inventory/"
pause

# Etapa 6 — Testes automatizados
run_aider_command "/add backend/tests/"
pause
run_aider_command "/drop backend/tests/"
pause

# Etapa 7 — Docker + Deploy
run_aider_command "/add docker-compose.yml backend/Dockerfile frontend/Dockerfile"
pause
run_aider_command "/drop docker-compose.yml backend/Dockerfile frontend/Dockerfile"
pause

# Etapa 8 — Documentação
run_aider_command "/add README.md terman_os_documentacao.md"
pause
run_aider_command "/drop README.md terman_os_documentacao.md"

echo "✅ Finalizado. O contexto do Aider foi totalmente orquestrado por etapas."