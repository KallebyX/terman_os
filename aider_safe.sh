#!/bin/bash

REPO_PATH="."
MAIN_MODEL="gpt-4o"
FALLBACK_MODEL="gpt-3.5-turbo"
MAX_TOKENS=20000  # Limite seguro para evitar falhas
OPENAI_KEY=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  # sua chave aqui

# Comando auxiliar para calcular tokens (simulado)
calculate_tokens() {
  local files="$@"
  wc -c $files | tail -n1 | awk '{print int($1/4)}'  # Aprox: 4 bytes por token
}

run_aider() {
  local files="$@"
  local total_tokens=$(calculate_tokens $files)

  if [ "$total_tokens" -gt "$MAX_TOKENS" ]; then
    echo "⚠️  O conjunto de arquivos ultrapassa ${MAX_TOKENS} tokens (~$((MAX_TOKENS*4/1000)) kB)."
    echo "👉 Reduza os arquivos com '/drop' ou adicione seletivamente com '/add'"
    return 1
  fi

  echo "✅ Iniciando Aider com $total_tokens tokens estimados..."
  aider "$REPO_PATH" --subtree-only --model "$MAIN_MODEL" --openai-api-key "$OPENAI_KEY"
}

# Use: ./aider_safe.sh backend/apps/pos/*.py
run_aider "$@"