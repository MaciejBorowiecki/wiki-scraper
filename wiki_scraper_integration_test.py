import sys
import os
from scraper_logic import WikiScraper

def normalize_text(text: str) -> str:
    """
    Removes whitespace and new lines from the text for more robust comparison.
    """
    if not text:
        return ""
    return ' '.join(text.split())
    
    
def test_kanto_summary():
    """
    Integration test for wiki_scraper CLI tool. Tests integration between modules
    by extracting summary from Kanto.html local file.
    """

    # prepare beginning and ending of the text for comparisons
    expected_text = (
        "The Kanto region (Japanese: カントー地方 Kanto region) is a region "
        "of the Pokémon world. Kanto is located east of Johto, which "
        "together form a joint landmass that is south of Sinnoh."
    )
    expected_normalized = normalize_text(expected_text)
    expected_start = expected_normalized[:50]
    expected_end = expected_normalized[-50:]
    base_dir = 'data/'
    phrase = 'Kanto'

    # check if testing html file exists
    path = base_dir + phrase + '.html'
    assert os.path.exists(path), "Error: file not found."

    try:
        scraper = WikiScraper(
            use_local_html_file_instead=True, base_path=base_dir)

        print(f"Scraping article: '{phrase}'...")
        article = scraper.scrape(phrase)

        assert article is not None, "Scraper.scrape() returned None."

        summary = article.get_summary()
        assert summary is not None, "Summary is empty."

        # normalize result text for comparison
        summary_normalized = ' '.join(summary.split())
        assert summary_normalized.startswith(expected_start), (
            f"Begginning error:\n"
            f"Expected: {expected_start}...\n"
            f"Got: {summary_normalized[:30]}"
        )
        
        assert summary_normalized.endswith(expected_end),(
            f"Ending error:\n" 
            f"Expected: {expected_end}...\n" 
            f"Got: {summary_normalized[-30:]}"
        )
        
        print("Integration test finished successfully.")
    except AssertionError as e:
        print(f"\nTest failed (Assertion): {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error occurred: {e}.")
        sys.exit(1)

if __name__ == "__main__":
    test_kanto_summary()