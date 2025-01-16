import unittest

from pydantic_core import ValidationError

from src.schema.input import Input


class TestWrongMode(unittest.TestCase):
    """
    Unittest case to test wrong mode value.
    """

    def test(self):
        """
        Test the mode value.
        """

        with self.assertRaises(ValidationError):
            Input(mode="WRONG_MODE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
