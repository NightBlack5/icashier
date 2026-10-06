## Purpose

Configurar o Xano CLI e a conexão com o workspace para que o código do backend possa ser baixado e versionado.

## ADDED Requirements

### Requirement: Xano CLI autenticado e vinculado a um workspace
O ambiente SHALL ter o Xano CLI autenticado e com um workspace definido no perfil ativo.

#### Scenario: Perfil ativo com workspace
- **WHEN** o desenvolvedor executa `xano profile me`
- **THEN** são exibidos a conta, a instância e o workspace configurados

### Requirement: Pull do workspace
O código do workspace SHALL ser gravado na pasta `xano/` para poder ser versionado.

#### Scenario: Pull inicial
- **WHEN** o desenvolvedor executa `xano workspace pull -d ./xano`
- **THEN** os arquivos XanoScript do workspace são gravados na pasta `xano/`

### Requirement: Credenciais fora do repositório
As credenciais do Xano SHALL ficar na pasta do usuário do sistema e SHALL NOT ser colocadas dentro do projeto.

#### Scenario: Autenticação concluída
- **WHEN** o login com `xano auth` termina com sucesso
- **THEN** as credenciais são gravadas na pasta do usuário e nenhum token aparece em arquivos do projeto
