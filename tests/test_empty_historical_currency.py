import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestEmptyHistoricalCurrency(unittest.TestCase):
    """
    Unittest case to test empty historical currency value.
    """

    def test(self):
        """
        Test the currency value.
        """

        with self.assertRaises(AssertionError):
            config = Input(
                categories="historical-data",
                countries="Italy",
                years=[2019, 2020],
                mode="country",
                historical_items="1 Pair of Jeans (Levis 501 Or Similar)",
            )
            NumbeoScraper(config=config)


if __name__ == "__main__":
    unittest.main(verbosity=2)
