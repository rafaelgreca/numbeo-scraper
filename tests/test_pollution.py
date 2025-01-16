import pandas as pd

import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestPollution(unittest.TestCase):
    """
    Unittest case to test pollution of a given country.
    """

    def test(self):
        """
        Test the pollution scraping.
        """
        valid_attributes = [
            "Rank",
            "Country",
            "Pollution Index",
            "Exp Pollution Index",
            "Year",
        ]

        config = Input(
            categories="pollution",
            years=2019,
            mode="country",
        )

        scraper = NumbeoScraper(
            config=config,
        )
        dataframes = scraper.scrap()  # will return a list of tuples

        assert len(dataframes) == 1

        data = dataframes[0]

        assert data[0] == "pollution_country"
        assert isinstance(data[1], pd.DataFrame)
        assert data[1].shape[1] == len(valid_attributes)
        assert all(a in data[1].columns.tolist() for a in valid_attributes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
