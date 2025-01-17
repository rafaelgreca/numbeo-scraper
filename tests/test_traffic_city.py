import pandas as pd

import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestTrafficCity(unittest.TestCase):
    """
    Unittest case to test traffic of a given city.
    """

    def test(self):
        """
        Test the traffic scraping.
        """
        valid_attributes = [
            "Header",
            "Category",
            "Value",
            "City",
        ]

        config = Input(
            categories="traffic",
            years=2019,
            mode="city",
            cities="Utrecht",
            currency="EUR",
        )

        scraper = NumbeoScraper(
            config=config,
        )
        dataframes = scraper.scrap()  # will return a list of tuples

        assert len(dataframes) == 1

        data = dataframes[0]

        assert data[0] == "traffic_city"
        assert isinstance(data[1], pd.DataFrame)
        assert data[1].shape[1] == len(valid_attributes)
        assert all(a in data[1].columns.tolist() for a in valid_attributes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
