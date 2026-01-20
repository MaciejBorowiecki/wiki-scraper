from scraper_logic import WikiScraper
import pandas as pd

class WikiManager:
    """
    Represents cotroller responsible for interpreting already parsed arguments
    and executing appriopriate methods.
    """
    
    def __init__(self, args):
        self.args = args
        self.scraper = WikiScraper()
        
    def handle_args(self):
        """
        Automatically handle all given arguments.
        """
        
        if self.args.summary:
            self.handle_summary()
        if self.args.table:
            self.handle_table()
    
    def handle_summary(self) -> None:
        phrase = self.args.summary

        article = self.scraper.scrape(phrase)
        
        if not article:
            print(f"Error scraping article: '{phrase}'.")
            return None
        summary_text = article.get_summary()
        
        if not summary_text:
            print(f"Summary error in: '{phrase}'.")
            return None
        
        print("\n-----Summary-----")
        print(summary_text, "\n")
        
        
    def handle_table(self) -> None:
        phrase = self.args.table
        
        article = self.scraper.scrape(phrase)
        
        if not article:
            print(f"Error scraping article: '{phrase}'.")
            return None
        
        df_table = article.get_table(self.args.number, self.args.first_row_is_header)
        if df_table is None:
            print(f"Error extracting table {self.args.number}.")
            return None
        
        print("\n-----Table-----")
        print(df_table.to_string(), "\n")
        
        filename = f"{phrase}.csv"
        df_table.to_csv(filename)
        print(f"Table saved to file: '{filename}'.\n")
        
        
        # TODO: maybe pandas has some function for counting each value?
        counts = {}
        
        for row in df_table.values:
            for item in row:
                val = str(item)
                if val in counts:
                    counts[val] += 1
                else:
                    counts[val] = 1
        
        stats_df = pd.DataFrame(counts.items(), columns=['Value', 'Count'])
        stats_df = stats_df.sort_values(by='Count', ascending=False)
        print(stats_df.to_string(index=False),"\n")
    