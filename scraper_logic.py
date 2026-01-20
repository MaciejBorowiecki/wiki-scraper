import requests
from wiki_article import WikiArticle


class WikiScraper:
    """
    Represents a scrapper responsible for fetching wiki data.
    Handles both network and local read requests.
    """

    def __init__(self, base_url: str = "https://bulbapedia.bulbagarden.net/wiki",
                 language: str = "en", use_local_html_file_instead: bool = False):
        self.base_url = base_url.rstrip('/')
        self.language = language
        self.use_local_file = use_local_html_file_instead
        self.history = {}

    def _handle_local_file(self, phrase):
        pass  # TODO

    def _handle_online_request(self, phrase):
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
        if phrase in self.history:
            return self.history[phrase]

        if self.use_local_file:
            content = self._handle_local_file(phrase)
        else:
            content = self._handle_online_request(phrase)

        if content:
            self.history[phrase] = WikiArticle(phrase, content, self.language)
            return self.history[phrase]

        print("There was no content after fetching webpage.")
        return None
