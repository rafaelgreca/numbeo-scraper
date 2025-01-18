import requests
from typing import List, Tuple, Union
from functools import reduce

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger

from .utils import REGIONS_MAPPING, ITENS_MAPPING
from ..schema.input import Input


BASE_URL = "https://www.numbeo.com"


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
        # initializing important variables
        if not config.regions is None:
            if isinstance(config.regions, str):
                self.regions = [config.regions]
            else:
                self.regions = config.regions
        else:
            self.regions = [None]  # we're creating a list to make it easier
            # to iterate over the regions

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

        if not config.cities is None:
            if isinstance(config.cities, str):
                self.cities = [config.cities]
            else:
                self.cities = config.cities
        else:
            self.cities = None

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

        if isinstance(config.years, int):
            self.years = [config.years]
        else:
            self.years = config.years

        self.mode = config.mode

        # validating if cities is None when the mode is 'city'
        if self.mode == "city":
            try:
                assert not self.cities is None
            except AssertionError as error:
                logger.error("Cities can not be empty when 'city' mode is chosen!\n")
                raise AssertionError("Cities can not be empty!\n") from error

        # validating if the currency value is None for a few specific cases
        if self.mode == "country":
            if "historical-data" in self.categories:
                try:
                    assert not self.currency is None
                except AssertionError as error:
                    logger.error(
                        "Currency can not be empty when 'historical-data' category is chosen!\n"
                    )
                    raise AssertionError("Currency can not be empty!\n") from error
        else:
            if any(
                c in self.categories for c in ["cost-of-living", "property-investment"]
            ):
                try:
                    assert not self.currency is None
                except AssertionError as error:
                    logger.error(
                        "Currency can not be empty when 'cost-of-living' or 'property-investment'"
                        + "is chosen for 'city' mode!\n"
                    )
                    raise AssertionError("Currency can not be empty!\n") from error

    @logger.catch
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

        # iterating over the categories
        for category in self.categories:
            data = pd.DataFrame()
            logger.info(f"Collecting '{category}' data using mode '{self.mode}'.\n")

            if self.mode == "country":
                if category == "historical-data":
                    data = self._historical_data_country_mode(
                        itens=self.historical_items,
                        countries=self.countries,
                    )
                else:
                    data = self._country_mode(
                        category=category,
                        regions=self.regions,
                    )
            else:
                if category in ["cost-of-living", "property-investment"]:
                    data = self._city_mode(
                        category=category,
                        cities=self.cities,
                    )
                elif category == "quality-of-life":
                    data = self._quality_of_life_city_mode(
                        category=category,
                        cities=self.cities,
                    )
                elif category == "traffic":
                    data = self._traffic_city_mode(
                        category=category,
                        cities=self.cities,
                    )
                elif category == "pollution":
                    data = self._pollution_city_mode(
                        category=category,
                        cities=self.cities,
                    )
                else:
                    data = self._others_city_mode(
                        category=category,
                        cities=self.cities,
                    )

            data_name = f"{category}_{self.mode}"
            dataframes.append((data_name, data))

        return dataframes

    def _country_mode(
        self,
        category: str,
        regions: Union[str, List[str]],
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

        for region in regions:
            for year in self.years:
                country_page = "rankings_by_country.jsp"

                if region is None:
                    full_url = f"{BASE_URL}/{category}/{country_page}?title={year}"
                    logger.info(
                        f"Collecting '{category}' data in 'country' mode for year '{year}'.\n"
                    )
                else:
                    region_code = REGIONS_MAPPING[region]
                    full_url = f"{BASE_URL}/{category}/{country_page}"
                    full_url = full_url + f"?title={year}&region={region_code}"
                    logger.info(
                        f"Collecting '{category}' data in 'country' mode "
                        + f"for year '{year}' and region '{region}'.\n"
                    )

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
                    logger.info(
                        f"Found {dataframe.shape[0]} data rows and "
                        + f"{dataframe.shape[0]} features.\n"
                    )
                else:
                    logger.error(f"Could not find data for URL {full_url}.\n")

        if not self.countries is None:
            logger.info(f"Selecting only the data of countries {self.countries}.\n")
            dataframes = dataframes[
                dataframes["Country"].isin(self.countries)
            ].reset_index(drop=True)
            logger.info(
                f"Found {dataframes.shape[0]} data rows and "
                + f"{dataframes.shape[0]} features.\n"
            )

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
            countries (Union[str, List[str]]): the countries that will be scraped.

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
                logger.info(
                    f"Collecting '{category}' data for country '{country}', "
                    + f"item '{item}', and currency '{self.currency}'.\n"
                )

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
                else:
                    logger.error(f"Could not find data for URL {full_url}.\n")

                items_dataframe.append(dataframe)

            if len(items_dataframe) > 1:
                country_dataframe = reduce(
                    lambda x, y: pd.merge(x, y, how="outer", on="Year"), items_dataframe
                )
            else:
                country_dataframe = items_dataframe[0].copy()

            logger.info(
                f"Found {country_dataframe.shape[0]} data rows "
                + f"and {country_dataframe.shape[0]} features.\n"
            )

            country_dataframe["Country"] = [country] * country_dataframe.shape[0]
            dataframes = pd.concat(
                [dataframes, country_dataframe], axis=0, ignore_index=True
            )

        logger.info(f"Selecting only the data from years {self.years}.\n")
        dataframes["Year"] = dataframes["Year"].astype(int)
        dataframes = dataframes[dataframes["Year"].isin(self.years)].reset_index(
            drop=True
        )
        logger.info(
            f"Found {dataframes.shape[0]} data rows and {dataframes.shape[0]} features.\n"
        )
        return dataframes

    def _city_mode(
        self,
        category: str,
        cities: Union[str, List[str]],
    ) -> pd.DataFrame:
        """
        Extracts the cost of living considering the 'city mode',
        which means that the data extracted will be for the desired city.

        Args:
            category (str): the current category.
            cities (Union[str, List[str]]): the cities that will be scraped.

        Returns:
            dataframes (List[Tuple[str, pd.DataFrame]]): a list containing
                the historical data (saved in a dataframe format) for the given
                cities.
        """
        dataframes = pd.DataFrame()
        logger.warning(
            "Filter by year option can not be used for this category and mode.\n"
        )

        for city in cities:
            city_dataframe = pd.DataFrame()
            city = city.title().replace(" ", "-")  # formatting the city's name

            full_url = f"{BASE_URL}/{category}/in/{city}"
            full_url = full_url + f"?displayCurrency={self.currency}"

            logger.info(
                f"Collecting '{category}' data in 'city' mode "
                + f"for city '{city}' and currency '{self.currency}'.\n"
            )

            request = requests.get(full_url, timeout=300)

            if request.status_code == 200:
                numbeo_html_data = BeautifulSoup(request.text, "html.parser")
                main_table = numbeo_html_data.find(
                    "table", attrs={"class": "data_wide_table new_bar_table"}
                )

                main_table_rows = main_table.find_all("tr")
                current_header = None

                for row in main_table_rows:
                    data = row.find_all("td")
                    data = [d.text for d in data]

                    if len(data) == 0:
                        current_header = row.find_all("th")[0].text
                        current_header = current_header.replace("\n", "").strip()
                        continue

                    row_df = None

                    if len(data) == 2:
                        item, mean = data
                        row_df = pd.DataFrame(
                            {
                                "Header": [current_header],
                                "Category": [item],
                                "Mean": [mean],
                                "Range": [pd.NA],
                            }
                        )

                    if len(data) == 3:
                        item, mean, data_range = data
                        data_range = data_range.replace("\n", "").strip()
                        row_df = pd.DataFrame(
                            {
                                "Header": [current_header],
                                "Category": [item],
                                "Mean": [mean],
                                "Range": [data_range],
                            }
                        )

                    logger.info(
                        f"Found {row_df.shape[0]} data rows "
                        + f"and {row_df.shape[0]} features.\n"
                    )

                    row_df["City"] = [city] * row_df.shape[0]

                    city_dataframe = pd.concat(
                        [city_dataframe, row_df], axis=0, ignore_index=True
                    )

                dataframes = pd.concat(
                    [dataframes, city_dataframe], axis=0, ignore_index=True
                )
            else:
                logger.error(f"Could not find data for URL {full_url}.\n")

        return dataframes

    def _quality_of_life_city_mode(
        self,
        category: str,
        cities: Union[str, List[str]],
    ) -> pd.DataFrame:
        """
        Extracts the cost of living considering the 'city mode',
        which means that the data extracted will be for the desired city.

        Args:
            category (str): the current category.
            cities (Union[str, List[str]]): the cities that will be scraped.

        Returns:
            dataframes (List[Tuple[str, pd.DataFrame]]): a list containing
                the quality of life data (saved in a dataframe format)
                for the given cities.
        """
        dataframes = pd.DataFrame()
        logger.warning(
            "Filter by year option can not be used for this category and mode.\n"
        )

        for city in cities:
            city_dataframe = pd.DataFrame()
            city = city.title().replace(" ", "-")  # formatting the city's name
            logger.info(
                f"Collecting '{category}' data in 'city' mode for city '{city}'.\n"
            )

            full_url = f"{BASE_URL}/{category}/in/{city}"

            request = requests.get(full_url, timeout=300)

            if request.status_code == 200:
                numbeo_html_data = BeautifulSoup(request.text, "html.parser")

                # getting the table values and removing the index table value
                main_table_rows = numbeo_html_data.find_all(
                    "td", attrs={"style": "text-align: right"}
                )
                rows_values = [row.text.strip() for row in main_table_rows][1:]

                # getting the table levels
                main_table_rows = numbeo_html_data.find_all(
                    "td", attrs={"style": "text-align: center; font-weight: 600"}
                )
                main_table_rows_cont = numbeo_html_data.find_all(
                    "td", attrs={"style": "text-align: center"}
                )  # getting the table footer level individually
                main_table_rows.extend(main_table_rows_cont)
                rows_levels = [row.text.strip() for row in main_table_rows]

                # getting the name of the categories
                main_table_rows = numbeo_html_data.find_all(
                    "a", attrs={"class": "discreet_link"}
                )
                rows_labels = [row.text.strip() for row in main_table_rows][1:-1]
                rows_labels.append("Quality of Life Index")  # fixing the footer label

                row_df = pd.DataFrame(
                    {
                        "Category": rows_labels,
                        "Value": rows_values,
                        "Level": rows_levels,
                    }
                )

                logger.info(
                    f"Found {row_df.shape[0]} data rows "
                    + f"and {row_df.shape[0]} features.\n"
                )

                row_df["City"] = [city] * row_df.shape[0]

                city_dataframe = pd.concat(
                    [city_dataframe, row_df], axis=0, ignore_index=True
                )

                dataframes = pd.concat(
                    [dataframes, city_dataframe], axis=0, ignore_index=True
                )
            else:
                logger.error(f"Could not find data for URL {full_url}.\n")

        return dataframes

    def _traffic_city_mode(
        self,
        category: str,
        cities: Union[str, List[str]],
    ) -> pd.DataFrame:
        """
        Extracts the traffic considering the 'city mode',
        which means that the data extracted will be for the desired city.

        Args:
            category (str): the current category.
            cities (Union[str, List[str]]): the cities that will be scraped.

        Returns:
            dataframes (List[Tuple[str, pd.DataFrame]]): a list containing
                the traffic data (saved in a dataframe format) for the given
                cities.
        """
        dataframes = pd.DataFrame()
        logger.warning(
            "Filter by year option can not be used for this category and mode.\n"
        )

        for city in cities:
            city_dataframe = pd.DataFrame()
            city = city.title().replace(" ", "-")  # formatting the city's name
            logger.info(
                f"Collecting '{category}' data in 'city' mode for city '{city}'.\n"
            )

            full_url = f"{BASE_URL}/{category}/in/{city}"

            request = requests.get(full_url, timeout=300)

            if request.status_code == 200:
                numbeo_html_data = BeautifulSoup(request.text, "html.parser")

                # getting the tables headers
                tables_headers = numbeo_html_data.find_all("h3")

                # getting the tables
                tables = [
                    tbl for tbl in numbeo_html_data.find_all("table") if not tbl.attrs
                ][:-1]

                # extracting the data from the tables
                city_dataframe = self._get_tables_city_mode(
                    tables_headers=tables_headers,
                    tables=tables,
                    attributes_class_name="trafficCaptionTd",
                    attributes_values_class_name="trafficTd",
                )

                # getting the indices table
                indices_df = self._get_index_table(
                    html_data=numbeo_html_data,
                    index_table_class_name="table_indices",
                    indices_values_style="text-align: right",
                    create_level_column=False,
                )

                city_dataframe = pd.concat(
                    [city_dataframe, indices_df], axis=0, ignore_index=True
                )

                logger.info(
                    f"Found {city_dataframe.shape[0]} data rows "
                    + f"and {city_dataframe.shape[0]} features.\n"
                )

                city_dataframe["City"] = [city] * city_dataframe.shape[0]

                dataframes = pd.concat(
                    [dataframes, city_dataframe], axis=0, ignore_index=True
                )
            else:
                logger.error(f"Could not find data for URL {full_url}.\n")

        return dataframes

    def _others_city_mode(
        self,
        category: str,
        cities: Union[str, List[str]],
    ) -> pd.DataFrame:
        """
        Extracts others measurements (crime and health care) considering
        the 'city mode', which means that the data extracted will be for the desired city.

        Args:
            category (str): the current category.
            cities (Union[str, List[str]]): the cities that will be scraped.

        Returns:
            dataframes (List[Tuple[str, pd.DataFrame]]): a list containing
                the data (saved in a dataframe format) for the given cities.
        """
        dataframes = pd.DataFrame()
        logger.warning(
            "Filter by year option can not be used for this category and mode.\n"
        )

        for city in cities:
            city_dataframe = pd.DataFrame()
            city = city.title().replace(" ", "-")  # formatting the city's name
            logger.info(
                f"Collecting '{category}' data in 'city' mode for city '{city}'.\n"
            )

            full_url = f"{BASE_URL}/{category}/in/{city}"

            request = requests.get(full_url, timeout=300)

            if request.status_code == 200:
                numbeo_html_data = BeautifulSoup(request.text, "html.parser")

                # getting the tables headers
                tables_headers = numbeo_html_data.find_all("h2")

                # getting the tables
                tables = numbeo_html_data.find_all(
                    "table",
                    attrs={
                        "class": "table_builder_with_value_explanation data_wide_table"
                    },
                )

                # extracting the data from the tables
                city_dataframe = self._get_tables_city_mode(
                    tables_headers=tables_headers,
                    tables=tables,
                    attributes_class_name="columnWithName",
                    attributes_values_class_name="indexValueTd",
                    levels_class_name="hidden_on_small_mobile",
                )

                # getting the indices table
                indices_df = self._get_index_table(
                    html_data=numbeo_html_data,
                    index_table_class_name="table_indices",
                    indices_values_style="text-align: right",
                )

                city_dataframe = pd.concat(
                    [city_dataframe, indices_df], axis=0, ignore_index=True
                )

                logger.info(
                    f"Found {city_dataframe.shape[0]} data rows "
                    + f"and {city_dataframe.shape[0]} features.\n"
                )

                city_dataframe["City"] = [city] * city_dataframe.shape[0]

                dataframes = pd.concat(
                    [dataframes, city_dataframe], axis=0, ignore_index=True
                )
            else:
                logger.error(f"Could not find data for URL {full_url}.\n")

        return dataframes

    def _pollution_city_mode(
        self,
        category: str,
        cities: Union[str, List[str]],
    ) -> pd.DataFrame:
        """
        Extracts pollution data considering the 'city mode',
        which means that the data extracted will be for the desired city.

        Args:
            category (str): the current category.
            cities (Union[str, List[str]]): the cities that will be scraped.

        Returns:
            dataframes (List[Tuple[str, pd.DataFrame]]): a list containing
                the pollution data (saved in a dataframe format) for the given
                cities.
        """
        dataframes = pd.DataFrame()
        logger.warning(
            "Filter by year option can not be used for this category and mode.\n"
        )

        for city in cities:
            city = city.title().replace(" ", "-")  # formatting the city's name
            logger.info(
                f"Collecting '{category}' data in 'city' mode for city '{city}'.\n"
            )

            full_url = f"{BASE_URL}/{category}/in/{city}"

            request = requests.get(full_url, timeout=300)

            if request.status_code == 200:
                numbeo_html_data = BeautifulSoup(request.text, "html.parser")

                # getting the tables headers
                tables_headers = numbeo_html_data.find_all("h2")

                # getting the tables
                tables = numbeo_html_data.find_all(
                    "table",
                    attrs={
                        "class": "table_builder_with_value_explanation data_wide_table"
                    },
                )

                # extracting the data from the tables
                city_dataframe = self._get_tables_city_mode(
                    tables_headers=tables_headers,
                    tables=tables,
                    attributes_class_name="columnWithName",
                    attributes_values_class_name="indexValueTd",
                    levels_class_name="hidden_on_small_mobile",
                )

                # creating the pollution indexes dataframe
                try:
                    pol_indices_df = self._get_index_table(
                        html_data=numbeo_html_data,
                        index_table_class_name="who_pollution_data_widget",
                        indices_values_style="text-align: right",
                        pollution_index_table=True,
                    )
                except AttributeError:
                    # some cities doesn't have the pollution index table,
                    # so we'll just ignore it
                    logger.warning(
                        f"Could not find pollution index for URL {full_url}.\n"
                    )
                    pol_indices_df = pd.DataFrame()

                # creating the indexes dataframe
                indices_df = self._get_index_table(
                    html_data=numbeo_html_data,
                    index_table_class_name="table_indices",
                    indices_values_style="text-align: right",
                )

                city_dataframe = pd.concat(
                    [city_dataframe, indices_df, pol_indices_df],
                    axis=0,
                    ignore_index=True,
                )

                logger.info(
                    f"Found {city_dataframe.shape[0]} data rows "
                    + f"and {city_dataframe.shape[0]} features.\n"
                )

                city_dataframe["City"] = [city] * city_dataframe.shape[0]

                dataframes = pd.concat(
                    [dataframes, city_dataframe], axis=0, ignore_index=True
                )
            else:
                logger.error(f"Could not find data for URL {full_url}.\n")

        return dataframes

    @logger.catch
    def _get_index_table(
        self,
        html_data: BeautifulSoup,
        index_table_class_name: str,
        indices_values_style: str,
        pollution_index_table: bool = False,
        create_level_column: bool = True,
    ) -> pd.DataFrame:
        """
        Extracts the index table within the page. This necessary only
        when we are getting the data using the 'city' mode (and only
        for the 'crime', 'health care', 'traffic', and 'pollution'
        measurements).

        Args:
            html_data (BeautifulSoup): the page HTML code.
            index_table_class_name (str): the index table class string.
                It's used to identify the index table.
            indices_values_style (str): the indices values style string.
                It's used to extract the table values.
            pollution_index_table (bool, optional): Whether it's a special
                case of the individual pollution index table or not. Defaults to False.
            create_level_column (bool, optional): Whether to create
                a 'Level' column or not. Defaults to True.

        Returns:
            pd.DataFrame: the index table in a dataframe format.
        """
        logger.info("Getting the index table using values:\n")
        logger.info(
            f"index_table_class_name: {index_table_class_name}, "
            + f"indices_values_style: {indices_values_style}, "
            + f"pollution_index_table: {pollution_index_table}, "
            + f"create_level_column: {create_level_column}\n"
        )

        # getting the indices table
        indices_table = html_data.find("table", attrs={"class": index_table_class_name})

        # extracting the indices name
        indices = [ind for ind in indices_table.find_all("td") if not ind.attrs]
        indices = [indice.text.strip().replace(":", "") for indice in indices]

        # extracting the indices values
        indices_values = indices_table.find_all(
            "td",
            attrs={"style": indices_values_style},
        )
        indices_values = [
            value.text.strip().replace(":", "") for value in indices_values
        ]

        # creating the index dataframe
        if not pollution_index_table:
            indices_df = pd.DataFrame(
                {
                    "Header": ["Index"] * len(indices),
                    "Category": indices,
                    "Value": indices_values,
                    "Level": [pd.NA] * len(indices),
                }
            )
        else:
            indices_df = pd.DataFrame(
                {
                    "Header": ["Index"] * len(indices),
                    "Category": indices,
                    "Value": indices_values[:-1] + [pd.NA],
                    "Level": [pd.NA, pd.NA, indices_values[-1]],
                }
            )

        # deleting the 'level' column
        if not create_level_column:
            logger.info("Deleting the 'level' column.\n")
            indices_df = indices_df.drop(columns=["Level"])

        return indices_df

    @logger.catch
    def _get_tables_city_mode(
        self,
        tables_headers: List,
        tables: List,
        attributes_class_name: str,
        attributes_values_class_name: str,
        levels_class_name: str = None,
    ) -> pd.DataFrame:
        """
        Extracts the tables for the majority of the measurements for the 'city'
        mode. With the exception of 'cost of living', the page for the other
        measures isn't organized in just only table, but rather multiple ones.

        Args:
            tables_headers (List): a list containing the tables headears.
            tables (List): a list containing the tables HTML.
            attributes_class_name (str): the table attributes class string.
                It's used to identify the table attributes.
            attributes_values_class_name (str): the table attributes values
                class string. It's used to identify the table data.
            levels_class_name (str, optional): the levels class string.
                It's used to identify the table measures levels. Defaults to None.

        Returns:
            pd.DataFrame: the collected data in a dataframe format.
        """
        logger.info("Getting the data table for city mode using values:\n")
        logger.info(
            f"attributes_class_name: {attributes_class_name}, "
            + f"attributes_values_class_name: {attributes_values_class_name}, "
            + f"levels_class_name: {levels_class_name}\n"
        )
        city_dataframe = pd.DataFrame()

        for header, table in zip(
            tables_headers,
            tables,
        ):
            # getting only the header text
            header_text = header.text

            # getting the attributes name
            attributes_name = table.find_all(
                "td",
                attrs={"class": attributes_class_name},
            )
            attributes_name = [att.text.strip() for att in attributes_name]

            # getting the attributes value
            values = table.find_all(
                "td",
                attrs={"class": attributes_values_class_name},
            )
            values = [value.text.strip() for value in values]

            # getting the levels value
            if not levels_class_name is None:
                logger.info("Getting the level data for all attributes.\n")
                levels = table.find_all(
                    "td",
                    attrs={"class": levels_class_name},
                )
                levels = [level.text.strip() for level in levels]

                row_df = pd.DataFrame(
                    {
                        "Header": [header_text] * len(values),
                        "Category": attributes_name,
                        "Value": values,
                        "Level": levels,
                    }
                )
            else:
                row_df = pd.DataFrame(
                    {
                        "Header": [header_text] * len(values),
                        "Category": attributes_name,
                        "Value": values,
                    }
                )

            city_dataframe = pd.concat(
                [city_dataframe, row_df], axis=0, ignore_index=True
            )

        return city_dataframe
