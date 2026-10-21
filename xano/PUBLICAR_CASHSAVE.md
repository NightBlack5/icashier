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

No Xano, `precondition` dispara o erro quando a condição é verdadeira. No
login, portanto, a definição correta é:

```xs
precondition ($password_valid == false) {
  error_type = "accessdenied"
  error = "E-mail ou senha inválidos."
}
```

Não use `$password_valid == true`: essa condição rejeita senhas válidas e
permite que senhas inválidas sigam para a criação do token.

## Verificações obrigatórias

Depois da publicação, confirme no painel:

- `POST /auth/login` rejeita senha incorreta com HTTP 401/403 e não retorna
  `authToken`;
- `GET /resumo` retorna `usuario`, `transacoes`, `contas`, `categorias`,
  `contas_a_pagar`, `orcamentos`, `metas`, `recorrencias` e `preferencias`;
- `GET /recorrencias` existe e exige autenticação;
- as consultas usam `$auth.id` para filtrar os dados do usuário.

Não publique os arquivos em `xano/api/authentication/` para o grupo
`cashsave`: eles pertencem ao exemplo genérico do Reflex/Xano e possuem
contratos diferentes.
