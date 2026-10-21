# Checkboxes de autenticação

## ADDED Requirements

### Requirement: alternar aceite de termos
O checkbox de cadastro SHALL alternar o estado de aceite ao ser clicado.

#### Scenario: aceitar termos
- **WHEN** a pessoa clica em “Concordo com o uso dos meus dados”
- **THEN** o checkbox muda visualmente e o cadastro pode prosseguir

### Requirement: alternar lembrança
O checkbox de login SHALL alternar o estado de “Lembrar de mim” e persistir a
preferência.

#### Scenario: desativar lembrança
- **WHEN** a pessoa desmarca “Lembrar de mim”
- **THEN** o e-mail não é salvo na preferência local
