from bs4 import BeautifulSoup

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

        self.content_div = self.soup.find('div', class_ = 'mw-content-ltr mw-parser-output')
        
        if not self.content_div:
            print(f"Warning: Main content container was not found for '{title}'.")
    
    def get_summary(self) -> str:
        if not self.content_div:
            print(f"Warning: Main content container was not found for '{self.title}'.")
            return None
        
        first_paragraph = self.content_div.find('p')
        
        if not first_paragraph:
            print(f"First paragraph was not found for '{self.title}'.")
            return None
        return first_paragraph.get_text().strip()
    
