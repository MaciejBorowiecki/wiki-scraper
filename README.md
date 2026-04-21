# WikiScraper

A Python tool for scraping and analyzing data from wiki websites (created with [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Main_Page) in mind). Extract article summaries, tables, and perform statistical analysis on word frequencies across wiki articles.

## Features

- **Article Summaries**: Extract and display the first paragraph of a wiki article
- **Table Extraction**: Fetch specific tables from wiki articles and save to CSV format
- **Word Statistics**: Count word occurrences in articles and save results to JSON
- **Frequency Analysis**: Compare word frequency in scraped articles against language statistics
- **Recursive Crawling**: Automatically crawl and analyze linked articles up to a specified depth
- **Visualization**: Generate charts comparing word frequencies between articles and language data
- Modular, object-oriented design for easy testing and reusability
- Support for local HTML file testing without network requests
- Comprehensive unit and integration tests

## Installation

### Prerequisites

- Python 3.7+
- Virtual environment (recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd wiki-scraper
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

```bash
# Extract article summary
python wiki_scraper.py --summary "Team Rocket"

# Extract specific table
python wiki_scraper.py --table "Type" --number 2

# Count words in an article
python wiki_scraper.py --count-words "Bulbasaur"

# Analyze word frequency relative to wiki language
python wiki_scraper.py --analyze-relative-word-frequency --mode article --count 10

# Generate frequency comparison chart
python wiki_scraper.py --analyze-relative-word-frequency --mode article --count 10 --chart "output.png"

# Recursive word counting with crawling
python wiki_scraper.py --auto-count-words "Pokemon" --depth 2 --wait 1
```

### Command Options

#### Summary Extraction
- `--summary PHRASE`: Fetch and print the first paragraph for the given phrase

#### Table Extraction
- `--table PHRASE`: Fetch a specific table from the article
- `--number INDEX`: Index of the table to extract (1-based, required with `--table`)
- `--first-row-is-header`: Treat the first row as column headers

#### Word Statistics
- `--count-words PHRASE`: Count word occurrences and save to `./word-counts.json`
- `--analyze-relative-word-frequency`: Compare article word frequency to language statistics (requires `--mode` and `--count`)
- `--mode {article|language}`: Sort results by article or language frequency
- `--count N`: Number of top words to compare
- `--chart PATH`: Generate visualization chart (optional, requires `--analyze-relative-word-frequency`)

#### Recursive Crawling
- `--auto-count-words PHRASE`: Start crawling from phrase
- `--depth N`: Maximum crawl depth (required with `--auto-count-words`)
- `--wait TIME`: Wait time in seconds between requests (required with `--auto-count-words`)

## Project Structure

```
wiki-scraper/
├── wiki_scraper.py                    # Main entry point
├── wiki_scraper_integration_test.py   # Integration tests with local HTML files
├── src/
│   ├── wiki_manager.py               # Main controller class
│   ├── wiki_article.py               # Wiki article representation
│   ├── scraper_logic.py              # Article scraping logic
│   ├── exceptions.py                 # Custom exceptions
│   └── __init__.py
├── tests/
│   ├── arguments_test.py             # Unit tests for argument parsing
│   ├── link_extraction_test.py       # Unit tests for link extraction
│   └── __init__.py
├── data/
│   ├── Kanto.html                    # Local HTML file for testing
│   ├── monty_python.html             # Local HTML file for testing
│   ├── pizza.html                    # Local HTML file for testing
│   └── pythonidae.html               # Local HTML file for testing
├── language_analysis.ipynb           # Language detection analysis and research
├── requirements.txt                  # Python dependencies
└── .gitignore
```

## Testing

### Run Unit Tests

```bash
python -m pytest tests/
```

### Run Integration Tests

```bash
python3 wiki_scraper_integration_test.py
```

The integration test loads HTML from local files (instead of fetching from the wiki) to avoid network dependencies.

## Language Detection Analysis

The project includes analysis of word frequency patterns. See `language_analysis.ipynb` for:

- Comparison of word frequencies between wiki articles and language statistics
- Word frequency analysis methods and results

## Architecture

The codebase follows object-oriented design principles with clear separation of concerns:

- **WikiManager**: Main controller that interprets command-line arguments and orchestrates all operations
- **WikiScraper**: Handles HTTP requests and HTML file loading (supports both network and local file sources)
- **WikiArticle**: Parses HTML content and provides methods to extract data (summaries, tables, word counts, links)

## Example Wiki Sites

The tool *(with slight modifications)* works with any wiki that allows scraping, out of the box it works with Bulbapedia and it is encouraged to use it with this one:

- [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Team_Rocket) - Pokémon wiki
- [Explain XKCD](https://www.explainxkcd.com/) - XKCD comic explanations
- [Proteopedia](https://proteopedia.org/) - Protein structure wiki

**Note**: Avoid Wikipedia subdomains as they have anti-scraping protections.

## Notes

- Words are analyzed in their original form without lemmatization
- The tool can work with any language
- Specify `--wait` time appropriately to avoid rate limiting
- Use `use_local_html_file_instead=True` parameter for testing without network requests

## Development

The code follows PEP8 style guidelines. Key design features:

- Modular architecture for easy testing and reusability
- Support for local HTML file testing
- Classes accept explicit parameters rather than global state
- Comprehensive error handling and validation
