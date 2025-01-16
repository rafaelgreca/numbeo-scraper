from setuptools import setup, find_packages

VERSION = "1.0.0"
DESCRIPTION = """A Numbeo Scraper developed using Python 3."""

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = f.read()

setup(
    name="Numbeo Scraper",
    version=VERSION,
    author="Rafael Greca Vieira",
    author_email="rgvieira97@gmail.com",
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
