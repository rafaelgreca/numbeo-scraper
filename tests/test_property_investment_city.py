import pandas as pd

import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestPropertyInvestmentCity(unittest.TestCase):
    """
    Unittest case to test property investment of a given city.
    """

    def test(self):
        """
        Test the property investment scraping.
        """
        valid_attributes = [
            "Header",
            "Category",
            "Mean",
            "Range",
            "City",
        ]

        config = Input(
            categories="property-investment",
            years=2019,
            mode="city",
            currency="EUR",
            cities=["Paris", "Porto", "New York"],
        )

        scraper = NumbeoScraper(
            config=config,
        )
        dataframes = scraper.scrap()  # will return a list of tuples

        assert len(dataframes) == 1

        data = dataframes[0]

        assert data[0] == "property-investment_city"
        assert isinstance(data[1], pd.DataFrame)
        assert data[1].shape[1] == len(valid_attributes)
        assert all(a in data[1].columns.tolist() for a in valid_attributes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
