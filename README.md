# wiki-scraper

A CLI tool for scraping, analysis and visualisation of the [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Main_Page) articles.

## Running project

#### firstly create virtual environment and install dependencies 

```bash
python3 -m venv venv
source venv/bin/activate
```

Then: 

```bash
pip install -r requirements.txt
```

#### Running program

```bash
python3 wiki_scraper.py [arguments]
```
*for more info about arguments check `python3 wiki_scraper.py --help`*

#### Running tests

```bash
pytest
```

or 

```bash
python3 wiki_scraper_integration_test.py
```