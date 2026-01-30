import requests
import os
from wiki_article import WikiArticle


class WikiScraper:
    """
    Represents a scrapper responsible for fetching wiki data.
    Handles both network and local read requests.
    """

    def __init__(self, base_url: str = "https://bulbapedia.bulbagarden.net/wiki",
                 language: str = "en", use_local_html_file_instead: bool = False,
                 base_path: str = ""):
        self.base_url = base_url.rstrip('/')
        self.language = language
        self.use_local_file = use_local_html_file_instead
        self.base_path = base_path

    def get_language(self):
        return self.language

    def _extract_text_from_file(self, filename: str):
        try:
            with open(filename, 'r') as f:
                content = f.read()
                return content
        except IOError as e:
            print(f"Error reading file: {e}")
            return None       

    def _handle_local_file(self, phrase: str):
        # Handle files with ' ' or '_' the same.
        file = self.base_path + phrase + ".html"
        file_ = self.base_path + file.replace(' ', '_')

        if not os.path.exists(file) and not os.path.exists(file_):
            print("Error, there is no file '{file}' in current directory.")
            return None

        if os.path.exists(file):
            return self._extract_text_from_file(file)
        else:
            return self._extract_text_from_file(file_)
            
    def _handle_online_request(self, phrase: str):
        url = f"{self.base_url}/{phrase.replace(' ', '_')}"

        try:
            response = requests.get(url)

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}.")
            return None

        return response.text

    def scrape(self, phrase: str):
        """
        Handles fetching raw html content and returns WikiArticle object or None in case of error.
        """

        if self.use_local_file:
            content = self._handle_local_file(phrase)
        else:
            content = self._handle_online_request(phrase)

        if content:
            return WikiArticle(phrase, content, self.language)

        print("There was no content after fetching webpage.")
        return None
