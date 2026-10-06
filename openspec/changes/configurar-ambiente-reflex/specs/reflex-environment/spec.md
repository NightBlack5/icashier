## Purpose

Garantir que o projeto CashSave tenha o ambiente Python e Reflex configurado e possa ser executado localmente.

## ADDED Requirements

### Requirement: Aplicação executável localmente
O sistema SHALL poder ser iniciado com o comando `reflex run` a partir da raiz do projeto, com o ambiente virtual ativo.

#### Scenario: Execução em desenvolvimento
- **WHEN** o desenvolvedor executa `reflex run` na raiz do projeto com o ambiente virtual ativo
- **THEN** a aplicação fica acessível em `http://localhost:3000`

### Requirement: Dependências registradas
O projeto SHALL listar suas dependências Python no arquivo `requirements.txt`, incluindo o Reflex em versão fixa.

#### Scenario: Versão do Reflex
- **WHEN** o arquivo `requirements.txt` é consultado
- **THEN** ele contém a dependência `reflex==0.9.12`
