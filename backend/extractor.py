"""
Data extractor for amounts and dates from document text.
"""

import re
from typing import List


def extract_amounts(text: str) -> List[str]:
    """
    Extract monetary amounts from text.

    Looks for patterns like:
    - 123,45
    - 1.234,56
    - 123.45

    Args:
        text: Document text to search

    Returns:
        List of found amount strings
    """
    # Pattern for German number format: 1.234,56 or 123,45
    german_pattern = r'\b\d{1,3}(?:\.\d{3})*(?:,\d{2})\b'

    # Pattern for international format: 123.45
    international_pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d{2})\b'

    amounts = []

    for match in re.finditer(german_pattern, text):
        amounts.append(match.group())

    # Only add international format if it doesn't match German format
    for match in re.finditer(international_pattern, text):
        value = match.group()
        if ',' not in value:  # Avoid duplicate matches
            amounts.append(value)

    return amounts


def extract_dates(text: str) -> List[str]:
    """
    Extract dates in German format (dd.mm.yyyy) from text.

    Args:
        text: Document text to search

    Returns:
        List of found date strings
    """
    # Pattern for dd.mm.yyyy
    pattern = r'\b(0?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|1[0-2])\.(19|20)?\d{2}\b'

    dates = []

    for match in re.finditer(pattern, text):
        dates.append(match.group())

    return dates


def extract_all(text: str) -> dict:
    """
    Extract all structured data from document text.

    Args:
        text: Document text to process

    Returns:
        Dictionary with amounts and dates lists
    """
    return {
        "amounts": extract_amounts(text),
        "dates": extract_dates(text)
    }
