from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import numpy as np
import re
from .exceptions import ContentExtractionError


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

    def _get_content_div(self):
        """
        Helper that ensures content div exists and returns it.
        Raises ContentExtractionError if main contetn div is missing.
        """
        if self.content_div is None:
            raise ContentExtractionError(
                f"Main content div not found for article: '{self.title}'"
            )
        return self.content_div

    def get_summary(self) -> str:
        """
        Extracts summary (the first paragraph) of the article.
        """

        content = self._get_content_div()

        first_paragraph = content.find('p')

        if not first_paragraph:
            raise ContentExtractionError(
                f"No paragraph found in '{self.title}'")

        return first_paragraph.get_text().strip()

    def get_table(self,
                  index: int,
                  use_first_row_as_header: bool = False
                  ) -> pd.DataFrame:
        """
        Extracts the nth table (index is 1-based) from the article content.
        """

        content = self._get_content_div()

        tables = content.find_all('table', limit=index)

        if not tables:
            raise ContentExtractionError(
                f"No tables found on page '{self.title}'")

        if index < 1 or index > len(tables):
            raise ContentExtractionError(
                f"Table index out of bounds. For '{self.title}' "
                f"page index should be between 1 and {len(tables)}."
            )

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
                raise ContentExtractionError(
                    "there is no data in selected table."
                )

            return df_selected_table[0].replace(np.nan, "")
        except ValueError as e:
            raise ContentExtractionError(
                "Pandas dataframe ValueError: {e}"
            )

    def _count_words(self, words: list[str]) -> dict[str, int]:
        word_count = {}
        for word in words:
            if word.isalpha():
                word_count[word] = word_count.get(word, 0) + 1
        return word_count

    def get_word_count(self) -> dict[str, int]:
        """
        Counts number of occurrences of any word from a given article except
        from constant elements of the page (e.g. menu).
        """

        content = self._get_content_div()

        text = content.get_text(separator=' ')
        words = re.findall(r'\w+', text.lower())

        word_dict = self._count_words(words)

        return word_dict

    def _is_valid_link(self, href: str) -> bool:
        """
        Check whether link is valid (it is content link and not technical
        or maintanence link).
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
        Returns a list of unique phrases (article titles) 
        found in links in this article.
        """

        content = self._get_content_div()

        unique_links = set()

        link_candidates = content.find_all('a', href=True)
        for a_tag in link_candidates:
            href = str(a_tag['href'])

            if self._is_valid_link(href):
                href_phrase = self._process_link(href)
                unique_links.add(href_phrase)

        return list(unique_links)
