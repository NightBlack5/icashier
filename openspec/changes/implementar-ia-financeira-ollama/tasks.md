# Tasks

## Planejamento e arquitetura

- [x] 1. Criar serviços puros para cliente Ollama, contexto, cálculos,
  orquestração e validação de respostas.
- [x] 2. Configurar variáveis de ambiente, limites e documentação sem instalar
  Ollama ou baixar modelos automaticamente.

## Integração

- [x] 3. Integrar a assistente local ao `AppState` com sessão, histórico limitado,
  loading, erros explícitos e sem escritas no Xano.
- [x] 4. Atualizar a interface existente para indicar o modo local e distinguir
  dados observados, calculados e estimados quando disponível.

## Testes e verificação

- [x] 5. Adicionar testes para Ollama, cálculos, projeções, metas, limites,
  respostas inválidas, timeout, indisponibilidade e isolamento.
- [x] 6. Executar testes, compilação Reflex e validação OpenSpec; documentar
  resultados reais e limitações da ausência de Ollama/modelo.
