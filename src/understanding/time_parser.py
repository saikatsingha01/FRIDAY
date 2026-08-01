import re

from src.understanding.understanding_models import TimeReference


class TimeParser:
    """
    Understands temporal references in natural language.

    Future:
    - Absolute dates
    - Relative dates
    - Date ranges
    - Calendar integration
    - Time arithmetic

    This module should only identify time.
    It should never retrieve memories.
    """

    def __init__(self):

        self.patterns = {

            "before": [

                r"\bbefore\b",

                r"\bprevious\b",

                r"\bpreviously\b",

                r"\bearlier\b",

                r"\bused to\b",

                r"\bold\b"

            ],

            "after": [

                r"\bafter\b",

                r"\blater\b"

            ],

            "present": [

                r"\bnow\b",

                r"\bcurrently\b",

                r"\bcurrent\b",

                r"\btoday\b"

            ],

            "yesterday": [

                r"\byesterday\b"

            ],

            "tomorrow": [

                r"\btomorrow\b"

            ],

            "last_week": [

                r"\blast week\b"

            ],

            "next_week": [

                r"\bnext week\b"

            ],

            "last_month": [

                r"\blast month\b"

            ],

            "next_month": [

                r"\bnext month\b"

            ]
        }



    def parse(self, text):

        text = text.lower()

        for reference_type, patterns in self.patterns.items():

            for pattern in patterns:

                if re.search(

                    pattern,

                    text

                ):

                    return TimeReference(

                        type="relative",

                        value=reference_type,

                        confidence=1.0

                    )



        return None



time_parser = TimeParser()