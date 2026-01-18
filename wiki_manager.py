from scraper_logic import WikiScraper, WikiArticle

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
        
        
    