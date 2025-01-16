import pandas as pd

import unittest

from src.schema.input import Input
from src.core.scraper import NumbeoScraper


class TestPropertyInvestment(unittest.TestCase):
    """
    Unittest case to test property investment of a given country.
    """

    def test(self):
        """
        Test the propert investment scraping.
        """
        valid_attributes = [
            "Rank",
            "Country",
            "Price To Income Ratio",
            "Gross Rental Yield City Centre",
            "Gross Rental Yield Outside of Centre",
            "Price To Rent Ratio City Centre",
            "Price To Rent Ratio Outside Of City Centre",
            "Mortgage As A Percentage Of Income",
            "Affordability Index",
            "Year",
        ]

        config = Input(
            categories="property-investment",
            years=2019,
            mode="country",
        )

        scraper = NumbeoScraper(
            config=config,
        )
        dataframes = scraper.scrap()  # will return a list of tuples

        assert len(dataframes) == 1

        data = dataframes[0]

        assert data[0] == "property-investment_country"
        assert isinstance(data[1], pd.DataFrame)
        assert data[1].shape[1] == len(valid_attributes)
        assert all(a in data[1].columns.tolist() for a in valid_attributes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
