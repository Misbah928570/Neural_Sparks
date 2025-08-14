import re
import unicodedata

import re

def normalize_spaces(text: str) -> str:
    """
    Normalize whitespace in text by:
    - Replacing multiple spaces with single spaces
    - Removing leading/trailing whitespace
    - Normalizing line breaks
    """
    if not text:
        return text
    # Replace any whitespace (including tabs, newlines) with single space
    text = re.sub(r'\s+', ' ', text.strip())
    return text
def normalize_unicode(text: str) -> str:
    """
    Normalize text to NFC form to handle different Unicode representations.
    """
    return unicodedata.normalize('NFC', text)

def remove_extra_spaces(text: str) -> str:
    """
    Remove extra spaces, tabs, and line breaks.
    """
    return re.sub(r'\s+', ' ', text).strip()

def clean_legal_text(text: str) -> str:
    """
    Cleans legal text for processing:
    - Normalizes unicode
    - Removes unwanted characters
    - Preserves legal symbols
    - Converts multiple spaces to single
    """
    if not text or not isinstance(text, str):
        return ""

    # Normalize Unicode characters
    text = normalize_unicode(text)

    # Remove unwanted control characters but keep legal symbols
    text = re.sub(r'[^\x20-\x7E§¶©®™\n]', '', text)

    # Remove HTML tags if any
    text = re.sub(r'<[^>]+>', '', text)

    # Normalize punctuation spacing
    text = re.sub(r'\s*([.,;:!?])\s*', r'\1 ', text)

    # Remove extra spaces
    text = remove_extra_spaces(text)

    return text

def extract_sentences(text: str) -> list:
    """
    Splits cleaned text into sentences for clause-level analysis.
    """
    text = clean_legal_text(text)
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

if __name__ == "__main__":
    sample_text = """
    THIS AGREEMENT is made on the 1st day of January 2025.
    <p>Between Party A (“Client”) and Party B (“Service Provider”).</p>
    § Clause 1: All services are subject to the terms stated herein.
    """
    print("Original:", sample_text)
    print("Cleaned:", clean_legal_text(sample_text))
    print("Sentences:", extract_sentences(sample_text))

