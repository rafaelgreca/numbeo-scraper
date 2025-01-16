import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

import requests
from typing import List, Union, Tuple

BASE_URL = 'https://www.numbeo.com/'

class NumbeoScraper:

    def __init__(
        self,
        category: Union[str, List[str]],
        mode: str,
        years: Union[int, List[Union[int, str]]],
    ) -> None:
        if isinstance(category, str):
            self.category = [category]
        else:
            self.category = category

        if isinstance(category, int):
            self.years = [years]
        else:
            self.years = years

        self.mode = mode

    def scrap(
        self,
    ) -> List[Tuple[str, pd.DataFrame]]:
        dataframes = []

        if self.mode == 'country':
            for category in self.category:
                data = self._country_mode(category=category)
                data_name = f'{category}_{self.mode}'
                dataframes.append((data_name, data))

        return dataframes

    def _country_mode(
        self,
        category: str,
    ) -> pd.DataFrame:
        dataframes = pd.DataFrame()

        for year in self.years:
            full_url = f'{BASE_URL}/{category}/rankings_by_country.jsp?title={year}'
            request = requests.get(full_url, timeout=300)
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
