# assistant-expense-write Specification

## Purpose

TBD: Update Purpose after archive.

## Requirements

### Requirement: interpretar comando claro

O sistema SHALL montar um payload de despesa para o usuário autenticado quando a mensagem contiver intenção de cadastro, valor positivo em reais e descrição não vazia.

#### Scenario: comando com valor e categoria

- **WHEN** a pessoa envia "gastei R$ 25,90 em transporte"
- **THEN** o sistema monta uma despesa de 2590 centavos e resolve a categoria

### Requirement: não gravar comando ambíguo

O sistema SHALL informar o campo ausente ou ambíguo e SHALL NOT chamar o endpoint de criação quando faltar valor, descrição ou houver categoria/conta não resolvida de forma inequívoca.

#### Scenario: comando sem valor

- **WHEN** a pessoa envia um comando de despesa sem valor
- **THEN** o sistema recusa o comando e não chama o endpoint de criação

### Requirement: confirmar persistência

O sistema SHALL atualizar o estado local e informar que a despesa foi cadastrada somente quando o Xano retornar uma transação com `id`; em erro ou resposta sem `id`, SHALL NOT apresentar sucesso.

#### Scenario: Xano confirma lançamento

- **WHEN** o endpoint retorna uma transação com `id`
- **THEN** a transação é adicionada ao estado local e a assistente informa sucesso

### Requirement: envio por Enter

O campo de mensagem SHALL submeter a mesma ação ao pressionar Enter e ao clicar no botão de envio.

#### Scenario: envio pelo formulário

- **WHEN** a pessoa pressiona Enter no campo de mensagem
- **THEN** o evento de envio da assistente é executado
