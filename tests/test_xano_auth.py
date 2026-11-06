import asyncio
import json
import unittest
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from urllib.error import HTTPError
from urllib.request import Request

from CashSave import state


class LoginRequestTests(unittest.TestCase):
    def setUp(self):
        self.api_url = patch.object(
            state,
            "API_BASE_URL",
            "https://example.xano.io/api:cashsave",
        )
        self.api_url.start()
        self.addCleanup(self.api_url.stop)

        self.response = patch.object(state, "urlopen")
        self.urlopen = self.response.start()
        self.addCleanup(self.response.stop)

    def test_sends_login_credentials_as_json(self):
        self.urlopen.return_value.__enter__.return_value.read.return_value = b"{}"

        state._send_request(
            "POST",
            "auth/login",
            {"email": "ana@example.com", "password": "plain-text"},
        )

        request = self.urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://example.xano.io/api:cashsave/auth/login",
        )
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Content-type"), "application/json")
        self.assertEqual(
            json.loads(request.data.decode("utf-8")),
            {"email": "ana@example.com", "password": "plain-text"},
        )

    def test_reads_friendly_message_from_nested_xano_error(self):
        self.urlopen.side_effect = HTTPError(
            "https://example.xano.io/api:cashsave/auth/login",
            401,
            "Unauthorized",
            {},
            BytesIO(
                '{"error":{"message":"E-mail ou senha inválidos."}}'.encode("utf-8")
            ),
        )

        with self.assertRaises(state.XanoAPIError) as raised:
            state._send_request(
                "POST",
                "auth/login",
                {"email": "ana@example.com", "password": "plain-text"},
            )

        self.assertEqual(raised.exception.status_code, 401)
        self.assertEqual(str(raised.exception), "E-mail ou senha inválidos.")

    def test_reads_message_from_response_data_shape(self):
        self.urlopen.side_effect = HTTPError(
            "https://example.xano.io/api:cashsave/auth/login",
            403,
            "Forbidden",
            {},
            BytesIO(b'{"response":{"data":{"message":"Acesso negado."}}}'),
        )

        with self.assertRaises(state.XanoAPIError) as raised:
            state._send_request("POST", "auth/login", {})

        self.assertEqual(str(raised.exception), "Acesso negado.")


class LoginFlowTests(unittest.TestCase):
    def create_state(self, **overrides):
        values = {
            "erro": "",
            "auth_email": "  Ana@Exemplo.COM ",
            "lembrar_email": "false",
            "auth_email_salvo": "",
            "auth_password": "  senha correta  ",
            "auth_password_confirmation": "",
            "auth_name": "",
            "auth_phone": "",
            "aceitou_termos": False,
            "cadastro": False,
            "carregando": False,
            "auth_token": "",
            "usuario": {},
            "avatar_url": "",
            "avatar_perfil_disponivel": False,
            "_avatar_from_user": state.AppState._avatar_from_user,
            "_mensagem_erro_login": state.AppState._mensagem_erro_login,
            "_api": AsyncMock(
                return_value={
                    "authToken": "session-token",
                    "user": {
                        "id": 7,
                        "name": "Ana",
                        "email": "ana@exemplo.com",
                        "avatar_url": "https://cdn.example.com/avatar.png",
                    },
                }
            ),
        }
        values.update(overrides)
        return SimpleNamespace(**values)

    def test_normalizes_credentials_and_stores_session_on_success(self):
        app_state = self.create_state()
        redirect = object()

        with patch("CashSave.state.rx.redirect", return_value=redirect):
            result = asyncio.run(state.AppState.autenticar.fn(app_state))

        app_state._api.assert_awaited_once_with(
            "POST",
            "auth/login",
            {"email": "ana@exemplo.com", "password": "senha correta"},
        )
        self.assertEqual(app_state.auth_token, "session-token")
        self.assertEqual(app_state.usuario["id"], 7)
        self.assertEqual(
            app_state.avatar_url,
            "https://cdn.example.com/avatar.png",
        )
        self.assertEqual(result, redirect)
        self.assertEqual(app_state.auth_password, "")
        self.assertFalse(app_state.carregando)

    def test_rejects_credentials_that_are_empty_after_trimming(self):
        for field in ("auth_email", "auth_password"):
            with self.subTest(field=field):
                app_state = self.create_state(**{field: "   "})

                asyncio.run(state.AppState.autenticar.fn(app_state))

                app_state._api.assert_not_awaited()
                self.assertTrue(app_state.erro)
                self.assertFalse(app_state.carregando)

    def test_displays_api_error_and_clears_loading_state(self):
        app_state = self.create_state(
            _api=AsyncMock(
                side_effect=state.XanoAPIError(
                    "E-mail ou senha inválidos.",
                    status_code=401,
                )
            )
        )

        asyncio.run(state.AppState.autenticar.fn(app_state))

        self.assertEqual(app_state.erro, "E-mail ou senha inválidos.")
        self.assertFalse(app_state.carregando)
        self.assertEqual(app_state.auth_token, "")

    def test_rejects_success_response_without_auth_token(self):
        app_state = self.create_state(_api=AsyncMock(return_value={"user": {}}))

        asyncio.run(state.AppState.autenticar.fn(app_state))

        self.assertEqual(
            app_state.erro,
            "O Xano não retornou um token de sessão.",
        )
        self.assertFalse(app_state.carregando)
        self.assertEqual(app_state.auth_token, "")


class SendRequestAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.api_url = patch.object(
            state,
            "API_BASE_URL",
            "https://example.xano.io/api:cashsave",
        )
        self.api_url.start()
        self.addCleanup(self.api_url.stop)

        self.response = patch.object(state, "urlopen")
        self.urlopen = self.response.start()
        self.addCleanup(self.response.stop)
        self.urlopen.return_value.__enter__.return_value.read.return_value = b"{}"

    def test_sends_session_token_as_bearer_authorization(self):
        state._send_request("GET", "resumo", None, "session-token")

        request = self.urlopen.call_args.args[0]
        self.assertIsInstance(request, Request)
        self.assertEqual(
            request.get_header("Authorization"),
            "Bearer session-token",
        )

    def test_omits_authorization_without_session_token(self):
        state._send_request("GET", "resumo", None)

        request = self.urlopen.call_args.args[0]
        self.assertIsInstance(request, Request)
        self.assertIsNone(request.get_header("Authorization"))

    def test_translates_http_errors_without_exposing_provider_details(self):
        self.urlopen.side_effect = HTTPError(
            "https://example.xano.io/api:cashsave/resumo",
            401,
            "Unauthorized",
            {},
            BytesIO(b'{"message":"token expired"}'),
        )

        with self.assertRaises(state.XanoAPIError) as raised:
            state._send_request("GET", "resumo", None, "session-token")

        self.assertEqual(raised.exception.status_code, 401)
        self.assertEqual(str(raised.exception), "token expired")


class LoginErrorMessageTests(unittest.TestCase):
    def test_rate_limit_message_does_not_expose_provider_details(self):
        error = state.XanoAPIError(
            "Whoa there! Your plan only supports 10 requests per 20 seconds.",
            status_code=429,
        )
        self.assertEqual(
            (
                "Muitas tentativas de login em pouco tempo. "
                "Aguarde cerca de 20 segundos e tente novamente."
            ),
            state.AppState._mensagem_erro_login(error),
        )


class DismissedNotificationStorageTests(unittest.TestCase):
    def test_reads_json_string_storage(self):
        self.assertEqual(
            state._notificacao_ids_from_storage('["bill-1","budget-2"]'),
            ["bill-1", "budget-2"],
        )

    def test_ignores_invalid_or_non_string_storage_values(self):
        self.assertEqual(state._notificacao_ids_from_storage("invalid"), [])
        self.assertEqual(state._notificacao_ids_from_storage('{"id":"bill-1"}'), [])
        self.assertEqual(
            state._notificacao_ids_from_storage('["bill-1",2]'),
            ["bill-1"],
        )


class AvatarResponseTests(unittest.TestCase):
    def test_reads_xano_file_url(self):
        self.assertEqual(
            state.AppState._avatar_from_user(
                {"avatar_url": {"path": "/vault/avatar.jpg", "url": "https://cdn/avatar.jpg"}}
            ),
            "https://cdn/avatar.jpg",
        )

    def test_reads_nested_xano_file_url(self):
        self.assertEqual(
            state.AppState._avatar_from_user(
                {"avatar_url": {"file": {"public_url": "https://cdn/avatar.webp"}}}
            ),
            "https://cdn/avatar.webp",
        )


if __name__ == "__main__":
    unittest.main()
