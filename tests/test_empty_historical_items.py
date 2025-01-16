import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestEmptyHistoricalItems(unittest.TestCase):
    """
    Unittest case to test empty historical items values.
    """

    def test(self):
        """
        Test the items value.
        """

        with self.assertRaises(AssertionError):
            config = Input(
                categories="historical-data",
                countries="Italy",
                years=[2019, 2020],
                mode="country",
            )
            NumbeoScraper(config=config)


if __name__ == "__main__":
    unittest.main(verbosity=2)
