import pandas as pd

import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestQualityOfLifeCity(unittest.TestCase):
    """
    Unittest case to test quality of life of a given city.
    """

    def test(self):
        """
        Test the quality of life scraping.
        """
        valid_attributes = [
            "Category",
            "Value",
            "Level",
            "City",
        ]

        config = Input(
            categories="quality-of-life",
            years=2019,
            mode="city",
            currency="EUR",
            cities=["Toronto"],
        )

        scraper = NumbeoScraper(
            config=config,
        )
        dataframes = scraper.scrap()  # will return a list of tuples

        assert len(dataframes) == 1

        data = dataframes[0]

        assert data[0] == "quality-of-life_city"
        assert isinstance(data[1], pd.DataFrame)
        assert data[1].shape[1] == len(valid_attributes)
        assert all(a in data[1].columns.tolist() for a in valid_attributes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
