# Cadastro de despesa por linguagem natural

## ADDED Requirements

### Requirement: interpretar comando claro
Quando uma mensagem contiver intenção de cadastrar uma despesa, valor positivo
em reais e descrição não vazia, o sistema deve montar um payload de despesa
para o usuário autenticado.

#### Scenario: comando com valor e categoria
- **WHEN** a pessoa envia "gastei R$ 25,90 em transporte"
- **THEN** o sistema monta uma despesa de 2590 centavos e resolve a categoria

### Requirement: não gravar comando ambíguo
Quando faltar valor, descrição ou houver categoria/conta não resolvida de forma
inequívoca, o sistema não deve chamar o endpoint de criação e deve informar o
campo ausente ou ambíguo.

#### Scenario: comando sem valor
- **WHEN** a pessoa envia um comando de despesa sem valor
- **THEN** o sistema recusa o comando e não chama o endpoint de criação

### Requirement: confirmar persistência
Quando o Xano retornar uma transação com `id`, o sistema deve atualizar o estado
local e informar que a despesa foi cadastrada. Em erro ou resposta sem `id`,
não deve apresentar sucesso.

#### Scenario: Xano confirma lançamento
- **WHEN** o endpoint retorna uma transação com `id`
- **THEN** a transação é adicionada ao estado local e a assistente informa sucesso

### Requirement: envio por Enter
O campo de mensagem deve continuar submetendo a mesma ação ao pressionar Enter
e ao clicar no botão de envio.

#### Scenario: envio pelo formulário
- **WHEN** a pessoa pressiona Enter no campo de mensagem
- **THEN** o evento de envio da assistente é executado
