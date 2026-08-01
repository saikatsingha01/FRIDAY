import re


class KnowledgeNormalizer:
    """
    Normalizes facts before retrieval and comparison.

    Future:
    - synonym expansion
    - entity extraction
    - lemmatization
    - embedding preprocessing
    """

    def normalize(self, text):

        if not text:
            return ""

        text = text.lower()

        text = re.sub(
            r"[^\w\s]",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()


normalizer = KnowledgeNormalizer()


def normalize_fact(text):
    return normalizer.normalize(text)