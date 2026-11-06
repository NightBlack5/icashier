# Design

## Context

O CashSave é uma aplicação Reflex em Python com autenticação e persistência
delegadas ao grupo de APIs Xano, além de uma integração opcional com Ollama
local e geração de relatórios de despesas via ReportLab. O repositório contém
capturas reais das rotas públicas e documentação que registra que as rotas
protegidas dependem de sessão e ambiente Xano. A entrega anterior em
`docs/APRESENTACAO.html` serve como referência visual, mas não cobre a
narrativa técnica de um case study.

## Goals / Non-Goals

**Goals:**

- Criar uma narrativa curta, visual e orientada a recrutadores.
- Usar imagens reais disponíveis e sinalizar claramente limites de validação.
- Explicar arquitetura e decisões técnicas com diagramas vetoriais no próprio
  HTML, mantendo texto selecionável.
- Entregar PDF A4 horizontal com layout editorial controlado, numeração e
  campos editáveis para identificação profissional.

**Non-Goals:**

- Alterar telas, APIs, banco, dependências ou código de runtime.
- Criar capturas falsas de dashboard autenticado, Finanças, Calendário, Jarvis
  ou Perfil.
- Preencher nome, links ou contatos não encontrados no projeto.

## Decisions

1. **HTML/CSS como fonte e Chromium como renderer.** Evita rasterizar o texto,
   mantém busca/cópia no PDF e permite paginação via `@page` e regras de
   impressão. Uma imagem única ou montagem em editor externo teria pior
   acessibilidade e texto não selecionável.
2. **A4 landscape.** A largura extra acomoda screenshots de interface,
   diagramas e colunas técnicas sem reduzir a tipografia. Cada seção será
   estruturada como uma página ou conjunto curto de páginas, com
   `break-before` explícito onde necessário.
3. **Paleta derivada do produto.** Fundo grafite, verde CashSave e acentos
   azul/âmbar distinguem produto, arquitetura e notas de verificação.
4. **Evidência em camadas.** A galeria usa os PNGs reais existentes. Um selo
   diferencia “capturado no runtime”, “implementado no código” e “depende de
   ambiente externo”, evitando claims além da evidência.
5. **Diagrama em SVG inline.** O fluxo Browser → Reflex → Xano e o caminho
   opcional Ollama serão desenhados como SVG no HTML, preservando nitidez e
   texto sem adicionar dependência.
6. **Revisão por renderização.** O HTML será aberto localmente, o PDF será
   gerado com um perfil Chrome isolado, e cada página será rasterizada para
   inspeção visual; também serão verificadas assinatura, quantidade de páginas,
   referências de assets e presença de texto.

## Risks / Trade-offs

- **[Rotas protegidas não capturáveis]** → mostrar a limitação explicitamente e
  usar somente evidências públicas, código e testes para descrever o restante.
- **[PDF muito denso]** → limitar cada página a uma mensagem principal,
  utilizar cartões curtos e mover detalhes para legenda ou nota.
- **[Fontes externas indisponíveis offline]** → usar pilha de fontes do sistema,
  sem CDN ou recursos remotos.
- **[Capturas com dados demonstrativos]** → reutilizar somente os arquivos já
  presentes no repositório e não incluir novos dados pessoais.

## Migration Plan

1. Criar os artefatos em `portfolio/` e copiar as capturas reais para
   `portfolio/assets/`.
2. Gerar o PDF com Chromium em perfil temporário isolado.
3. Renderizar todas as páginas para PNG, revisar visualmente e ajustar o HTML.
4. Validar o change, caminhos, texto selecionável e integridade do PDF.
5. Não há migração nem rollback de aplicação; remover somente temporários de
   renderização após a revisão.
