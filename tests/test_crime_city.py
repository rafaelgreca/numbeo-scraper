import pandas as pd

import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestCrimeCity(unittest.TestCase):
    """
    Unittest case to test crime of a given city.
    """

    def test(self):
        """
        Test the crime scraping.
        """
        valid_attributes = [
            "Header",
            "Category",
            "Value",
            "Level",
            "City",
        ]

        config = Input(
            categories="crime",
            years=2019,
            mode="city",
            currency="EUR",
            cities=["Rio de Janeiro", "Brasilia"],
        )

        scraper = NumbeoScraper(
            config=config,
        )
        dataframes = scraper.scrap()  # will return a list of tuples

        assert len(dataframes) == 1

        data = dataframes[0]

        assert data[0] == "crime_city"
        assert isinstance(data[1], pd.DataFrame)
        assert data[1].shape[1] == len(valid_attributes)
        assert all(a in data[1].columns.tolist() for a in valid_attributes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
