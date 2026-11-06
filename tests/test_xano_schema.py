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


if __name__ == "__main__":
    unittest.main()
