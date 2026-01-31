from .scraper_logic import WikiScraper
import time
import pandas as pd
import json
import os
import wordfreq
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from .exceptions import ArticleFetchError, ContentExtractionError


class WikiManager:
    """
    Represents controller responsible for interpreting already parsed arguments
    and executing appropriate methods.
    """

    def __init__(self, args, use_local_html_files_instead: bool = False):
        self.args = args
        self.scraper = WikiScraper(
            use_local_html_file_instead=use_local_html_files_instead
            )

    def _print_license_info(self, url: str):
        print(f"\nWyjście programu na licencji zgodnej z źródłem "
              + " (CC BY-NC-SA).")
        print(f"Dane pobrane z: {url}")

    def handle_args(self) -> None:
        """
        Automatically handle all given arguments.
        """

        phrase = ""

        if self.args.summary:
            self.handle_summary()
            phrase = self.args.summary
        if self.args.table:
            self.handle_table()
            phrase = self.args.table
        if self.args.count_words:
            self.handle_count_words()
            phrase = self.args.count_words
        if self.args.analyze_relative_word_frequency:
            self.handle_relative_word_frequency_analysis()
        if self.args.auto_count_words:
            self.handle_auto_count_words()
            phrase = self.args.auto_count_words

        full_url = self.scraper.base_url + "/" + phrase.replace(" ", "_")
        self._print_license_info(full_url)

    def handle_summary(self) -> None:
        phrase = self.args.summary
        try:
            article = self.scraper.scrape(phrase)
            summary_text = article.get_summary()

            print("\n-----Summary-----")
            print(summary_text, "\n")

        except ArticleFetchError as e:
            print(f"Error scraping article {phrase} : {e}.")
        except ContentExtractionError as e:
            print(f"Error. Failed to extract summary for '{phrase}': {e}")

    def handle_table(self) -> None:
        phrase = self.args.table
        try:
            article = self.scraper.scrape(phrase)

            df_table = article.get_table(
                self.args.number,
                self.args.first_row_is_header
            )

            print("\n-----Table-----")
            print(df_table.to_string(), "\n")

            filename = f"{phrase}.csv"
            df_table.to_csv(filename)
            print(f"Table saved to file: '{filename}'.\n")

            counts = {}

            for row in df_table.values:
                for item in row:
                    val = str(item)
                    if val in counts:
                        counts[val] += 1
                    else:
                        counts[val] = 1

            stats_df = pd.DataFrame(counts.items(), columns=["Value", "Count"])
            stats_df = stats_df.sort_values(by="Count", ascending=False)
            print(stats_df.to_string(index=False), "\n")

        except (ArticleFetchError, ContentExtractionError) as e:
            print(f"Error. Table operation failed: {e}")
        except Exception as e:
            print(f"Error. Unexpected error: {e}")

    def _get_total_counts(
        self,
        filename: str = "./word-counts.json"
    ) -> dict[str, int]:
        total_counts = {}
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    total_counts = json.load(f)
            except json.JSONDecodeError:
                print(
                    f"File '{filename}' corrupted or empty, creating new one.")
        else:
            print(f"File '{filename}' does not exist. Creating new one.")

        return total_counts

    def _update_json_stats(
        self, new_words_dict: dict[str, int],
        filename: str = "./word-counts.json"
    ) -> None:
        total_counts = self._get_total_counts()
        for word, count in new_words_dict.items():
            total_counts[word] = total_counts.get(word, 0) + count

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(total_counts, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error occurred while saving file: {e}")

        print("JSON file: 'word-counts.json' has been updated.")

    def handle_count_words(self) -> None:
        phrase = self.args.count_words

        try:
            article = self.scraper.scrape(phrase)
            word_dict = article.get_word_count()
            self._update_json_stats(word_dict)

        except ArticleFetchError as e:
            print(f"Error scraping article {phrase} : {e}.")
        except ContentExtractionError as e:
            print(f"Error. Could not extract words from '{phrase}': {e}.")

    def _get_n_most_popular(
        self,
        mode: str,
        total_counts: dict[str, int],
        n: int,
        language: str = "en"
    ) -> list[str]:
        if mode == "article":
            sorted_words = sorted(
                total_counts.keys(), key=lambda x: total_counts[x], reverse=True
            )
            return sorted_words[:n]
        else:
            return wordfreq.top_n_list(language, n)

    def _handle_chart(
        self,
        data: pd.DataFrame,
        path: str,
        language: str,
        base_width: int = 6,
        per_item_width: float = 0.4,
    ) -> None:
        """
        Generates a plot file comparing word frequencies across
        wiki language and scraping data.
        """

        n_items = len(data)
        fig_width = max(10, base_width + (n_items * per_item_width))
        fig_height = 6
        ax = data.plot(kind="bar", figsize=(fig_width, fig_height), width=0.8)

        plt.title("Frequency of some words on Wiki")
        plt.ylabel("frequency")
        plt.xlabel("words")
        plt.legend(["Wiki", f"Language: {language}"])
        plt.tight_layout()
        plt.xticks(rotation=45)  # rotate words under columns for readability

        try:
            plt.savefig(path)
            print(f"Chart saved to '{path}'.")
        except IOError as e:
            print(f"Error occurred while saving chart: {e}.")
        finally:
            plt.close()

    def handle_relative_word_frequency_analysis(self) -> None:
        mode = self.args.mode
        n_rows = self.args.count

        total_counts = self._get_total_counts()

        if not total_counts:
            print("Warning: there is no data collected from wiki yet.")
            return None

        language = self.scraper.get_language()

        n_most_popular = self._get_n_most_popular(
            mode, total_counts, n_rows, language)

        data = []
        for word in n_most_popular:
            wiki_count = total_counts.get(word, 0)
            lang_freq = wordfreq.word_frequency(word, language)

            data.append({"word": word, "wiki": wiki_count, "lang": lang_freq})

        data_pd = pd.DataFrame(data).set_index("word")

        wiki_count_max = data_pd["wiki"].max() if data_pd["wiki"].max() > 0 else 1
        lang_freq_max = data_pd["lang"].max() if data_pd["lang"].max() > 0 else 1
        data_pd["wiki_norm"] = data_pd["wiki"] / wiki_count_max
        data_pd["lang_norm"] = data_pd["lang"] / lang_freq_max

        sort_norm = "wiki_norm" if mode == "article" else "lang_norm"
        data_pd_sorted = data_pd.sort_values(by=sort_norm, ascending=True)
        data_pd_sorted = data_pd_sorted.replace(0, np.nan)

        print("\n-----Relative Word Frequency Analysis-----")
        print(data_pd_sorted[["wiki_norm", "lang_norm"]].to_string(
            na_rep=" ",
            float_format="%.6f"
        ))

        if self.args.chart:
            self._handle_chart(
                data_pd_sorted[["wiki_norm", "lang_norm"]],
                self.args.chart, language
            )

    def handle_auto_count_words(self) -> None:
        start_phrase = self.args.auto_count_words
        max_depth = self.args.depth
        wait_time = self.args.wait

        queue = deque([(start_phrase, 0)])
        visited = {start_phrase}

        # visiting next links untill max_depth is reached
        # or there are no more links to visit
        while queue:
            current_phrase, current_depth = queue.popleft()

            print(
                f"\n-----Counting Words on '{current_phrase}'" +
                " (Depth: {current_depth})-----"
            )
            try:
                current_article = self.scraper.scrape(current_phrase)
                if not current_article:
                    print(
                        f"Skipping '{current_phrase}'" +
                        " (Article not found or error occurred)."
                    )
                    continue

                word_dict = current_article.get_word_count()
                if word_dict:
                    self._update_json_stats(word_dict)

                if current_depth < max_depth:
                    links = current_article.get_linked_phrases()
                    for link in links:
                        if link not in visited:
                            visited.add(link)
                            queue.append((link, current_depth + 1))

                # Wait only if there are more links waiting for processing.
                if queue:
                    print(f"Waiting {wait_time}s")
                    time.sleep(wait_time)
            except (ArticleFetchError, ContentExtractionError) as e:
                print(f"Skipped '{current_phrase}' - error occured : {e}.")
                continue
            except Exception as e:
                print(f"Unexpected error on '{current_phrase}': {e}")
                continue
