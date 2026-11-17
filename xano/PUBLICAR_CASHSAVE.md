# Publicar o CashSave no Xano

No workspace Xano, use o grupo de APIs `cashsave` e publique os arquivos deste
diretório, não os arquivos de exemplo em `xano/api/authentication/`.

## Rotas obrigatórias

1. `POST /auth/login` usando `api/cashsave/auth/login_POST.xs`
2. `POST /auth/signup` usando `api/cashsave/auth/signup_POST.xs`
3. `GET /auth/me` usando `api/cashsave/auth/me_GET.xs`
4. `GET /resumo` usando `api/cashsave/resumo_GET.xs`
5. `GET /recorrencias` usando `api/cashsave/recorrencias_GET.xs`
6. `POST /recorrencias` usando `api/cashsave/recorrencias_POST.xs`
7. `PATCH /recorrencias/{recorrencia_id}` usando
   `api/cashsave/recorrencias/recorrencia_id_PATCH.xs`
8. `DELETE /recorrencias/{recorrencia_id}` usando
   `api/cashsave/recorrencias/recorrencia_id_DELETE.xs`

Publique também `table/recorrencias.xs` antes de publicar as quatro rotas de
recorrência.

Para a Bolsa de Valores, publique primeiro
`table/investimento_operacoes.xs`, `table/investimento_proventos.xs` e
`table/investimento_favoritos.xs` e `table/investimento_alertas.xs`, depois
as funções `function/cashsave/aplicar_operacao_investimento.xs` e
`function/cashsave/validar_historico_operacoes.xs`, e então as rotas:

- `GET` e `POST /investimentos/operacoes`
- `PATCH` e `DELETE /investimentos/operacoes/{operacao_id}`
- `GET` e `POST /investimentos/proventos`
- `PATCH` e `DELETE /investimentos/proventos/{provento_id}`
- `GET` e `POST /investimentos/favoritos`
- `DELETE /investimentos/favoritos/{ativo_codigo}`
- `GET` e `POST /investimentos/alertas`
- `DELETE /investimentos/alertas/{alerta_id}`

Todas as rotas de investimento exigem autenticação e derivam `usuario_id` de
`$auth.id`; não adicione esse campo aos inputs públicos.
As mutações de operações revalidam a sequência cronológica de compras e vendas
antes de gravar, editar ou remover um lançamento.
Confirme também que o workspace executa a revalidação e a gravação sob a
garantia transacional/serial confirmada para a carteira antes de habilitar as
rotas em produção.

No Xano, `precondition` continua o fluxo quando a condição é verdadeira e
dispara o erro quando ela é falsa. No login, portanto, a definição correta é:

```xs
precondition ($password_valid == true) {
  error_type = "accessdenied"
  error = "E-mail ou senha inválidos."
}
```

Não use `$password_valid == false`: essa condição permite que senhas inválidas
sigam para a criação do token e rejeita senhas válidas.

## Verificações obrigatórias

Depois da publicação, confirme no painel:

- `POST /auth/login` rejeita senha incorreta com HTTP 401/403 e não retorna
  `authToken`;
- `GET /resumo` retorna `usuario`, `transacoes`, `contas`, `categorias`,
  `contas_a_pagar`, `orcamentos`, `metas`, `recorrencias` e `preferencias`;
- `GET /recorrencias` existe e exige autenticação;
- as consultas usam `$auth.id` para filtrar os dados do usuário.
- as rotas de proventos exigem data de pagamento para status `pago`, e
  registros `anunciado` não entram nos totais recebidos;
- operações e proventos de dois usuários de teste permanecem isolados entre si.

Não publique os arquivos em `xano/api/authentication/` para o grupo
`cashsave`: eles pertencem ao exemplo genérico do Reflex/Xano e possuem
contratos diferentes.
