import unittest
from io import BytesIO
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request

from CashSave import state


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
