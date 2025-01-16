import unittest

from pydantic_core import ValidationError

from src.schema.input import Input


class TestWrongCategory(unittest.TestCase):
    """
    Unittest case to test wrong category value.
    """

    def test(self):
        """
        Test the category value.
        """

        with self.assertRaises(ValidationError):
            Input(categories="WRONG_MODE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
