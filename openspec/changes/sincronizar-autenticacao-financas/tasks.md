# Tarefas

## Implementação já presente no código local
- [x] 1. Criar fluxos de cadastro/login com validação dos dados e controle da sessão.
- [x] 2. Adicionar suporte a upload e remoção de foto de perfil no estado, interface e APIs Xano.
- [x] 3. Expandir o resumo autenticado com os dados financeiros, perfil e preferências usados pela aplicação.
- [x] 4. Adicionar filtros e exportação CSV para transações.
- [x] 5. Adicionar tabela, APIs e processamento de lançamentos recorrentes.
- [x] 6. Adicionar contribuição a metas e preferências/notificações relacionadas a metas.
- [x] 7. Aplicar máscara brasileira progressiva ao telefone durante o cadastro.

## Verificação pendente
- [ ] 1. Publicar as alterações Xano e validar cadastro, perfil e fluxos financeiros de ponta a ponta. A definição local agora exige `password_valid == true`; a validação remota de 2026-10-21 encontrou login aceitando senha incorreta e o endpoint `resumo` publicado sem todos os campos versionados. A publicação requer acesso administrativo ao workspace Xano.
- [ ] 2. Confirmar no navegador o processamento e gerenciamento de recorrências, filtros/CSV e notificações. O endpoint remoto `recorrencias` ainda responde HTTP 404.
