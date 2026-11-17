import asyncio
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from CashSave.market_data import MarketMover, MarketMovers
from CashSave.state import AppState, XanoAPIError


class MarketDashboardTests(unittest.TestCase):
    def create_state(self):
        return SimpleNamespace(
            auth_token="test-session",
            bolsa_carregando=False,
            bolsa_erro="",
            bolsa_carteira_erro="",
            bolsa_indicadores=[],
            bolsa_altas=[],
            bolsa_baixas=[],
            bolsa_grafico_altas=[],
            bolsa_movers_origem="",
            bolsa_movers_referencia="",
            bolsa_movers_atrasado=False,
            bolsa_indisponivel="",
            erro="",
            _carregar_dados=AsyncMock(),
            _carregar_favoritos_bolsa=AsyncMock(),
            _carregar_alertas_bolsa=AsyncMock(),
            _carregar_operacoes_bolsa=AsyncMock(),
            _carregar_proventos_bolsa=AsyncMock(),
            _carregar_analise_carteira_bolsa=AsyncMock(),
        )

    @staticmethod
    def sample_movers():
        reference_at = datetime(2026, 11, 16, 13, 0, tzinfo=timezone.utc)
        return MarketMovers(
            gainers=(
                MarketMover(
                    symbol="PETR4",
                    name="Petrobras",
                    price=Decimal("37.12"),
                    daily_change_percent=Decimal("1.25"),
                    volume=1000,
                    source="brapi.dev",
                    reference_at=reference_at,
                ),
            ),
            losers=(),
            source="brapi.dev",
            reference_at=reference_at,
        )

    def test_xano_failure_does_not_replace_market_dashboard_data(self):
        state = self.create_state()
        state._carregar_favoritos_bolsa.side_effect = XanoAPIError(
            "Rota de favoritos indisponível."
        )
        service = SimpleNamespace(
            configured=True,
            market_movers=Mock(return_value=self.sample_movers()),
        )

        with patch("CashSave.state.market_data_service", service):
            asyncio.run(AppState.carregar_bolsa.fn(state))

        self.assertEqual(state.bolsa_erro, "")
        self.assertEqual(
            state.bolsa_carteira_erro,
            "Rota de favoritos indisponível.",
        )
        self.assertEqual(state.bolsa_altas[0]["symbol"], "PETR4")
        self.assertEqual(state.bolsa_grafico_altas[0]["variation"], 1.25)
        self.assertEqual(state.bolsa_movers_origem, "brapi.dev")

    def test_missing_market_token_shows_unavailable_without_fake_data(self):
        state = self.create_state()
        service = SimpleNamespace(configured=False)

        with patch("CashSave.state.market_data_service", service):
            asyncio.run(AppState.carregar_bolsa.fn(state))

        self.assertEqual(state.bolsa_altas, [])
        self.assertEqual(state.bolsa_baixas, [])
        self.assertIn("CASHSAVE_BRAPI_TOKEN", state.bolsa_indisponivel)
        self.assertEqual(state.bolsa_erro, "")

    def test_empty_provider_results_do_not_show_a_quote_timestamp(self):
        state = self.create_state()
        reference_at = datetime(2026, 11, 16, 13, 0, tzinfo=timezone.utc)
        empty_movers = MarketMovers(
            gainers=(),
            losers=(),
            source="brapi.dev",
            reference_at=reference_at,
        )
        service = SimpleNamespace(
            configured=True,
            market_movers=Mock(return_value=empty_movers),
        )

        with patch("CashSave.state.market_data_service", service):
            asyncio.run(AppState.carregar_bolsa.fn(state))

        self.assertEqual(state.bolsa_altas, [])
        self.assertEqual(state.bolsa_baixas, [])
        self.assertEqual(state.bolsa_movers_origem, "brapi.dev")
        self.assertEqual(state.bolsa_movers_referencia, "")
        self.assertIn("não encontrou ações", state.bolsa_indisponivel)


if __name__ == "__main__":
    unittest.main()
