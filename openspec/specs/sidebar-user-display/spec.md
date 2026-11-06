# sidebar-user-display Specification

## Purpose

Mantém a identificação do usuário legível na barra lateral sem permitir que nomes longos ultrapassem os limites do menu ou cubram o conteúdo principal.

## Requirements

### Requirement: conter nome longo

O sistema SHALL limitar o nome exibido à largura disponível no bloco lateral e usar reticências quando o texto não couber.

#### Scenario: nome extenso

- **WHEN** o usuário possui um nome maior que o espaço disponível
- **THEN** o menu permanece contido e o nome é exibido truncado com reticências

### Requirement: preservar identificação completa

O sistema SHALL manter o nome completo disponível para tecnologias assistivas ou inspeção do elemento.

#### Scenario: nome truncado

- **WHEN** o nome visual é truncado
- **THEN** o elemento mantém o nome completo como descrição acessível

