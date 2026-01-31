import pytest
import argparse
from wiki_scraper import validate_arguments
from wiki_scraper import _check_mutually_dependent

# Check _check_mutually_dependent method.

dependency_failure_scenarios = [
    ((True, None), "One present, one None"),
    ((None, "Value"), "One None, one Value"),
    ((None, None, "C"), "One of three args presetn"),
    ((False, True), "One False (should be treated as missing), one True"),
]

@pytest.mark.parametrize("args_tuple, description", dependency_failure_scenarios)
def test_check_mutually_dependent_failure(args_tuple, description):
    """
    Tests that the function returns False when arguments are partially provided.
    """

    result = _check_mutually_dependent(*args_tuple)
    
    assert result is False, f"Failed: {description} should return False"


dependency_success_scenarios = [
    # all missign
    ((None, None), "All None"),
    ((False, False), "All False"),
    ((None, False), "Mixed None and False (both should be counted as missing)"),
    
    # all present
    ((True, True), "Same type, all present"),
    ((1, "Text", True), "Mixed types, all present"),
]

@pytest.mark.parametrize("args_tuple, description", dependency_success_scenarios)
def test_check_mutually_dependent_success(args_tuple, description):
    """
    Tests that the function returns True when either all or none arguments
    are provided.
    """

    result = _check_mutually_dependent(*args_tuple)
    
    assert result is True, f"Failed: {description} should return True"


# check validate_arguments method
def get_default_args():
    """
    Helper function initializes all possible args as not given.
    """
    
    return argparse.Namespace(
        summary=None,
        table=None,
        number=None,
        count_words=None,
        auto_count_words=None,
        analyze_relative_word_frequency=None,
        depth=None,
        wait=None,
        first_row_is_header=False,
        mode=None,
        count=None,
        chart=False,
    )


failure_scenarios = [
    # table failures
    ({"table": "Rocket", "number": None}, "Table without number"),
    ({"table": None, "number": 1}, "Number without table"),
    ({"table": "Rocket", "number": 0}, "Number is zero"),

    # mode selection failures
    ({}, "No mode selected"),
    ({"summary": "A", "count_words": "A"}, "Two main modes selected"),

    # context failures
    ({"summary": "Pika", "first_row_is_header": True}, "Header without table"),
    ({"summary": "Wykład z Analizy", "chart": True}, "Chart without analyze"),

    # Relative Word Frequency Analysis failures
    ({"analyze_relative_word_frequency": "A",
     "count": 10, "mode": None}, "Analyze missing mode"),
    ({"analyze_relative_word_frequency": "A",
     "count": None, "mode": "Language"}, "Analyze missing count"),
    ({"analyze_relative_word_frequency": "A",
     "count": 10, "mode": "bad"}, "Analyze invalid mode"),

    # Auto Count Words failures
    ({"auto_count_words": "Mew",
    "wait": 1.0,
      "depth": None},
     "Crawler missing depth"),
    
    ({"auto_count_words": "Mew",
      "wait": None,
      "depth": 2},
     "Crawler missing wait"),
    
    ({"auto_count_words": "Mew",
      "wait": 1.0,
      "depth": -1},
     "Crawler negative depth"),
    
    ({"auto_count_words": "Mew",
      "wait": -1.0,
      "depth": 1},
     "Crawler negative wait"),
]


@pytest.mark.parametrize("overrides, description", failure_scenarios)
def test_validate_arguments_failure(overrides, description):
    parser = argparse.ArgumentParser()
    args = get_default_args()

    for key, value in overrides.items():
        setattr(args, key, value)

    with pytest.raises(SystemExit):
        validate_arguments(parser, args)


success_scenarios = [
    ({"summary": "Pikachu"}, "Valid Summary"),
    ({"table": "Kanto", "number": 5, "first_row_is_header": True}, "Valid Table"),
    ({"count_words": "Eevee"}, "Valid Count Words"),
    ({"analyze_relative_word_frequency": True, "count": 10,
     "mode": "language", "chart": './van_gogh'}, "Valid Analyze"),
    ({"auto_count_words": "PO", "depth": 1000, "wait": 0.5}, "Valid Crawler"),
]


@pytest.mark.parametrize("overrides, description", success_scenarios)
def test_validate_arguments_success(overrides, description):
    parser = argparse.ArgumentParser()
    args = get_default_args()

    for key, value in overrides.items():
        setattr(args, key, value)

    # parser will throw error in case of errors.
    validate_arguments(parser, args)
