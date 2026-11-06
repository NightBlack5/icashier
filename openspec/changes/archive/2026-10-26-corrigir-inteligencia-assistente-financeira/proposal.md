# Corrigir inteligência da assistente financeira

## Objetivo

Impedir que a assistente invente fatos sobre o CashSave ou afirme que executou
operações financeiras que a primeira versão não suporta. Perguntas baseadas nos
dados disponíveis devem priorizar cálculos verificáveis, enquanto pedidos de
escrita devem receber uma negativa clara.

## Escopo

- Classificação local de pedidos de escrita e perguntas financeiras observáveis.
- Respostas determinísticas para totais, saldo, categorias, orçamentos e metas.
- Prompt mais restritivo para perguntas educativas encaminhadas ao Ollama.
- Testes para o caso mostrado, alucinação de identidade e bloqueio de escrita.

## Fora de escopo

- Permitir criação, edição ou exclusão de registros pela IA.
- Treinar ou trocar o modelo Ollama.
