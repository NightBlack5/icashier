# Design

## Context

O CashSave possui rotas públicas e protegidas implementadas em Reflex. A
apresentação precisa funcionar como um artefato estático e não pode depender
de uma sessão autenticada estar disponível para o leitor. Ver a
`proposal.md` para a motivação e o escopo.

## Goals / Non-Goals

**Goals:**

- produzir HTML responsivo com identidade visual coerente com o CashSave;
- incluir imagens reais capturadas do runtime sempre que acessíveis;
- distinguir visualmente telas públicas, telas protegidas e limitações de
  captura;
- gerar PDF navegável/compartilhável a partir da apresentação;
- manter todos os artefatos dentro de `docs/`.

**Non-Goals:**

- alterar páginas, estado, APIs, dependências ou configuração do aplicativo;
- criar mockups que se passem por capturas reais;
- afirmar funcionamento autenticado sem Xano publicado e conta de teste;
- capturar ou armazenar credenciais reais.

## Decisions

1. **Capturas via navegador real.** Usar o servidor Reflex e Playwright/browser
   para capturar as rotas públicas e, quando houver sessão segura disponível,
   as rotas protegidas. Isso é preferível a reconstruir a interface em imagens,
   pois preserva evidência visual do produto.
2. **Apresentação autocontida.** O HTML usará referências relativas às imagens
   versionadas em `docs/assets/screenshots/`, sem CDN ou imagens genéricas.
   Assim o material continua funcionando offline depois de aberto no projeto.
3. **PDF derivado do HTML.** Gerar o PDF com Chromium/Playwright ou ferramenta
   equivalente disponível no ambiente, mantendo o mesmo layout, tipografia,
   cores e legendas. Se a conversão local não estiver disponível, registrar a
   limitação em vez de gerar um PDF falso ou incompleto.
4. **Conteúdo curto e visual.** A apresentação resumirá a documentação
   demonstrativa existente em blocos de produto, galeria, fluxos, tecnologia,
   diferenciais e limitações, evitando duplicar o relatório técnico.
5. **Dados demonstrativos controlados.** Não preencher formulários autenticados
   nem capturar dados pessoais. Quando uma conta não estiver disponível, as
   telas protegidas serão documentadas com uma indicação explícita de que a
   captura E2E requer ambiente de demonstração.
6. **Impressão própria para o PDF.** A captura mobile terá uma composição
   dedicada no modo de impressão, com largura legível e legenda ao lado. As
   demais imagens terão limites de altura e a página usará margens A4 explícitas
   para evitar conteúdo comprimido ou cortado.

## Risks / Trade-offs

- **[Runtime indisponível]** → capturar as rotas públicas somente e registrar
  as rotas protegidas como não capturadas; não substituir por imagens inventadas.
- **[Xano/credenciais ausentes]** → não executar login real nem incluir valores
  sensíveis; incluir um quadro de pré-requisitos para a demonstração completa.
- **[Conversor PDF ausente]** → tentar a ferramenta disponível no ambiente e
  reportar a verificação pendente se nenhuma existir.
- **[Alterações no layout do app]** → manter as imagens datadas e legendadas,
  deixando claro que são capturas desta execução.

## Migration Plan

Não há migração de aplicação. Criar os artefatos em `docs/`, validar caminhos
das imagens, abrir o HTML no navegador, gerar o PDF, conferir suas páginas e
deixar o change disponível para revisão.
