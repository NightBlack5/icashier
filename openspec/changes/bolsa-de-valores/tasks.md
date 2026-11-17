# Tasks

## 1. Fundacao e dados de mercado

- [x] 1.1 Pesquisar provedores candidatos para B3 e registrar a brapi.dev como alvo selecionado, com cobertura, atraso Pro de cinco minutos, uso comercial em plano pago e exigencia de credencial/termos aplicaveis; manter dados indisponiveis ate uma credencial valida ser configurada.
- [x] 1.2 Criar o contrato normalizado de dados de mercado, adaptador server-side e cache limitado pelos termos do provedor; verificar por testes quotes, timestamps, estado atrasado, limite de requisicoes, erros, dados ausentes e configuracao sem credenciais.
- [x] 1.3 Adicionar a rota e navegacao autenticadas Bolsa de Valores e um dashboard responsivo para indicadores disponiveis; verificar compilacao e estados com dados, carregamento, erro e provedor nao configurado, sem numeros ficticios.

## 2. Exploracao e detalhes de ativos

- [x] 2.1 Implementar pesquisa por codigo/nome, filtros de acoes/FIIs/ETFs e ordenacao usando apenas ativos suportados pelo provedor; verificar busca, filtros, ordenacao, resultados vazios e falhas com testes.
- [x] 2.2 Implementar detalhes de ativo com cotacao, variacao, metricas especificas da categoria, fonte, referencia temporal e estados de indisponibilidade; verificar que metricas ausentes nao sao inferidas e documentar os campos suportados.
- [x] 2.3 Implementar graficos historicos com periodos suportados e Recharts ja instalado; verificar periodos sem dados, normalizacao temporal, atualizacao de origem e comportamento responsivo por testes.

## 3. Carteira e proventos

- [x] 3.1 Adicionar tabelas e endpoints Xano para operacoes e proventos com autenticacao e verificacao de propriedade por `$auth.id`; validar schemas e testar acesso negado, valores invalidos e que nenhum endpoint aceite proprietario enviado pelo cliente.
- [x] 3.2 Implementar calculos puros com `Decimal` e custo medio ponderado, incluindo custos de compra/venda, venda parcial, venda acima do saldo, resultado realizado e nao realizado; verificar os casos com testes deterministas e valores monetarios em centavos.
- [x] 3.3 Implementar cadastro, edicao e exclusao de operacoes com validacao cronologica e consistencia do historico; testar alteracoes que invalidem vendas posteriores e documentar a semantica de custo medio e arredondamento.
- [x] 3.4 Implementar registro e historico de proventos efetivamente recebidos, distinguindo anunciados de pagos; verificar datas, valores, quantidade elegivel opcional, totais por periodo e isolamento de usuario com testes.

## 4. Analise e ferramentas da carteira

- [x] 4.1 Implementar painel de carteira com custo investido, valor de mercado, resultados separados, rentabilidade, distribuicao, evolucao e proventos; testar precos indisponiveis e garantir que patrimonio investido nao seja somado ao caixa bancario.
- [x] 4.2 Implementar favoritos persistidos em endpoints Xano autenticados; verificar adicao/remocao, cotacoes com origem e isolamento entre usuarios por testes.
- [x] 4.3 Implementar comparacao de dois ou mais ativos em periodos equivalentes e indicadores compativeis; testar series incompletas e categorias distintas sem comparar metricas incompativeis.
- [x] 4.4 Persistir condicoes de alerta e exibir estado nao monitorado enquanto nao houver avaliador em background; testar que nenhum evento/notificacao e apresentado sem avaliacao de cotacao verificada e documentar a limitacao operacional.

## 5. Jarvis e validacao integrada

- [x] 5.1 Estender o contexto do Jarvis existente com calculos da carteira autenticada e contexto verificado do ativo aberto; testar fatos, calculos, ausencia de dados, fonte/horario e rejeicao de dados de outro usuario sem criar nova IA ou historico.
- [x] 5.2 Reutilizar o perfil de investidor existente somente para contextualizacao educativa, sem tratar LocalStorage como permissao ou adequacao garantida; testar perfil ausente, riscos e respostas sem recomendacao personalizada de compra/venda.
- [x] 5.3 Validar fluxo de pesquisa, detalhe, operacoes, proventos, carteira e Jarvis em telas autenticadas; executar `reflex compile --dry`, a suite `unittest`, `openspec validate bolsa-de-valores` e verificacoes responsivas, corrigindo falhas antes de concluir.

## 6. Integracao brapi.dev

- [x] 6.1 Implementar o adaptador brapi.dev para pesquisa, cotacao, historico e movimentos diarios usando somente o contrato normalizado; testar conversao de respostas, erros HTTP e limites de plano com requisicoes simuladas, sem depender de chamadas externas.
- [x] 6.2 Configurar `CASHSAVE_BRAPI_TOKEN` no servidor e documentar o nome sem valor secreto em `.env.example`; testar que a ausencia de token deixa o provedor indisponivel e nunca expoe credenciais no estado ou bundle do navegador.
- [x] 6.3 Redesenhar o topo da Bolsa para priorizar o grafico de altas e listas dos cinco maiores movimentos diarios, usando apenas acoes ativas com volume e variacao verificaveis; mostrar fonte, referencia temporal e atraso de cinco minutos, com estados vazios e testes sem token ou dados e com falhas Xano separadas.
- [x] 6.4 Validar a integracao com `openspec validate bolsa-de-valores`, os testes direcionados e `reflex compile --dry`; corrigir falhas e confirmar que o alerta de rotas Xano permanece separado dos estados de dados de mercado.
