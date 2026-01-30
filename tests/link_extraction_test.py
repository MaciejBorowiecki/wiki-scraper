import pytest
from wiki_article import WikiArticle


def create_dummy_article(html_content: str = "") -> WikiArticle:
    """
    Helper function to create a WikiArticle object with dummy data.
    """

    return WikiArticle("Test Article",html_content,"en")



validation_scenarios = [
    # valid wiki links
    ("/wiki/Pikachu", True, "Standard article link"),
    ("/wiki/Team_Rocket", True, "Article link with underscore"),
    ("/wiki/Mimuw#Harmonogram_Sesji", True, "Link with '#'"),

    # invalid: banned prefixes (technical sits)
    ("/wiki/File:Image.png", False, "File site"),
    ("/wiki/Template:Info", False, "Template site"),
    ("/wiki/User:Admin", False, "User site"),
    ("/wiki/Category:Pokemon", False, "Category site"),
    ("/wiki/Help:Editing", False, "Help site"),
    ("/wiki/Special:Search", False, "Special site"),

    # invalid: non-wiki links
    ("https://google.com", False, "External link"),
]

@pytest.mark.parametrize("href, expected, description", validation_scenarios)
def test_is_valid_link(href, expected, description):
    """
    Tests the _is_valid_link method to ensure it correctly identifies
    whether a link should be processed or ignored.
    """

    article = create_dummy_article()
    
    result = article._is_valid_link(href)
    
    assert result is expected, f"Failed: {description}"



processing_scenarios = [
    # removal of /wiki/ prefix
    ("/wiki/Pikachu", "Pikachu", "Standard prefix removal"),
    ("/wiki/Charmander", "Charmander", "Standard prefix removal"),

    # handle duplicates with '#'
    ("/wiki/Bulbasaur#Stats", "Bulbasaur", "Remove anchor"),
    ("/wiki/Mewtwo#Mega_Mewtwo_X", "Mewtwo", "Remove complex anchor"),
]

@pytest.mark.parametrize("href, expected_phrase, description", processing_scenarios)
def test_process_link(href, expected_phrase, description):
    """
    Tests the _process_link method to ensure it correctly cleans the URL
    and extracts the article phrase.
    """
    article = create_dummy_article()
    
    result = article._process_link(href)
    
    assert result == expected_phrase, f"Failed: {description}"



def test_get_linked_phrases():
    """
    Tests the main get_linked_phrases method using a small HTML snippet.
    This verifies if the method correctly combines finding, validating, 
    and processing links.
    """

    html_content = """
    <div class="mw-content-ltr mw-parser-output">
        <p>Try to find links that are not sketchy adventurer! Good Luck!:</p>
        <a href="/wiki/Pikachu">Pikachu</a>
        <a href="/wiki/Raichu">Raichu original</a>
        <a href="/wiki/Raichu#Evolution">Raichu almost original</a>
        <a href="/wiki/File:Pika.jpg">Image</a> 
        <a href="https://informatorects.uw.edu.pl/pl/courses/view?prz_kod=1000-213bPYT">
        Zaawansowany kurs programowania niskopoziomowego.</a> 
    </div>
    """
    
    article = create_dummy_article(html_content)
    
    results = article.get_linked_phrases()
    
    # assert valid phrases are present
    assert "Pikachu" in results
    assert "Raichu" in results
    
    # assert invalid links are filtered out
    assert "File:Pika.jpg" not in results
    assert "https://informatorects.uw.edu.pl/pl/courses/view?prz_kod=1000-213bPYT" not in results
    
    # assert correct number of results
    assert len(results) == 2