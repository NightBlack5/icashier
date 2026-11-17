import unittest
from datetime import date

from CashSave.investment_proventos import (
    format_provento_record,
    total_received_proventos_centavos,
)


def provento(**overrides):
    record = {
        "id": 1,
        "ativo_codigo": "PETR4",
        "ativo_categoria": "acao",
        "tipo": "dividendo",
        "status": "pago",
        "valor_centavos": 1250,
        "quantidade_elegivel": None,
        "data_anuncio": None,
        "data_pagamento": "2026-03-15",
        "observacoes": None,
    }
    return {**record, **overrides}


class InvestmentProventoTests(unittest.TestCase):
    def test_paid_totals_filter_by_payment_date_and_exclude_announcements(self):
        records = [
            provento(valor_centavos=1000, data_pagamento="2026-03-01"),
            provento(
                id=2,
                status="anunciado",
                valor_centavos=9000,
                data_pagamento=None,
                data_anuncio="2026-03-10",
            ),
            provento(
                id=3,
                valor_centavos=2500,
                data_pagamento="2026-04-02",
            ),
        ]

        self.assertEqual(total_received_proventos_centavos(records), 3500)
        self.assertEqual(
            total_received_proventos_centavos(
                records,
                start_date=date(2026, 3, 1),
                end_date=date(2026, 3, 31),
            ),
            1000,
        )

    def test_paid_provento_requires_a_payment_date(self):
        with self.assertRaisesRegex(ValueError, "sem data de pagamento"):
            format_provento_record(provento(data_pagamento=None))

    def test_provento_validates_amount_dates_and_optional_quantity(self):
        formatted = format_provento_record(
            provento(
                quantidade_elegivel="12.5",
                data_anuncio="2026-03-01",
            )
        )

        self.assertEqual(formatted["quantidade_elegivel_formatada"], "12.5")
        self.assertEqual(formatted["data_referencia"], "2026-03-15")
        self.assertEqual(
            format_provento_record(
                provento(quantidade_elegivel="10")
            )["quantidade_elegivel_formatada"],
            "10",
        )
        with self.assertRaisesRegex(ValueError, "valor inválido"):
            format_provento_record(provento(valor_centavos=0))
        with self.assertRaisesRegex(ValueError, "data de anúncio"):
            format_provento_record(provento(data_anuncio="15/03/2026"))

    def test_invalid_period_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "período"):
            total_received_proventos_centavos(
                [],
                start_date=date(2026, 4, 1),
                end_date=date(2026, 3, 1),
            )


if __name__ == "__main__":
    unittest.main()
