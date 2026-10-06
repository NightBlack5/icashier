# Design: configurar-ambiente-reflex

## Context

A disciplina pede a inicialização do projeto e a configuração do ambiente com Reflex. Sem essa base não é possível construir as telas nem integrar o backend.

## Decisions

1. Python + Reflex é a tecnologia exigida pela disciplina para o frontend e a lógica da aplicação.
2. A versão do Reflex é fixada em `requirements.txt` para evitar quebras por mudança de API.

## Risks / Trade-offs

A API do Reflex pode mudar entre versões; por isso a versão é fixada.

Nota de processo: esta mudança foi documentada em formato OpenSpec depois de a implementação já ter sido feita. As mudanças seguintes seguem a ordem proposta, specs, design, tarefas e só então código.
