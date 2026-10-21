from pathlib import Path
import unittest


class EncodingTests(unittest.TestCase):
    def test_state_text_has_no_common_mojibake_markers(self):
        state_path = Path(__file__).parents[1] / "CashSave" / "state.py"
        source = state_path.read_text(encoding="utf-8")
        self.assertFalse(any(marker in source for marker in ("Ã", "Â", "�")))
