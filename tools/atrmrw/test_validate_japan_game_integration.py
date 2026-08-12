#!/usr/bin/env python3

import unittest

from tools.atrmrw.validate_japan_game_integration import validate


class ValidateJapanGameIntegrationTest(unittest.TestCase):
    def test_checked_in_integration_passes(self) -> None:
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
