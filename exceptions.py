class WikiScraperError(Exception):
    """
    Base error class for exceptions in this project.
    """
    pass

class ArticleFetchError(Exception):
    """
    Raised when article can't be fetched (no file or network error).
    """
    pass

class ContentExtractionError(Exception):
    """
    Raised, when parsing html goes wrong (no table, no content div, etc).
    """
    pass