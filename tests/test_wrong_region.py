import unittest

from pydantic_core import ValidationError

from src.schema.input import Input


class TestWrongRegion(unittest.TestCase):
    """
    Unittest case to test wrong region value.
    """

    def test(self):
        """
        Test the region value.
        """

        with self.assertRaises(ValidationError):
            Input(regions="WRONG_REGION")


if __name__ == "__main__":
    unittest.main(verbosity=2)
