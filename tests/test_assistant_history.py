import json
import unittest

from CashSave.state import _conversas_assistente_do_storage


class AssistantHistoryStorageTests(unittest.TestCase):
    def test_restores_valid_conversations_and_active_id(self):
        raw = json.dumps(
            {
                "user:7": {
                    "active_id": 2,
                    "conversations": [
                        {
                            "id": 2,
                            "title": "Como economizar?",
                            "messages": [
                                {"tipo": "usuario", "texto": "Como economizar?"},
                                {"tipo": "ia", "texto": "Revise seus gastos."},
                            ],
                        }
                    ],
                }
            }
        )

        conversations, active_id = _conversas_assistente_do_storage(raw, "user:7")

        self.assertEqual(active_id, 2)
        self.assertEqual(conversations[0]["title"], "Como economizar?")

    def test_invalid_storage_starts_empty(self):
        conversations, active_id = _conversas_assistente_do_storage(
            "not-json",
            "user:7",
        )

        self.assertEqual(conversations, [])
        self.assertEqual(active_id, 0)

    def test_ignores_invalid_messages_and_limits_history(self):
        raw = json.dumps(
            {
                "user:7": {
                    "active_id": 999,
                    "conversations": [
                        {
                            "id": index,
                            "title": "Conversa",
                            "messages": [
                                {"tipo": "usuario", "texto": f"Mensagem {index}"},
                                {"tipo": "outro", "texto": "ignorar"},
                            ],
                        }
                        for index in range(1, 10)
                    ],
                }
            }
        )

        conversations, active_id = _conversas_assistente_do_storage(raw, "user:7")

        self.assertEqual(len(conversations), 8)
        self.assertEqual(len(conversations[0]["messages"]), 1)
        self.assertEqual(active_id, 0)


if __name__ == "__main__":
    unittest.main()
