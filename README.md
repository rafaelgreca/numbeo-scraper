<a id="readme-top"></a>

# Numbeo Scraper

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#examples">Examples</a></li>
    <li><a href="#running-tests">Running Tests</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

The largest crowdsourced global database of quality of life data, including housing indicators, perceived crime rates, healthcare quality, transportation quality, and other statistics, is [Numbeo](https://www.numbeo.com/). In order to save time when searching for information about the quality of life in a particular country or city, the project's goal is to use web scraping frameworks (in this case, the BeautifulSoup4 library) to extract data from Numbeo's website.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- INSTALLATION -->
## Installation

To install this package, first clone the repository to the directory of your choice using the following command:

```bash
git clone https://github.com/rafaelgreca/numbeo-scraper.git
```

### Using Virtual Environment

Create a virtual environment (ideally using conda) and install the requirements using the following command:

```bash
conda create --name numbeo-scraper python=3.10.16 
conda activate numbeo-scraper
pip install -r requirements.txt
```

### Using Docker

Build the Docker image using the following command:

```bash
sudo docker build -f Dockerfile -t numbeo-scraper . --no-cache
```

Run the Docker container using the following command:

```bash
sudo docker run -it --name numbeo-scraper-container numbeo-scraper
```

Finally, run the following command inside the container:

```bash
python3 -m <YOUR_PYTHON_FILE_LOCATION>
```

Example (this is the same command as used with the virtual environment approach):

```bash
python3 -m examples.by_country.get_quality_of_life_data
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features

* [Cost of living index by country](https://www.numbeo.com/cost-of-living/rankings_by_country.jsp) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_country/get_cost_of_living_data.py)) or [by city](https://www.numbeo.com/cost-of-living/) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_city/get_cost_of_living_data.py)).

* [Property price/investment index by country](https://www.numbeo.com/property-investment/rankings_by_country.jsp) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_country/get_property_investment_data.py)) or [by city](https://www.numbeo.com/property-investment/) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_city/get_property_investment_data.py)).

* [Quality of life index by country](https://www.numbeo.com/quality-of-life/rankings_by_country.jsp) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_country/get_quality_of_life_data.py)) or [by city](https://www.numbeo.com/quality-of-life/) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_city/get_quality_of_life_data.py)).

* [Crime index by country](https://www.numbeo.com/crime/rankings_by_country.jsp) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_country/get_crime_data.py)) or [by city](https://www.numbeo.com/crime/) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_city/get_crime_data.py)).

* [Health care index by country](https://www.numbeo.com/health-care/rankings_by_country.jsp) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_country/get_health_care_data.py)) or [by city](https://www.numbeo.com/health-care/) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_city/get_health_care_data.py)).

* [Pollution index by country](https://www.numbeo.com/pollution/rankings_by_country.jsp) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_country/get_pollution_data.py)) or [by city](https://www.numbeo.com/pollution/) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_city/get_pollution_data.py)).

* [Traffic index by country](https://www.numbeo.com/traffic/rankings_by_country.jsp) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_country/get_traffic_data.py)) or [by city](https://www.numbeo.com/traffic/) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_city/get_traffic_data.py)).

* [Historical data in a country](https://www.numbeo.com/cost-of-living/historical-data-country) (check an example [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/examples/by_country/get_historical_data.py)).

<!-- EXAMPLES -->
## Examples

You can pass the variables that will be used to collect the desired data by creating a YAML file (such as the `config.yaml` file located in the root folder) and creating a piece of code like the one below (and saving in a Python file, obviously):

```python
from pathlib import Path

from src.core.utils import read_yaml_credentials_file
from src.schema.input import Input
from src.core.scraper import NumbeoScraper

if __name__ == "__main__":
    # reading the YAML file
    config = Input(
        **read_yaml_credentials_file(
            file_path=Path(__file__).resolve().parents[1], # the folder where the config file is located
            file_name="config.yaml", # the configuration file name
        )
    )

    scraper = NumbeoScraper(
        config=config,
    )
    dataframes = scraper.scrap()  # will return a list of tuples (each category will be saved separately)
                                  # where the first index is the name of the dataframe
                                  # and the second one is the collected data 

    dataframe_name, data = dataframes[0]  # the name is used to identify the data

    print(f"\nDataframe '{dataframe_name}' has a shape of {data.shape}.")
    print(f"The first five rows of the dataset:\n{data.head(5)}\n")
```

Or you can pass the values directly, like this:

```python
from src.schema.input import Input
from src.core.scraper import NumbeoScraper

if __name__ == "__main__":
    config = Input(
        categories="historical-data",
        years=2021,
        mode="country",
        currency="EUR",
        historical_items=[
          '1 Pair of Jeans (Levis 501 Or Similar)',
          'Banana (1kg)'
        ],
        countries=[
          'China',
          'France',
          'United States'
        ],
    )

    scraper = NumbeoScraper(
        config=config,
    )
    dataframes = scraper.scrap()  # will return a list of tuples (each category will be saved separately)
                                  # where the first index is the name of the dataframe
                                  # and the second one is the collected data 

    dataframe_name, data = dataframes[0]  # the name is used to identify the data

    print(f"\nDataframe '{dataframe_name}' has a shape of {data.shape}.")
    print(f"The first five rows of the dataset:\n{data.head(5)}\n")
```

Available parameters that can/must be used:

* `categories` (can be a list of strings or just a string, **mandatory**): Which type of data will be collected. You can see the available categories [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/src/schema/input.py#L38).

* `years` (can be a list of integers or just an integer, **mandatory**): Which years the data will be extracted from. You can see the available years [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/src/schema/input.py#L8).

* `mode` (a string, **mandatory**): Whether the data will be collected by `country` or by `city`. You can see the available modes [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/src/schema/input.py#L49).

* currency (a string, **optional**): Which currency the values will be displayed. You can see the available currencies [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/src/schema/input.py#L53). This parameter is optional; however it **must be** used when the chosen category is `historical-data` with mode `country` or `cost-of-living` or `property-investment` with mode `city`.

* historical_items (can be a list of strings or just a string, **optional**): Which items the historical data will be extracted from. You can see the available items [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/src/schema/input.py#L448). This parameter is optional, however it **must be** used when the chosen category is `historical-data` with mode `country`.

* `countries` (can be a list of strings or just a string, **optional**): Which countries the data will be extracted from. You can see the available countries [here](https://github.com/rafaelgreca/numbeo-scraper/blob/main/src/schema/input.py#L212).

* `cities` (can be a list of strings or just a string, **mandatory**): Which cities will the data be extracted from. This parameter is mandatory when the mode `city` is chosen.

Check the `examples` folder to see more examples of how to use this library.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- RUNNING TESTS -->

## Running Tests

Run the following command on the root folder:

```bash
python3 -m unittest discover -p 'test_*.py'
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Add a feature to get the [food prices](https://www.numbeo.com/food-prices/) by country or by city.

- [ ] Fix logging (currently it's not saving the logs into a file, but rather showing them directly in the terminal).

- [ ] Improve testing cases, especially to validate the parameters values and typing.

- [X] Test the code using Docker.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Rafael Greca Vieira - [GitHub](https://github.com/rafaelgreca) - [LinkedIn](https://www.linkedin.com/in/rafaelgreca/) - me@rgrecav.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Acknowledgments -->
## Acknowledgments

In addition to helping people from all over the world plan their travels and find a new place to call home, [Numbeo](https://www.numbeo.com/) is the world's largest cost-of-living crowdsourced global database, and for that, I want to express my profound gratitude to everyone who works behind the scenes to make it possible.