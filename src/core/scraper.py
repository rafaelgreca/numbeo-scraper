import requests
from typing import List, Tuple

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from ..schema.input import Input


BASE_URL = 'https://www.numbeo.com/'
REGIONS_MAPPING = {
    'Africa': '002',
    'America': '019',
    'Asia': '142',
    'Europe': '150',
    'Oceania': '009',
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

        if isinstance(config.category, str):
            self.category = [config.category]
        else:
            self.category = config.category

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

        if self.mode == 'country':
            # iterating over the categories
            for category in self.category:
                if not self.regions is None:
                    # iterating over the regions, if not none
                    for region in self.regions:
                        data = self._country_mode(
                            category=category,
                            region=region,
                        )
                        data_name = f'{category}_{self.mode}'
                        dataframes.append((data_name, data))
                else:
                    data = self._country_mode(
                        category=category,
                        region=self.regions,
                    )
                    data_name = f'{category}_{self.mode}'
                    dataframes.append((data_name, data))

        return dataframes

    def _country_mode(
        self,
        category: str,
        region: str,
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
            country_page = 'rankings_by_country.jsp'

            if region is None:
                full_url = f'{BASE_URL}/{category}/{country_page}?title={year}'
            else:
                region_code = REGIONS_MAPPING[region]
                full_url = f'{BASE_URL}/{category}/{country_page}?title={year}&region={region_code}'

            request = requests.get(full_url, timeout=300)

            if request.status_code == 200:
                numbeo_html_data = BeautifulSoup(request.text, 'html.parser')
                main_table = numbeo_html_data.find('table', attrs={'id':'t2'})

                main_table_header = main_table.find('thead')
                main_table_header_rows = main_table_header.find_all('th')
                table_columns_name = [row.text for row in main_table_header_rows]
                dataframe = pd.DataFrame(columns=table_columns_name)

                main_table_body = main_table.find('tbody')
                main_table_rows = main_table_body.find_all('tr')

                for rank, row in enumerate(main_table_rows, start=1):
                    data = row.find_all('td')[1:]
                    data = [d.text for d in data]
                    data = [rank] + data # appeding rank to the list
                    data = np.asarray(data).reshape(1, -1).tolist() # reshaping so we can concatenate it

                    new_row = pd.DataFrame(
                        data,
                        columns=table_columns_name
                    )
                    dataframe = pd.concat([dataframe, new_row], axis=0, ignore_index=True)

                dataframe['Year'] = [year] * dataframe.shape[0]
                dataframes = pd.concat([dataframes, dataframe], axis=0, ignore_index=True)

        return dataframes
