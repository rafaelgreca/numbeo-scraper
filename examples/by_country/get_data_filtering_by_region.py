from pathlib import Path

from src.core.utils import read_yaml_credentials_file
from src.schema.input import Input
from src.core.scraper import NumbeoScraper


if __name__ == "__main__":
    # reading the YAML file
    config = Input(
        **read_yaml_credentials_file(
            file_path=Path.joinpath(
                Path(__file__).resolve().parents[1],
                "configs",
            ),
            file_name="filter_data_by_region_country.yaml",
        )
    )

    scraper = NumbeoScraper(
        config=config,
    )
    dataframes = scraper.scrap()  # will return a list of tuples

    for dataframe_name, data in dataframes:
        print(f"\nDataframe '{dataframe_name}' has a shape of {data.shape}.")
        print(f"The first five rows of the dataset:\n{data.head(5)}\n")
        print()
