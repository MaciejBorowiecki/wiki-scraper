import requests
import os
from .wiki_article import WikiArticle
from .exceptions import ArticleFetchError


class WikiScraper:
    """
    Represents a scrapper responsible for fetching wiki data.
    Handles both network and local read requests.
    """

    def __init__(
        self,
        base_url: str = "https://bulbapedia.bulbagarden.net/wiki",
        language: str = "en",
        use_local_html_file_instead: bool = False,
        base_path: str = "",
    ):
        self.base_url = base_url.rstrip("/")
        self.language = language
        self.use_local_file = use_local_html_file_instead
        self.base_path = base_path

    def get_language(self) -> str:
        return self.language

    def _extract_text_from_file(self, filename: str) -> str :
        try:
            with open(filename, "r") as f:
                content = f.read()
                return content
        except IOError as e:
            raise ArticleFetchError(f"Error reading local file: {e}")

    def _handle_local_file(self, phrase: str) -> str:
        # Handle files with ' ' or '_' the same.
        file = self.base_path + phrase + ".html"
        file_ = self.base_path + file.replace(" ", "_")

        if not os.path.exists(file) and not os.path.exists(file_):
            raise ArticleFetchError(f"Local file not found for phrase: {phrase}")

        if os.path.exists(file):
            return self._extract_text_from_file(file)
        else:
            return self._extract_text_from_file(file_)

    def _handle_online_request(self, phrase: str) -> str:
        url = f"{self.base_url}/{phrase.replace(' ', '_')}"

        try:
            response = requests.get(url)

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ArticleFetchError(f"Network error fetching '{url}': {e}.")

        return response.text

    def scrape(self, phrase: str) -> WikiArticle:
        """
        Handles fetching raw html content and returns WikiArticle object.
        Raises ArticleFetchError if error occurs.
        """

        if self.use_local_file:
            content = self._handle_local_file(phrase)
        else:
            content = self._handle_online_request(phrase)

        return WikiArticle(phrase, content, self.language)
