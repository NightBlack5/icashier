import unittest
from types import SimpleNamespace

from CashSave import state


class CurrencyInputFormattingTests(unittest.TestCase):
    def test_formats_whole_amount_with_thousands(self):
        self.assertEqual(state._formatar_entrada_reais("20031"), "20.031,00")

    def test_formats_decimal_amount_with_two_places(self):
        self.assertEqual(state._formatar_entrada_reais("20031,5"), "20.031,50")

    def test_formatted_amount_keeps_cent_value(self):
        self.assertEqual(state._money_to_cents("20.031,50"), 2_003_150)

    def test_bill_amount_formats_on_blur(self):
        account_state = SimpleNamespace(conta_valor="20031")

        state.AppState.formatar_conta_valor.fn(account_state)

        self.assertEqual(account_state.conta_valor, "20.031,00")


if __name__ == "__main__":
    unittest.main()