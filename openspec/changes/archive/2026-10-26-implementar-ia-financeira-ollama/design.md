# Design

## Fluxo

1. `AppState` valida sessão e limita a pergunta.
2. `FinancialContextService` recebe somente listas financeiras já carregadas no
   estado atual do usuário.
3. `FinancialCalculator` produz números determinísticos em centavos e
   projeções com premissas identificadas.
4. `FinancialOrchestrator` classifica a intenção, monta um contexto mínimo e
   solicita ao `OllamaClient` uma resposta em português.
5. `ResponseValidator` valida o envelope JSON, limita o texto e rejeita números
   ou campos ausentes quando o contrato não for respeitado.
6. O estado atualiza somente mensagens locais; não há escrita em Xano.

## Limites e segurança

- O cliente usa `OLLAMA_BASE_URL` local, modelo configurável, timeout e limites
  de pergunta, contexto, histórico e resposta.
- O navegador nunca chama Ollama diretamente.
- O prompt instrui o modelo a distinguir observado, calculado e estimado e a
  não inventar dados.
- O contexto não inclui token, credenciais, identificadores desnecessários ou
  registros de outros usuários.
- Falhas de conexão, timeout e JSON inválido viram mensagens explícitas sem
  fallback que pareça resposta financeira válida.

## Compatibilidade

O módulo será Python puro, sem dependência obrigatória de SDK externo, para que
os testes possam usar mocks e o CashSave continue compilando mesmo sem Ollama.
