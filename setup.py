from setuptools import setup, find_packages

VERSION = "2.0.0"
DESCRIPTION = """
The largest crowdsourced global database of quality of life data, including housing indicators, perceived crime rates, healthcare quality, transportation quality, and other statistics, is [Numbeo](https://www.numbeo.com/). In order to save time when searching for information about the quality of life in a particular country or city, the project's goal is to use web scraping frameworks (in this case, the BeautifulSoup4 library) to extract data from Numbeo's website.
"""

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = f.read()

setup(
    name="Numbeo Scraper",
    version=VERSION,
    author="Rafael Greca Vieira",
    author_email="me@rgrecav.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["src"]),
    install_requires=install_requires,
    test_suite="tests",
    keywords=[
        "python",
        "scraper",
        "web scraping",
        "numbeo",
    ],
    python_requires=">=3.10",
)
