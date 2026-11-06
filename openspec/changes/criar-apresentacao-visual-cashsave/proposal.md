# Proposal

## Why

O projeto possui uma documentação textual, mas ainda não oferece um material
visual adequado para demonstrar o CashSave a usuários, clientes ou investidores.
Uma apresentação responsiva, com capturas reais do aplicativo e uma versão PDF,
permitirá conhecer o produto sem depender da execução local.

## What Changes

- Criar uma apresentação HTML responsiva em `docs/APRESENTACAO.html`.
- Capturar telas reais do CashSave executado localmente, quando o ambiente
  permitir, e organizá-las em `docs/assets/screenshots/`.
- Incorporar as capturas na apresentação com legendas e explicações curtas.
- Gerar `docs/APRESENTACAO.pdf` a partir do material visual.
- Registrar limitações explícitas quando uma tela autenticada ou operação
  depender de Xano, credenciais de demonstração ou serviço externo.

## Capabilities

### New Capabilities

Nenhuma. Esta é uma entrega documental e visual; não altera requisitos ou
comportamento do aplicativo.

### Modified Capabilities

Nenhuma.

## Impact

- Afeta somente arquivos de documentação e artefatos visuais em `docs/`.
- Pode usar o servidor Reflex, navegador automatizado e ferramentas de
  conversão HTML/PDF durante a geração, sem alterar o código principal.
- Não altera APIs, banco, dependências ou comportamento de runtime.
