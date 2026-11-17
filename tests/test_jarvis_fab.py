import unittest

import reflex as rx

from CashSave.components.layout import (
    botao_jarvis_global,
    jarvis_fab_route_enabled,
)


class JarvisFloatingAccessTests(unittest.TestCase):
    def test_route_availability_excludes_assistant_and_profile(self):
        for route in ("/assistente", "/perfil"):
            with self.subTest(route=route):
                self.assertFalse(jarvis_fab_route_enabled(route))

    def test_route_availability_includes_authenticated_app_pages(self):
        for route in (
            "/app",
            "/financas",
            "/bolsa",
            "/calendario",
            "/sobre",
            "/suporte",
            "/apoiar",
        ):
            with self.subTest(route=route):
                self.assertTrue(jarvis_fab_route_enabled(route))

    def test_floating_button_opens_existing_assistant_with_accessible_tooltip(self):
        component = botao_jarvis_global()
        self.assertIsInstance(component, rx.Component)

        tooltip = component.children[0].children[0]
        link = tooltip.children[0]
        self.assertEqual(link.children[0].to._var_value, "/assistente")
        self.assertEqual(tooltip.content._var_value, "Converse com o Jarvis")

        serialized = str(component.__dict__["children"])
        self.assertIn("aria-label", serialized)
        self.assertNotIn("online", serialized.lower())


if __name__ == "__main__":
    unittest.main()
