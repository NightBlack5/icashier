import unittest
from pathlib import Path


class XanoAuthenticationSchemaTests(unittest.TestCase):
    def test_login_receives_password_as_text(self):
        schema = Path("xano/api/cashsave/auth/login_POST.xs").read_text(
            encoding="utf-8"
        )

        self.assertIn("text password", schema)
        self.assertNotIn("password password", schema)
        self.assertIn("text_password = $input.password", schema)

    def test_login_requires_a_valid_password(self):
        schema = Path("xano/api/cashsave/auth/login_POST.xs").read_text(
            encoding="utf-8"
        )

        self.assertIn("precondition ($password_valid == true)", schema)
        self.assertNotIn("precondition ($password_valid == false)", schema)

    def test_login_returns_persisted_avatar_url(self):
        schema = Path("xano/api/cashsave/auth/login_POST.xs").read_text(
            encoding="utf-8"
        )
        response = schema.split("response = {", maxsplit=1)[1]

        self.assertIn(
            'output = ["id", "name", "email", "password", "avatar_url"]',
            schema,
        )
        self.assertIn("avatar_url: $user.avatar_url", response)

    def test_financial_summary_returns_persisted_avatar_url(self):
        schema = Path("xano/api/cashsave/resumo_GET.xs").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'output = ["id", "name", "email", "created_at", "avatar_url"]',
            schema,
        )
        self.assertIn("data_inicio", schema)
        self.assertIn("saldo_periodo_centavos", schema)

class XanoInvestmentSchemaTests(unittest.TestCase):
    endpoint_paths = (
        "xano/api/cashsave/investimentos/operacoes_GET.xs",
        "xano/api/cashsave/investimentos/operacoes_POST.xs",
        "xano/api/cashsave/investimentos/operacoes/operacao_id_PATCH.xs",
        "xano/api/cashsave/investimentos/operacoes/operacao_id_DELETE.xs",
        "xano/api/cashsave/investimentos/proventos_GET.xs",
        "xano/api/cashsave/investimentos/proventos_POST.xs",
        "xano/api/cashsave/investimentos/proventos/provento_id_PATCH.xs",
        "xano/api/cashsave/investimentos/proventos/provento_id_DELETE.xs",
        "xano/api/cashsave/investimentos/favoritos_GET.xs",
        "xano/api/cashsave/investimentos/favoritos_POST.xs",
        "xano/api/cashsave/investimentos/favoritos/ativo_codigo_DELETE.xs",
        "xano/api/cashsave/investimentos/alertas_GET.xs",
        "xano/api/cashsave/investimentos/alertas_POST.xs",
        "xano/api/cashsave/investimentos/alertas/alerta_id_DELETE.xs",
    )

    def test_investment_tables_have_owner_and_validated_fields(self):
        operations = Path("xano/table/investimento_operacoes.xs").read_text(
            encoding="utf-8"
        )
        proventos = Path("xano/table/investimento_proventos.xs").read_text(
            encoding="utf-8"
        )
        favorites = Path("xano/table/investimento_favoritos.xs").read_text(
            encoding="utf-8"
        )
        alerts = Path("xano/table/investimento_alertas.xs").read_text(
            encoding="utf-8"
        )

        self.assertIn('int usuario_id {\n      table = "user"', operations)
        self.assertIn("decimal quantidade filters=min:0.0001", operations)
        self.assertIn("int preco_unitario_centavos filters=min:1", operations)
        self.assertIn('int usuario_id {\n      table = "user"', proventos)
        self.assertIn('values = ["anunciado", "pago"]', proventos)
        self.assertIn("int valor_centavos filters=min:1", proventos)
        self.assertIn('int usuario_id {\n      table = "user"', favorites)
        self.assertIn('"btree|unique"', favorites)
        self.assertIn('enum monitoramento_status?=nao_monitorado', alerts)

    def test_every_investment_endpoint_requires_auth_and_rejects_client_owner(self):
        for endpoint_path in self.endpoint_paths:
            with self.subTest(endpoint=endpoint_path):
                schema = Path(endpoint_path).read_text(encoding="utf-8")
                input_block = schema.split("  input {", maxsplit=1)[1].split(
                    "\n  }\n\n  stack",
                    maxsplit=1,
                )[0]
                self.assertIn('auth = "user"', schema)
                self.assertNotIn("usuario_id", input_block)

    def test_investment_reads_and_mutations_are_owner_scoped(self):
        for endpoint_path in self.endpoint_paths:
            with self.subTest(endpoint=endpoint_path):
                schema = Path(endpoint_path).read_text(encoding="utf-8")
                if endpoint_path.endswith("_POST.xs"):
                    self.assertIn("usuario_id: $auth.id", schema)
                else:
                    self.assertIn("usuario_id == $auth.id", schema)

    def test_received_provento_requires_a_payment_date(self):
        for endpoint_path in (
            "xano/api/cashsave/investimentos/proventos_POST.xs",
            "xano/api/cashsave/investimentos/proventos/provento_id_PATCH.xs",
        ):
            with self.subTest(endpoint=endpoint_path):
                schema = Path(endpoint_path).read_text(encoding="utf-8")
                self.assertIn(
                    '$status != "pago" || $data_pagamento != null'
                    if endpoint_path.endswith("_PATCH.xs")
                    else '$input.status != "pago" || $input.data_pagamento != null',
                    schema,
                )

    def test_favorites_are_unique_and_restricted_to_the_authenticated_owner(self):
        create = Path(
            "xano/api/cashsave/investimentos/favoritos_POST.xs"
        ).read_text(encoding="utf-8")
        delete = Path(
            "xano/api/cashsave/investimentos/favoritos/ativo_codigo_DELETE.xs"
        ).read_text(encoding="utf-8")

        self.assertIn("Este ativo já está nos favoritos.", create)
        self.assertIn("usuario_id: $auth.id", create)
        self.assertIn("usuario_id == $auth.id", delete)

    def test_alerts_validate_thresholds_and_remain_unmonitored(self):
        create = Path(
            "xano/api/cashsave/investimentos/alertas_POST.xs"
        ).read_text(encoding="utf-8")
        table = Path("xano/table/investimento_alertas.xs").read_text(
            encoding="utf-8"
        )

        self.assertIn("Informe o limite correspondente", create)
        self.assertIn('monitoramento_status: "nao_monitorado"', create)
        self.assertIn('enum monitoramento_status?=nao_monitorado', table)
        self.assertNotIn("notificacao", create.lower())

    def test_operation_mutations_validate_chronological_quantity(self):
        for endpoint_path in self.endpoint_paths:
            if "/operacoes" not in endpoint_path or endpoint_path.endswith(
                "operacoes_GET.xs"
            ):
                continue
            with self.subTest(endpoint=endpoint_path):
                schema = Path(endpoint_path).read_text(encoding="utf-8")
                self.assertIn(
                    'function.run "CashSave/validar_historico_operacoes"',
                    schema,
                )

        validation = Path(
            "xano/function/cashsave/validar_historico_operacoes.xs"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "function.run \"CashSave/aplicar_operacao_investimento\"",
            validation,
        )
        self.assertIn("A venda excede a quantidade disponível", Path(
            "xano/function/cashsave/aplicar_operacao_investimento.xs"
        ).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
