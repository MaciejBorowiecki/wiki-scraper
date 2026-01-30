from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import re


class WikiArticle:
    """
    Represents a parsed Wiki article and provides methods to extract data.
    Handles parsing of raw HTML contnet using BeautifulSoup.
    """

    def __init__(self, title: str, content: str, language: str):
        self.title = title
        self.content = content
        self.language = language
        self.soup = BeautifulSoup(content, 'html.parser')
        self._BANNED_PREFIXES = (
            '/wiki/File:',
            '/wiki/Template:',
            '/wiki/Bulbapedia:',
            '/wiki/MediaWiki:',
            '/wiki/User:',
            '/wiki/Category:',
            '/wiki/Help:',
            '/wiki/Browse:',
            '/wiki/Special:'
        )

        self.content_div = self.soup.find(
            'div', class_='mw-content-ltr mw-parser-output')

        if not self.content_div:
            print(
                f"Warning: Main content container was not found for '{title}'.")

    def get_summary(self):
        """
        Extracts summary (the first paragraph) of the article.
        """

        if not self.content_div:
            print(
                f"Warning: Main content container was not found for '{self.title}'.")
            return None

        first_paragraph = self.content_div.find('p')

        if not first_paragraph:
            print(f"First paragraph was not found for '{self.title}'.")
            return None
        return first_paragraph.get_text().strip()

    def get_table(self, index: int, use_first_row_as_header: bool = False):
        """
        Extracts the nth table (index is 1-based) from the article content.
        """

        if not self.content_div:
            print(
                f"Warning: Main content container was not found for '{self.title}'.")
            return None

        tables = self.content_div.find_all('table', limit=index)

        if not tables:
            print(f"Error: There are no tables on the '{self.title}' page.")
            return None

        if index < 1 or index > len(tables):
            print(f"Error: Table index out of bounds. For '{self.title}' ",
                  f"page index should be between 1 and {len(tables)}.")
            return None

        selected_table = tables[-1]
        selected_table_pd = StringIO(str(selected_table))

        header_row = 0 if use_first_row_as_header else None
        try:
            df_selected_table = pd.read_html(
                selected_table_pd,
                header=header_row,
                index_col=0
            )

            if df_selected_table[0].empty:
                print("Error: there is no data in selected table.")
                return None
            return df_selected_table[0]
        except ValueError:
            print("Error: {e}.")
            return None

    def _count_words(self, words: list[str]) -> dict[str, int]:
        word_count = {}
        for word in words:
            if word.isalpha():
                word_count[word] = word_count.get(word, 0) + 1
        return word_count

    def get_word_count(self):
        """
        Counts number of occurrences of any word from a given article except from 
        constant elements of the page (e.g. menu).
        """

        if not self.content_div:
            print(
                f"Warning: Main content container was not found for '{self.title}'.")
            return {}

        text = self.content_div.get_text(separator=' ')
        words = re.findall(r'\w+', text.lower())

        word_dict = self._count_words(words)

        return word_dict

    def _is_valid_link(self, href: str) -> bool:
        """
        Check whether link is valid (it is content link and not technical or maintanence link).
        """
        if not href.startswith('/wiki/'):
            return False

        if href.startswith(self._BANNED_PREFIXES):
            return False

        return True

    def _process_link(self, href: str) -> str:
        """
        Eliminate repetitions caused by '#'.
        """
        if '#' in href:
            href = href.split('#')[0]

        href_phrase = href.replace('/wiki/', '')
        return href_phrase

    def get_linked_phrases(self) -> list[str]:
        """
        Returns a list of unique phrases (article titles) found in links in this article.
        """

        if not self.content_div:
            print(
                f"Warning: Main content container was not found for '{self.title}'.")
            return []

        unique_links = set()

        link_candidates = self.content_div.find_all('a', href=True)
        for a_tag in link_candidates:
            href = str(a_tag['href'])
            
            if self._is_valid_link(href):
                href_phrase = self._process_link(href)
                unique_links.add(href_phrase)

        return list(unique_links)
