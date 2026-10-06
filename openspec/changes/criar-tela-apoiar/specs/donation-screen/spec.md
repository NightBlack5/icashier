## Purpose

Apresentar a tela de apoio ao projeto com Pix, QR Code e botão para copiar a chave.

## ADDED Requirements

### Requirement: Tela Apoiar o CashSave
O sistema SHALL exibir na rota `/apoiar` o texto de apoio ao projeto, o QR Code, a chave Pix e um botão para copiar a chave.

#### Scenario: Abrir a tela de apoio
- **WHEN** o usuário abre a rota `/apoiar`
- **THEN** o texto, o QR Code e a chave Pix são exibidos

### Requirement: Copiar a chave Pix
O botão de cópia SHALL colocar a chave Pix na área de transferência do usuário.

#### Scenario: Clicar em copiar
- **WHEN** o usuário clica em "Copiar chave Pix"
- **THEN** a chave Pix é copiada para a área de transferência
