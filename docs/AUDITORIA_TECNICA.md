# Auditoria técnica do CashSave

**Data:** 2026-10-19  
**Escopo:** diagnóstico somente leitura do repositório, execução local e
definições versionadas do Xano. Nenhum dado remoto foi criado, alterado ou
apagado.

## 1. Resumo executivo

O CashSave é uma aplicação Reflex/Python com frontend e backend de eventos
servidos pelo Reflex e persistência/autenticação delegadas a um grupo de APIs
Xano. A aplicação compila e o servidor local responde às rotas registradas.
As páginas públicas e a tela de login renderizam, e os testes unitários
existentes passam.

O estado não é pronto para demonstrar fluxos autenticados como funcionais. Foi
encontrado um defeito P1 em que o cliente envia o literal `******` no cabeçalho
de autorização em vez do token recebido do Xano. O teste atual confirma esse
comportamento, portanto ele não protege o comportamento esperado. O mesmo
ambiente também exibiu a notificação visual `Connection Error` do Reflex; os
assets HTTP carregaram, mas a conexão de eventos não foi comprovada.

As definições `.xs` mostram boa intenção de isolamento por `usuario_id`,
autenticação nos endpoints de dados e armazenamento monetário em centavos.
Isso não prova que o workspace remoto esteja publicado com o mesmo conteúdo.

## 2. Arquitetura identificada

- **UI e runtime:** Reflex 0.9.12, Python, componentes em
  [CashSave/CashSave.py](../CashSave/CashSave.py) e
  [CashSave/pages/](../CashSave/pages/).
- **Estado e integração:** [CashSave/state.py](../CashSave/state.py), com
  eventos Reflex, `urllib.request`, JSON e chamadas HTTP ao grupo Xano.
- **Persistência:** tabelas e endpoints versionados em [xano/](../xano/);
  não há banco local nem ORM no aplicativo.
- **Configuração:** [rxconfig.py](../rxconfig.py), [requirements.txt](../requirements.txt)
  e [.env.example](../.env.example). Valores reais de `.env` não foram
  reproduzidos.
- **Páginas registradas:** `/`, `/login`, `/cadastro`, `/app`, `/assistente`,
  `/financas`, `/calendario`, `/perfil`, `/sobre`, `/suporte` e `/apoiar`,
  conforme [CashSave/CashSave.py](../CashSave/CashSave.py:1061).

## 3. Inventário funcional

| Funcionalidade | Estado | Evidência |
|---|---|---|
| Landing page e navegação âncora | Aprovado localmente | HTTP 200 e conteúdo renderizado em `/` |
| Login/cadastro: campos, obrigatoriedade e mensagens locais | Parcial | Componentes em [auth.py](../CashSave/pages/auth.py), validação em [state.py](../CashSave/state.py:909) |
| Autenticação real Xano | Falhou | Cabeçalho literal em [state.py](../CashSave/state.py:69) |
| Sessão por cookie | Parcial | `rx.Cookie`, `same_site="strict"` e `max_age=86400` em [state.py](../CashSave/state.py:268); runtime completo não foi comprovado |
| Dashboard, finanças, calendário e perfil sem sessão | Parcial | Rotas respondem, mas mostram estado de login; dados reais não são carregados |
| CRUD de transações, contas, contas a pagar, orçamentos e metas | Não verificado | Código e endpoints existem; requer token funcional e conta de teste |
| Filtros, resumos e gráficos | Parcial | Cálculos locais em [state.py](../CashSave/state.py:386); sem confirmação com dados remotos |
| Assistente de IA | Não verificado | Endpoint e UI existem; depende de Xano AI e autenticação |
| Upload de avatar | Parcial | Validação de extensão, assinatura e limite de 5 MB em [state.py](../CashSave/state.py:1770); upload remoto não foi exercitado |
| Suporte/FAQ | Aprovado localmente | FAQ abriu no navegador; links sociais internos são placeholders |
| Logout | Não verificado | Evento existe, mas conexão de eventos e sessão real não foram comprovadas |

## 4. Diagnóstico de persistência e modelo

### Implementado

- As tabelas financeiras usam inteiros em centavos, por exemplo
  [transacoes.xs](../xano/table/transacoes.xs) e
  [contas_a_pagar.xs](../xano/table/contas_a_pagar.xs).
- Há índices por usuário e por campos usados em listagens.
- O endpoint [resumo_GET.xs](../xano/api/cashsave/resumo_GET.xs) filtra
  transações, contas, contas a pagar, orçamentos, metas, recorrências e
  preferências por `$auth.id`.
- Endpoints de escrita revisados usam `auth = "user"` e validam referências de
  conta, categoria, recorrência ou registro do usuário. Exemplos:
  [transacoes_POST.xs](../xano/api/cashsave/transacoes_POST.xs) e
  [transacao_id_DELETE.xs](../xano/api/cashsave/transacoes/transacao_id_DELETE.xs).
- A tabela de usuário possui email único e senha com filtros mínimos em
  [user.xs](../xano/table/user.xs).
- O cliente usa `Decimal` e arredondamento explícito para conversão monetária
  em [state.py](../CashSave/state.py:150).

### Não comprovado ou ausente

- Não existe conexão local com um banco para verificar registros, migrações,
  transações, backup, restauração ou persistência após reinicialização.
- Não foi possível comprovar que as definições `.xs` estão sincronizadas com o
  workspace Xano remoto.
- Não foi encontrado fluxo local de transferência entre contas, parcelamento,
  reconciliação bancária ou cálculo de saldo por conta; o `saldo_total` é
  calculado a partir das transações do mês em [state.py](../CashSave/state.py:405).
- Não há evidência de transação atômica envolvendo a criação de usuário e a
  criação de preferências em [signup_POST.xs](../xano/api/cashsave/auth/signup_POST.xs).
  Se a segunda escrita falhar no Xano, a conta pode ficar parcialmente criada;
  isso requer confirmação da semântica transacional do ambiente.
- A conta inicial aceita saldo opcional no endpoint
  [contas_POST.xs](../xano/api/cashsave/contas/contas_POST.xs), mas a revisão não
  confirmou limites de negócio para valores negativos além do contrato de dados.

## 5. Documentação e consistência

O [README.md](../README.md) documenta criação do ambiente, `.env`, comando de
produção local, testes e a limitação de depender do Xano. Isso corresponde ao
fluxo observado em parte.

Discrepâncias e lacunas:

1. O README não alerta que o teste atual de autorização espera
   `******` nem que essa implementação impede fluxos autenticados.
2. O README não documenta um smoke test rota a rota, apesar de a mudança
   `corrigir-prerender-e-testar-app` exigir esse procedimento.
3. Não há documentação dos contratos de payload/resposta dos endpoints Xano,
   nem de como confirmar a publicação das definições em `xano/`.
4. O comando `python -m unittest discover -s tests -v` documentado só cobre
   quatro testes; não há cobertura de rotas, CRUD, expiração de sessão ou
   respostas HTTP reais.
5. O README informa que a URL local é “por padrão” 3000; o log confirmou 3000
   nesta execução, mas a porta deve continuar sendo obtida do log.

## 6. Segurança

### Revisão realizada

A revisão de segurança foi somente leitura. Não foram encontradas
vulnerabilidades concretas adicionais no escopo revisado. O código evita
imprimir o token em mensagens e valida formato de URL, valores monetários,
assinaturas básicas de imagens e nomes de arquivo.

As definições Xano revisadas usam autenticação e filtros por usuário na camada
de API. Isso é uma evidência positiva, não uma prova do ambiente publicado.

### Limitações de segurança

Não foi possível verificar, sem ambiente externo ou conta dedicada:

- se endpoints e filtros publicados são idênticos aos `.xs`;
- se credenciais remotas estão ativas ou revogadas;
- comportamento final de `HttpOnly` dos cookies no runtime instalado;
- HTTPS, CSP, CORS, cabeçalhos de segurança, proxy reverso e origem WebSocket;
- vulnerabilidades das versões instaladas contra uma base externa;
- comportamento de upload e `Content-Disposition` no serviço remoto;
- CSRF e autorização ponta a ponta contra Xano.

## 7. Qualidade e arquitetura

Pontos positivos:

- Separação razoável entre páginas, estado e definições Xano.
- Erros de API são convertidos em `XanoAPIError` com status HTTP.
- Uso de `Decimal` para entrada e formatação monetária.
- Validação local de senha, telefone, email, arquivo e formulários principais.
- Proteção de sessão limpa os dados locais quando há resposta 401 em fluxos
  revisados.

Riscos de manutenção:

- [state.py](../CashSave/state.py) concentra aproximadamente dois mil linhas,
  estado, HTTP, validação, transformação, regras financeiras e upload.
- Os componentes de página têm responsabilidades e estilos repetidos.
- A disponibilidade dos endpoints é parcialmente detectada por respostas
  e flags, em vez de um contrato centralizado de capacidades.
- A auditoria encontrou strings de desenvolvimento em
  [CashSave.py](../CashSave/CashSave.py:912), indicando pelo menos uma página
  explicitamente incompleta.

## 8. Testes e execução realizados

| Verificação | Resultado | Evidência |
|---|---|---|
| `reflex compile --dry` no ambiente do projeto | Aprovado | Compilação Reflex 0.9.12 concluída |
| `python -m unittest discover -s tests -v` no ambiente do projeto | Aprovado | 4 testes, 4 OK |
| `python -m compileall -q CashSave tests` | Aprovado | `compileall=passed` |
| `pip check` | Não verificado | O ambiente `.venv-cashsave` não possui módulo `pip` |
| Servidor `reflex run --env prod --single-port` | Aprovado parcialmente | Log em [reflex.log](../reflex.log) indica porta 3000 |
| Rotas registradas | Aprovado para HTTP/renderização | 10 rotas retornaram 200 |
| Rota inexistente | Aprovado | `/rota-inexistente` retornou 404 |
| Conexão Reflex de eventos | Falhou/Parcial | UI mostrou `Connection Error`; assets HTTP retornaram 200 |
| Fluxos Xano reais | Não verificado | Sem conta de teste e sem alteração remota |

### Rotas verificadas no navegador

`/`, `/login`, `/cadastro`, `/app`, `/financas`, `/calendario`, `/assistente`,
`/perfil`, `/sobre`, `/suporte` e `/apoiar` responderam HTTP 200. As rotas
protegidas exibiram o estado não autenticado. A FAQ de suporte abriu uma
resposta corretamente. Os assets observados carregaram sem `requestfailed`.

## 9. Problemas classificados

### P1-001 — Token de autorização não é enviado

- **Prioridade:** P1 — alto; bloqueia a funcionalidade essencial autenticada.
- **Estado:** reproduzido; não corrigido nesta auditoria.
- **Evidência:** [state.py](../CashSave/state.py:69) atribui
  `headers["Authorization"] = f"******"` quando existe token. O teste
  [test_xano_auth.py](../tests/test_xano_auth.py:23) confirma exatamente esse
  literal.
- **Reprodução segura:** executar o teste
  `test_sends_session_token_as_bearer_authorization` e inspecionar o header
  capturado pelo mock.
- **Impacto:** login pode obter um token, mas chamadas subsequentes a
  `resumo`, CRUD, perfil e assistente recebem uma autorização inválida.
- **Causa provável:** mascaramento de segredo aplicado no valor real do header,
  em vez de ser usado apenas em logs/testes.
- **Correção recomendada:** enviar o token real no header com o esquema exigido
  pelo Xano e manter qualquer mascaramento restrito a logs; atualizar o teste
  para validar o valor real fornecido pelo fixture.
- **Teste necessário:** mockar um token sentinela não secreto e afirmar
  `Authorization == "Bearer <sentinela>"`, além de testar 401 e limpeza da
  sessão.

### P1-002 — Conexão de eventos Reflex não comprovada

- **Prioridade:** P1 — alto; pode bloquear todos os eventos interativos.
- **Estado:** reproduzido no navegador.
- **Evidência:** a região de notificação mostrou `Connection Error` em páginas
  públicas e protegidas; HTTP e assets, porém, retornaram 200.
- **Impacto:** cliques podem renderizar, mas não executar eventos no backend,
  impedindo autenticação, CRUD e logout.
- **Causa provável:** não determinada; pode ser configuração de WebSocket/event
  backend ou incompatibilidade entre servidor e build. O literal de
  autorização é um problema distinto de API.
- **Correção recomendada:** capturar handshake/event endpoint no navegador,
  correlacionar com logs do processo e validar a configuração single-port antes
  de alterar o runtime.
- **Teste necessário:** smoke test que aguarde conexão sem notificação de erro e
  execute um evento local não destrutivo.

### P2-001 — Cobertura não prova os fluxos financeiros

- **Prioridade:** P2 — médio.
- **Estado:** confirmado como lacuna.
- **Evidência:** existem apenas quatro testes em
  [tests/test_xano_auth.py](../tests/test_xano_auth.py), cobrindo header mockado
  e parsing de local storage; não há testes de CRUD, 401, valores inválidos,
  isolamento, upload ou assistente.
- **Impacto:** regressões financeiras podem passar sem detecção.
- **Correção recomendada:** adicionar testes unitários isolados para cada evento
  de escrita, respostas HTTP de sucesso/erro, sessão expirada e cálculos em
  centavos; adicionar smoke de rotas sem Xano.

### P2-002 — Transação de cadastro potencialmente parcial

- **Prioridade:** P2 — médio, hipótese dependente do Xano.
- **Estado:** não confirmado no ambiente remoto.
- **Evidência:** [signup_POST.xs](../xano/api/cashsave/auth/signup_POST.xs)
  adiciona `user`, depois `preferencias_usuario`, sem transação explícita no
  arquivo.
- **Impacto:** falha intermediária pode deixar uma conta sem preferências.
- **Correção recomendada:** confirmar a atomicidade do Xano; se não houver,
  usar mecanismo transacional ou rotina compensatória idempotente.
- **Teste necessário:** teste de falha controlada entre as duas escritas em
  workspace descartável.

### P3-001 — Documentação de operação e contratos incompleta

- **Prioridade:** P3 — baixo.
- **Estado:** confirmado.
- **Evidência:** [README.md](../README.md) não lista rotas, smoke test,
  contratos Xano ou procedimento de confirmação do workspace.
- **Impacto:** configuração e diagnóstico dependem de conhecimento local.
- **Correção recomendada:** documentar rotas, testes, limites Xano e
  troubleshooting de WebSocket sem incluir segredos.

### P3-002 — Links sociais do suporte são placeholders

- **Prioridade:** P3 — baixo.
- **Estado:** confirmado visualmente.
- **Evidência:** [suporte.py](../CashSave/pages/suporte.py:100) recebe links
  internos `/suporte/` para os botões sociais.
- **Impacto:** usuários não chegam às redes sociais esperadas.
- **Correção recomendada:** substituir por URLs oficiais ou remover os botões
  até que existam destinos definidos.

## 10. Rastreamento

| Área | Item verificado | Resultado | Evidência | Próxima ação |
|---|---|---|---|---|
| Runtime | Compilação Reflex | Aprovado | Comando e saída de compilação | Manter no CI |
| Runtime | Eventos Reflex | Falhou/Parcial | `Connection Error` no browser | Diagnosticar handshake e logs |
| Autenticação | Header de token | Falhou | [state.py](../CashSave/state.py:69) e teste | Corrigir P1-001 |
| Autorização | Filtros Xano por usuário | Parcial | `.xs` com `auth` e `usuario_id` | Comparar com workspace publicado |
| Dados | Valores monetários | Aprovado localmente | Inteiros em centavos e `Decimal` | Adicionar testes de limites |
| Dados | Atomicidade do cadastro | Não verificado | Duas escritas no signup | Testar em workspace descartável |
| UI | Rotas registradas | Aprovado para renderização | HTTP 200 nas 10 rotas | Repetir após corrigir eventos |
| UI | Interatividade autenticada | Não verificado | Sem token funcional | Criar conta de teste isolada |
| Segurança | Segredos no relatório | Aprovado | Valores não expostos | Continuar revisão em CI |
| Segurança | Dependências contra CVE | Não verificado | `pip` ausente e sem auditor externo | Executar auditoria em ambiente com ferramenta aprovada |
| Documentação | Instalação básica | Parcial | README cobre setup principal | Adicionar troubleshooting e rotas |
| Testes | Unidade existente | Aprovado | 4/4 OK | Expandir cobertura P2-001 |

## 11. Plano de correção ordenado

1. Corrigir P1-001 e substituir o teste que cristaliza o literal mascarado.
2. Diagnosticar P1-002 com captura de handshake e logs, sem expor tokens.
3. Reexecutar rotas e eventos após os dois P1; só então testar Xano com conta
   de demonstração isolada.
4. Adicionar testes mocked para autenticação, 401, CRUD financeiro, cálculos
   monetários, uploads inválidos e assistente.
5. Confirmar atomicidade do cadastro e atualizar a definição Xano se necessário.
6. Completar README, contratos e smoke procedure.
7. Executar auditoria de dependências e revisão de headers no ambiente de
   implantação.

## 12. Limitações

- Não foi usado token, conta de usuário ou escrita real no Xano.
- Não foi possível verificar dados, índices efetivos, migrações, backups ou
  publicação remota.
- O teste de navegador confirmou HTML/HTTP e algumas interações, não a
  persistência real.
- O ambiente virtual não possui `pip`, então não foi executado um `pip check`
  nem auditoria de CVEs.
- A revisão de segurança não encontrou falhas concretas adicionais, mas não
  substitui teste de implantação, proxy, headers, WebSocket e Xano publicados.
- Alterações preexistentes em [state.py](../CashSave/state.py),
  [README.md](../README.md), `tests/` e mudanças OpenSpec foram preservadas;
  esta auditoria não as reverteu.
