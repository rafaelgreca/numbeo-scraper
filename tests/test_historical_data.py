import pandas as pd

import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestHistoricalData(unittest.TestCase):
    """
    Unittest case to test historical data of a given country.
    """

    def test(self):
        """
        Test the historical data scraping.
        """
        valid_attributes = [
            "Year",
            "1 Pair of Jeans (Levis 501 Or Similar)",
            "Banana (1kg)",
            "Country",
        ]

        config = Input(
            categories="historical-data",
            years=2019,
            mode="country",
            countries=["Italy", "Brazil"],
            currency="EUR",
            historical_items=[
                "1 Pair of Jeans (Levis 501 Or Similar)",
                "Banana (1kg)",
            ],
        )

        scraper = NumbeoScraper(
            config=config,
        )
        dataframes = scraper.scrap()  # will return a list of tuples

        assert len(dataframes) == 1

        data = dataframes[0]

        assert data[0] == "historical-data_country"
        assert isinstance(data[1], pd.DataFrame)
        assert data[1].shape[1] == len(valid_attributes)
        assert all(a in data[1].columns.tolist() for a in valid_attributes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
