import unicodedata

def normalize_text(text: str) -> str:
    """
    Normalize text for rule-based processing.
    - Fix unicode (smart quotes)
    - Lowercase

    Ex. Input: "He said, “Don’t touch Café’s menu!”"
    Ex. output: he said, "don't touch cafe's menu!"
    """

    if not isinstance(text, str):
        return ""
    
    # converts visually different but logically same text into a single clean, predictable format
    # Café’s -> Cafe's
    text = unicodedata.normalize("NFKD", text)
    
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')

    return text.lower()