import unittest
from pathlib import Path


class XanoAuthenticationSchemaTests(unittest.TestCase):
    def test_login_requires_a_valid_password(self):
        schema = Path("xano/api/cashsave/auth/login_POST.xs").read_text(
            encoding="utf-8"
        )

        self.assertIn("precondition ($password_valid == false)", schema)
        self.assertNotIn("precondition ($password_valid == true)", schema)


if __name__ == "__main__":
    unittest.main()
