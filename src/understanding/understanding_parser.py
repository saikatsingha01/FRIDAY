import json


class UnderstandingParser:
    """
    Converts the raw LLM response into a Python dictionary.

    Responsibilities:
    - Remove markdown code fences
    - Repair simple JSON mistakes
    - Parse JSON
    - Return a dictionary

    Does NOT:
    - Validate semantics
    - Perform reasoning
    - Create contracts
    """

    def _remove_markdown(self, response: str):

        response = response.strip()

        if response.startswith("```"):

            lines = response.splitlines()

            if lines:

                lines = lines[1:]

            if lines and lines[-1].startswith("```"):

                lines = lines[:-1]

            response = "\n".join(lines).strip()

        return response

    def _repair_json(self, response: str):

        response = response.strip()

        # --------------------------------------
        # Remove trailing commas
        # --------------------------------------

        response = response.replace(",}", "}")

        response = response.replace(",]", "]")

        # --------------------------------------
        # Balance braces
        # --------------------------------------

        open_curly = response.count("{")
        close_curly = response.count("}")

        if open_curly > close_curly:

            response += "}" * (open_curly - close_curly)

        # --------------------------------------
        # Balance brackets
        # --------------------------------------

        open_square = response.count("[")
        close_square = response.count("]")

        if open_square > close_square:

            response += "]" * (open_square - close_square)

        return response

    def parse(self, response: str):

        if response is None:

            return None

        response = self._remove_markdown(

            response

        )

        response = self._repair_json(

            response

        )

        try:

            return json.loads(

                response

            )

        except Exception as error:

            print()

            print("====================================")
            print("UNDERSTANDING PARSER ERROR")
            print("====================================")

            print(error)

            print()

            print("RAW RESPONSE:")

            print(response)

            print()

            print("====================================")

            return None


understanding_parser = UnderstandingParser()


def parse_understanding(response: str):

    return understanding_parser.parse(

        response

    )