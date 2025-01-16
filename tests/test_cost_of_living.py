import pandas as pd

import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestCostOfLiving(unittest.TestCase):
    """
    Unittest case to test cost of living of a given country.
    """

    def test(self):
        """
        Test the cost of living scraping.
        """
        valid_attributes = [
            "Rank",
            "Country",
            "Cost of Living Index",
            "Rent Index",
            "Cost of Living Plus Rent Index",
            "Groceries Index",
            "Restaurant Price Index",
            "Local Purchasing Power Index",
            "Year",
        ]

        config = Input(
            categories="cost-of-living",
            years=2019,
            mode="country",
        )

        scraper = NumbeoScraper(
            config=config,
        )
        dataframes = scraper.scrap()  # will return a list of tuples

        assert len(dataframes) == 1

        data = dataframes[0]

        assert data[0] == "cost-of-living_country"
        assert isinstance(data[1], pd.DataFrame)
        assert data[1].shape[1] == len(valid_attributes)
        assert all(a in data[1].columns.tolist() for a in valid_attributes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
