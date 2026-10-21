import unittest
from unittest.mock import patch

import reflex as rx

from CashSave.CashSave import app
from CashSave.pages.landing import landing_page


EXPECTED_ROUTES = {
    "/",
    "/login",
    "/cadastro",
    "/app",
    "/assistente",
    "/financas",
    "/calendario",
    "/perfil",
    "/sobre",
    "/suporte",
    "/apoiar",
}

PUBLIC_ROUTES = {"/", "/login", "/cadastro", "/sobre", "/suporte", "/apoiar"}
PROTECTED_ROUTES = {"/app", "/assistente", "/financas", "/calendario", "/perfil"}


class RouteSmokeTests(unittest.TestCase):
    def test_all_expected_routes_are_registered(self):
        routes = {
            "/" if route == "index" else f"/{route}"
            for route in app._unevaluated_pages
        }
        self.assertEqual(routes, EXPECTED_ROUTES)

    def test_public_routes_have_no_authenticated_data_loader(self):
        for route, page in app._unevaluated_pages.items():
            normalized_route = "/" if route == "index" else f"/{route}"
            if normalized_route in PUBLIC_ROUTES:
                handler_name = getattr(getattr(page.on_load, "fn", None), "__name__", "")
                self.assertNotEqual(
                    handler_name,
                    "carregar_dados",
                    f"{normalized_route} must not load authenticated data",
                )

    def test_protected_routes_use_an_on_load_handler(self):
        for route, page in app._unevaluated_pages.items():
            normalized_route = "/" if route == "index" else f"/{route}"
            if normalized_route in PROTECTED_ROUTES:
                self.assertIsNotNone(
                    page.on_load,
                    f"{normalized_route} must load its protected state",
                )

    def test_landing_page_does_not_call_xano(self):
        with patch("CashSave.state._send_request") as send_request:
            component = landing_page()

        self.assertIsInstance(component, rx.Component)
        send_request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
