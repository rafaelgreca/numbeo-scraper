import requests
from typing import List, Tuple, Union
from functools import reduce

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from ..schema.input import Input


BASE_URL = "https://www.numbeo.com"
REGIONS_MAPPING = {
    "Africa": "002",
    "America": "019",
    "Asia": "142",
    "Europe": "150",
    "Oceania": "009",
}
ITENS_MAPPING = {
    "Price per Square Meter to Buy Apartment Outside of Centre": 101,
    "Price per Square Meter to Buy Apartment in City Centre": 100,
    "International Primary School, Yearly for 1 Child": 228,
    "Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child": 224,
    "1 Pair of Jeans (Levis 501 Or Similar)": 60,
    "1 Pair of Men Leather Business Shoes": 66,
    "1 Pair of Nike Running Shoes (Mid-Range)": 64,
    "1 Summer Dress in a Chain Store (Zara, H&M, ...)": 62,
    "Apples (1kg)": 110,
    "Banana (1kg)": 118,
    "Beef Round (1kg) (or Equivalent Back Leg Red Meat)": 121,
    "Bottle of Wine (Mid-Range)": 14,
    "Chicken Fillets (1kg)": 19,
    "Cigarettes 20 Pack (Marlboro)": 17,
    "Domestic Beer (0.5 liter bottle)": 15,
    "Eggs (regular) (12)": 11,
    "Markets: Imported Beer (0.33 liter bottle)": 16,
    "Lettuce (1 head)": 113,
    "Loaf of Fresh White Bread (500g)": 9,
    "Local Cheese (1kg)": 12,
    "Milk (regular), (1 liter)": 8,
    "Onion (1kg)": 119,
    "Oranges (1kg)": 111,
    "Potato (1kg)": 112,
    "Rice (white), (1kg)": 115,
    "Tomato (1kg)": 116,
    "Water (1.5 liter bottle)": 13,
    "Apartment (1 bedroom) Outside of Centre": 27,
    "Apartment (1 bedroom) in City Centre": 26,
    "Apartment (3 bedrooms) Outside of Centre": 29,
    "Apartment (3 bedrooms) in City Centre": 28,
    "Cappuccino (regular)": 114,
    "Coke/Pepsi (0.33 liter bottle)": 6,
    "Domestic Beer (0.5 liter draught)": 4,
    "Restaurants: Imported Beer (0.33 liter bottle)": 5,
    "McMeal at McDonalds (or Equivalent Combo Meal)": 3,
    "Meal for 2 People, Mid-range Restaurant, Three-course": 2,
    "Meal, Inexpensive Restaurant": 1,
    "Water (0.33 liter bottle)": 7,
    "Average Monthly Net Salary (After Tax)": 105,
    "Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate": 106,
    "Cinema, International Release, 1 Seat": 44,
    "Fitness Club, Monthly Fee for 1 Adult": 40,
    "Tennis Court Rent (1 Hour on Weekend)": 42,
    "Gasoline (1 liter)": 24,
    "Monthly Pass (Regular Price)": 20,
    "One-way Ticket (Local Transport)": 18,
    "Taxi 1hour Waiting (Normal Tariff)": 109,
    "Taxi 1km (Normal Tariff)": 108,
    "Taxi Start (Normal Tariff)": 107,
    "Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car)": 206,
    "Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car)": 25,
    "Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment": 30,
    "Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)": 33,
    "Mobile Phone Monthly Plan with Calls and 10GB+ Data": 34,
}


class NumbeoScraper:
    """
    Numbeo's scraper class.
    """

    def __init__(
        self,
        config: Input,
    ) -> None:
        """
        Creates a Numbeo's scraper instance.

        Args:
            config (Input): the configuration values obtained from the YAML file.
        """
        if not config.regions is None:
            if isinstance(config.regions, str):
                self.regions = [config.regions]
            else:
                self.regions = config.regions
        else:
            self.regions = None

        if not config.historical_items is None:
            if isinstance(config.historical_items, str):
                self.historical_items = [config.historical_items]
            else:
                self.historical_items = config.historical_items
        else:
            self.historical_items = None

        if not config.countries is None:
            if isinstance(config.countries, str):
                self.countries = [config.countries]
            else:
                self.countries = config.countries
        else:
            self.countries = None

        if isinstance(config.categories, str):
            self.categories = [config.categories]
        else:
            self.categories = config.categories

        if not config.currency is None:
            self.currency = config.currency
        else:
            self.currency = None

        # validating items when historical-data is chosen
        for c in self.categories:
            if c == "historical-data":
                try:
                    assert not self.historical_items is None
                except AssertionError as error:
                    raise AssertionError(
                        "Historical items can not be empty!\n"
                    ) from error

                try:
                    assert not self.currency is None
                except AssertionError as error:
                    raise AssertionError("Currency can not be empty!\n") from error

        if isinstance(config.years, int):
            self.years = [config.years]
        else:
            self.years = config.years

        self.mode = config.mode

    def scrap(
        self,
    ) -> List[Tuple[str, pd.DataFrame]]:
        """
        Main function responsible for scraping the data.

        Returns:
            dataframes (List[Tuple[str, pd.DataFrame]]): a list containing
                the extracted data (saved in a dataframe format) with it
                respective name used to identify it.
        """
        dataframes = []

        if self.mode == "country":
            # iterating over the categories
            for category in self.categories:
                if category == "historical-data":
                    data = self._historical_data_country_mode(
                        itens=self.historical_items,
                        countries=self.countries,
                    )
                    data_name = f"{category}_{self.mode}"
                    dataframes.append((data_name, data))

                else:
                    if not self.regions is None:
                        # iterating over the regions, if not none
                        for region in self.regions:
                            data = self._country_mode(
                                category=category,
                                region=region,
                            )
                            data_name = f"{category}_{self.mode}"
                            dataframes.append((data_name, data))
                    else:
                        data = self._country_mode(
                            category=category,
                            region=self.regions,
                        )
                        data_name = f"{category}_{self.mode}"
                        dataframes.append((data_name, data))

        return dataframes

    def _country_mode(
        self,
        category: str,
        region: Union[str, List[str]],
    ) -> pd.DataFrame:
        """
        Extracts the data considering the 'country mode', which means that
        the data extracted will be for the country as a whole.

        Args:
            category (str): the current category.
            region (str): the current region.

        Returns:
            dataframes (List[Tuple[str, pd.DataFrame]]): a list containing
                the extracted data (saved in a dataframe format) with it
                respective name used to identify it.
        """
        dataframes = pd.DataFrame()

        for year in self.years:
            country_page = "rankings_by_country.jsp"

            if region is None:
                full_url = f"{BASE_URL}/{category}/{country_page}?title={year}"
            else:
                region_code = REGIONS_MAPPING[region]
                full_url = f"{BASE_URL}/{category}/{country_page}?title={year}&region={region_code}"

            request = requests.get(full_url, timeout=300)

            if request.status_code == 200:
                numbeo_html_data = BeautifulSoup(request.text, "html.parser")
                main_table = numbeo_html_data.find("table", attrs={"id": "t2"})

                main_table_header = main_table.find("thead")
                main_table_header_rows = main_table_header.find_all("th")
                table_columns_name = [row.text for row in main_table_header_rows]
                dataframe = pd.DataFrame(columns=table_columns_name)

                main_table_body = main_table.find("tbody")
                main_table_rows = main_table_body.find_all("tr")

                for rank, row in enumerate(main_table_rows, start=1):
                    data = row.find_all("td")[1:]
                    data = [d.text for d in data]
                    data = [rank] + data  # appeding rank to the list
                    data = (
                        np.asarray(data).reshape(1, -1).tolist()
                    )  # reshaping so we can concatenate it

                    new_row = pd.DataFrame(data, columns=table_columns_name)
                    dataframe = pd.concat(
                        [dataframe, new_row], axis=0, ignore_index=True
                    )

                dataframe["Year"] = [year] * dataframe.shape[0]
                dataframes = pd.concat(
                    [dataframes, dataframe], axis=0, ignore_index=True
                )

        if not self.countries is None:
            dataframes = dataframes[
                dataframes["Country"].isin(self.countries)
            ].reset_index(drop=True)

        return dataframes

    def _historical_data_country_mode(
        self,
        itens: Union[str, List[str]],
        countries: Union[str, List[str]],
    ) -> pd.DataFrame:
        """
        Extracts the historical data considering the 'country mode',
        which means that the data extracted will be for the country as a whole.

        Args:
            itens (Union[str, List[str]]): the itens that will be scraped.
            countries (Union[str, List[str]]): the itens that will be scraped.

        Returns:
            dataframes (List[Tuple[str, pd.DataFrame]]): a list containing
                the historical data (saved in a dataframe format) for the given
                countries and itens.
        """
        dataframes = pd.DataFrame()
        country_page = "historical-data-country"
        category = "cost-of-living"

        for country in countries:
            country_dataframe = pd.DataFrame()
            items_dataframe = []

            for item in itens:
                item_id = ITENS_MAPPING[item]
                full_url = f"{BASE_URL}/{category}/{country_page}?itemId={item_id}"
                full_url = full_url + f"&country={country}&currency={self.currency}"

                request = requests.get(full_url, timeout=300)

                if request.status_code == 200:
                    numbeo_html_data = BeautifulSoup(request.text, "html.parser")
                    main_table = numbeo_html_data.find("table", attrs={"id": "t2"})

                    main_table_header = main_table.find("thead")
                    main_table_header_rows = main_table_header.find_all("th")
                    table_columns_name = [row.text for row in main_table_header_rows]
                    dataframe = pd.DataFrame(columns=table_columns_name)

                    main_table_body = main_table.find("tbody")
                    main_table_rows = main_table_body.find_all("tr")

                    for row in main_table_rows:
                        data = row.find_all("td")
                        data = [d.text for d in data]
                        data = (
                            np.asarray(data).reshape(1, -1).tolist()
                        )  # reshaping so we can concatenate it
                        new_row = pd.DataFrame(data, columns=table_columns_name)

                        dataframe = pd.concat(
                            [dataframe, new_row], axis=0, ignore_index=True
                        )

                # dataframe[item] = dataframe[item].astype(float)
                items_dataframe.append(dataframe)

            if len(items_dataframe) > 1:
                country_dataframe = reduce(
                    lambda x, y: pd.merge(x, y, how="outer", on="Year"), items_dataframe
                )
            else:
                country_dataframe = items_dataframe[0].copy()

            country_dataframe["Country"] = [country] * country_dataframe.shape[0]
            dataframes = pd.concat(
                [dataframes, country_dataframe], axis=0, ignore_index=True
            )

        dataframes["Year"] = dataframes["Year"].astype(int)
        dataframes = dataframes[dataframes["Year"].isin(self.years)].reset_index(
            drop=True
        )
        return dataframes
