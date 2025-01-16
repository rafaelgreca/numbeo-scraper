import unittest

from pydantic_core import ValidationError

from src.schema.input import Input


class TestWrongYear(unittest.TestCase):
    """
    Unittest case to test wrong year value.
    """

    def test1(self):
        """
        Test the year value.
        """

        with self.assertRaises(ValidationError):
            Input(years="2027")

    def test2(self):
        """
        Test the year value.
        """

        with self.assertRaises(ValidationError):
            Input(years="2021mid")


if __name__ == "__main__":
    unittest.main(verbosity=2)
