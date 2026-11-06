# Tasks

## 1. Captura e organização de evidências

- [x] 1.1 Iniciar o CashSave em modo de produção local e verificar a porta no log; confirmar que a landing page responde no navegador.
- [x] 1.2 Capturar as rotas públicas disponíveis (`/`, `/login`, `/cadastro`, `/sobre`, `/suporte` e `/apoiar`) em `docs/assets/screenshots/`, verificando que cada arquivo é uma imagem real do runtime.
- [x] 1.3 Verificar a possibilidade de usar uma sessão de demonstração isolada para rotas protegidas; registrar que `/app` redireciona para `/login` sem sessão e não criar capturas falsas.
- [x] 1.4 Verificar a disponibilidade das rotas protegidas e capturar a landing page em largura mobile; registrar que dashboard, finanças, calendário, Jarvis e perfil exigem sessão Xano não disponível neste ambiente.

## 2. Apresentação visual

- [x] 2.1 Criar `docs/APRESENTACAO.html` com layout responsivo, capa, navegação interna, galeria, telas individuais, fluxos, tecnologias, diferenciais e considerações finais; verificar que o arquivo abre sem dependências externas.
- [x] 2.2 Inserir somente capturas existentes em `docs/assets/screenshots/`, com legendas, texto alternativo e indicação de limitações; verificar que não há referências quebradas.
- [x] 2.3 Gerar `docs/APRESENTACAO.pdf` a partir do HTML usando uma ferramenta disponível; verificar existência, número de páginas e renderização das imagens.

## 3. Validação integrada

- [x] 3.1 Abrir o HTML e o PDF gerados, conferir capa, galeria, links internos, imagens e versão mobile; corrigir apenas problemas dos artefatos de apresentação.
- [x] 3.2 Executar `openspec validate criar-apresentacao-visual-cashsave` e `git diff --check`; confirmar que nenhuma alteração ocorreu no código principal.
- [x] 3.3 Ajustar o modo de impressão para que a captura mobile permaneça legível no PDF, com composição própria, margens A4 e limites de altura para as demais capturas.
- [x] 3.4 Corrigir a revisão visual do PDF: impressão A4 horizontal, contraste dos cards, quebra controlada por seção, galeria sem cortes e composição editorial responsiva sem ampliar a captura mobile estreita.
