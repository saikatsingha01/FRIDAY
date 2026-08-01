import re


def clean_text(text):
    """
    Cleans speech-to-text output before it enters
    the reasoning pipeline.
    """

    if text is None:
        return ""

    text = text.lower().strip()

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()