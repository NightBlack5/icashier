# Design: criar-tela-apoiar

## Context

O CashSave é gratuito e aceita apoio opcional dos usuários. A tela explica o projeto e oferece o Pix.

## Decisions

1. A chave Pix fica em uma constante e a imagem do QR Code em `assets/qrcode_pix.png`.
2. A chave real deve ser definida por quem vai receber os apoios; o projeto não usa a chave da versão antiga.

Nota de processo: esta mudança foi documentada em formato OpenSpec depois de a implementação já ter sido feita. As mudanças seguintes seguem a ordem proposta, specs, design, tarefas e só então código.
