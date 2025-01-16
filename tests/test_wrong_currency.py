import unittest

from pydantic_core import ValidationError

from src.schema.input import Input


class TestWrongCurrency(unittest.TestCase):
    """
    Unittest case to test wrong currency value.
    """

    def test(self):
        """
        Test the currency value.
        """

        with self.assertRaises(ValidationError):
            Input(currency="WRONG_CURRENCY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
