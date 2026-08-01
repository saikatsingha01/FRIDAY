import re

from src.understanding.understanding_models import Entity


class EntityExtractor:
    """
    Extracts meaningful entities from user input.

    Future versions may use:
    - spaCy
    - GLiNER
    - transformer NER
    - LLM extraction

    The interface should remain unchanged.
    """

    def __init__(self):

        self.patterns = {

            "game": [

                r"ghost of tsushima",

                r"sekiro",

                r"minecraft",

                r"elden ring",

                r"black myth wukong",

                r"gta ?6?",

                r"phasmophobia"

            ],

            "device": [

                r"laptop",

                r"computer",

                r"pc",

                r"phone",

                r"gpu",

                r"cpu",

                r"ram",

                r"rtx\s*\d+"

            ],

            "project": [

                r"friday",

                r"loan sphere"

            ],

            "person": [

                r"mom",

                r"mother",

                r"dad",

                r"father",

                r"friend",

                r"girlfriend"

            ]

        }


    def extract(self, text):

        text = text.lower()

        entities = []

        for label, patterns in self.patterns.items():

            for pattern in patterns:

                matches = re.finditer(

                    pattern,

                    text,

                    flags=re.IGNORECASE

                )

                for match in matches:

                    entities.append(

                        Entity(

                            text=match.group(),

                            label=label,

                            confidence=1.0

                        )

                    )

        return entities


entity_extractor = EntityExtractor()