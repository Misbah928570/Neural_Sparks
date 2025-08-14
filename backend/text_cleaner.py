import re

def normalize_spaces(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\t+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \u00A0]{2,}", " ", text)
    return text.strip()
