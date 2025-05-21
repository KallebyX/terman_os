#!/bin/bash

# CONFIGURAÇÃO DAS CHAVES
OPENAI_KEY=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
OPENROUTER_KEY=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
ANTHROPIC_API_KEY=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
REPO_PATH="."  # Caminho do repositório

check_openai_model_access() {
    MODEL=$1
    RESPONSE=$(curl -s https://api.openai.com/v1/models \
        -H "Authorization: Bearer $OPENAI_KEY" | grep -F "\"id\": \"$MODEL\"")
    [[ -n "$RESPONSE" ]]
}

check_claude_direct() {
    RESPONSE=$(curl -s https://api.anthropic.com/v1/models \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01")
    [[ "$RESPONSE" == *"claude-3-sonnet-20240229"* ]]
}

echo "🎯 Iniciando análise inteligente de modelo disponível..."

if check_openai_model_access "gpt-4o"; then
    echo "✅ Usando GPT-4o com OpenAI..."
    aider "$REPO_PATH" --model gpt-4o --openai-api-key "$OPENAI_KEY"

elif check_openai_model_access "gpt-3.5-turbo"; then
    echo "⚠️ GPT-4o indisponível. Usando GPT-3.5-turbo com OpenAI..."
    aider "$REPO_PATH" --model gpt-3.5-turbo --openai-api-key "$OPENAI_KEY"

elif check_claude_direct; then
    echo "✨ Usando Claude 3 Sonnet via API da Anthropic..."
    ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" aider "$REPO_PATH" --model claude-3-sonnet-20240229

else
    echo "🔁 Nenhum modelo OpenAI nem Claude via API direta disponível. Verificando OpenRouter..."
    RESPONSE=$(curl -s https://openrouter.ai/api/v1/models \
        -H "Authorization: Bearer $OPENROUTER_KEY")

    if [[ "$RESPONSE" == *"mistralai/mistral-7b-instruct"* ]]; then
        echo "💨 Usando Mistral via OpenRouter..."
        aider "$REPO_PATH" --model mistralai/mistral-7b-instruct:free --openrouter-api-key "$OPENROUTER_KEY"
    else
        echo "🚨 Nenhum modelo disponível no momento. Verifique suas chaves de API."
        exit 1
    fi
fi