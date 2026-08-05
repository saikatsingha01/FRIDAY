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

    def normalize_for_understanding(self, text):
        """
        Prepares a message for the Understanding LLM before it
        decides uncertain_terms.

        Variant spellings of one concept are collapsed so the LLM
        reads a canonical form instead of something that looks like
        a typo: "b.tech"/"b-tech"/"spider-man" become
        "b tech"/"b tech"/"spider man".

        Keeps apostrophes and sentence punctuation — only separator
        variants (period, hyphen, underscore, slash) between words
        are collapsed.
        """

        if not text:
            return ""

        text = text.lower()

        text = re.sub(
            r"[-./_·]+",
            " ",
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


def normalize_for_understanding(text):
    return normalizer.normalize_for_understanding(text)