<a id="readme-top"></a>

# Numbeo Scraper

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
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

Create a virtual environment (ideally using conda) and install the requirements with the following command:

```bash
conda create --name numbeo-scraper python=3.10.16 
conda activate numbeo-scraper
pip install -r requirements.txt
```

### (RECOMMENDED) Using Docker

Build the Docker image using the following command:

```bash
sudo docker build -f Dockerfile -t numbeo-scraper . --no-cache
```

Run the Docker container using the following command:

```bash
sudo docker run -d --name numbeo-scraper-container numbeo-scraper
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- EXAMPLES -->

## Examples

Check the `examples` folder to see some examples of how to use   this library.

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

- [x] Country
    - [x] Extract the data related to the cost of living of each country.
    - [x] Extract the data related to the property prices of each country.
    - [x] Extract the data related to the quality of life of each country.
    - [x] Extract the data related to the crime index of each country.
    - [x] Extract the data related to the health care index of each country.
    - [x] Extract the data related to the pollution index of each country.
    - [x] Extract the data related to the traffic index of each country.
- [ ] City
    - [x] Extract the data related to the cost of living of each city.
    - [x] Extract the data related to the property prices of each city.
    - [x] Extract the data related to the quality of life of each city.
    - [ ] Extract the data related to the crime index of each city.
    - [ ] Extract the data related to the health care index of each city.
    - [ ] Extract the data related to the pollution index of each city.
    - [ ] Extract the data related to the traffic index of each city.

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